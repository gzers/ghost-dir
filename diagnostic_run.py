"""
跳过权限检查的诊断启动脚本
"""
import sys
import os
import traceback

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def diagnostic_run():
    print("--- 启动运行时诊断 ---")
    try:
        from src.gui.app import run_app
        # 我们在这里不模拟 QApplication 的执行，而是尝试初始化核心组件
        # 看看是否会有导入或初始化错误
        run_app()
    except Exception:
        print("\n❌ 捕获到运行时错误:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    diagnostic_run()
