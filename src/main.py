"""
主程序入口
用于打包后的 exe
"""
import os
import sys

if __name__ == "__main__":
    os.environ["QSG_RHI_BACKEND"] = "d3d12"

    # ── PyInstaller 打包环境兼容：显式指定 Qt platform plugin 路径 ──
    # 部分目标机器未安装 Qt，Qt 无法通过注册表/环境变量自动定位 plugins 目录，
    # 需在最早阶段（import Qt 之前）手动注入路径，防止"no Qt platform plugin"报错。
    if getattr(sys, "frozen", False):
        # _MEIPASS 是 PyInstaller 解包后的临时目录根路径
        _base = sys._MEIPASS
        _plugin_path = os.path.join(_base, "PySide6", "plugins")
        _platform_path = os.path.join(_plugin_path, "platforms")
        os.environ.setdefault("QT_PLUGIN_PATH", _plugin_path)
        os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", _platform_path)

    # 自动请求管理员权限（与 run.py 保持一致）
    from src.drivers.windows import is_admin, run_as_admin

    if not is_admin():
        run_as_admin()
    else:
        from src.gui.app import run_app
        run_app()
