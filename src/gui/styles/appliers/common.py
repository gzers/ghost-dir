"""
通用样式应用
提供常用的样式应用函数，如透明背景、无边框等
"""
from qfluentwidgets import setCustomStyleSheet


def apply_transparent_style(widget):
    """
    应用透明背景样式

    Args:
        widget: 目标 QWidget
    """
    setCustomStyleSheet(
        widget,
        lightQss="background: transparent; border: none;",
        darkQss="background: transparent; border: none;"
    )


def apply_transparent_background_only(widget):
    """
    仅应用透明背景样式（保留边框）

    Args:
        widget: 目标 QWidget
    """
    setCustomStyleSheet(
        widget,
        lightQss="background: transparent;",
        darkQss="background: transparent;"
    )


def apply_no_border(widget):
    """
    应用无边框样式

    Args:
        widget: 目标 QWidget
    """
    setCustomStyleSheet(
        widget,
        lightQss="border: none;",
        darkQss="border: none;"
    )
