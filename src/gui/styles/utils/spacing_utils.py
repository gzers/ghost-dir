"""
间距工具函数
获取间距、内边距、外边距和圆角像素值
"""
from typing import Tuple
from ..constants import spacing

def get_spacing(size: str = "md") -> int:
    """获取基础间距像素值"""
    return spacing.SPACING_SCALE.get(size, spacing.SPACING_SCALE["md"])

def get_padding(size: str = "md") -> Tuple[int, int, int, int]:
    """获取内边距规范 (top, right, bottom, left)"""
    return spacing.PADDING_SCALE.get(size, spacing.PADDING_SCALE["md"])

def get_margin(size: str = "md") -> Tuple[int, int, int, int]:
    """获取外边距规范 (top, right, bottom, left)"""
    return spacing.MARGIN_SCALE.get(size, spacing.MARGIN_SCALE["md"])

def get_radius(size: str = "md") -> int:
    """获取圆角像素值"""
    return spacing.BORDER_RADIUS.get(size, spacing.BORDER_RADIUS["md"])

def get_layout_margins() -> dict:
    """获取布局边距规范"""
    return spacing.LAYOUT_MARGINS

def get_list_spacing() -> dict:
    """获取列表间距规范"""
    return spacing.LIST_SPACING

def get_content_width(level: str = "narrow") -> int:
    """获取预定义的容器最大宽度"""
    from ..constants.components import COMPONENT_STYLES
    widths = COMPONENT_STYLES.get("content_width", {})
    return widths.get(level)

def get_card_padding() -> Tuple[int, int, int, int]:
    """获取标准卡片内边距规范 (top, right, bottom, left)"""
    from ..constants.components import COMPONENT_STYLES
    return COMPONENT_STYLES["card"]["padding"]

def get_badge_padding() -> Tuple[int, int, int, int]:
    """获取标准徽章内边距规范 (top, right, bottom, left)"""
    from ..constants.components import COMPONENT_STYLES
    return COMPONENT_STYLES["badge"]["padding"]
