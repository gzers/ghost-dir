"""
卡片组件基类
支持 QSS 样式渲染，实现亚克力和边框效果
"""
from PySide6.QtWidgets import QWidget, QStyle, QStyleOption
from PySide6.QtGui import QPainter
from ..styles import apply_card_style

class Card(QWidget):
    """
    基础卡片类
    
    解决了 QWidget 子类无法直接通过 QSS 渲染背景和边框的问题。
    所有的亚克力卡片组件都应继承此类。
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_style()
        
        # 监听主题变更
        from ...common.signals import signal_bus
        signal_bus.theme_changed.connect(self.update_style)
        
    def update_style(self, theme=None):
        """更新并应用卡片样式"""
        apply_card_style(self)
        self.update()

    def paintEvent(self, event):
        """支持 QSS 渲染自定义控件"""
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
