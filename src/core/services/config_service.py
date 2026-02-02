"""
配置服务 (ConfigService)
负责全局配置的读写、副作用执行以及 UserManager 的业务封装
"""
from typing import Any, Optional, Dict
from src.data.user_manager import UserManager


class ConfigService:
    """配置业务服务"""

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def get_config(self, key: str, default: Any = None) -> Any:
        """读取配置项（映射到 UserManager 的具体字段）"""
        # 映射表：Key -> UserManager 属性名或方法名
        mappers = {
            "theme": lambda: self.user_manager.get_theme(),
            "startup_page": lambda: self.user_manager.get_startup_page(),
            "default_link_view": lambda: self.user_manager.get_default_link_view(),
            "theme_color": lambda: self.user_manager.get_theme_color(),
            "target_root": lambda: self.user_manager.get_default_target_root(),
            "transparency": lambda: self.user_manager.get_transparency(),
        }
        
        if key in mappers:
            return mappers[key]()
        
        return default

    def set_config(self, key: str, value: Any) -> bool:
        """写入配置项并触发副作用"""
        # 1. 业务校验
        if key == "target_root":
            import os
            if not os.path.exists(os.path.expandvars(value)):
                return False

        # 2. 映射表：Key -> UserManager 设置方法
        mappers = {
            "theme": self.user_manager.set_theme,
            "startup_page": self.user_manager.set_startup_page,
            "default_link_view": self.user_manager.set_default_link_view,
            "theme_color": self.user_manager.set_theme_color,
            "target_root": self.user_manager.set_default_target_root,
            "transparency": self.user_manager.set_transparency,
        }

        if key not in mappers:
            return False

        # 3. 执行持久化
        success = mappers[key](value)
        
        # 4. 副作用执行 (Side Effects)
        if success:
            self._handle_side_effect(key, value)
            
        return success

    def _handle_side_effect(self, key: str, value: Any):
        """处理配置变更的副作用"""        # 广播信号
        from src.common.signals import signal_bus
        
        # 发射全局通知
        signal_bus.config_changed.emit(key, value)
        
        # 特殊副作用逻辑
        if key == "theme":
            # 动态切换主题逻辑
            pass

    def get_app_stats(self) -> Dict[str, Any]:
        """获取应用统计信息"""
        return {
            "version": "1.2.0",
            "custom_template_count": len(self.user_manager.get_custom_templates()),
            "link_count": len(self.user_manager.get_links())
        }

    # 业务快捷方法
    def get_theme(self) -> str:
        return self.user_manager.get_theme()

    def set_theme(self, theme: str) -> bool:
        return self.set_config("theme", theme)

    def get_startup_page(self) -> str:
        return self.user_manager.get_startup_page()

    def set_startup_page(self, page: str) -> bool:
        return self.set_config("startup_page", page)

    def get_default_target_root(self) -> str:
        return self.user_manager.get_default_target_root()

    def set_default_target_root(self, path: str) -> bool:
        return self.set_config("target_root", path)

    def get_default_link_view(self) -> str:
        return self.user_manager.get_default_link_view()

    def set_default_link_view(self, view: str) -> bool:
        return self.set_config("default_link_view", view)

    def get_theme_color(self) -> str:
        return self.user_manager.get_theme_color()

    def set_theme_color(self, color: str) -> bool:
        return self.set_config("theme_color", color)

    def get_transparency(self) -> bool:
        return self.user_manager.get_transparency()

    def set_transparency(self, enabled: bool) -> bool:
        return self.set_config("transparency", enabled)
