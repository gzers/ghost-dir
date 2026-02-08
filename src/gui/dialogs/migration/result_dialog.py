# coding: utf-8
"""
迁移结果对话框
向用户展示最终的操作结果
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, IconWidget, FluentIcon

class MigrationResultDialog(MessageBoxBase):
    """迁移结果对话框"""

    def __init__(self, success: bool, message: str = "", parent=None):
        """
        初始化结果对话框
        
        Args:
            success: 是否成功
            message: 错误信息 (如果失败)
            parent: 父窗口
        """
        super().__init__(parent)
        self.success = success
        self.message = message
        self._init_ui()

    def _init_ui(self):
        # 1. 标题和图标
        if self.success:
            title = "迁移成功"
            icon = FluentIcon.COMPLETED
            color = "#22C55E" # 绿色
            content = "数据已成功同步。您现在可以继续后续操作。"
        else:
            title = "迁移失败"
            icon = FluentIcon.INFO
            color = "#EF4444" # 红色
            content = f"在数据迁移过程中遇到问题：\n\n{self.message}"

        self.titleLabel = SubtitleLabel(title, self)
        
        # 2. 状态图标
        self.stateIcon = IconWidget(icon, self)
        self.stateIcon.setFixedSize(48, 48)
        self.stateIcon.setStyleSheet(f"color: {color};")
        
        # 3. 描述内容
        self.contentLabel = BodyLabel(content, self)
        self.contentLabel.setWordWrap(True)
        
        # 4. 布局添加
        self.viewLayout.addSpacing(16)
        icon_layout = QHBoxLayout()
        icon_layout.addStretch()
        icon_layout.addWidget(self.stateIcon)
        icon_layout.addStretch()
        
        self.viewLayout.addLayout(icon_layout)
        self.viewLayout.addSpacing(16)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)
        self.viewLayout.addSpacing(16)
        
        # 5. 按钮配置
        self.cancelButton.hide() # 只显示确定按钮
        self.yesButton.setText("确定")
        
        self.widget.setMinimumWidth(450)
