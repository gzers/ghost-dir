"""
全局配置常量
"""
import os
import sys
from pathlib import Path


# 应用信息
APP_NAME = "Ghost-Dir"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Ghost-Dir Team"

# 路径计算：区分开发环境和打包环境
if getattr(sys, 'frozen', False):
    # 打包环境：
    # sys.executable = "D:\Software\Common\Ghost Dir\Ghost-Dir.exe"
    # exe_dir = "D:\Software\Common\Ghost Dir"
    exe_dir = Path(sys.executable).parent
    PROJECT_ROOT = exe_dir / "_internal"  # 只读资源目录（assets）
    DATA_DIR = exe_dir / ".ghost-dir"      # 用户数据目录（所有配置文件）
else:
    # 开发环境：从当前文件向上找到项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / ".ghost-dir"


def get_config_path(filename: str) -> str:
    """获取配置文件的完整路径"""
    config_path = DATA_DIR / filename
    return str(config_path)



# ========== 配置文件路径 ==========

# --- 官方配置（只读，打包在 _internal/config 或 开发环境的 config/）---
DEFAULT_CONFIG_FILE = PROJECT_ROOT / "config" / "default_config.json"
DEFAULT_CATEGORIES_FILE = PROJECT_ROOT / "config" / "default_categories.json"
DEFAULT_TEMPLATES_FILE = PROJECT_ROOT / "config" / "default_templates.json"

# --- 用户配置（可读写，存储在 .ghost-dir）---
USER_CONFIG_FILE = DATA_DIR / "config.json"
USER_CATEGORIES_FILE = DATA_DIR / "categories.json"
USER_TEMPLATES_FILE = DATA_DIR / "templates.json"
USER_LINKS_FILE = DATA_DIR / "links.json"

# --- 兼容性别名（逐步废弃）---
CONFIG_FILE = USER_CONFIG_FILE  # 兼容旧代码
USER_DATA_FILE = USER_LINKS_FILE  # 兼容旧代码
CATEGORIES_CONFIG = USER_CATEGORIES_FILE  # 兼容旧代码
DEFAULT_TEMPLATES_CONFIG = DEFAULT_TEMPLATES_FILE  # 兼容旧代码

# --- 运行时数据 ---
TEMPLATE_CACHE_FILE = DATA_DIR / "template_cache.json"
CATEGORY_LOG_FILE = DATA_DIR / "category_log.json"
LOCK_FILE = DATA_DIR / ".ghost.lock"

# 日志目录
LOG_DIR = DATA_DIR / "logs"

# 已废弃，保留用于兼容性
TEMPLATES_FILE = "assets/templates.json"

# 确保数据目录和日志目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 配置文件初始化：首次运行时从官方配置复制到用户目录
import shutil

# 配置文件映射：官方 → 用户
config_mapping = {
    "default_config.json": "config.json",
    "default_categories.json": "categories.json",
    "default_templates.json": "templates.json"
}

for default_name, user_name in config_mapping.items():
    default_file = DEFAULT_CONFIG_FILE.parent / default_name  # config/default_*.json
    user_file = DATA_DIR / user_name  # .ghost-dir/*.json

    # 首次运行：复制官方配置到用户目录
    if not user_file.exists() and default_file.exists():
        shutil.copy2(default_file, user_file)

# 兼容旧版本：自动迁移旧配置文件
old_user_config = DATA_DIR / "user_config.json"
new_config = DATA_DIR / "config.json"
if old_user_config.exists() and not new_config.exists():
    old_user_config.rename(new_config)

old_user_data = DATA_DIR / "user_data.json"
new_links = DATA_DIR / "links.json"
if old_user_data.exists() and not new_links.exists():
    old_user_data.rename(new_links)


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
DEFAULT_STARTUP_PAGE = "wizard"  # 可选值: "wizard", "links", "library"
DEFAULT_LINK_VIEW = "category"   # 可选值: "list", "category"

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
    {"value": "#2F6BFF", "i18n_key": "settings.theme_color_quantum_blue"},
    {"value": "#2FBF9B", "i18n_key": "settings.theme_color_matte_jade"},
    {"value": "#3DFF7A", "i18n_key": "settings.theme_color_fluorescent_cyan"},
    {"value": "#9A7BFF", "i18n_key": "settings.theme_color_ice_purple_star"},
    {"value": "#FF5C34", "i18n_key": "settings.theme_color_persimmon_orange"},
    {"value": "#FF5C8A", "i18n_key": "settings.theme_color_digital_rose_pink"},
    {"value": "#E9F056", "i18n_key": "settings.theme_color_mustard_yellow"},
    {"value": "#351E28", "i18n_key": "settings.theme_color_deep_plum_purple"},
]

# 启动页选项
STARTUP_PAGE_OPTIONS = [
    {"value": "wizard", "i18n_key": "settings.startup_wizard"},
    {"value": "links", "i18n_key": "settings.startup_connected"},
    {"value": "library", "i18n_key": "settings.startup_library"},
]

# 连接视图选项
LINK_VIEW_OPTIONS = [
    {"value": "list", "i18n_key": "settings.view_list"},
    {"value": "category", "i18n_key": "settings.view_category"},
]

# ========== 系统路径黑名单 ==========
# 核心黑名单：绝对禁止操作该目录及其下所有内容
CORE_BLACKLIST = [
    "C:\\Windows",
    "C:\\Users",
]

# 容器黑名单：禁止操作根目录本身，但允许管理其下的子目录（如具体软件）
CONTAINER_BLACKLIST = [
    "C:\\",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData",
]

# 导出汇总黑名单 (用于向后兼容或基础校验)
BLACKLIST_PATHS = CORE_BLACKLIST + CONTAINER_BLACKLIST

# UI 常量
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# 状态颜色
STATUS_COLORS = {
    "disconnected": "#E74C3C",  # 红色
    "connected": "#27AE60",     # 绿色
    "ready": "#F39C12",         # 黄色
    "invalid": "#95A5A6",       # 灰色
    "error": "#992D22",         # 深红
}

# 状态图标
STATUS_ICONS = {
    "disconnected": "🔴",
    "connected": "🟢",
    "ready": "🟡",
    "invalid": "⚪",
    "error": "❌",
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
