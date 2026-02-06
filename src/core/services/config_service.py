"""
配置服务 (ConfigService)
负责全局配置的读写、副作用执行
"""
from typing import Any, Optional, Dict
from src.data.app_config_manager import AppConfigManager


class ConfigService:
    """配置业务服务"""

    def __init__(self, app_config_manager: AppConfigManager):
        self.app_config_manager = app_config_manager

    def get_config(self, key: str, default: Any = None) -> Any:
        """读取配置项"""
        return self.app_config_manager.get(key, default)

    def set_config(self, key: str, value: Any) -> bool:
        """写入配置项并触发副作用"""
        # 1. 业务校验
        if key == "default_target_root":
            import os
            if not os.path.exists(os.path.expandvars(value)):
                return False

        # 2. 执行持久化
        success = self.app_config_manager.set(key, value)
        
        # 3. 副作用执行 (Side Effects)
        if success:
            self._handle_side_effect(key, value)
            
        return success

    def _handle_side_effect(self, key: str, value: Any):
        """处理配置变更的副作用"""
        # 广播信号
        from src.common.signals import signal_bus
        
        # 发射全局通知
        signal_bus.config_changed.emit(key, value)
        
        # 特殊副作用逻辑
        if key == "theme":
            # 动态切换主题逻辑
            pass

    def get_app_stats(self) -> Dict[str, Any]:
        """获取应用统计信息"""
        # TODO: 需要从其他地方获取统计信息
        return {
            "version": "1.2.0"
        }

    # 业务快捷方法
    def get_theme(self) -> str:
        return self.app_config_manager.get_theme()

    def set_theme(self, theme: str) -> bool:
        success = self.app_config_manager.set_theme(theme)
        if success:
            self._handle_side_effect("theme", theme)
        return success

    def get_startup_page(self) -> str:
        return self.app_config_manager.get_startup_page()

    def set_startup_page(self, page: str) -> bool:
        return self.set_config("startup_page", page)

    def get_default_target_root(self) -> str:
        return self.app_config_manager.get_default_target_root()

    def set_default_target_root(self, path: str) -> bool:
        return self.set_config("default_target_root", path)

    def get_default_link_view(self) -> str:
        return self.app_config_manager.get_default_link_view()

    def set_default_link_view(self, view: str) -> bool:
        return self.set_config("default_link_view", view)

    def get_theme_color(self) -> str:
        return self.app_config_manager.get_theme_color()

    def set_theme_color(self, color: str) -> bool:
        return self.set_config("theme_color", color)

    def get_transparency(self) -> bool:
        return self.app_config_manager.get_transparency()

    def set_transparency(self, enabled: bool) -> bool:
        return self.set_config("transparency", enabled)
