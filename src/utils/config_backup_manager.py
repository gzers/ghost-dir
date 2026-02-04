# coding:utf-8
"""
配置文件备份管理器
独立的备份与还原逻辑，与 UI 完全解耦
"""
import json
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Optional

from src.common.config import CONFIG_FILE, CATEGORIES_CONFIG, DEFAULT_TEMPLATES_CONFIG, DATA_DIR, APP_VERSION
from src.utils.config_validator import ConfigValidator


class ConfigBackupManager:
    """配置文件备份管理器"""
    
    def __init__(self, backup_dir: Path = None):
        """
        初始化备份管理器
        
        Args:
            backup_dir: 备份目录，默认为 DATA_DIR/backups
        """
        self.backup_dir = backup_dir or (DATA_DIR / "backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置文件映射
        self.config_files = {
            "config.json": CONFIG_FILE,
            "categories.json": CATEGORIES_CONFIG,
            "default_templates.json": DEFAULT_TEMPLATES_CONFIG
        }
    
    def export_all_configs(self, output_path: Path = None) -> Tuple[bool, str]:
        """
        导出所有配置文件到 ZIP
        
        Args:
            output_path: 输出路径，为 None 时自动生成
            
        Returns:
            (是否成功, 输出路径或错误信息)
        """
        try:
            # 自动生成备份文件名
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = self.backup_dir / f"config_backup_{timestamp}.zip"
            
            # 确保输出目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建 ZIP 压缩包
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # 添加配置文件
                for archive_name, file_path in self.config_files.items():
                    if file_path.exists():
                        zf.write(file_path, archive_name)
                
                # 添加元数据
                metadata = {
                    "version": APP_VERSION,
                    "timestamp": datetime.now().isoformat(),
                    "files": list(self.config_files.keys())
                }
                zf.writestr("metadata.json", json.dumps(metadata, indent=2, ensure_ascii=False))
            
            return True, str(output_path)
        except Exception as e:
            return False, f"导出失败: {str(e)}"
    
    def restore_from_backup(self, backup_path: Path, validate: bool = True) -> Tuple[bool, str]:
        """
        从备份还原配置文件
        
        Args:
            backup_path: 备份文件路径
            validate: 是否校验文件格式
            
        Returns:
            (是否成功, 错误信息)
        """
        temp_dir = None
        try:
            # 检查备份文件是否存在
            if not backup_path.exists():
                return False, f"备份文件不存在: {backup_path}"
            
            # 解压到临时目录
            temp_dir = Path(tempfile.mkdtemp())
            
            with zipfile.ZipFile(backup_path, 'r') as zf:
                zf.extractall(temp_dir)
            
            # 校验备份文件完整性
            for archive_name in self.config_files.keys():
                file_path = temp_dir / archive_name
                if not file_path.exists():
                    return False, f"备份文件不完整，缺少: {archive_name}"
                
                # 校验格式
                if validate:
                    is_valid, error_msg = ConfigValidator.validate_json_syntax(file_path)
                    if not is_valid:
                        return False, f"{archive_name} 格式错误: {error_msg}"
            
            # 备份当前配置（防止还原失败）
            auto_backup_path = self.backup_dir / f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            self.export_all_configs(auto_backup_path)
            
            # 还原配置文件
            for archive_name, target_path in self.config_files.items():
                source_path = temp_dir / archive_name
                if source_path.exists():
                    shutil.copy(source_path, target_path)
            
            return True, ""
        except Exception as e:
            return False, f"还原失败: {str(e)}"
        finally:
            # 清理临时目录
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def list_backups(self) -> List[Dict]:
        """
        列出所有备份记录
        
        Returns:
            备份列表，每项包含: name, path, size, created_time
        """
        backups = []
        
        if not self.backup_dir.exists():
            return backups
        
        for backup_file in self.backup_dir.glob("*.zip"):
            try:
                backups.append({
                    "name": backup_file.name,
                    "path": str(backup_file),
                    "size": backup_file.stat().st_size,
                    "created_time": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
                })
            except Exception:
                continue
        
        # 按创建时间倒序排列
        backups.sort(key=lambda x: x["created_time"], reverse=True)
        
        return backups
    
    def delete_backup(self, backup_name: str) -> Tuple[bool, str]:
        """
        删除指定备份
        
        Args:
            backup_name: 备份文件名
            
        Returns:
            (是否成功, 错误信息)
        """
        try:
            backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                return False, f"备份文件不存在: {backup_name}"
            
            backup_path.unlink()
            return True, ""
        except Exception as e:
            return False, f"删除失败: {str(e)}"
