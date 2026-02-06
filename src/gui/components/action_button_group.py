"""
操作按钮组组件
根据连接状态显示相应的操作按钮
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Signal
from qfluentwidgets import PushButton, FluentIcon
from src.models.link import LinkStatus  # 新架构: 使用 models 层
from src.gui.styles import get_spacing
from src.gui.i18n import t


class ActionButtonGroup(QWidget):
    """操作按钮组组件"""
    
    # 信号
    establish_clicked = Signal()    # 建立连接
    disconnect_clicked = Signal()   # 断开连接
    delete_clicked = Signal()       # 删除
    
    def __init__(self, status: LinkStatus, parent=None):
        """
        初始化操作按钮组
        
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(get_spacing("sm"))
        
        # 根据状态显示不同的按钮
        if self.status == LinkStatus.DISCONNECTED:
            # 未连接:显示"建立连接"按钮
            establish_btn = PushButton(FluentIcon.LINK, t("connected.establish"))
            establish_btn.clicked.connect(self.establish_clicked.emit)
            layout.addWidget(establish_btn)
            
        elif self.status == LinkStatus.CONNECTED:
            # 已连接:显示"断开连接"按钮
            disconnect_btn = PushButton(FluentIcon.CLOSE, t("connected.disconnect"))
            disconnect_btn.clicked.connect(self.disconnect_clicked.emit)
            layout.addWidget(disconnect_btn)
            
        elif self.status == LinkStatus.READY:
            # 就绪:显示"重新连接"按钮
            reconnect_btn = PushButton(FluentIcon.SYNC, t("connected.reconnect"))
            reconnect_btn.clicked.connect(self.establish_clicked.emit)
            layout.addWidget(reconnect_btn)
        
        # 所有状态都显示"删除"按钮
        delete_btn = PushButton(FluentIcon.DELETE, t("common.delete"))
        delete_btn.clicked.connect(self.delete_clicked.emit)
        layout.addWidget(delete_btn)
        
        layout.addStretch()
    
    def update_status(self, status: LinkStatus):
        """
        更新状态并刷新按钮
        
        Args:
            status: 新的连接状态
        """
        self.status = status
        
        # 清除旧的布局
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 重新初始化
        self._init_ui()
