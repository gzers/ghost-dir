"""
卡片组件基类
支持 QSS 样式渲染，实现亚克力和边框效果
"""
from PySide6.QtWidgets import QFrame
from ..styles import apply_card_style

class Card(QFrame):
    """
    基础卡片类
    
    采用 QFrame 确保样式能够被正确渲染。
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.update_style()
        
        # 监听主题变更
        from ...common.signals import signal_bus
        signal_bus.theme_changed.connect(self.update_style)
        
    def update_style(self, theme=None):
        """更新并应用卡片样式"""
        apply_card_style(self)
        self.update()
