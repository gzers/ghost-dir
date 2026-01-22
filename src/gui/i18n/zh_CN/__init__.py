"""
中文文案 (zh_CN)
组装所有文案模块
"""
from .common import COMMON_TEXTS, STATUS_TEXTS, CATEGORY_TEXTS, ERROR_TEXTS, DIALOG_TEXTS
from .console import CONSOLE_TEXTS
from .wizard import WIZARD_TEXTS
from .library import LIBRARY_TEXTS
from .help import HELP_TEXTS
from .settings import SETTINGS_TEXTS
from .app import APP_TEXTS

# 组装完整文案字典
TEXTS = {
    "common": COMMON_TEXTS,
    "status": STATUS_TEXTS,
    "category": CATEGORY_TEXTS,
    "error": ERROR_TEXTS,
    "dialog": DIALOG_TEXTS,
    "console": CONSOLE_TEXTS,
    "wizard": WIZARD_TEXTS,
    "library": LIBRARY_TEXTS,
    "help": HELP_TEXTS,
    "settings": SETTINGS_TEXTS,
    "app": APP_TEXTS,
}
