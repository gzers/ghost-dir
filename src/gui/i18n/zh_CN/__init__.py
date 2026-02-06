"""
中文文案 (zh_CN)
组装所有文案模块
"""
from src.gui.i18n.zh_CN.common import COMMON_TEXTS, STATUS_TEXTS, CATEGORY_TEXTS, ERROR_TEXTS, DIALOG_TEXTS
from src.gui.i18n.zh_CN.links import LINKS_TEXTS
from src.gui.i18n.zh_CN.wizard import WIZARD_TEXTS
from src.gui.i18n.zh_CN.library import LIBRARY_TEXTS
from src.gui.i18n.zh_CN.help import HELP_TEXTS
from src.gui.i18n.zh_CN.settings import SETTINGS_TEXTS
from src.gui.i18n.zh_CN.app import APP_TEXTS

# 组装完整文案字典
TEXTS = {
    "common": COMMON_TEXTS,
    "status": STATUS_TEXTS,
    "category": CATEGORY_TEXTS,
    "error": ERROR_TEXTS,
    "dialog": DIALOG_TEXTS,
    "links": LINKS_TEXTS,
    "wizard": WIZARD_TEXTS,
    "library": LIBRARY_TEXTS,
    "help": HELP_TEXTS,
    "settings": SETTINGS_TEXTS,
    "app": APP_TEXTS,
}
