"""
帮助/关于视图
"""
from ...i18n import t
from ...components import BasePageView
from .widgets.about_card import AboutCard


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
        # 关于卡片
        about_card = AboutCard(self)
        self.add_to_content(about_card, before_stretch=True)
