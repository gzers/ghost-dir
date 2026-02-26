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
from src.services.scan_service import SmartScanner
from src.common.service_bus import service_bus

from src.gui.i18n import t, get_category_text
from src.gui.styles import apply_font_style


class ScanWorker(QThread):
    """扫描工作线程"""
    finished = Signal(list)  # discovered templates
    progress = Signal(str)    # current scanning path

    def __init__(self, scanner: SmartScanner):
        super().__init__()
        self.scanner = scanner
        # 绑定扫描器的进度回调到我们的信号
        self.scanner.set_progress_callback(self.progress.emit)

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
        
        # 实例化扫描器 (注入 link_service 以支持持久化导出)
        all_templates = service_bus.template_service.get_all_templates()
        self.scanner = SmartScanner(all_templates, link_service=service_bus.link_service)

        self.discovered = []
        self.result_cards = {}

        self.setWindowTitle("智能扫描")
        self._init_ui()
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
        self.scanProgressBar = IndeterminateProgressBar(self)
        self.scanProgressBar.setFixedWidth(260)
        
        self.statusLabel = BodyLabel('正在深度检查磁盘，请稍候...', self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        apply_font_style(self.statusLabel, size=11, color='secondary')
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setFixedWidth(400)

        loading_layout.addWidget(self.loading_title)
        loading_layout.addWidget(self.scanProgressBar)
        loading_layout.addWidget(self.statusLabel)

        # --- 阶段 2：结果展示 UI ---
        self.result_overlay = QWidget()
        result_layout = QVBoxLayout(self.result_overlay)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(12)

        # 标题行：左侧标题 + 右侧全选按钮
        from PySide6.QtWidgets import QHBoxLayout
        from qfluentwidgets import HyperlinkButton

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)

        self.result_title = SubtitleLabel(t("wizard.scan_complete"))
        title_row.addWidget(self.result_title)
        title_row.addStretch(1)

        self.select_all_btn = HyperlinkButton("", "取消全选")
        self.select_all_btn.clicked.connect(self._on_toggle_select_all)
        title_row.addWidget(self.select_all_btn)

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

        result_layout.addLayout(title_row)
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
        if self.scanner is None:
            return

        self.stack.setCurrentIndex(0)
        
        self.scanWorker = ScanWorker(self.scanner)
        self.scanWorker.finished.connect(self._on_scan_finished)
        self.scanWorker.progress.connect(self.statusLabel.setText)
        self.scanWorker.start()

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
                # 直接读取模板中的分类全路径名称
                display_cat_name = template.category_path_name or "未分类"

                card = ScanResultCard(
                    template,
                    category_name=display_cat_name,
                    category_manager=self.category_manager,
                )
                card.selected_changed.connect(self._update_selection_count)

                self.list_layout.insertWidget(self.list_layout.count() - 1, card)
                self.result_cards[template.id] = card

            self._update_selection_count()
        else:
            no_result = BodyLabel("未发现可管理的软件")
            no_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.insertWidget(0, no_result)
            self.yesButton.setEnabled(False)

    def _on_toggle_select_all(self):
        """全选/取消全选切换"""
        total = len(self.result_cards)
        selected = sum(1 for c in self.result_cards.values() if c.is_selected())
        # 当前全选 → 取消全选；否则 → 全选
        new_state = selected < total
        for card in self.result_cards.values():
            card.set_selected(new_state)
        self._update_selection_count()

    def _update_selection_count(self):
        """实时刷新导入按钮上的数量统计 & 全选按钮文字"""
        selected_count = sum(1 for card in self.result_cards.values() if card.is_selected())
        self.yesButton.setText(f"导入选中项 ({selected_count})")
        self.yesButton.setEnabled(selected_count > 0)
        # 同步全选按钮文字
        all_selected = selected_count == len(self.result_cards) and selected_count > 0
        self.select_all_btn.setText("取消全选" if all_selected else "全选")

    def get_selected_templates(self) -> List:
        """获取所有最终被勾选的模版"""
        return [
            card.get_template()
            for card in self.result_cards.values()
            if card.is_selected()
        ]

    def validate(self):
        """异步触发导入操作"""
        if self.scanner is None:
            return False

        selected = self.get_selected_templates()
        if not selected:
            return False

        # 切换到导入中状态
        self.stack.setCurrentIndex(2)
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

        # 开启导入工作线程
        self.import_worker = ImportWorker(self.scanner, selected)
        self.import_worker.finished.connect(self._on_import_finished)
        self.import_worker.start()

        # 返回 False 阻止 MessageBox 立即自动关闭
        return False

    def _on_import_finished(self, count: int):
        """导入完成回调"""
        from qfluentwidgets import InfoBar
        if count > 0:
            InfoBar.success(
                t("common.success"),
                f"成功导入 {count} 个连接",
                duration=3000,
                position='TopCenter',
                parent=service_bus.main_window or self.window()
            )
        
        self.scan_completed.emit(count)
        # 手动触发表单接受并关闭对话框
        self.accept()
