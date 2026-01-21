"""
状态徽章组件
显示连接状态的可视化指示器
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel
from ...data.model import LinkStatus
from ...common.config import STATUS_COLORS, STATUS_ICONS


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
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)
        
        # 状态图标
        icon_label = QLabel(STATUS_ICONS[self.status.value])
        icon_label.setStyleSheet("font-size: 14px;")
        
        # 状态文本
        status_text = {
            LinkStatus.DISCONNECTED: "未连接",
            LinkStatus.CONNECTED: "已连接",
            LinkStatus.READY: "就绪",
            LinkStatus.INVALID: "失效"
        }
        
        text_label = BodyLabel(status_text[self.status])
        text_label.setStyleSheet(f"color: {STATUS_COLORS[self.status.value]};")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        
        # 设置背景颜色
        self.setStyleSheet(f"""
            StatusBadge {{
                background-color: {STATUS_COLORS[self.status.value]}20;
                border-radius: 4px;
            }}
        """)
    
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
