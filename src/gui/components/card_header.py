"""
卡片头部组件
显示图标、标题和副标题
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import StrongBodyLabel, BodyLabel
from ..styles import (
    apply_font_style, apply_muted_text_style,
    get_spacing, apply_icon_style
)


class CardHeader(QWidget):
    """卡片头部组件"""

    def __init__(self, icon: str, title: str, subtitle: str = "", parent=None):
        """
        初始化卡片头部

        Args:
            icon: 图标字符（emoji 或 Unicode）
            title: 标题文本
            subtitle: 副标题文本（可选）
            parent: 父组件
        """
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self.subtitle = subtitle
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(get_spacing("md"))

        # 图标
        self.icon_label = QLabel(self.icon)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        apply_icon_style(self.icon_label, size="lg")
        layout.addWidget(self.icon_label)

        # 标题和副标题
        text_layout = QVBoxLayout()
        text_layout.setSpacing(get_spacing("xs"))

        self.title_label = StrongBodyLabel(self.title)
        apply_font_style(self.title_label, size="lg", weight="semibold")
        text_layout.addWidget(self.title_label)

        if self.subtitle:
            self.subtitle_label = BodyLabel(self.subtitle)
            self.subtitle_label.setWordWrap(True)
            apply_muted_text_style(self.subtitle_label, size="sm")
            text_layout.addWidget(self.subtitle_label)

        layout.addLayout(text_layout, stretch=1)

    def set_title(self, title: str):
        """
        设置标题

        Args:
            title: 新标题
        """
        self.title = title
        self.title_label.setText(title)

    def set_subtitle(self, subtitle: str):
        """
        设置副标题

        Args:
            subtitle: 新副标题
        """
        self.subtitle = subtitle
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)
