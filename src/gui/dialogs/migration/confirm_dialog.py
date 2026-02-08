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
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

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
        
        # 软件路径 (现有数据所在位置)
        source_info = QHBoxLayout()
        source_icon = IconWidget(FluentIcon.FOLDER, self.warningCard)
        source_icon.setFixedSize(16, 16)
        source_label = BodyLabel(f"软件路径 (现有数据): {self.source}", self.warningCard)
        source_label.setStyleSheet("color: #EF4444; font-weight: bold;") # 红色警告
        source_info.addWidget(source_icon)
        source_info.addWidget(source_label)
        source_info.addStretch()
        
        # 库路径 (迁移目的地)
        target_info = QHBoxLayout()
        target_icon = IconWidget(FluentIcon.SEND, self.warningCard)
        target_icon.setFixedSize(16, 16)
        target_label = BodyLabel(f"迁移至 (库路径): {self.target}", self.warningCard)
        target_info.addWidget(target_icon)
        target_info.addWidget(target_label)
        target_info.addStretch()
        
        path_layout.addLayout(source_info)
        path_layout.addLayout(target_info)
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
        occ_detail = self.occupancy_service.get_detailed_occupancy(self.target)
        hard_locks = occ_detail["hard"]
        soft_conflicts = occ_detail["soft"]
        
        # 1. 处理硬锁定 (阻断性)
        if hard_locks:
            self.occupancyStatusLabel.setText(f"❌ 严重占用: {hard_locks[0]}。必须先解除锁定才能继续。")
            self.occupancyStatusLabel.setStyleSheet("color: #EF4444;") # 红色
            self.yesButton.setEnabled(False)
            self.yesButton.setToolTip("检测到物理占用，无法迁移")
            self.pulseRing.hide() # 停止加载动画显示
            return

        # 2. 处理软冲突 (提醒性)
        if soft_conflicts:
            proc_str = "、".join(soft_conflicts[:3])
            if len(soft_conflicts) > 3: proc_str += " 等"
            self.occupancyStatusLabel.setText(f"⚠️ 提示: {proc_str} 正在运行。建议关闭以确保迁移万无一失。")
            self.occupancyStatusLabel.setStyleSheet("color: #F59E0B;") # 橙色
            self.yesButton.setEnabled(True) # 软冲突不阻断
            self.yesButton.setToolTip("相关程序运行中，点击仍可尝试迁移")
        else:
            # 3. 完全通过
            self.occupancyStatusLabel.setText("✅ 探测完成: 未检测到明显占用，可以安全迁移。")
            self.occupancyStatusLabel.setStyleSheet("color: #10B981;") # 绿色
            self.yesButton.setEnabled(True)
            self.yesButton.setToolTip("")
        
        self.pulseRing.hide() # 无论如何，检查完毕后隐藏或淡化加载动画
        self.occupancyTitle.setText("占用结果检查 (实时监控中)")

    def closeEvent(self, event):
        """窗口关闭时停止定时器"""
        if self.occupancy_timer.isActive():
            self.occupancy_timer.stop()
        super().closeEvent(event)
