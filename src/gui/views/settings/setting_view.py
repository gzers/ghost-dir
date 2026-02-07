"""
设置视图
页面主体 - 负责布局和协调
"""
from qfluentwidgets import (
    TitleLabel, SettingCardGroup, FluentIcon
)
# TODO: 通过 app 实例访问 Service
from src.common.signals import signal_bus
from src.gui.components import BasePageView
from src.gui.i18n import t
from src.gui.styles import get_spacing, apply_font_style, apply_transparent_background_only
from PySide6.QtCore import Qt


from src.gui.views.settings.widgets.theme_color_card import ThemeColorCard
from src.gui.views.settings.widgets.theme_card import ThemeCard
from src.gui.views.settings.widgets.startup_card import StartupCard
from src.gui.views.settings.widgets.link_view_card import LinkViewCard
from src.gui.views.settings.widgets.target_root_card import TargetRootCard
from src.gui.views.settings.widgets.log_folder_card import LogFolderCard
from src.gui.views.settings.widgets.restore_config_cards import (
    RestoreConfigCard, RestoreCategoriesCard, RestoreTemplatesCard
)
from src.gui.views.settings.widgets.backup_cards import (
    ExportBackupCard, ImportBackupCard
)
from src.common.service_bus import service_bus


class SettingView(BasePageView):
    """设置视图"""

    def __init__(self, parent=None):
        """初始化设置视图"""
        super().__init__(
            parent=parent,
            title="",
            show_toolbar=False,
            enable_scroll=True,
            use_expand_layout=True
        )
        # 重新加载模板
        service_bus.template_manager.load_templates()
        signal_bus.data_refreshed.emit()
        self.config_service = service_bus.config_service
        self.user_manager = service_bus.user_manager

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
        self.targetRootCard = TargetRootCard(self.config_service, self.dirGroup)
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
        self.themeCard = ThemeCard(self.config_service, self.appearanceGroup)
        self.appearanceGroup.addSettingCard(self.themeCard)

        # 主题强调色
        self.themeColorCard = ThemeColorCard(self.config_service, self.appearanceGroup)
        self.appearanceGroup.addSettingCard(self.themeColorCard)

        expand_layout.addWidget(self.appearanceGroup)

        # --- 启动设置组 ---
        self.startupGroup = SettingCardGroup(t("settings.group_startup"), self.get_content_container())
        self.startupGroup.setAutoFillBackground(False)
        apply_transparent_background_only(self.startupGroup)

        # 首次打开功能
        self.startupCard = StartupCard(self.config_service, self.startupGroup)
        self.startupGroup.addSettingCard(self.startupCard)

        # 默认视图设置
        self.link_view_card = LinkViewCard(self.config_service, self.startupGroup)
        self.startupGroup.addSettingCard(self.link_view_card)

        expand_layout.addWidget(self.startupGroup)

        # --- 配置管理组 ---
        self.configGroup = SettingCardGroup("配置管理", self.get_content_container())
        self.configGroup.setAutoFillBackground(False)
        apply_transparent_background_only(self.configGroup)

        # 恢复所有默认配置
        self.restoreAllCard = RestoreConfigCard(self.configGroup)
        self.configGroup.addSettingCard(self.restoreAllCard)

        # 恢复默认分类
        self.restoreCategoriesCard = RestoreCategoriesCard(self.configGroup)
        self.configGroup.addSettingCard(self.restoreCategoriesCard)

        # 恢复默认模板
        self.restoreTemplatesCard = RestoreTemplatesCard(self.configGroup)
        self.configGroup.addSettingCard(self.restoreTemplatesCard)

        # 导出配置备份
        self.exportBackupCard = ExportBackupCard(self.configGroup)
        self.configGroup.addSettingCard(self.exportBackupCard)

        # 导入配置备份
        self.importBackupCard = ImportBackupCard(self.configGroup)
        self.configGroup.addSettingCard(self.importBackupCard)

        expand_layout.addWidget(self.configGroup)

        # 暴力清理：针对 qfluentwidgets 组件内部可能持有的背景进行穿透化透明处理
        self.setStyleSheet("""
            SettingCardGroup,
            SettingCardGroup > QWidget {
                background-color: transparent !important;
                border: none !important;
            }
        """)
