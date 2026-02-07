"""
国际化管理器
"""
from typing import Dict, Any


class I18nManager:
    """国际化管理器"""

    _instance = None
    _current_language = "zh_CN"  # 当前语言
    _texts = {}  # 文案字典

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化国际化管理器"""
        pass

    def set_texts(self, texts: Dict[str, Any]):
        """设置文案字典"""
        self._texts = texts

    def get(self, key: str, **kwargs) -> str:
        """
        获取文案

        Args:
            key: 文案键,支持点号分隔的路径,如 "common.confirm"
            **kwargs: 动态参数,用于替换文案中的占位符

        Returns:
            文案字符串
        """
        keys = key.split(".")
        value = self._texts

        try:
            for k in keys:
                value = value[k]

            # 如果有参数,进行替换
            if kwargs:
                return value.format(**kwargs)
            return value
        except (KeyError, TypeError):
            return f"[Missing: {key}]"

    def set_language(self, language: str):
        """设置当前语言"""
        self._current_language = language
