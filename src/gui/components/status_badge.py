"""
状态徽章组件
显示连接状态的可视化指示器
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel
from ...data.model import LinkStatus
from ..styles import (
    get_spacing, apply_badge_style, apply_icon_style, 
    get_status_icon, get_status_colors
)
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
        # 应用标准徽章样式
        apply_badge_style(self, status=self.status.value)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # apply_badge_style 处理内边距
        layout.setSpacing(get_spacing("xs"))

        # 状态图标
        icon_char = get_status_icon(self.status.value)
        icon_label = QLabel(icon_char)
        apply_icon_style(icon_label, size="md") # 文字图标也使用图标规范

        # 状态文本 - 使用 i18n
        status_colors = get_status_colors()
        text_label = BodyLabel(get_status_text(self.status.value))
        text_label.setStyleSheet(f"color: {status_colors[self.status.value]}; background: transparent; border: none;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
    
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
