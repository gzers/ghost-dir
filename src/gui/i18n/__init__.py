"""
国际化模块
提供多语言支持和文案管理
"""
from .zh_CN import (
    I18nManager,
    t,
    get_status_text,
    get_category_text,
    TEXTS,
)

__all__ = [
    "I18nManager",
    "t",
    "get_status_text",
    "get_category_text",
    "TEXTS",
]
