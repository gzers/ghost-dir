# coding: utf-8
"""文件系统操作驱动"""
import os
import subprocess
from pathlib import Path


def create_junction(source: str, target: str) -> bool:
    """创建目录联接点"""
    try:
        if os.path.exists(target):
            return False
        
        os.makedirs(os.path.dirname(target), exist_ok=True)
        
        cmd = f'mklink /J "{target}" "{source}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def remove_junction(path: str) -> bool:
    """删除目录联接点"""
    try:
        if not os.path.exists(path):
            return True
        
        if is_junction(path):
            os.rmdir(path)
            return True
        return False
    except Exception:
        return False


def is_junction(path: str) -> bool:
    """检查路径是否为联接点"""
    try:
        if not os.path.exists(path):
            return False
        
        import ctypes
        from ctypes import wintypes
        
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
        
        if attrs == -1:
            return False
        
        return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except Exception:
        return False
