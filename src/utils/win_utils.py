"""
Windows 系统相关工具函数
"""
import sys
import winreg

def is_transparency_enabled() -> bool:
    """检查 Windows 系统是否开启了透明效果"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "EnableTransparency")
        winreg.CloseKey(key)
        return value == 1
    except Exception:
        # 如果读取失败，默认返回已开启，或者根据系统版本保守返回
        return True

def get_windows_version() -> float:
    """获取 Windows 版本号 (如 10.0, 11.0 等)"""
    return float(f"{sys.getwindowsversion().major}.{sys.getwindowsversion().minor}")

def is_win11() -> bool:
    """判断是否为 Windows 11"""
    # Windows 11 的内部版本号通常大于等于 22000
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000
