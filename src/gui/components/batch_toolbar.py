"""
通用批量操作工具栏组件
"""
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Signal
from qfluentwidgets import BodyLabel, PushButton, ToolButton, FluentIcon
from src.gui.components.card import Card
from src.gui.i18n import t


class BatchToolbar(Card):
    """批量操作工具栏"""

    # 信号
    batch_establish_clicked = Signal()
    batch_disconnect_clicked = Signal()
    batch_remove_clicked = Signal()
    batch_delete_clicked = Signal()  # 模版库专用
    clear_selection_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode = "links"
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(16, 8, 16, 8)

        self.selected_label = BodyLabel(t("links.selected_count", count=0))
        self.layout.addWidget(self.selected_label)
        self.layout.addStretch()

        # 链接页面按钮 (使用 links 命名空间)
        self.batch_establish_btn = PushButton(FluentIcon.LINK, t("links.batch_establish"))
        self.batch_establish_btn.clicked.connect(self.batch_establish_clicked.emit)

        self.batch_disconnect_btn = PushButton(FluentIcon.CANCEL, t("links.batch_disconnect"))
        self.batch_disconnect_btn.clicked.connect(self.batch_disconnect_clicked.emit)

        self.batch_remove_btn = PushButton(FluentIcon.DELETE, t("links.batch_remove"))
        self.batch_remove_btn.clicked.connect(self.batch_remove_clicked.emit)

        # 模版库页面按钮 (使用 library 命名空间)
        self.batch_delete_btn = PushButton(FluentIcon.DELETE, t("library.btn_delete"))
        self.batch_delete_btn.clicked.connect(self.batch_delete_clicked.emit)

        self.clear_selection_btn = ToolButton(FluentIcon.CLOSE)
        self.clear_selection_btn.setToolTip(t("links.clear_selection"))
        self.clear_selection_btn.clicked.connect(self.clear_selection_clicked.emit)

        self.layout.addWidget(self.batch_establish_btn)
        self.layout.addWidget(self.batch_disconnect_btn)
        self.layout.addWidget(self.batch_remove_btn)
        self.layout.addWidget(self.batch_delete_btn)
        self.layout.addWidget(self.clear_selection_btn)

        self.set_mode("links")

    def set_mode(self, mode: str):
        """设置显示模式"""
        self._mode = mode
        # 兼容旧的 connected 命称和新的 links 名称
        is_links = (mode in ["connected", "links"])
        is_library = (mode == "library")

        self.batch_establish_btn.setVisible(is_links)
        self.batch_disconnect_btn.setVisible(is_links)
        self.batch_remove_btn.setVisible(is_links)
        self.batch_delete_btn.setVisible(is_library)

    def update_count(self, count: int):
        """更新选中数量"""
        self.selected_label.setText(t("links.selected_count", count=count))
