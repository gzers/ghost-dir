"""
帮助/关于视图
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel
from ..settings.widgets.about_card import AboutCard

class HelpView(QWidget):
    """帮助/关于视图"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        title = TitleLabel("帮助")
        layout.addWidget(title)
        
        # 关于卡片
        about_card = AboutCard(self)
        layout.addWidget(about_card)
        
        layout.addStretch()
