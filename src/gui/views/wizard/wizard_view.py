"""
智能向导视图 (Wizard View)
引导式操作，快速完成常见任务。已接入 Service 层。
"""
from PySide6.QtCore import Qt
from qfluentwidgets import MessageBox

from src.gui.i18n import t
# TODO: 通过 app 实例访问 Service
from src.common.signals import signal_bus
from src.gui.components import BasePageView
from src.gui.dialogs import ScanFlowDialog
from src.gui.views.wizard.widgets import ScanProgressCard


class WizardView(BasePageView):
    """智能向向导视图 - 业务逻辑已移交 Service"""

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("wizard.title"),
            show_toolbar=False,
            enable_scroll=True
        )

        # 依赖注入
        self.template_service = service_bus.template_service
        self.category_service = service_bus.category_service

        # 扫描状态缓存 (UI 状态)
        self.discovered_templates = []
        self.scan_result_cards = {}

        # 添加页面内容
        self._setup_content()

        # 连接信号
        self._connect_signals()

    def _setup_content(self):
        """设置页面内容"""
        # 扫描进度卡片（固定内容，始终可见）
        self.scan_progress = ScanProgressCard()
        self.add_fixed_content(
            self.scan_progress, 
            before_scroll=True, 
            use_padding=True,
            top_margin=0,
            bottom_margin=12
        )
        
        # 配置编辑器卡片（固定内容）
        from src.gui.views.wizard.widgets import ConfigEditorCard
        self.config_editor = ConfigEditorCard()
        self.add_fixed_content(
            self.config_editor,
            before_scroll=True,
            use_padding=True,
            top_margin=0,
            bottom_margin=12
        )

        # 结果滚动区域初始隐藏
        self.get_scroll_area().setVisible(False)

    def _on_theme_changed(self, theme: str):
        """主题变更处理"""
        super()._on_theme_changed(theme)

    def _connect_signals(self):
        """连接信号"""
        self.scan_progress.scan_clicked.connect(self._on_scan_clicked)
        self.scan_progress.import_clicked.connect(self._on_import_clicked)
        self.scan_progress.refresh_clicked.connect(self._on_refresh_clicked)
        self.scan_progress.cancel_clicked.connect(self._on_cancel_clicked)

    def _on_scan_clicked(self):
        """开始扫描 - 统一流程"""
        # 弹出统一的全功能扫描对话框
        dialog = ScanFlowDialog(service_bus.category_manager, self)
        if dialog.exec():
            # 通知链接列表刷新
            signal_bus.data_refreshed.emit()
            
        # 刷新进度卡片状态（复位）
        self.scan_progress.reset()

    def _on_selection_changed(self, template_id, selected):
        """选择状态改变"""
        selected_count = sum(
            1 for card in self.scan_result_cards.values()
            if card.is_selected()
        )
        self.scan_progress.update_selected_count(selected_count)

    def _on_import_clicked(self):
        """一键导入选中的软件 (待 Service 化重写)"""
        # 目前 ScanFlow 内部已处理导入业务
        pass

    def _on_refresh_clicked(self):
        """重新扫描"""
        self._on_scan_clicked()

    def _on_cancel_clicked(self):
        """取消扫描结果，返回初始状态"""
        self.discovered_templates.clear()
        for card in self.scan_result_cards.values():
            card.deleteLater()
        self.scan_result_cards.clear()

        self.get_scroll_area().setVisible(False)
        self.scan_progress.reset()
