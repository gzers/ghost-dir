# coding: utf-8
"""
迁移进度对话框
实时显示迁移进度和详细信息
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, ProgressBar
from src.common.config import format_size

class MigrationProgressDialog(MessageBoxBase):
    """迁移进度对话框"""
    
    cancel_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        # 1. 标题
        self.titleLabel = SubtitleLabel("正在迁移数据", self)
        
        # 2. 状态描述 (当前文件名)
        self.statusLabel = BodyLabel("准备中...", self)
        self.statusLabel.setWordWrap(True)
        
        # 3. 进度条
        self.progressBar = ProgressBar(self)
        self.progressBar.setRange(0, 100)
        
        # 4. 详细进度文本 (已处理 / 总量)
        self.detailLabel = BodyLabel("0 MB / 0 MB (0%)", self)
        self.detailLabel.setStyleSheet("color: palette(highlight);")
        
        # 5. 布局添加
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.statusLabel)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(self.progressBar)
        self.viewLayout.addWidget(self.detailLabel)
        
        # 6. 按钮配置
        self.yesButton.hide() # 不需要确定按钮，完成会自动关闭或显示结果
        self.cancelButton.setText("取消迁移")
        self.cancelButton.clicked.connect(self._on_cancel_clicked)
        
        self.widget.setMinimumWidth(500)

    def update_progress(self, current: int, total: int, filename: str):
        """更新进度显示"""
        if total <= 0:
            percent = 0
        else:
            percent = int((current / total) * 100)
            
        self.progressBar.setValue(percent)
        self.statusLabel.setText(f"正在处理: {filename}")
        
        detail = f"{format_size(current)} / {format_size(total)} ({percent}%)"
        self.detailLabel.setText(detail)

    def _on_cancel_clicked(self):
        """处理取消点击"""
        self.statusLabel.setText("正在取消并清理...")
        self.cancelButton.setEnabled(False)
        self.cancel_requested.emit()
