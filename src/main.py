"""
主程序入口
用于打包后的 exe
"""
from src.gui.app import run_app
import os

if __name__ == "__main__":
    os.environ["QSG_RHI_BACKEND"] = "d3d12"
    run_app()
