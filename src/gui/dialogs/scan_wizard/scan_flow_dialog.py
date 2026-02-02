"""
全流程序扫描对话框
集成扫描进度展示与结果列表预览
"""
from typing import List, Optional
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt, Signal, QThread
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, BodyLabel, 
    ProgressBar, ScrollArea, FluentIcon
)

from src.gui.views.wizard.widgets.scan_result_card import ScanResultCard
from src.core.scanner import SmartScanner
from src.data.template_manager import TemplateManager
from src.data.user_manager import UserManager
from src.gui.i18n import t, get_category_text
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


class ScanFlowDialog(MessageBoxBase):
    """全流程扫描对话框 - 统一标准版本"""
    
    scan_completed = Signal(int)  # 成功导入的数量
    
    def __init__(self, category_manager=None, parent=None):
        super().__init__(parent)
        
        # 数据准备
        # 🆕 增强稳健性：如果透传失败，主动实例化并触发加载
        if not category_manager:
            from src.data.category_manager import CategoryManager
            self.category_manager = CategoryManager()
        else:
            self.category_manager = category_manager
            
        self.template_manager = TemplateManager(category_manager=self.category_manager)
        self.user_manager = UserManager()
        self.scanner = SmartScanner(self.template_manager, self.user_manager)
        
        self.discovered = []
        self.result_cards = {}
        
        self.setWindowTitle("智能扫描")
        self._init_ui()
        
        # 自动开始扫描
        self._start_scan()
        
    def _init_ui(self):
        """初始化 UI 结构"""
        # 主堆栈，用于切换扫描中/结果列表
        self.stack = QStackedWidget()
        
        # --- 阶段 1：扫描中 UI ---
        self.loading_widget = QWidget()
        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setContentsMargins(0, 40, 0, 40)
        loading_layout.setSpacing(24)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.loading_title = SubtitleLabel("正在扫描本机应用...")
        self.progress_bar = ProgressBar()
        self.progress_bar.setRange(0, 0)
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
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 16, 0)
        self.list_layout.setSpacing(12)
        self.list_layout.addStretch(1)
        
        self.scroll_area.setWidget(self.list_container)
        
        result_layout.addWidget(self.result_title)
        result_layout.addWidget(self.result_subtitle)
        result_layout.addWidget(self.scroll_area)
        
        # 添加到堆栈
        self.stack.addWidget(self.loading_widget)
        self.stack.addWidget(self.result_overlay)
        
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
            # 记录：不再在此处手动构建 cat_map，统一走 get_category_text (配置驱动+智能降级)
            
            # 加载卡片
            for template in discovered:
                # 🆕 增强型映射：尝试 category_id，回退到 category 字段
                cat_id = getattr(template, 'category_id', getattr(template, 'category', ''))
                cat_name = get_category_text(cat_id)
                
                card = ScanResultCard(template, category_name=cat_name)
                # 连接选中状态，用于实时更新底部按钮
                card.selected_changed.connect(self._update_selection_count)
                
                # 插入到 stretch 之前
                self.list_layout.insertWidget(self.list_layout.count() - 1, card)
                self.result_cards[template.id] = card
                
            self._update_selection_count()
        else:
            # 未发现结果处理
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
        """重写确定按钮逻辑，执行导入操作"""
        selected = self.get_selected_templates()
        if not selected:
            return False
            
        # 物理导入
        count = self.scanner.import_templates(selected)
        self.scan_completed.emit(count)
        return True
