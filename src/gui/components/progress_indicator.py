"""
进度指示器组件
显示进度条和状态信息
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import ProgressBar, BodyLabel
from src.gui.styles import apply_font_style, get_spacing


class ProgressIndicator(QWidget):
    """进度指示器组件"""

    def __init__(self, parent=None):
        """
        初始化进度指示器

        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(get_spacing("sm"))

        # 进度条
        self.progress_bar = ProgressBar()
        self.progress_bar.setRange(0, 0)  # 默认为不确定进度
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 状态文本
        self.status_label = BodyLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        apply_font_style(self.status_label, weight="medium", color="secondary")
        layout.addWidget(self.status_label)

    def set_status(self, text: str):
        """
        设置状态文本

        Args:
            text: 状态文本
        """
        self.status_label.setText(text)

    def start_indeterminate(self):
        """开始不确定进度（无限循环）"""
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(True)

    def set_progress(self, current: int, total: int):
        """
        设置确定进度

        Args:
            current: 当前进度
            total: 总进度
        """
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
        self.progress_bar.setVisible(True)

    def complete(self):
        """完成进度"""
        if self.progress_bar.maximum() > 0:
            self.progress_bar.setValue(self.progress_bar.maximum())

    def hide_progress(self):
        """隐藏进度条"""
        self.progress_bar.setVisible(False)

    def reset(self):
        """重置状态"""
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.status_label.setText("")
