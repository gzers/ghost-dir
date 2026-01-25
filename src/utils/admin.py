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
        # 方法 1: 使用 IsUserAnAdmin
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True

        # 方法 2: 检查进程令牌
        try:
            # 尝试提升权限
            hToken = ctypes.windll.advapi32.OpenProcessToken(
                ctypes.windll.kernel32.GetCurrentProcess(),
                ctypes.c_ulong(0x0008),  # TOKEN_QUERY
                ctypes.byref(ctypes.c_void_p())
            )
            if hToken:
                ctypes.windll.kernel32.CloseHandle(hToken)
                return True
        except:
            pass

        return False
    except Exception:
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
            # 获取脚本绝对路径
            script_path = os.path.abspath(sys.argv[0])
            # 构建参数：用引号包裹脚本路径
            params = f'"{script_path}"'
            if sys.argv[1:]:
                # 其余参数不需要额外引号
                params += ' ' + ' '.join(sys.argv[1:])

        # 调试输出
        print(f"[DEBUG] Python 可执行文件: {script}")
        print(f"[DEBUG] 脚本路径: {os.path.abspath(sys.argv[0])}")
        print(f"[DEBUG] 启动参数: {params}")

        # 方法 1: 使用 ShellExecuteW
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",  # 请求管理员权限
            script,
            params,
            None,
            1  # SW_SHOWNORMAL
        )

        # ShellExecuteW 返回值：>32 表示成功，<=32 表示失败
        # 但有时候 >32 也不一定意味着真正启动了
        if ret > 32:  # 技术上成功
            print("提权请求已发送（ShellExecuteW）...")
            # 延迟退出，给系统时间处理
            import time
            time.sleep(0.5)
            sys.exit(0)
        else:
            # 方法 2: 如果 ShellExecuteW 失败，尝试使用 PowerShell
            print("ShellExecuteW 失败，尝试使用 PowerShell...")
            try:
                powershell_cmd = f'Start-Process -FilePath "{script}" -ArgumentList "{params}" -Verb RunAs'
                print(f"[DEBUG] PowerShell 命令: {powershell_cmd}")

                # 使用 ShellExecuteW 调用 PowerShell
                ps_ret = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    "powershell.exe",
                    f"-Command \"{powershell_cmd}\"",
                    None,
                    1
                )

                if ps_ret > 32:
                    print("提权请求已发送（PowerShell）...")
                    import time
                    time.sleep(0.5)
                    sys.exit(0)
                else:
                    print(f"PowerShell 提权也失败，错误代码: {ps_ret}")

            except Exception as e:
                print(f"PowerShell 提权失败: {e}")

            # 最终提示
            print("\n自动提权失败，请手动操作：")
            print("1. 右键点击命令提示符或 PowerShell")
            print("2. 选择 '以管理员身份运行'")
            print(f"3. 然后运行: {script} {params}")

    except Exception as e:
        print(f"提权过程出错: {e}")
        import traceback
        traceback.print_exc()


def ensure_admin():
    """
    确保程序以管理员权限运行
    如果不是管理员，则请求提权并退出当前进程
    """
    if not is_admin():
        print("检测到未以管理员权限运行，正在请求提权...")

        # 检查环境变量，允许跳过管理员检查（用于调试）
        skip_admin = os.environ.get('GHOSTDIR_SKIP_ADMIN_CHECK', '').lower() in ('1', 'true', 'yes')
        if skip_admin:
            print("注意：已跳过管理员检查（调试模式）")
            return True

        try:
            run_as_admin()
            sys.exit(0)
        except Exception as e:
            print(f"提权失败: {e}")
            print("请右键点击程序，选择'以管理员身份运行'")
            print("或者设置环境变量 GHOSTDIR_SKIP_ADMIN_CHECK=1 跳过检查（调试用）")
            return False
    else:
        print("已以管理员权限运行")
    return True
