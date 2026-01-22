"""
图标工具函数
获取图标尺寸、颜色、间距和状态规范
"""
from ..constants import icons
from .color_utils import (
    get_text_primary, get_text_secondary, get_text_tertiary, get_text_disabled,
    get_accent_color, get_success_color, get_warning_color, get_error_color, get_info_color
)

def get_icon_size(size: str = "md") -> int:
    """获取图标尺寸像素值"""
    return icons.ICON_SIZES.get(size, icons.ICON_SIZES["md"])

def get_icon_color(level: str = "primary") -> str:
    """获取语义化图标颜色"""
    color_map = {
        "primary": get_text_primary(),
        "secondary": get_text_secondary(),
        "tertiary": get_text_tertiary(),
        "disabled": get_text_disabled(),
        "accent": get_accent_color(),
        "success": get_success_color(),
        "warning": get_warning_color(),
        "error": get_error_color(),
        "info": get_info_color(),
    }
    return color_map.get(level, color_map["primary"])

def get_icon_spacing(type: str = "icon_text") -> int:
    """获取图标相关间距"""
    return icons.ICON_SPACING.get(type, icons.ICON_SPACING["icon_text"])

def get_icon_state(state: str = "default") -> dict:
    """获取图标状态属性 (opacity, scale)"""
    return icons.ICON_STATES.get(state, icons.ICON_STATES["default"])

def get_status_icon(status: str) -> str:
    """获取状态对应的图标字符"""
    return icons.STATUS_ICONS.get(status, icons.STATUS_ICONS["invalid"])
