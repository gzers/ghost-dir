"""
图标样式应用
应用图标大小、颜色、间距及交互状态
"""
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from src.gui.styles.utils import icon_utils, spacing_utils, typography_utils

def apply_icon_style(widget, size: str = "md", color_level: str = "primary"):
    """
    应用图标样式

    Args:
        widget: 目标 widget (通常是 QLabel 或 QPushButton)
        size: 尺寸阶梯 ('xs' 到 'xxxl')
        color_level: 颜色层级 ('primary', 'accent', 'success', etc.)
    """
    px_size = icon_utils.get_icon_size(size)
    color = icon_utils.get_icon_color(color_level)

    style = f"font-size: {px_size}px; color: {color};"
    # 如果已有 styleSheet，则追加
    existing = widget.styleSheet()
    if style not in existing:
        widget.setStyleSheet(existing + style)

def create_icon_with_text(
    icon_char: str,
    text: str,
    icon_size: str = "md",
    text_size: str = "md",
    spacing: str = "icon_text",
    parent=None
) -> QWidget:
    """
    创建一个包含图标和文字的组合组件

    Args:
        icon_char: 图标字符 (如 '🔗')
        text: 文本内容
        icon_size: 图标尺寸阶梯
        text_size: 文本尺寸阶梯
        spacing: 间距类型 ('icon_text', 'icon_icon', etc.)
        parent: 父组件
    """
    container = QWidget(parent)
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(icon_utils.get_icon_spacing(spacing))

    # 图标标签
    icon_label = QLabel(icon_char)
    apply_icon_style(icon_label, size=icon_size)

    # 文本标签
    text_label = QLabel(text)
    from src.gui.styles.appliers.component import apply_font_style
    apply_font_style(text_label, size=text_size)

    layout.addWidget(icon_label)
    layout.addWidget(text_label)
    layout.addStretch()

    return container

def get_icon_state_style(state: str = "default") -> str:
    """获取图标状态的 CSS 样式片段"""
    st = icon_utils.get_icon_state(state)
    return f"opacity: {st['opacity']};"
