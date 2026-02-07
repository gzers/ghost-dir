"""
状态徽章组件
显示连接状态的可视化指示器
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel
from src.models.link import LinkStatus  # 新架构: 使用 models 层
from src.gui.styles import (
    get_spacing, apply_badge_style, apply_icon_style,
    get_status_icon, get_status_colors, apply_font_style, apply_transparent_background_only
)
from src.gui.i18n import get_status_text


class StatusBadge(QWidget):
    """状态徽章组件"""

    def __init__(self, status, parent=None):
        """
        初始化状态徽章

        Args:
            status: 连接状态 (LinkStatus 枚举或其字符串值)
            parent: 父组件
        """
        super().__init__(parent)
        self.status = status
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        status_val = self.status.value if hasattr(self.status, 'value') else self.status
        # 应用标准徽章样式
        apply_badge_style(self, status=status_val)

        # 清空布局边距以防干扰
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(get_spacing("xs"))
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        # 状态图标
        icon_char = get_status_icon(status_val)
        icon_label = QLabel(icon_char)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        apply_icon_style(icon_label, size="md")

        # 状态文本 - 使用 i18n
        status_colors = get_status_colors()
        text_label = BodyLabel(get_status_text(status_val))
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # 使用状态色作为文本颜色
        apply_font_style(text_label, color=status_colors[status_val])
        apply_transparent_background_only(text_label)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

    def update_status(self, status: LinkStatus):
        """更新状态"""
        self.status = status
        # 清除旧的布局
        if self.layout():
            while self.layout().count():
                child = self.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            # 重新初始化 UI 逻辑（由于 apply_badge_style 会修改样式，直接重新调用 _init_ui 即可）
            self._init_ui()
