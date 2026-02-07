"""
组件样式应用
应用卡片、按钮、徽章、文字等组件级别样式
"""
from src.gui.styles.utils import color_utils, spacing_utils, typography_utils
from src.gui.styles.constants.components import COMPONENT_STYLES

def apply_card_style(widget, size: str = "md"):
    """
    应用标准卡片样式

    Args:
        widget: 目标 QWidget
        size: 尺寸（预留，目前使用标准规范）
    """
    spec = COMPONENT_STYLES["card"]
    bg = color_utils.get_card_background()
    hover_bg = color_utils.get_hover_background()
    border = color_utils.get_border_color()
    radius = spec["border_radius"]
    p = spec["padding"]

    # 为组件设置对象名以实现精确定位选择器
    if not widget.objectName():
        widget.setObjectName(f"card_{id(widget)}")
    obj_name = widget.objectName()

    style = f"""
        #{obj_name} {{
            background-color: {bg};
            border: {spec['border_width']}px solid {border};
            border-radius: {radius}px;
            padding: {p[0]}px {p[1]}px {p[2]}px {p[3]}px;
        }}
        #{obj_name}:hover {{
            background-color: {hover_bg};
        }}
    """
    widget.setStyleSheet(style)

def apply_badge_style(widget, status: str = "invalid"):
    """应用状态徽章样式"""
    status_colors = color_utils.get_status_colors()
    color = status_colors.get(status, status_colors["invalid"])
    radius = spacing_utils.get_radius("sm")
    p = spacing_utils.get_padding("xs")

    # 为组件设置对象名以实现精确定位选择器
    if not widget.objectName():
        widget.setObjectName(f"badge_{id(widget)}")
    obj_name = widget.objectName()

    style = f"""
        #{obj_name} {{
            background-color: {color}20;
            border-radius: {radius}px;
            padding: {p[0]}px {p[1]}px {p[2]}px {p[3]}px;
        }}
        #{obj_name} QLabel {{
            color: {color};
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: 500;
        }}
    """
    widget.setStyleSheet(style)

def apply_accent_badge_style(widget):
    """应用强调色背景的徽章样式 (标准按钮强调色)"""
    color = color_utils.get_accent_color()
    radius = spacing_utils.get_radius("sm")

    # 为组件设置对象名
    if not widget.objectName():
        widget.setObjectName(f"accent_badge_{id(widget)}")
    obj_name = widget.objectName()

    # 强调色背景，白色文字，半透明边缘感
    style = f"""
        #{obj_name} {{
            background-color: {color};
            color: white;
            border-radius: {radius}px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
    """
    widget.setStyleSheet(style)

def apply_font_style(
    widget,
    size: str = "md",
    weight: str = "normal",
    color: str = "primary"
):
    """应用字体样式"""
    family = typography_utils.get_font_family()
    px_size = typography_utils.get_font_size(size)
    px_weight = typography_utils.get_font_weight(weight)

    # 尝试作为预定义颜色层级
    color_map = {
        "primary": color_utils.get_text_primary(),
        "secondary": color_utils.get_text_secondary(),
        "tertiary": color_utils.get_text_tertiary(),
        "muted": color_utils.get_text_muted(),
        "disabled": color_utils.get_text_disabled(),
    }

    # 如果输入的 color 在 map 中，则使用 map 里的值，否则直接使用 color (作为十六进制字符串等)
    text_color = color_map.get(color, color)

    style = f"""
        font-family: {family};
        font-size: {px_size}px;
        font-weight: {px_weight};
        color: {text_color};
        background: transparent;
        border: none;
    """
    widget.setStyleSheet(style)

def apply_muted_text_style(widget, size: str = "sm"):
    """应用弱化文本样式"""
    apply_font_style(widget, size=size, color="muted")
