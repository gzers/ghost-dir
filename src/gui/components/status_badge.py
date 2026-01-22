"""
状态徽章组件
显示连接状态的可视化指示器
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel
from ...data.model import LinkStatus
from ..styles import StyleManager, get_spacing, get_radius, get_font_style
from ..i18n import get_status_text


class StatusBadge(QWidget):
    """状态徽章组件"""

    def __init__(self, status: LinkStatus, parent=None):
        """
        初始化状态徽章

        Args:
            status: 连接状态
            parent: 父组件
        """
        super().__init__(parent)
        self.status = status
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        spacing = get_spacing()
        layout.setContentsMargins(spacing["sm"], spacing["xs"], spacing["sm"], spacing["xs"])
        layout.setSpacing(spacing["xs"])

        # 获取样式
        status_colors = StyleManager.get_status_colors()
        status_icons = StyleManager.get_status_icons()

        # 状态图标 - 使用统一字体规范
        icon_label = QLabel(status_icons[self.status.value])
        icon_label.setStyleSheet(get_font_style(size="md"))

        # 状态文本 - 使用 i18n
        text_label = BodyLabel(get_status_text(self.status.value))
        text_label.setStyleSheet(f"color: {status_colors[self.status.value]};")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()

        # 设置背景颜色 - 使用统一样式
        self.setStyleSheet(StyleManager.get_badge_style(self.status.value))
    
    def update_status(self, status: LinkStatus):
        """更新状态"""
        self.status = status
        # 清除旧的布局
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # 重新初始化
        self._init_ui()
