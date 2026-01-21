"""
智能向导视图
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel

class WizardView(QWidget):
    """智能向导视图"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("智能向导"))
        layout.addWidget(BodyLabel("引导式操作，快速完成常见任务"))
        layout.addStretch()
