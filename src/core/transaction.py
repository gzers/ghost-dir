"""
事务管理器
提供原子回滚机制，确保数据安全
"""
import os
import json
import shutil
from pathlib import Path
from typing import Optional
from src.common.config import LOCK_FILE, BLACKLIST_PATHS
from src.data.model import TransactionRecord
from src.core.link_opt import create_junction, remove_junction, validate_path


class TransactionManager:
    """事务管理器（支持上下文管理器）"""
    
    def __init__(self, source_path: str, target_path: str, link_id: str):
        """
        初始化事务管理器
        
        Args:
            source_path: 源路径（C 盘）
            target_path: 目标路径（D 盘）
            link_id: 连接 ID
        """
        self.source_path = source_path
        self.target_path = target_path
        self.link_id = link_id
        self.operation = None
        self.lock_file = LOCK_FILE
        
    def __enter__(self):
        """进入上下文"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文，自动清理锁文件"""
        if self.lock_file.exists():
            self.lock_file.unlink()
        
        # 如果有异常，返回 False 让异常继续传播
        return False
    
    def _write_lock(self, operation: str):
        """写入锁文件"""
        record = TransactionRecord(
            operation=operation,
            source_path=self.source_path,
            target_path=self.target_path,
            link_id=self.link_id
        )
        
        with open(self.lock_file, 'w', encoding='utf-8') as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _delete_lock(self):
        """删除锁文件"""
        if self.lock_file.exists():
            self.lock_file.unlink()
    
    def establish_link(self) -> bool:
        """
        建立连接（C -> D，创建连接点）
        
        Returns:
            True 如果成功，否则 False
        """
        try:
            # 验证路径安全性
            if not validate_path(self.source_path, BLACKLIST_PATHS):
                raise ValueError(f"路径在黑名单中，禁止操作: {self.source_path}")
            
            # 检查源路径是否存在
            if not os.path.exists(self.source_path):
                raise FileNotFoundError(f"源路径不存在: {self.source_path}")
            
            # 检查目标路径是否已存在
            if os.path.exists(self.target_path):
                raise FileExistsError(f"目标路径已存在: {self.target_path}")
            
            # 写入锁文件
            self._write_lock("establish")
            
            # 步骤 1: 创建目标目录的父目录
            target_parent = Path(self.target_path).parent
            target_parent.mkdir(parents=True, exist_ok=True)
            
            # 步骤 2: 移动文件（C -> D）
            print(f"正在移动文件: {self.source_path} -> {self.target_path}")
            shutil.move(self.source_path, self.target_path)
            
            # 步骤 3: 创建连接点（C <- D）
            print(f"正在创建连接点: {self.source_path} -> {self.target_path}")
            if not create_junction(self.source_path, self.target_path):
                raise RuntimeError("创建连接点失败")
            
            # 成功：删除锁文件
            self._delete_lock()
            print("✓ 连接建立成功")
            return True
            
        except Exception as e:
            print(f"✗ 建立连接失败: {e}")
            # 自动回滚
            self._rollback_establish()
            return False
    
    def _rollback_establish(self):
        """回滚建立连接操作"""
        print("正在执行回滚...")
        
        try:
            # 如果连接点已创建，删除它
            if os.path.exists(self.source_path):
                remove_junction(self.source_path)
            
            # 如果文件已移动到目标位置，移回来
            if os.path.exists(self.target_path):
                shutil.move(self.target_path, self.source_path)
                print("✓ 文件已恢复到原位置")
            
            # 删除目标目录（如果为空）
            target_parent = Path(self.target_path).parent
            if target_parent.exists() and not any(target_parent.iterdir()):
                target_parent.rmdir()
                
        except Exception as e:
            print(f"回滚时出错: {e}")
        finally:
            self._delete_lock()
    
    def disconnect_link(self) -> bool:
        """
        断开连接（删除连接点，D -> C）
        
        Returns:
            True 如果成功，否则 False
        """
        try:
            # 检查连接点是否存在
            if not os.path.exists(self.source_path):
                raise FileNotFoundError(f"连接点不存在: {self.source_path}")
            
            # 检查目标路径是否存在
            if not os.path.exists(self.target_path):
                raise FileNotFoundError(f"目标路径不存在: {self.target_path}")
            
            # 写入锁文件
            self._write_lock("disconnect")
            
            # 步骤 1: 删除连接点
            print(f"正在删除连接点: {self.source_path}")
            if not remove_junction(self.source_path):
                raise RuntimeError("删除连接点失败")
            
            # 步骤 2: 移动文件回来（D -> C）
            print(f"正在移动文件: {self.target_path} -> {self.source_path}")
            shutil.move(self.target_path, self.source_path)
            
            # 成功：删除锁文件
            self._delete_lock()
            print("✓ 连接断开成功")
            return True
            
        except Exception as e:
            print(f"✗ 断开连接失败: {e}")
            # 自动回滚
            self._rollback_disconnect()
            return False
    
    def _rollback_disconnect(self):
        """回滚断开连接操作"""
        print("正在执行回滚...")
        
        try:
            # 如果文件已移回 C 盘，再移回 D 盘
            if os.path.exists(self.source_path) and not os.path.exists(self.target_path):
                shutil.move(self.source_path, self.target_path)
            
            # 重新创建连接点
            if not os.path.exists(self.source_path):
                create_junction(self.source_path, self.target_path)
                print("✓ 连接点已恢复")
                
        except Exception as e:
            print(f"回滚时出错: {e}")
        finally:
            self._delete_lock()


def check_crash_recovery() -> Optional[TransactionRecord]:
    """
    检查是否有未完成的事务（崩溃恢复）
    
    Returns:
        TransactionRecord 如果有未完成的事务，否则 None
    """
    if not LOCK_FILE.exists():
        return None
    
    try:
        with open(LOCK_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return TransactionRecord.from_dict(data)
    except Exception as e:
        print(f"读取锁文件时出错: {e}")
        return None


def recover_from_crash(record: TransactionRecord) -> bool:
    """
    从崩溃中恢复
    
    Args:
        record: 事务记录
        
    Returns:
        True 如果恢复成功，否则 False
    """
    print(f"检测到未完成的操作: {record.operation}")
    print(f"源路径: {record.source_path}")
    print(f"目标路径: {record.target_path}")
    
    manager = TransactionManager(
        record.source_path,
        record.target_path,
        record.link_id
    )
    
    if record.operation == "establish":
        # 回滚建立连接操作
        manager._rollback_establish()
    elif record.operation == "disconnect":
        # 回滚断开连接操作
        manager._rollback_disconnect()
    
    return True
