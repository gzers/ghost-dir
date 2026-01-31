"""
设置视图
页面主体 - 负责布局和协调
"""
from qfluentwidgets import (
    TitleLabel, SettingCardGroup, FluentIcon
)
from ....data.user_manager import UserManager
from ...i18n import t
from ...components import BasePageView
from ...styles import get_spacing, apply_font_style, apply_transparent_background_only
from PySide6.QtCore import Qt


from .widgets.theme_color_card import ThemeColorCard
from .widgets.theme_card import ThemeCard
from .widgets.startup_card import StartupCard
from .widgets.link_view_card import LinkViewCard
from .widgets.target_root_card import TargetRootCard
from .widgets.log_folder_card import LogFolderCard


class SettingView(BasePageView):
    """设置视图"""

    def __init__(self, parent=None, user_manager=None):
        """初始化设置视图"""
        super().__init__(
            parent=parent,
            title="",
            show_toolbar=False,
            enable_scroll=True,
            use_expand_layout=True
        )
        self.user_manager = user_manager or UserManager()

        # 设置页面内容
        self._setup_content()

    def _setup_content(self):
        """设置页面内容"""
        # 获取 ExpandLayout
        expand_layout = self.get_content_layout()
        expand_layout.setSpacing(get_spacing("lg"))

        # 页面标题
        self.titleLabel = TitleLabel(t("settings.title"), self.get_content_container())
        apply_font_style(self.titleLabel, size="xxl", weight="semibold")
        expand_layout.addWidget(self.titleLabel)
        
        # --- 目录配置组 ---
        self.dirGroup = SettingCardGroup(t("settings.group_path"), self.get_content_container())
        self.dirGroup.setAutoFillBackground(False)
        apply_transparent_background_only(self.dirGroup)

        # 默认仓库路径
        self.targetRootCard = TargetRootCard(self.user_manager, self.dirGroup)
        self.dirGroup.addSettingCard(self.targetRootCard)

        # 打开日志文件夹
        self.logFolderCard = LogFolderCard(self.dirGroup)
        self.dirGroup.addSettingCard(self.logFolderCard)

        expand_layout.addWidget(self.dirGroup)

        # --- 外观设置组 ---
        self.appearanceGroup = SettingCardGroup(t("settings.group_appearance"), self.get_content_container())
        self.appearanceGroup.setAutoFillBackground(False)
        apply_transparent_background_only(self.appearanceGroup)

        # 主题设置
        self.themeCard = ThemeCard(self.user_manager, self.appearanceGroup)
        self.appearanceGroup.addSettingCard(self.themeCard)

        # 主题强调色
        self.themeColorCard = ThemeColorCard(self.user_manager, self.appearanceGroup)
        self.appearanceGroup.addSettingCard(self.themeColorCard)

        expand_layout.addWidget(self.appearanceGroup)

        # --- 启动设置组 ---
        self.startupGroup = SettingCardGroup(t("settings.group_startup"), self.get_content_container())
        self.startupGroup.setAutoFillBackground(False)
        apply_transparent_background_only(self.startupGroup)

        # 首次打开功能
        self.startupCard = StartupCard(self.user_manager, self.startupGroup)
        self.startupGroup.addSettingCard(self.startupCard)

        # 默认视图设置
        self.linkViewCard = LinkViewCard(self.user_manager, self.startupGroup)
        self.startupGroup.addSettingCard(self.linkViewCard)

        expand_layout.addWidget(self.startupGroup)

        # 暴力清理：针对 qfluentwidgets 组件内部可能持有的背景进行穿透化透明处理
        self.setStyleSheet("""
            SettingCardGroup, 
            SettingCardGroup > QWidget {
                background-color: transparent !important;
                border: none !important;
            }
        """)
