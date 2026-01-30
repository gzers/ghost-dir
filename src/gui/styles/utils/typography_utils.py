"""
排版工具函数
获取字体、大小、粗细、行高及层级规范
"""
from typing import Dict, Any
from ..constants import typography

def get_font_family() -> str:
    """获取默认字体族"""
    return typography.FONT_FAMILY

def get_font_size(size: str = "md") -> int:
    """获取字体大小像素值"""
    return typography.FONT_SIZES.get(size, typography.FONT_SIZES["md"])

def get_font_weight(weight: str = "normal") -> int:
    """获取字体粗细数值"""
    return typography.FONT_WEIGHTS.get(weight, typography.FONT_WEIGHTS["normal"])

def get_line_height(level: str = "normal") -> float:
    """获取行高倍数"""
    return typography.LINE_HEIGHTS.get(level, typography.LINE_HEIGHTS["normal"])

def get_typography_scale() -> Dict[str, Dict[str, Any]]:
    """获取完整排版阶梯"""
    return typography.TYPOGRAPHY_SCALE

def get_text_hierarchy() -> Dict[str, Dict[str, Any]]:
    """获取文字层级规范"""
    return typography.TEXT_HIERARCHY

def get_font_style(
    size: str = "md",
    weight: str = "normal",
    color: str = None
) -> str:
    """
    获取字体样式字符串（用于内联样式）

    Args:
        size: 字体大小 (xs, sm, md, lg, xl, xxl, title, display)
        weight: 字体粗细 (light, regular/normal, medium, semibold, bold)
        color: 文本颜色（可选）

    Returns:
        CSS 样式字符串
    """
    from .color_utils import get_text_primary
    
    font_family = get_font_family()
    font_size = get_font_size(size)
    font_weight = get_font_weight(weight)
    text_color = color or get_text_primary()

    return (
        f"font-family: {font_family}; "
        f"font-size: {font_size}px; "
        f"font-weight: {font_weight}; "
        f"color: {text_color};"
    )
def format_required_label(text: str) -> str:
    """
    格式化必填项标签，添加规范化的红色星号及间距
    
    Args:
        text: 标签文字
        
    Returns:
        包含 HTML 样式的字符串
    """
    from ..constants.spacing import SPACING_SCALE
    
    # 获取设计系统中的 xs 级间距 (目前定义为 4px)
    # 为了解决 Qt Rich Text 对 margin 支持不佳的问题，改用 &nbsp; 配合 padding
    spacing = SPACING_SCALE["xs"]
    
    # 规范：红色标星，使用 inline-block 模拟间距
    # 注意：Qt 对某些 CSS 属性支持有限，这里使用 padding-left 确保在 QLabel 中生效
    star_style = (
        f"color: #EF4444; "
        f"font-weight: bold; "
        f"padding-left: {spacing}px;"
    )
    star_html = f'<span style="{star_style}">*</span>'
    return f"{text}{star_html}"
