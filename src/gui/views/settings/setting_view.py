"""
设置视图（重构版）
页面主体 - 负责布局和协调
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    TitleLabel, SettingCardGroup, PushSettingCard, OptionsSettingCard,
    FluentIcon, ScrollArea, ExpandLayout, InfoBar, InfoBarPosition,
    OptionsConfigItem, OptionsValidator, qconfig
)
from ....data.user_manager import UserManager
from ....common.config import LOG_DIR, CONFIG_FILE
import os
import subprocess


class SettingView(ScrollArea):
    """设置视图"""

    def __init__(self, parent=None):
        """初始化设置视图"""
        super().__init__(parent)
        self.user_manager = UserManager()

        # 使用会滚动的容器
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self._init_ui()
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

    def _init_ui(self):
        """初始化 UI"""
        # 页面标题
        self.titleLabel = TitleLabel("设置", self.scrollWidget)
        self.expandLayout.addWidget(self.titleLabel)

        # --- 目录配置组 ---
        self.dirGroup = SettingCardGroup("路径配置", self.scrollWidget)

        # 默认仓库路径
        self.targetRootCard = PushSettingCard(
            "选择路径",
            FluentIcon.FOLDER,
            "默认仓库根路径",
            self.user_manager.get_default_target_root(),
            self.dirGroup
        )
        self.targetRootCard.clicked.connect(self._on_select_target_root)
        self.dirGroup.addSettingCard(self.targetRootCard)

        # 打开日志文件夹
        self.logFolderCard = PushSettingCard(
            "查看日志",
            FluentIcon.DOCUMENT,
            "调试日志目录",
            str(LOG_DIR),
            self.dirGroup
        )
        self.logFolderCard.clicked.connect(self._on_open_log_folder)
        self.dirGroup.addSettingCard(self.logFolderCard)

        self.expandLayout.addWidget(self.dirGroup)

        # --- 外观设置组 ---
        self.appearanceGroup = SettingCardGroup("外观设置", self.scrollWidget)

        # 主题设置
        # 创建主题配置项
        theme_config = OptionsConfigItem(
            "Appearance", "Theme", "system", 
            OptionsValidator(["system", "light", "dark"])
        )
        self.themeCard = OptionsSettingCard(
            theme_config,
            FluentIcon.BRUSH,
            "应用主题",
            "选择应用的主题模式",
            texts=["跟随系统", "亮色", "暗色"],
            parent=self.appearanceGroup
        )
        current_theme = self.user_manager.get_theme()
        # 设置当前主题值
        self.themeCard.setValue(current_theme)
        self.themeCard.optionChanged.connect(self._on_theme_changed)
        self.appearanceGroup.addSettingCard(self.themeCard)

        self.expandLayout.addWidget(self.appearanceGroup)

        # --- 启动设置组 ---
        self.startupGroup = SettingCardGroup("启动设置", self.scrollWidget)

        # 首次打开功能
        # 创建启动页面配置项
        startup_config = OptionsConfigItem(
            "Startup", "Page", "wizard",
            OptionsValidator(["wizard", "console", "library"])
        )
        self.startupCard = OptionsSettingCard(
            startup_config,
            FluentIcon.GAME,
            "启动页面",
            "设置程序启动时显示的页面",
            texts=["智能向导", "我的连接", "模版库"],
            parent=self.startupGroup
        )
        current_page = self.user_manager.get_startup_page()
        # 设置当前启动页面值
        self.startupCard.setValue(current_page)
        self.startupCard.optionChanged.connect(self._on_startup_changed)
        self.startupGroup.addSettingCard(self.startupCard)

        self.expandLayout.addWidget(self.startupGroup)

    def _on_select_target_root(self):
        """选择默认仓库路径"""
        from PySide6.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(
            self, "选择默认仓库根目录",
            self.user_manager.get_default_target_root()
        )
        if path:
            path = path.replace("/", "\\")
            if self.user_manager.set_default_target_root(path):
                self.targetRootCard.setContent(path)

    def _on_open_log_folder(self):
        """打开日志文件夹"""
        if os.path.exists(LOG_DIR):
            os.startfile(LOG_DIR)
        else:
            # 如果不存在则创建并打开
            os.makedirs(LOG_DIR, exist_ok=True)
            os.startfile(LOG_DIR)

    def _on_theme_changed(self, index):
        """主题改变"""
        theme_map = {
            0: "system",
            1: "light",
            2: "dark"
        }
        theme = theme_map.get(index, "system")
        if self.user_manager.set_theme(theme):
            InfoBar.success(
                title="主题已更新",
                content=f"已切换到 {['跟随系统', '亮色', '暗色'][index]} 主题",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=2000
            )

    def _on_startup_changed(self, index):
        """首启动页面改变"""
        page_map = {
            0: "wizard",
            1: "console",
            2: "library"
        }
        page = page_map.get(index, "wizard")
        if self.user_manager.set_startup_page(page):
            InfoBar.success(
                title="设置已更新",
                content=f"首启动页面已设置为 {['智能向导', '我的连接', '模版库'][index]}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=2000
            )
