"""
管理员权限工具
处理 UAC 提权
"""
import sys
import ctypes
import os


def is_admin() -> bool:
    """
    检查当前进程是否以管理员权限运行
    
    Returns:
        True 如果是管理员，否则 False
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    以管理员权限重新启动当前程序
    """
    if sys.platform != 'win32':
        print("此功能仅支持 Windows 系统")
        return
    
    try:
        # 获取当前脚本路径
        if getattr(sys, 'frozen', False):
            # 打包后的 exe
            script = sys.executable
            params = ' '.join(sys.argv[1:])
        else:
            # 开发环境
            script = sys.executable
            params = ' '.join([f'"{sys.argv[0]}"'] + sys.argv[1:])
        
        # 使用 ShellExecute 以管理员权限运行
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",  # 请求管理员权限
            script,
            params,
            None,
            1  # SW_SHOWNORMAL
        )
        
        if ret > 32:  # 成功
            sys.exit(0)
        else:
            print(f"提权失败，错误代码: {ret}")
            
    except Exception as e:
        print(f"提权过程出错: {e}")


def ensure_admin():
    """
    确保程序以管理员权限运行
    如果不是管理员，则请求提权并退出当前进程
    """
    if not is_admin():
        print("检测到未以管理员权限运行，正在请求提权...")
        try:
            run_as_admin()
            sys.exit(0)
        except Exception as e:
            print(f"提权失败: {e}")
            print("请右键点击程序，选择'以管理员身份运行'")
            return False
    return True
