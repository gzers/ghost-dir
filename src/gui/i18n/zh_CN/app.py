"""
应用信息文案
"""
from src import __app_name__, __version__, __author__, __github_url__

APP_TEXTS = {
    "name": __app_name__,
    "version": __version__,
    "subtitle": "目录连接管理器 · 安全迁移系统盘文件",
    "description_line1": f"{__app_name__} 是一款专为 Windows 设计的目录连接管理工具",
    "description_line2": "帮助您轻松将系统盘的大型软件数据迁移到其他磁盘",
    "description_line3": "同时保持软件正常运行，采用事务安全机制，确保数据零丢失",
    "author": __author__,
    "github": "GitHub 仓库",
    "github_url": __github_url__,
    "license": "MIT License",
    "splash_initializing": "正在初始化...",
    "splash_check_admin": "正在校验管理员权限...",
    "splash_check_data": "正在检查数据完整性...",
    "splash_loading_main": "正在加载主界面...",
}
