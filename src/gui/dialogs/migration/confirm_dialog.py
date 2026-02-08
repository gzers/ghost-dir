# coding: utf-8
"""
迁移确认对话框
用于在路径冲突时询问用户是否迁移数据
"""
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, IconWidget, FluentIcon
from src.gui.styles import apply_card_style, get_font_style

class MigrationConfirmDialog(MessageBoxBase):
    """迁移确认对话框"""

    def __init__(self, source: str, target: str, parent=None):
        """
        初始化确认对话框
        
        Args:
            source: 源路径
            target: 目标路径
            parent: 父窗口
        """
        super().__init__(parent)
        self.source = source
        self.target = target
        
        self._init_ui()

    def _init_ui(self):
        """初始化 UI 布局"""
        # 1. 标题和图标
        self.titleLabel = SubtitleLabel("检测到路径冲突", self)
        
        # 2. 警告区域 (使用卡片式设计)
        self.warningCard = QWidget(self)
        apply_card_style(self.warningCard)
        warning_layout = QVBoxLayout(self.warningCard)
        warning_layout.setContentsMargins(16, 16, 16, 16)
        
        desc_text = (
            "链接的目标路径已存在数据。您可以选择将这些数据迁移到源路径，"
            "或者手动处理冲突后再继续。"
        )
        self.descLabel = BodyLabel(desc_text, self)
        self.descLabel.setWordWrap(True)
        warning_layout.addWidget(self.descLabel)
        
        # 3. 路径详情
        path_layout = QVBoxLayout()
        path_layout.setSpacing(12)
        
        # 目标路径 (冲突源)
        target_info = QHBoxLayout()
        target_icon = IconWidget(FluentIcon.FOLDER, self.warningCard)
        target_icon.setFixedSize(16, 16)
        target_label = BodyLabel(f"目标路径 (现有数据): {self.target}", self.warningCard)
        target_label.setStyleSheet("color: #EF4444; font-weight: bold;") # 红色警告
        target_info.addWidget(target_icon)
        target_info.addWidget(target_label)
        target_info.addStretch()
        
        # 源路径 (迁移目的地)
        source_info = QHBoxLayout()
        source_icon = IconWidget(FluentIcon.SEND, self.warningCard)
        source_icon.setFixedSize(16, 16)
        source_label = BodyLabel(f"迁移至 (源路径): {self.source}", self.warningCard)
        source_info.addWidget(source_icon)
        source_info.addWidget(source_label)
        source_info.addStretch()
        
        path_layout.addLayout(target_info)
        path_layout.addLayout(source_info)
        warning_layout.addLayout(path_layout)
        
        # 4. 按钮设置
        self.yesButton.setText("迁移数据并继续")
        self.cancelButton.setText("取消操作")
        
        # 5. 添加到主视图布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(self.warningCard)
        self.viewLayout.addSpacing(16)
        
        # 设置最小宽度
        self.widget.setMinimumWidth(550)
