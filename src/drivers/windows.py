# coding: utf-8
"""Windows 系统操作驱动"""
import ctypes
import sys
import os


def is_admin() -> bool:
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """以管理员权限重新启动程序"""
    if is_admin():
        return
    
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv),
            None,
            1
        )
        sys.exit(0)
    except Exception:
        pass
