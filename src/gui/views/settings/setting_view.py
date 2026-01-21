"""
设置视图（重构版）
页面主体 - 负责布局和协调
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel
from .about_card import AboutCard


class SettingView(QWidget):
    """设置视图"""
    
    def __init__(self, parent=None):
        """初始化设置视图"""
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 标题
        title = TitleLabel("设置")
        layout.addWidget(title)
        
        # 关于卡片组件
        about_card = AboutCard(self)
        layout.addWidget(about_card)
        
        layout.addStretch()
