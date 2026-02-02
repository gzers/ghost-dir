"""
自定义进度对话框
解决 qfluentwidgets 某些版本缺失 ProgressDialog 的问题
"""
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, ProgressBar


class ProgressDialog(MessageBoxBase):
    """标准的进度对话框"""
    
    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.contentLabel = BodyLabel(content, self)
        self.progressBar = ProgressBar(self)
        
        # 将组件添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)
        self.viewLayout.addWidget(self.progressBar)
        
        # 默认隐藏取消按钮（如果需要可以手动开启）
        self.cancelButton.setText("取消")
        self.yesButton.hide() # 这种对话框通常不需要确认按钮，由程序自动关闭
        
        self.widget.setMinimumWidth(400)

    def setProgress(self, value: int):
        """设置百分比 (0-100)"""
        self.progressBar.setValue(value)

    def setDescription(self, text: str):
        """更新状态描述"""
        self.contentLabel.setText(text)
