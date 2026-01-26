# coding:utf-8
"""
测试 MessageBoxBase 中的 TreeWidget 复选框
"""
import sys
from PySide6.QtWidgets import QApplication, QTreeWidgetItem
from PySide6.QtCore import Qt
from qfluentwidgets import TreeWidget, MessageBoxBase, SubtitleLabel


class TestMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 标题
        self.titleLabel = SubtitleLabel("测试复选框")
        
        # 树形控件
        self.tree = TreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMinimumHeight(200)
        
        # 添加测试项 - 完全复制 test_checkbox.py 的代码
        for i in range(3):
            item = QTreeWidgetItem(self.tree)
            item.setText(0, f"分类 {i+1}")
            
            # 设置复选框
            item.setFlags(
                item.flags() | 
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsUserCheckable |
                Qt.ItemFlag.ItemIsSelectable
            )
            item.setCheckState(0, Qt.CheckState.Unchecked)
        
        # 添加到视图
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.tree)
        
        # 按钮
        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = TestMessageBox()
    dialog.exec()
    sys.exit(0)
