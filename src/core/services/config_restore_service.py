# coding:utf-8
"""
配置恢复服务
提供恢复默认配置的功能
"""
import shutil
from pathlib import Path
from typing import Tuple

from src.common.config import (
    DEFAULT_CONFIG_FILE, DEFAULT_CATEGORIES_FILE, DEFAULT_TEMPLATES_FILE,
    USER_CONFIG_FILE, USER_CATEGORIES_FILE, USER_TEMPLATES_FILE
)


class ConfigRestoreService:
    """配置恢复服务"""
    
    def restore_all_defaults(self) -> Tuple[bool, str]:
        """
        恢复所有默认配置（不影响 links.json）
        
        Returns:
            (是否成功, 错误信息)
        """
        try:
            # 恢复 UI 配置
            success, msg = self.restore_ui_config()
            if not success:
                return False, f"恢复 UI 配置失败: {msg}"
            
            # 恢复分类
            success, msg = self.restore_categories()
            if not success:
                return False, f"恢复分类失败: {msg}"
            
            # 恢复模板
            success, msg = self.restore_templates()
            if not success:
                return False, f"恢复模板失败: {msg}"
            
            return True, ""
        except Exception as e:
            return False, f"恢复失败: {str(e)}"
    
    def restore_categories(self) -> Tuple[bool, str]:
        """
        仅恢复默认分类
        
        Returns:
            (是否成功, 错误信息)
        """
        return self._restore_config_file(
            DEFAULT_CATEGORIES_FILE,
            USER_CATEGORIES_FILE,
            "分类配置"
        )
    
    def restore_templates(self) -> Tuple[bool, str]:
        """
        仅恢复默认模板
        
        Returns:
            (是否成功, 错误信息)
        """
        return self._restore_config_file(
            DEFAULT_TEMPLATES_FILE,
            USER_TEMPLATES_FILE,
            "模板配置"
        )
    
    def restore_ui_config(self) -> Tuple[bool, str]:
        """
        仅恢复默认 UI 配置
        
        Returns:
            (是否成功, 错误信息)
        """
        return self._restore_config_file(
            DEFAULT_CONFIG_FILE,
            USER_CONFIG_FILE,
            "UI 配置"
        )
    
    def _restore_config_file(
        self,
        default_file: Path,
        user_file: Path,
        config_name: str
    ) -> Tuple[bool, str]:
        """
        恢复单个配置文件
        
        Args:
            default_file: 官方配置文件路径
            user_file: 用户配置文件路径
            config_name: 配置名称（用于错误信息）
            
        Returns:
            (是否成功, 错误信息)
        """
        try:
            # 检查官方配置是否存在
            if not default_file.exists():
                return False, f"官方{config_name}文件不存在: {default_file}"
            
            # 确保用户配置目录存在
            user_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制官方配置到用户目录（覆盖）
            shutil.copy2(default_file, user_file)
            
            return True, ""
        except Exception as e:
            return False, f"复制{config_name}失败: {str(e)}"
    
    def merge_official_updates(self, target: str) -> Tuple[bool, str]:
        """
        合并官方更新（保留用户自定义）
        
        Args:
            target: 目标配置类型 ('categories' 或 'templates')
            
        Returns:
            (是否成功, 错误信息)
            
        Note:
            此功能需要实现智能合并逻辑，当前版本暂未实现
        """
        return False, "合并功能暂未实现"
