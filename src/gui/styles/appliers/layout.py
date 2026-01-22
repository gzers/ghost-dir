"""
布局样式应用
应用页面、容器、布局及间距样式
"""
from ..utils import color_utils, spacing_utils

def apply_page_style(widget) -> None:
    """应用页面主背景颜色"""
    if not widget.objectName():
        widget.setObjectName(f"page_{id(widget)}")
    obj_name = widget.objectName()
    bg_color = color_utils.get_page_background()
    widget.setStyleSheet(f"#{obj_name} {{ background-color: {bg_color}; border: none; }}")

def apply_container_style(widget) -> None:
    """应用容器背景（半透明）"""
    if not widget.objectName():
        widget.setObjectName(f"container_{id(widget)}")
    obj_name = widget.objectName()
    bg_color = color_utils.get_container_background()
    widget.setStyleSheet(f"#{obj_name} {{ background-color: {bg_color}; border: none; }}")

def apply_page_layout(layout, spacing: str = "group"):
    """
    应用标准化页面布局规范（边距和间距）
    
    Args:
        layout: QLayout 实例
        spacing: 间距类型 ('group', 'section', 'item')
    """
    margins = spacing_utils.get_layout_margins()
    spacing_val = spacing_utils.get_list_spacing().get(spacing, 20)
    
    m = margins["page"]
    layout.setContentsMargins(m, m, m, m)
    layout.setSpacing(spacing_val)

def apply_spacing(layout, size: str = "md"):
    """应用特定大小的间距到布局"""
    val = spacing_utils.get_spacing(size)
    layout.setSpacing(val)

def apply_padding(widget, size: str = "md"):
    """应用标准化内边距到 QWidget (通过 setStyleSheet)"""
    p = spacing_utils.get_padding(size)
    # p is (top, right, bottom, left)
    style = f"padding: {p[0]}px {p[1]}px {p[2]}px {p[3]}px;"
    existing = widget.styleSheet()
    widget.setStyleSheet(existing + style)

def apply_layout_margins(layout, preset: str = "card") -> None:
    """
    通过预设名称应用布局边距
    
    Args:
        layout: 目标 QLayout
        preset: 预设名称 ('card', 'badge', 'page', 'section', 'compact')
    """
    if preset == "card":
        p = spacing_utils.get_card_padding()
    elif preset == "badge":
        p = spacing_utils.get_badge_padding()
    else:
        # fallback 到基础布局边距
        m_val = spacing_utils.get_layout_margins().get(preset, 0)
        p = (m_val, m_val, m_val, m_val)
    
    # p is (top, right, bottom, left)
    # Qt setContentsMargins uses (left, top, right, bottom)
    layout.setContentsMargins(p[3], p[0], p[1], p[2])
