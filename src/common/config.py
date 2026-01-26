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
CATEGORIES_CONFIG = PROJECT_ROOT / "config" / "categories.json"  # 分类配置文件

# 配置和日志目录
CONFIG_FILE = DATA_DIR / "config.json"
LOG_DIR = DATA_DIR / "logs"

# 确保数据目录和日志目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ========== 应用默认设置 ==========
# 这些是应用级的默认值常量，不会在运行时改变
# UserManager 会使用这些常量作为初始值和回退值

# 文件系统默认值
DEFAULT_TARGET_DRIVE = "D:\\"
DEFAULT_TARGET_ROOT = "D:\\Ghost_Library"

# 分类默认值
DEFAULT_CATEGORY = "未分类"

# 主题默认值
DEFAULT_THEME = "system"  # 可选值: "light", "dark", "system"
DEFAULT_THEME_COLOR = "system"  # 可选值: "system" 或 十六进制颜色值如 "#009FAA"

# 启动页默认值
DEFAULT_STARTUP_PAGE = "wizard"  # 可选值: "wizard", "console", "library"

# ========== 主题和颜色选项配置 ==========
# 这些配置定义了 UI 组件中的可选项
# 格式: {"value": "内部值", "i18n_key": "国际化键"}

# 主题模式选项
THEME_OPTIONS = [
    {"value": "system", "i18n_key": "settings.theme_system"},
    {"value": "light", "i18n_key": "settings.theme_light"},
    {"value": "dark", "i18n_key": "settings.theme_dark"},
]

# 主题色选项
THEME_COLOR_OPTIONS = [
    {"value": "system", "i18n_key": "settings.theme_color_system"},
    {"value": "#009FAA", "i18n_key": "settings.theme_color_teal"},
    {"value": "#0078D4", "i18n_key": "settings.theme_color_blue"},
    {"value": "#107C10", "i18n_key": "settings.theme_color_green"},
    {"value": "#D83B01", "i18n_key": "settings.theme_color_orange"},
    {"value": "#E81123", "i18n_key": "settings.theme_color_red"},
    {"value": "#80397B", "i18n_key": "settings.theme_color_purple"},
]

# 启动页选项
STARTUP_PAGE_OPTIONS = [
    {"value": "wizard", "i18n_key": "settings.startup_wizard"},
    {"value": "console", "i18n_key": "settings.startup_console"},
    {"value": "library", "i18n_key": "settings.startup_library"},
]

# ========== 系统路径黑名单 ==========
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

# ========== 分类系统配置 ==========
# 分类树最大深度限制
MAX_CATEGORY_DEPTH = 3

# 系统保留分类（不可删除、不可修改关键属性）
SYSTEM_CATEGORIES = ["uncategorized"]

# 旧版分类名称映射（用于数据迁移）
LEGACY_CATEGORY_MAP = {
    "开发工具": "dev_tools",
    "浏览器": "browsers",
    "社交": "social",
    "游戏": "games",
    "云存储": "cloud_storage",
    "办公软件": "office",
    "多媒体": "media",
    "未分类": "uncategorized"
}


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    import math
    unit_index = min(int(math.log(size_bytes, 1024)), len(SIZE_UNITS) - 1)
    size = size_bytes / (1024 ** unit_index)
    
    return f"{size:.2f} {SIZE_UNITS[unit_index]}"
