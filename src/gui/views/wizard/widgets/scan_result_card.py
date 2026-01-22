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


class ScanResultCard(CardWidget):
    """扫描结果卡片组件"""

    # 信号定义
    selected_changed = Signal(str, bool)  # template_id, selected
    ignore_requested = Signal(str)  # template_id
    import_requested = Signal(str)  # template_id

    def __init__(self, template, parent=None):
        super().__init__(parent)
        self.template = template
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # 复选框
        self.checkbox = CheckBox()
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(
            lambda state: self.selected_changed.emit(self.template.id, state == 2)
        )
        layout.addWidget(self.checkbox)

        # 图标
        icon = BodyLabel("💾")
        from ....theme import StyleManager
        icon.setStyleSheet(StyleManager.get_icon_style("md"))
        icon.setFixedSize(32, 32)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        # 信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        self.name_label = BodyLabel(self.template.name)
        self.name_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self.name_label)

        self.path_label = BodyLabel(self.template.default_src)
        from ....theme import apply_muted_text_style
        apply_muted_text_style(self.path_label, size=12)
        self.path_label.setWordWrap(True)
        info_layout.addWidget(self.path_label)

        layout.addLayout(info_layout, stretch=1)

        # 分类标签
        category = BodyLabel(self.template.category)
        category.setStyleSheet("""
            background-color: #E6F7FF;
            color: #1890FF;
            padding: 4px 12px;
            border-radius: 4px;
        """)
        layout.addWidget(category)

        # 操作按钮
        self.import_button = ToolButton(FluentIcon.DOWNLOAD, self)
        self.import_button.setToolTip("导入此软件")
        self.import_button.clicked.connect(
            lambda: self.import_requested.emit(self.template.id)
        )
        layout.addWidget(self.import_button)

        # 忽略按钮
        self.ignore_button = ToolButton(FluentIcon.DELETE, self)
        self.ignore_button.setToolTip("永久忽略此软件")
        self.ignore_button.clicked.connect(self._on_ignore_clicked)
        layout.addWidget(self.ignore_button)

    def _on_ignore_clicked(self):
        """忽略按钮点击"""
        # 显示确认菜单
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
