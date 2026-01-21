"""
模版库视图（占位）
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel

class LibraryView(QWidget):
    """模版库视图"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("模版库"))
        layout.addWidget(BodyLabel("浏览所有官方和自定义模版"))
        layout.addStretch()
