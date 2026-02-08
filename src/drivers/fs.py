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

def get_real_path(path: str) -> str:
    """获取链接指向的真实物理路径 (规范化后)"""
    try:
        if not os.path.exists(path):
            return ""
        # 使用 os.path.realpath 解析联接点/符号链接
        resolved = os.path.realpath(path)
        # ⚠️ 关键修正：Windows 下 realpath 可能会带上 \\?\ 前缀，导致比较失败
        path_str = os.path.normpath(resolved)
        if path_str.startswith("\\\\?\\"):
            path_str = path_str[4:]
        return path_str
    except Exception:
        return ""
