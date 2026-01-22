"""
样式管理器
负责主题感知和统一样式访问
"""
from qfluentwidgets import isDarkTheme
from ...common.signals import signal_bus
from .utils import color_utils, spacing_utils, typography_utils, icon_utils

class StyleManager:
    """样式管理器 - 提供主题感知的样式访问 (保持向后兼容)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化样式管理器"""
        if self._initialized:
            return
        self._initialized = True
        
        # 监听主题变更
        signal_bus.theme_changed.connect(self._on_theme_changed)
    
    def _on_theme_changed(self, theme: str):
        """主题变更回调"""
        pass
    
    # ========== 桥接颜色系统 ==========
    @staticmethod
    def get_page_background(): return color_utils.get_page_background()
    
    @staticmethod
    def get_container_background(): return color_utils.get_container_background()
    
    @staticmethod
    def get_card_background(): return color_utils.get_card_background()
    
    @staticmethod
    def get_hover_background(): return color_utils.get_hover_background()
    
    @staticmethod
    def get_border_color(): return color_utils.get_border_color()
    
    @staticmethod
    def get_text_primary(): return color_utils.get_text_primary()
    
    @staticmethod
    def get_text_secondary(): return color_utils.get_text_secondary()
    
    @staticmethod
    def get_text_tertiary(): return color_utils.get_text_tertiary()
    
    @staticmethod
    def get_text_muted(): return color_utils.get_text_muted()
    
    @staticmethod
    def get_text_disabled(): return color_utils.get_text_disabled()
    
    @staticmethod
    def get_status_colors(): return color_utils.get_status_colors()
    
    @staticmethod
    def get_success_color(): return color_utils.get_success_color()
    
    @staticmethod
    def get_warning_color(): return color_utils.get_warning_color()
    
    @staticmethod
    def get_error_color(): return color_utils.get_error_color()
    
    @staticmethod
    def get_info_color(): return color_utils.get_info_color()

    # ========== 桥接间距系统 ==========
    @staticmethod
    def get_icon_sizes(): return {k: icon_utils.get_icon_size(k) for k in ["sm", "md", "lg", "xl"]}
    
    @staticmethod
    def get_spacing(): return {k: spacing_utils.get_spacing(k) for k in ["xs", "sm", "md", "lg", "xl", "xxl", "xxxl"]}
    
    @staticmethod
    def get_layout_margins(): return spacing_utils.get_layout_margins()
    
    @staticmethod
    def get_list_spacing(): return spacing_utils.get_list_spacing()
    
    @staticmethod
    def get_border_radius(): return {k: spacing_utils.get_radius(k) for k in ["sm", "md", "lg", "xl", "xxl"]}

    # ========== 桥接排版系统 ==========
    @staticmethod
    def get_font_family(): return typography_utils.get_font_family()
    
    @staticmethod
    def get_font_weights(): return {k: typography_utils.get_font_weight(k) for k in ["light", "regular", "normal", "medium", "semibold", "bold"]}
    
    @staticmethod
    def get_line_heights(): return {k: typography_utils.get_line_height(k) for k in ["tight", "normal", "relaxed"]}
    
    @staticmethod
    def get_font_sizes(): return {k: typography_utils.get_font_size(k) for k in ["xs", "sm", "md", "lg", "xl", "xxl", "title", "display"]}
    
    @staticmethod
    def get_typography_scale(): return typography_utils.get_typography_scale()
    
    @staticmethod
    def get_text_hierarchy(): return typography_utils.get_text_hierarchy()

    # ========== 桥接组件样式 (内联样式) ==========
    @staticmethod
    def get_badge_style(status: str) -> str:
        """获取徽章样式字符串"""
        colors = color_utils.get_status_colors()
        color = colors.get(status, colors["invalid"])
        radius = spacing_utils.get_radius("sm")
        spacing = spacing_utils.get_spacing("sm")
        xs_spacing = spacing_utils.get_spacing("xs")
        
        return f"""
            QWidget {{
                background-color: {color}20;
                border-radius: {radius}px;
                padding: {xs_spacing}px {spacing}px;
            }}
            QLabel {{
                color: {color};
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def get_label_style(color: str = None, size: int = 14, weight: str = "normal") -> str:
        """获取标签样式字符串"""
        text_color = color or color_utils.get_text_primary()
        return f"color: {text_color}; font-size: {size}px; font-weight: {weight};"

    @staticmethod
    def get_icon_style(size: str = "md") -> str:
        """获取图标样式字符串"""
        px_size = icon_utils.get_icon_size(size)
        return f"font-size: {px_size}px;"

    @staticmethod
    def get_button_style(variant: str = "primary") -> str:
        """获取按钮样式基础字符串"""
        spacing = spacing_utils.get_spacing("sm")
        lg_spacing = spacing_utils.get_spacing("lg")
        radius = spacing_utils.get_radius("md")
        return f"padding: {spacing}px {lg_spacing}px; border-radius: {radius}px; font-size: 14px;"

    @staticmethod
    def get_card_style() -> str:
        """获取卡片样式字符串"""
        bg = color_utils.get_card_background()
        border = color_utils.get_border_color()
        radius = spacing_utils.get_radius("lg")
        return f"background-color: {bg}; border: 1px solid {border}; border-radius: {radius}px;"
