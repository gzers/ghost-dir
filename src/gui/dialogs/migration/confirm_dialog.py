# coding: utf-8
"""
迁移确认对话框
用于在路径冲突时询问用户是否迁移数据
"""
import os
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, BodyLabel, IconWidget, FluentIcon,
    IndeterminateProgressRing, CardWidget, TransparentToolButton
)
from src.gui.styles import apply_card_style, get_font_style
from src.services.occupancy_service import OccupancyService
from PySide6.QtCore import Qt, QTimer

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
        self.occupancy_service = OccupancyService()
        
        self._init_ui()
        
        # 启动“脉冲”定时器，每 2 秒扫描一次占用
        self.occupancy_timer = QTimer(self)
        self.occupancy_timer.timeout.connect(self._perform_occupancy_check)
        self.occupancy_timer.start(2000)
        
        # 立即执行一次初始检查
        self._perform_occupancy_check()

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
        
        # 4. 🆕 进程占用“脉冲”探测区
        self.occupancyCard = CardWidget(self)
        occupancy_layout = QVBoxLayout(self.occupancyCard)
        occupancy_layout.setContentsMargins(12, 12, 12, 12)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        self.pulseRing = IndeterminateProgressRing(self)
        self.pulseRing.setFixedSize(14, 14)
        self.pulseRing.setStrokeWidth(2)
        
        self.occupancyTitle = BodyLabel("应用/服务占用检查 (脉冲侦测中...)", self)
        self.occupancyTitle.setStyleSheet("font-weight: bold;")
        
        header_layout.addWidget(self.pulseRing)
        header_layout.addWidget(self.occupancyTitle)
        header_layout.addStretch()
        
        self.refreshBtn = TransparentToolButton(FluentIcon.SYNC, self)
        self.refreshBtn.clicked.connect(self._perform_occupancy_check)
        header_layout.addWidget(self.refreshBtn)
        
        self.occupancyStatusLabel = BodyLabel("正在初始化探测系统...", self)
        self.occupancyStatusLabel.setStyleSheet("color: palette(highlight);")
        
        occupancy_layout.addLayout(header_layout)
        occupancy_layout.addWidget(self.occupancyStatusLabel)

        # 5. 按钮设置
        self.yesButton.setText("迁移数据并继续")
        self.cancelButton.setText("取消操作")
        
        # 6. 添加到主视图布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(self.warningCard)
        self.viewLayout.addSpacing(12)
        self.viewLayout.addWidget(self.occupancyCard) # 插入探测卡片
        self.viewLayout.addSpacing(16)
        
        # 设置最小宽度
        self.widget.setMinimumWidth(550)

    def _perform_occupancy_check(self):
        """执行实际的占用检测并更新 UI"""
        locking_procs = self.occupancy_service.get_locking_processes(self.target)
        
        if not locking_procs:
            self.occupancyStatusLabel.setText("✅ 未检测到应用占用，可以安全迁移。")
            self.occupancyStatusLabel.setStyleSheet("color: #10B981;") # 绿色
            self.yesButton.setEnabled(True)
            self.yesButton.setToolTip("")
        else:
            proc_str = "、".join(locking_procs[:3])
            if len(locking_procs) > 3: proc_str += " 等"
            self.occupancyStatusLabel.setText(f"⚠️ 警告: {proc_str} 正在访问该目录。迁移可能会失败，请先关闭相关应用。")
            self.occupancyStatusLabel.setStyleSheet("color: #F59E0B;") # 橙色
            # 为了严谨，如果检测到占用，暂时禁用迁移按钮（或给予强提醒）
            self.yesButton.setEnabled(False)
            self.yesButton.setToolTip("请先关闭占用该目录的应用以确保数据安全。")

    def closeEvent(self, event):
        """窗口关闭时停止定时器"""
        if self.occupancy_timer.isActive():
            self.occupancy_timer.stop()
        super().closeEvent(event)
