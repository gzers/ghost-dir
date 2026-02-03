"""
全流程序扫描对话框
集成扫描进度展示与结果列表预览
"""
from typing import List, Optional
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt, Signal, QThread
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, BodyLabel, 
    IndeterminateProgressBar, ScrollArea, FluentIcon
)

from src.gui.views.wizard.widgets.scan_result_card import ScanResultCard
from src.core.services.scan_service import SmartScanner

from src.gui.i18n import t, get_category_text
from src.core.services.context import service_bus
from src.gui.styles import apply_font_style


class ScanWorker(QThread):
    """扫描工作线程"""
    finished = Signal(list)  # discovered templates
    
    def __init__(self, scanner: SmartScanner):
        super().__init__()
        self.scanner = scanner
    
    def run(self):
        """执行扫描"""
        discovered = self.scanner.scan()
        self.finished.emit(discovered)


class ImportWorker(QThread):
    """导入工作线程"""
    finished = Signal(int)
    
    def __init__(self, scanner: SmartScanner, templates: List):
        super().__init__()
        self.scanner = scanner
        self.templates = templates
        
    def run(self):
        count = self.scanner.import_templates(self.templates)
        self.finished.emit(count)


class ScanFlowDialog(MessageBoxBase):
    """全流程扫描对话框 - 统一标准版本"""
    
    scan_completed = Signal(int)  # 成功导入的数量
    
    def __init__(self, category_manager=None, parent=None):
        super().__init__(parent)
        
        # 数据准备
        self.category_manager = service_bus.category_manager
        self.template_manager = service_bus.template_manager
        self.user_manager = service_bus.user_manager
        self.scanner = SmartScanner(self.template_manager, self.user_manager)
        
        self.discovered = []
        self.result_cards = {}
        
        self.setWindowTitle("智能扫描")
        self._init_ui()
        
        # 自动开始扫描
        self._start_scan()
        
    def _init_ui(self):
        """初始化 UI 结构"""
        # 主堆栈，用于切换扫描中/结果列表/导入中
        self.stack = QStackedWidget()
        
        # --- 阶段 1：扫描中 UI ---
        self.loading_widget = QWidget()
        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setContentsMargins(0, 40, 0, 40)
        loading_layout.setSpacing(24)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.loading_title = SubtitleLabel("正在扫描本机应用...")
        self.progress_bar = IndeterminateProgressBar()
        self.progress_bar.setFixedWidth(400)
        self.loading_status = BodyLabel("正在深度检查磁盘，请稍候...")
        apply_font_style(self.loading_status, color="secondary")
        
        loading_layout.addWidget(self.loading_title)
        loading_layout.addWidget(self.progress_bar)
        loading_layout.addWidget(self.loading_status)
        
        # --- 阶段 2：结果展示 UI ---
        self.result_overlay = QWidget()
        result_layout = QVBoxLayout(self.result_overlay)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(12)
        
        self.result_title = SubtitleLabel(t("wizard.scan_complete"))
        self.result_subtitle = BodyLabel("")
        apply_font_style(self.result_subtitle, size="sm", color="secondary")
        
        self.scroll_area = ScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(ScrollArea.NoFrame)
        # 设置透明背景
        self.scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.list_container = QWidget()
        # 设置透明背景
        self.list_container.setStyleSheet("QWidget { background: transparent; }")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 16, 0)
        self.list_layout.setSpacing(12)
        self.list_layout.addStretch(1)
        
        self.scroll_area.setWidget(self.list_container)
        
        result_layout.addWidget(self.result_title)
        result_layout.addWidget(self.result_subtitle)
        result_layout.addWidget(self.scroll_area)

        # --- 阶段 3：导入中 UI ---
        self.importing_widget = QWidget()
        importing_layout = QVBoxLayout(self.importing_widget)
        importing_layout.setContentsMargins(0, 40, 0, 40)
        importing_layout.setSpacing(24)
        importing_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.importing_title = SubtitleLabel("正在导入连接...")
        self.import_progress = IndeterminateProgressBar()
        self.import_progress.setFixedWidth(400)
        self.import_status = BodyLabel("正在同步配置并刷新列表...")
        apply_font_style(self.import_status, color="secondary")
        
        importing_layout.addWidget(self.importing_title)
        importing_layout.addWidget(self.import_progress)
        importing_layout.addWidget(self.import_status)
        
        # 添加到堆栈
        self.stack.addWidget(self.loading_widget)  # 0
        self.stack.addWidget(self.result_overlay)  # 1
        self.stack.addWidget(self.importing_widget) # 2
        
        # 将堆栈添加到 MessageBox 视图
        self.viewLayout.addWidget(self.stack)
        
        # 按钮初始状态
        self.yesButton.setText("导入选中项")
        self.yesButton.setEnabled(False)
        self.cancelButton.setText("取消")
        
        # 尺寸标准：800x600 大气预览
        self.widget.setMinimumWidth(800)
        self.widget.setMinimumHeight(600)
        
    def _start_scan(self):
        """开始执行异步扫描"""
        self.stack.setCurrentIndex(0)
        self.worker = ScanWorker(self.scanner)
        self.worker.finished.connect(self._on_scan_finished)
        self.worker.start()
        
    def _on_scan_finished(self, discovered):
        """扫描完成，转换 UI 阶段"""
        self.discovered = discovered
        self.stack.setCurrentIndex(1)
        
        # 更新标题
        self.result_title.setText(t("wizard.scan_complete"))
        self.result_subtitle.setText(t("wizard.scan_complete_detail", count=len(discovered)))
        
        if discovered:
            # 加载卡片
            for template in discovered:
                cat_id = getattr(template, 'category_id', getattr(template, 'category', ''))
                cat_name = get_category_text(cat_id)
                
                card = ScanResultCard(template, category_name=cat_name)
                card.selected_changed.connect(self._update_selection_count)
                
                self.list_layout.insertWidget(self.list_layout.count() - 1, card)
                self.result_cards[template.id] = card
                
            self._update_selection_count()
        else:
            no_result = BodyLabel("未发现可管理的软件")
            no_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.insertWidget(0, no_result)
            self.yesButton.setEnabled(False)
            
    def _update_selection_count(self):
        """实时刷新导入按钮上的数量统计"""
        selected_count = sum(1 for card in self.result_cards.values() if card.is_selected())
        self.yesButton.setText(f"导入选中项 ({selected_count})")
        self.yesButton.setEnabled(selected_count > 0)
        
    def get_selected_templates(self) -> List:
        """获取所有最终被勾选的模版"""
        return [
            card.get_template()
            for card in self.result_cards.values()
            if card.is_selected()
        ]

    def validate(self):
        """异步触发导入操作"""
        selected = self.get_selected_templates()
        if not selected:
            return False
            
        # 切换到导入中状态
        self.stack.setCurrentIndex(2)
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        
        # 启动异步导入
        self.import_worker = ImportWorker(self.scanner, selected)
        self.import_worker.finished.connect(self._on_import_finished)
        self.import_worker.start()
        
        # 返回 False 阻止 MessageBox 立即自动关闭
        return False

    def _on_import_finished(self, count: int):
        """导入完成回调"""
        self.scan_completed.emit(count)
        # 手动触发表单接受并关闭对话框
        self.accept()
