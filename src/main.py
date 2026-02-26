"""
主程序入口
用于打包后的 exe
"""
import os
import sys

if __name__ == "__main__":
    os.environ["QSG_RHI_BACKEND"] = "d3d12"

    # 自动请求管理员权限（与 run.py 保持一致）
    from src.drivers.windows import is_admin, run_as_admin

    if not is_admin():
        run_as_admin()
    else:
        from src.gui.app import run_app
        run_app()
