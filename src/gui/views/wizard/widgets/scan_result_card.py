"""
扫描结果卡片组件
显示单个扫描结果的详细信息
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMenu
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    CardWidget, CheckBox, BodyLabel, PushButton,
    ToolButton, FluentIcon
)


from ....components import Card
from ....styles import (
    apply_font_style, apply_badge_style,
    get_spacing, get_radius, apply_muted_text_style, get_icon_background
)

class ScanResultCard(Card):
    """扫描结果卡片组件"""

    # 信号定义
    selected_changed = Signal(str, bool)  # template_id, selected
    ignore_requested = Signal(str)  # template_id
    import_requested = Signal(str)  # template_id

    def __init__(self, template, parent=None):
        super().__init__(parent)
        self.template = template
        self._init_ui()
        self._refresh_content_styles()

    def _init_ui(self):
        """初始化 UI"""
        # 主布局
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(16, 12, 16, 12)
        self.main_layout.setSpacing(12)

        # 复选框
        self.checkbox = CheckBox()
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(
            lambda state: self.selected_changed.emit(self.template.id, state == 2)
        )
        self.main_layout.addWidget(self.checkbox)

        # 图标
        icon_label = BodyLabel("💾")
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(icon_label)

        # 信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        self.name_label = BodyLabel(self.template.name)
        info_layout.addWidget(self.name_label)

        self.path_label = BodyLabel(self.template.default_src)
        self.path_label.setWordWrap(True)
        info_layout.addWidget(self.path_label)

        self.main_layout.addLayout(info_layout, stretch=1)

        # 分类标签
        self.category_badge = BodyLabel(self.template.category)
        self.main_layout.addWidget(self.category_badge)

        # 操作按钮
        self.import_button = ToolButton(FluentIcon.DOWNLOAD, self)
        self.import_button.setToolTip("导入此软件")
        self.import_button.clicked.connect(
            lambda: self.import_requested.emit(self.template.id)
        )
        self.main_layout.addWidget(self.import_button)

        # 忽略按钮
        self.ignore_button = ToolButton(FluentIcon.DELETE, self)
        self.ignore_button.setToolTip("永久忽略此软件")
        self.ignore_button.clicked.connect(self._on_ignore_clicked)
        self.main_layout.addWidget(self.ignore_button)

    def _refresh_content_styles(self):
        """刷新文字样式"""
        apply_font_style(self.name_label, weight="semibold")
        apply_muted_text_style(self.path_label, size="sm")
        apply_badge_style(self.category_badge, status="info")

    def _on_ignore_clicked(self):
        """忽略按钮点击"""
        menu = QMenu(self)
        action = menu.addAction(f"永久忽略 {self.template.name}")
        action.triggered.connect(
            lambda: self.ignore_requested.emit(self.template.id)
        )
        menu.exec(self.ignore_button.mapToGlobal(self.ignore_button.rect().bottomLeft()))

    def set_selected(self, selected):
        """设置选中状态"""
        self.checkbox.setChecked(selected)

    def is_selected(self):
        """获取选中状态"""
        return self.checkbox.isChecked()

    def get_template(self):
        """获取关联的模版"""
        return self.template
