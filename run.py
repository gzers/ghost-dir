"""
程序入口
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 正常启动应用（管理员检查和崩溃恢复在 app.py 中处理）
    from src.gui.app import run_app
    run_app()
