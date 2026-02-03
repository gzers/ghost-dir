"""
底层连接点操作
Windows Junction (mklink /J) 的 Python 封装
"""
import os
import subprocess
from pathlib import Path
from typing import Optional


def is_junction(path: str) -> bool:
    """
    检查路径是否为连接点
    
    Args:
        path: 要检查的路径
        
    Returns:
        True 如果是连接点，否则 False
    """
    if not os.path.exists(path):
        return False
    
    try:
        # 使用 os.path.islink 在 Windows 上可以检测 junction
        # 补充：必须确保是目录才能进行属性检查
        if os.path.islink(path):
            return True
        
        # 检查属性是否包含 0x400 (Reparse Point)
        return os.path.isdir(path) and (
            os.stat(path, follow_symlinks=False).st_file_attributes & 0x400
        )
    except Exception as e:
        print(f"检查 {path} 是否为连接点时出错: {e}")
        return False


def get_junction_target(path: str) -> Optional[str]:
    """
    获取连接点的目标路径
    
    Args:
        path: 连接点路径
        
    Returns:
        目标路径，如果不是连接点则返回 None
    """
    if not is_junction(path):
        return None
    
    try:
        return os.readlink(path)
    except:
        return None


def create_junction(source: str, target: str) -> bool:
    """
    创建连接点
    
    Args:
        source: 连接点路径（将创建在这里）
        target: 目标路径（实际数据所在位置）
        
    Returns:
        True 如果成功，否则 False
    """
    try:
        # 确保目标路径存在
        if not os.path.exists(target):
            raise FileNotFoundError(f"目标路径不存在: {target}")
        
        # 确保源路径不存在
        if os.path.exists(source):
            raise FileExistsError(f"源路径已存在: {source}")
        
        # 确保源路径的父目录存在
        parent = Path(source).parent
        parent.mkdir(parents=True, exist_ok=True)
        
        # 使用 mklink /J 创建连接点
        cmd = f'mklink /J "{source}" "{target}"'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return True
        else:
            raise RuntimeError(f"创建连接点失败: {result.stderr}")
            
    except Exception as e:
        print(f"创建连接点时出错: {e}")
        return False


def remove_junction(path: str) -> bool:
    """
    删除连接点（不删除目标数据）
    
    Args:
        path: 连接点路径
        
    Returns:
        True 如果成功，否则 False
    """
    try:
        if not os.path.exists(path):
            return True  # 已经不存在了
        
        if not is_junction(path):
            raise ValueError(f"路径不是连接点: {path}")
        
        # 使用 rmdir 删除连接点（不会删除目标数据）
        os.rmdir(path)
        return True
        
    except Exception as e:
        print(f"删除连接点时出错: {e}")
        return False


def validate_path(path: str, blacklist: list = None) -> bool:
    """
    验证路径是否安全（分级黑名单校验）
    
    规则：
    1. CORE_BLACKLIST: 绝对禁止（匹配路径本身或其任何子路径）
    2. CONTAINER_BLACKLIST: 只禁止根（匹配路径本身禁止，但允许操作子目录）
    
    Args:
        path: 要验证的路径
        blacklist: 基础黑名单（兼容旧接口，主要使用 config 中的分级名单）
        
    Returns:
        True 如果安全，否则 False
    """
    from src.common.config import CORE_BLACKLIST, CONTAINER_BLACKLIST
    
    try:
        path_obj = Path(path).resolve()
        
        # 1. 检查核心黑名单 (全封锁)
        for blocked in CORE_BLACKLIST:
            blocked_obj = Path(blocked).resolve()
            try:
                # 检查是否是黑名单路径或其子路径
                path_obj.relative_to(blocked_obj)
                return False
            except ValueError:
                continue
                
        # 2. 检查容器黑名单 (仅封锁根)
        for blocked in CONTAINER_BLACKLIST:
            blocked_obj = Path(blocked).resolve()
            if path_obj == blocked_obj:
                return False
                
        return True
    except Exception as e:
        print(f"路径验证出错: {e}")
        return False
