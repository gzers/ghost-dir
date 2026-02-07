# coding: utf-8
"""
配置服务 - 管理应用程序配置
"""
import json
from pathlib import Path
from typing import Any, Optional
from src.common.config import (
    USER_CONFIG_FILE,
    DEFAULT_THEME,
    DEFAULT_THEME_COLOR,
    DEFAULT_STARTUP_PAGE,
    DEFAULT_LINK_VIEW,
    DEFAULT_TARGET_ROOT
)


class ConfigService:
    """配置服务 - 负责读写应用程序配置"""

    def __init__(self):
        """初始化配置服务"""
        self.config_file = Path(USER_CONFIG_FILE)
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件"""
        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}

    def _save_config(self) -> bool:
        """保存配置文件"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)

    def set_config(self, key: str, value: Any) -> bool:
        """设置配置项"""
        self._config[key] = value
        return self._save_config()

    def get_theme(self) -> str:
        """获取主题设置"""
        return self.get_config("theme", DEFAULT_THEME)

    def set_theme(self, theme: str) -> bool:
        """设置主题"""
        return self.set_config("theme", theme)

    def get_theme_color(self) -> str:
        """获取主题色"""
        return self.get_config("theme_color", DEFAULT_THEME_COLOR)

    def set_theme_color(self, color: str) -> bool:
        """设置主题色"""
        return self.set_config("theme_color", color)

    def get_startup_page(self) -> str:
        """获取启动页"""
        return self.get_config("startup_page", DEFAULT_STARTUP_PAGE)

    def set_startup_page(self, page: str) -> bool:
        """设置启动页"""
        return self.set_config("startup_page", page)

    def get_default_link_view(self) -> str:
        """获取默认链接视图"""
        return self.get_config("default_link_view", DEFAULT_LINK_VIEW)

    def set_default_link_view(self, view: str) -> bool:
        """设置默认链接视图"""
        return self.set_config("default_link_view", view)

    def get_default_target_root(self) -> str:
        """获取默认目标根目录"""
        return self.get_config("default_target_root", DEFAULT_TARGET_ROOT)

    def set_default_target_root(self, path: str) -> bool:
        """设置默认目标根目录"""
        return self.set_config("default_target_root", path)

    def get_transparency(self) -> bool:
        """获取窗口透明度设置"""
        return self.get_config("transparency", True)

    def set_transparency(self, enabled: bool) -> bool:
        """设置窗口透明度"""
        return self.set_config("transparency", enabled)
