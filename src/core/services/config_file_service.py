# coding:utf-8
"""
配置文件管理服务
专门负责配置文件的校验、备份和还原
与 ConfigService (用户配置服务) 分离
"""
from pathlib import Path
from typing import Tuple

from src.common.config import USER_CONFIG_FILE, USER_CATEGORIES_FILE, USER_LINKS_FILE, DATA_DIR
from src.utils.config_validator import ConfigValidator
from src.utils.config_backup_manager import ConfigBackupManager
from src.core.services.context import service_bus
from src.common.signals import signal_bus


class ConfigFileService:
    """配置文件管理服务"""
    
    def __init__(self):
        """初始化配置文件服务"""
        self.validator = ConfigValidator()
        self.backup_manager = ConfigBackupManager(DATA_DIR / "backups")
    
    def validate_config_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        校验配置文件（语法 + 结构）
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        # 1. 语法校验
        is_valid, error_msg = self.validator.validate_json_syntax(file_path)
        if not is_valid:
            return False, error_msg
        
        # 2. 结构校验
        if file_path == USER_CONFIG_FILE:
            return self.validator.validate_config_structure(file_path)
        elif file_path == USER_CATEGORIES_FILE:
            return self.validator.validate_categories_structure(file_path)
        elif file_path == USER_LINKS_FILE:
            # links.json 的结构校验 (简单校验)
            return True, ""
        
        return True, ""
    
    def reload_config(self, file_path: Path) -> Tuple[bool, str]:
        """
        重新加载配置文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            (是否成功, 错误信息)
        """
        try:
            if file_path == USER_CONFIG_FILE:
                # 重载 QFluentWidgets 配置
                from qfluentwidgets import qconfig
                qconfig.load(str(USER_CONFIG_FILE))
                # 重载应用配置
                service_bus.app_config_manager._load_config()
            
            elif file_path == USER_CATEGORIES_FILE:
                # 重载分类管理器
                service_bus.category_manager.load_categories()
                # 通知 UI 刷新
                signal_bus.data_refreshed.emit()
            
            elif file_path == USER_LINKS_FILE:
                # 重载链接数据
                service_bus.user_manager._load_data()
                # 通知 UI 刷新
                signal_bus.data_refreshed.emit()
            
            return True, ""
        except Exception as e:
            return False, f"重载失败: {str(e)}"
    
    def export_configs(self, output_path: Path = None) -> Tuple[bool, str]:
        """
        导出配置备份
        
        Args:
            output_path: 输出路径，为 None 时自动生成
            
        Returns:
            (是否成功, 输出路径或错误信息)
        """
        return self.backup_manager.export_all_configs(output_path)
    
    def restore_configs(self, backup_path: Path) -> Tuple[bool, str]:
        """
        还原配置备份
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            (是否成功, 错误信息)
        """
        # 还原配置文件
        is_success, error_msg = self.backup_manager.restore_from_backup(backup_path)
        
        if is_success:
            # 重新加载所有配置
            self.reload_config(USER_CONFIG_FILE)
            self.reload_config(USER_CATEGORIES_FILE)
            self.reload_config(USER_LINKS_FILE)
        
        return is_success, error_msg
    
    def list_backups(self):
        """列出所有备份记录"""
        return self.backup_manager.list_backups()
    
    def delete_backup(self, backup_name: str) -> Tuple[bool, str]:
        """删除指定备份"""
        return self.backup_manager.delete_backup(backup_name)
