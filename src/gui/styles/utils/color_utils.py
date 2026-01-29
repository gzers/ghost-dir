"""
颜色工具函数
提供主题感知的颜色访问接口
"""
from ..constants import colors

def get_page_background() -> str:
    return colors.get_page_background()

def get_container_background() -> str:
    return colors.get_container_background()

def get_card_background() -> str:
    return colors.get_card_background()

def get_hover_background() -> str:
    return colors.get_hover_background()

def get_border_color() -> str:
    return colors.get_border_color()

def get_text_primary() -> str:
    return colors.get_text_primary()

def get_text_secondary() -> str:
    return colors.get_text_secondary()

def get_text_tertiary() -> str:
    return colors.get_text_tertiary()

def get_text_muted() -> str:
    return colors.get_text_muted()

def get_text_disabled() -> str:
    return colors.TEXT_DISABLED

def get_status_colors() -> dict:
    return colors.STATUS_COLORS

def get_success_color() -> str:
    return colors.SUCCESS_COLOR

def get_warning_color() -> str:
    return colors.WARNING_COLOR

def get_error_color() -> str:
    return colors.ERROR_COLOR

def get_info_color() -> str:
    return colors.INFO_COLOR

def get_surface_color() -> str:
    return colors.get_surface_color()

def get_outline_color() -> str:
    return colors.get_outline_color()

def get_divider_color() -> str:
    return colors.get_divider_color()

def get_shadow_color() -> str:
    return colors.get_shadow_color()

def get_accent_color() -> str:
    """获取当前的强调色 (Hex 格式)"""
    from qfluentwidgets import ThemeColor
    return ThemeColor.PRIMARY.color().name()

def get_icon_background(opacity: float = 0.05) -> str:
    """
    获取图标背景色

    Args:
        opacity: 透明度 (0.0 - 1.0)，默认 0.05

    Returns:
        RGBA 格式的背景色字符串
    """
    from qfluentwidgets import isDarkTheme
    # 根据主题选择白色或黑色作为基色
    if isDarkTheme():
        # 暗色主题使用白色
        return f"rgba(255,255,255,{opacity})"
    else:
        # 亮色主题使用黑色
        return f"rgba(0,0,0,{opacity})"
