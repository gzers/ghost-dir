"""
资源加载器
处理开发环境和打包环境的资源路径
"""
import os
import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """
    获取资源文件的绝对路径
    兼容开发环境和 PyInstaller 打包环境

    Args:
        relative_path: 相对于项目根目录的路径

    Returns:
        资源文件的绝对路径
    """
    # PyInstaller 打包后的临时目录
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        # 开发环境：从当前文件向上找到项目根目录
        base_path = Path(__file__).parent.parent.parent

    return base_path / relative_path


def get_icon_path(icon_name: str) -> Path:
    """
    获取图标文件路径

    Args:
        icon_name: 图标文件名

    Returns:
        图标文件的绝对路径
    """
    return get_resource_path(f"assets/icons/{icon_name}")


def get_data_file_path(filename: str) -> Path:
    """
    获取数据文件路径

    Args:
        filename: 数据文件名

    Returns:
        数据文件的绝对路径
    """
    return get_resource_path(f"assets/{filename}")
