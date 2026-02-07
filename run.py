"""
程序入口
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 自动请求管理员权限
    from src.drivers.windows import is_admin, run_as_admin
    
    if not is_admin():
        # 如果没有管理员权限，自动以管理员身份重新启动
        run_as_admin()
    else:
        # 已有管理员权限，正常启动应用
        from src.gui.app import run_app
        run_app()
