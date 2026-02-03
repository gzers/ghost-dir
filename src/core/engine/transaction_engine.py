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
from src.core.engine.link_engine import create_junction, remove_junction, validate_path




class TransactionEngine:
    """事务引擎（支持上下文管理器）"""

    
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
        self._op_type = None # 内部操作子类型: establish 或 repair
        
    def _pre_check_access(self, path: str) -> bool:
        """预检路径是否可访问/被占用"""
        if not os.path.exists(path):
            return True
        try:
            # 对于目录，尝试通过重命名进行锁定测试（最稳健的目录占用检查）
            if os.path.isdir(path):
                test_path = str(path) + ".lock_test"
                os.rename(path, test_path)
                os.rename(test_path, path)
            else:
                # 对于文件，尝试以追加模式打开
                with open(path, 'a'):
                    pass
            return True
        except Exception as e:
            print(f"路径占用预检失败: {path}, 错误: {e}")
            return False

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
        支持修复场景：如果 D 盘已有数据且 C 盘是断开状态，尝试智能恢复。
        
        Returns:
            True 如果成功，否则 False
        """
        try:
            # 验证路径安全性
            if not validate_path(self.source_path, BLACKLIST_PATHS):
                raise ValueError(f"路径在黑名单中，禁止操作: {self.source_path}")
            
            src_exists = os.path.exists(self.source_path)
            dst_exists = os.path.exists(self.target_path)
            
            # 场景 1: 完美状态 (C 存，D 不存) -> 搬迁模式
            if src_exists and not dst_exists:
                # 预检 C 盘是否被占用
                if not self._pre_check_access(self.source_path):
                    raise PermissionError(f"源路径被程序占用或无权限（可能是相关软件正在运行），请关闭后再试: {self.source_path}")

                self._op_type = "establish"
                self._write_lock("establish")
                target_parent = Path(self.target_path).parent
                target_parent.mkdir(parents=True, exist_ok=True)
                
                print(f"正在移动文件: {self.source_path} -> {self.target_path}")
                shutil.move(self.source_path, self.target_path)
                
                if not create_junction(self.source_path, self.target_path):
                    raise RuntimeError("创建连接点失败")
                self._delete_lock()
                return True

            # 场景 2: 失效修复状态 (C 存/不存，D 已有) -> 修复模式
            elif dst_exists:
                self._op_type = "repair"
                print(f"检测到目标路径已存在，尝试修复连接: {self.target_path}")
                
                # 如果 C 盘是普通文件或目录，且不是 Junction
                from src.core.engine.link_engine import is_junction
                if src_exists:
                    if is_junction(self.source_path):
                        print("✓ 连接已存在且正常")
                        return True
                    
                    # 预检 C 盘残留是否可清理
                    if not self._pre_check_access(self.source_path):
                        raise PermissionError(f"C 盘残留路径被某些程序占用（可能是 Adobe 后台服务），导致无法清理进行修复: {self.source_path}")

                    # 如果 C 盘是一个空目录，可以直接删除并重建 Junction
                    if os.path.isdir(self.source_path) and not any(os.scandir(self.source_path)):
                        print(f"清理 C 盘残留空目录: {self.source_path}")
                        os.rmdir(self.source_path)
                    else:
                        raise FileExistsError(f"C 盘原路径已存在且非空（可能由于软件更新自动生成），请手动清理后再试: {self.source_path}")

                # 重新链接 (修复模式通常不涉及搬迁，无需回滚文件)
                self._write_lock("repair")
                if not create_junction(self.source_path, self.target_path):
                    raise RuntimeError("重建连接点失败")
                self._delete_lock()
                print("✓ 修复连接成功")
                return True

            # 场景 3: 异常状态 (C 不存，D 也不存)
            else:
                raise FileNotFoundError(f"源路径和目标路径均不存在，无法建立连接: {self.source_path}")
            
        except Exception as e:
            print(f"✗ 建立/修复连接失败: {e}")
            # 仅在真正的搬迁模式（establish）下且已发生物理改变时才执行移动回滚
            if self._op_type == "establish":
                self._rollback_establish()
            raise e # 抛出异常让上层捕获错误消息
    
    def _rollback_establish(self):
        """回滚建立连接操作"""
        print("正在执行回滚...")
        
        try:
            # 如果连接点已创建，删除它
            from src.core.engine.link_engine import is_junction
            if os.path.exists(self.source_path) and is_junction(self.source_path):
                remove_junction(self.source_path)
            
            # 如果文件已移动到目标位置，且 C 盘现在不存在，则移回来
            if os.path.exists(self.target_path) and not os.path.exists(self.source_path):
                shutil.move(self.target_path, self.source_path)
                print("✓ 文件已恢复到原位置")
        except Exception as e:
            print(f"回滚过程中出错: {e}")
            
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
    
    manager = TransactionEngine(

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
