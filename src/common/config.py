"""
全局配置常量
"""
import os
from pathlib import Path


# 应用信息
APP_NAME = "Ghost-Dir"
APP_VERSION = "7.4.0"
APP_AUTHOR = "Ghost-Dir Team"

# 项目根目录（获取脚本所在目录）
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 数据文件路径（统一使用项目根目录下的 .ghost-dir）
DATA_DIR = PROJECT_ROOT / ".ghost-dir"
TEMPLATES_FILE = "assets/templates.json"  # 已废弃，保留用于兼容性
USER_DATA_FILE = DATA_DIR / "user_data.json"
LOCK_FILE = DATA_DIR / ".ghost.lock"

# 模板配置文件
DEFAULT_TEMPLATES_CONFIG = PROJECT_ROOT / "config" / "default_templates.json"  # 内置默认模板（进版本控制）
TEMPLATE_CACHE_FILE = DATA_DIR / "template_cache.json"  # API 模板缓存（运行时数据）

# 配置和日志目录
CONFIG_FILE = DATA_DIR / "config.json"
LOG_DIR = DATA_DIR / "logs"

# 确保数据目录和日志目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 默认设置
DEFAULT_TARGET_DRIVE = "D:\\"
DEFAULT_CATEGORY = "未分类"

# 系统路径黑名单（禁止操作这些路径）
BLACKLIST_PATHS = [
    "C:\\",
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users",
    "C:\\ProgramData",
]

# UI 常量
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# 状态颜色
STATUS_COLORS = {
    "disconnected": "#E74C3C",  # 红色
    "connected": "#27AE60",     # 绿色
    "ready": "#F39C12",         # 黄色
    "invalid": "#95A5A6",       # 灰色
}

# 状态图标
STATUS_ICONS = {
    "disconnected": "🔴",
    "connected": "🟢",
    "ready": "🟡",
    "invalid": "⚪",
}

# 文件大小单位
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    import math
    unit_index = min(int(math.log(size_bytes, 1024)), len(SIZE_UNITS) - 1)
    size = size_bytes / (1024 ** unit_index)
    
    return f"{size:.2f} {SIZE_UNITS[unit_index]}"
