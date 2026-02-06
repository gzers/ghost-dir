# coding:utf-8
"""
应用配置管理器
管理应用级配置（主题、启动页、默认路径等）
"""
import json
from pathlib import Path
from typing import Any, Optional
from src.common.config import (
    USER_CONFIG_FILE, USER_LINKS_FILE,
    DEFAULT_TARGET_ROOT, DEFAULT_THEME, DEFAULT_THEME_COLOR, 
    DEFAULT_STARTUP_PAGE, DEFAULT_LINK_VIEW
)


class AppConfigManager:
    """应用配置管理器"""
    
    def __init__(self):
        """初始化应用配置管理器"""
        self.config_file = USER_CONFIG_FILE
        self.config = self._load_config()
        # 执行数据迁移
        self._migrate_from_old_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        if not self.config_file.exists():
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 确保有 app 配置段
            if 'app' not in data:
                data['app'] = self._get_default_app_config()
                self._save_config(data)
            
            return data
        except Exception as e:
            print(f"加载应用配置失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            "QFluentWidgets": {
                "FontFamilies": [
                    "Segoe UI",
                    "Microsoft YaHei",
                    "PingFang SC"
                ],
                "ThemeColor": "#ff5b6c96",
                "ThemeMode": "Dark"
            },
            "app": self._get_default_app_config()
        }
    
    def _get_default_app_config(self) -> dict:
        """获取默认应用配置"""
        return {
            "default_target_root": DEFAULT_TARGET_ROOT,
            "theme": DEFAULT_THEME,
            "theme_color": DEFAULT_THEME_COLOR,
            "startup_page": DEFAULT_STARTUP_PAGE,
            "default_link_view": DEFAULT_LINK_VIEW,
            "transparency": True
        }
    
    def _save_config(self, config: dict = None):
        """保存配置"""
        if config is None:
            config = self.config
        
        try:
            # 确保目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存应用配置失败: {e}")
    
    def _migrate_from_old_config(self):
        """从旧的 links.json 迁移应用配置"""
        # 如果 config.json 已经有 app 配置，且不是默认值，则不迁移
        if 'app' in self.config:
            # 检查是否有自定义配置
            app_config = self.config['app']
            default_config = self._get_default_app_config()
            if app_config != default_config:
                # 已经有自定义配置，不迁移
                return
        
        # 尝试从旧的 links.json 读取配置
        try:
            if not USER_LINKS_FILE.exists():
                return
            
            with open(USER_LINKS_FILE, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            
            # 检查是否有应用配置字段
            config_keys = ['default_target_root', 'theme', 'theme_color', 
                          'startup_page', 'default_link_view', 'transparency']
            
            has_old_config = any(key in old_data for key in config_keys)
            
            if has_old_config:
                print("🔄 检测到旧的应用配置，正在迁移...")
                
                # 迁移配置
                migrated_config = {}
                for key in config_keys:
                    if key in old_data:
                        migrated_config[key] = old_data[key]
                
                # 合并到当前配置
                if 'app' not in self.config:
                    self.config['app'] = {}
                
                self.config['app'].update(migrated_config)
                self._save_config()
                
                print(f"✅ 已迁移 {len(migrated_config)} 个应用配置项")
                
                # 从 links.json 中删除已迁移的配置
                self._cleanup_old_config(old_data, config_keys)
                
        except Exception as e:
            print(f"迁移配置时出错: {e}")
    
    def _cleanup_old_config(self, old_data: dict, config_keys: list):
        """从 links.json 中清理已迁移的配置"""
        try:
            # 删除应用配置字段
            modified = False
            for key in config_keys:
                if key in old_data:
                    del old_data[key]
                    modified = True
            
            # 删除 categories 和 custom_templates（它们已经有独立的管理器）
            if 'categories' in old_data:
                del old_data['categories']
                modified = True
            
            if 'custom_templates' in old_data:
                del old_data['custom_templates']
                modified = True
            
            if modified:
                # 保存清理后的 links.json
                with open(USER_LINKS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(old_data, f, ensure_ascii=False, indent=2)
                print("✅ 已清理 links.json 中的旧配置")
                
        except Exception as e:
            print(f"清理旧配置时出错: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get('app', {}).get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置项"""
        try:
            if 'app' not in self.config:
                self.config['app'] = {}
            
            self.config['app'][key] = value
            self._save_config()
            return True
        except Exception as e:
            print(f"设置配置项失败: {e}")
            return False
    
    # ========== 便捷方法 ==========
    
    def get_default_target_root(self) -> str:
        """获取默认仓库路径"""
        return self.get('default_target_root', DEFAULT_TARGET_ROOT)
    
    def set_default_target_root(self, path: str) -> bool:
        """设置默认仓库路径"""
        return self.set('default_target_root', path)
    
    def get_theme(self) -> str:
        """获取主题"""
        return self.get('theme', DEFAULT_THEME)
    
    def set_theme(self, theme: str) -> bool:
        """设置主题"""
        if theme not in ['light', 'dark', 'system']:
            return False
        return self.set('theme', theme)
    
    def get_theme_color(self) -> str:
        """获取主题色"""
        return self.get('theme_color', DEFAULT_THEME_COLOR)
    
    def set_theme_color(self, color: str) -> bool:
        """设置主题色"""
        return self.set('theme_color', color)
    
    def get_startup_page(self) -> str:
        """获取启动页"""
        return self.get('startup_page', DEFAULT_STARTUP_PAGE)
    
    def set_startup_page(self, page: str) -> bool:
        """设置启动页"""
        if page not in ['wizard', 'connected', 'library']:
            return False
        return self.set('startup_page', page)
    
    def get_default_link_view(self) -> str:
        """获取默认链接视图"""
        return self.get('default_link_view', DEFAULT_LINK_VIEW)
    
    def set_default_link_view(self, view: str) -> bool:
        """设置默认链接视图"""
        if view not in ['list', 'category']:
            return False
        return self.set('default_link_view', view)
    
    def get_transparency(self) -> bool:
        """获取透明效果"""
        return self.get('transparency', True)
    
    def set_transparency(self, enabled: bool) -> bool:
        """设置透明效果"""
        return self.set('transparency', enabled)
