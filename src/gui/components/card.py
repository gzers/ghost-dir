"""
卡片组件基类
使用 QFluentWidgets 官方 CardWidget
"""
from qfluentwidgets import CardWidget, setCustomStyleSheet
from ..styles import color_utils

class Card(CardWidget):
    """
    基础卡片类
    
    提供一致的半透明背景，以完美呈现底层的 Mica/Acrylic 特效。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._update_card_style()
        
    def _update_card_style(self):
        """应用统一的卡片背景样式"""
        bg = color_utils.get_card_background()
        border = color_utils.get_border_color()
        # 强制设置背景和边框，确保穿透效果
        setCustomStyleSheet(
            self,
            lightQss=f"Card {{ background-color: {bg}; border: 1px solid {border}; }}",
            darkQss=f"Card {{ background-color: {bg}; border: 1px solid {border}; }}"
        )
