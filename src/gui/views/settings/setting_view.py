"""
设置视图（重构版）
页面主体 - 负责布局和协调
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    TitleLabel, SettingCardGroup, PushSettingCard, 
    FluentIcon, ScrollArea, ExpandLayout
)
from ....data.user_manager import UserManager
from ....common.config import LOG_DIR
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
        self.dirGroup = SettingCardGroup("路径配置预览 (v7.4)", self.scrollWidget)
        
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
