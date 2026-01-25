"""
样式表管理
使用 StyleSheetBase 管理主题感知的 QSS 文件
"""
from pathlib import Path
from qfluentwidgets import StyleSheetBase, Theme

# 获取样式表文件目录
QSS_DIR = Path(__file__).parent / "qss"


class WindowStyleSheet(StyleSheetBase):
    """主窗口样式表"""

    def path(self, theme: Theme):
        """根据主题返回对应的 QSS 文件路径"""
        if theme == Theme.DARK:
            return QSS_DIR / "window_dark.qss"
        return QSS_DIR / "window.qss"


class LinkTableStyleSheet(StyleSheetBase):
    """连接表格样式表"""

    def path(self, theme: Theme):
        """根据主题返回对应的 QSS 文件路径"""
        if theme == Theme.DARK:
            return QSS_DIR / "link_table_dark.qss"
        return QSS_DIR / "link_table.qss"


# 样式表实例
window_style_sheet = WindowStyleSheet()
link_table_style_sheet = LinkTableStyleSheet()
