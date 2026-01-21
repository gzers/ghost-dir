"""
空间分析工具
计算目录大小并缓存
"""
import os
from pathlib import Path


def calculate_directory_size(path: str) -> int:
    """
    递归计算目录大小
    
    Args:
        path: 目录路径
        
    Returns:
        总大小（字节）
    """
    total_size = 0
    
    try:
        if not os.path.exists(path):
            return 0
        
        # 如果是文件，直接返回大小
        if os.path.isfile(path):
            return os.path.getsize(path)
        
        # 递归遍历目录
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total_size += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total_size += calculate_directory_size(entry.path)
            except (PermissionError, OSError):
                # 跳过无权限访问的文件/目录
                continue
                
    except (PermissionError, OSError) as e:
        print(f"计算目录大小时出错: {path}, {e}")
    
    return total_size


def format_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化后的字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    import math
    
    unit_index = min(int(math.log(size_bytes, 1024)), len(units) - 1)
    size = size_bytes / (1024 ** unit_index)
    
    return f"{size:.2f} {units[unit_index]}"
