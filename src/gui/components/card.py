"""
卡片组件基类
使用 QFluentWidgets 官方 CardWidget
"""
from qfluentwidgets import CardWidget

class Card(CardWidget):
    """
    基础卡片类
    
    继承自 QFluentWidgets 的 CardWidget，提供一致的样式和主题支持。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
