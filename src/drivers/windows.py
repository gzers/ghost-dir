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


def is_transparency_enabled() -> bool:
    """检查 Windows 是否启用了透明度效果

    Returns:
        bool: 如果启用了透明度效果返回 True，否则返回 False
    """
    try:
        # 检查 Windows 10/11 的透明度设置
        # 注册表路径: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            0,
            winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, "EnableTransparency")
        winreg.CloseKey(key)
        return bool(value)
    except Exception:
        # 如果无法读取注册表，默认返回 True（启用透明度）
        return True
