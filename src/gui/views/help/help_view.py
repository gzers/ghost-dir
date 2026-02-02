"""
帮助/关于视图
"""
from src.gui.i18n import t
from src.gui.components import BasePageView
from src.gui.views.help.widgets.about_card import AboutCard


class HelpView(BasePageView):
    """帮助/关于视图"""

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("help.title"),
            show_toolbar=False,
            enable_scroll=False
        )

        # 设置页面内容
        self._setup_content()

    def _setup_content(self):
        """设置页面内容"""
        from PySide6.QtCore import Qt
        # 关于卡片 - 显式靠左对齐，防止被拉伸
        about_card = AboutCard(self)
        self.add_to_content(about_card, before_stretch=True)
        self.get_content_layout().setAlignment(about_card, Qt.AlignmentFlag.AlignLeft)
