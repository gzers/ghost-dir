# coding:utf-8
"""
最小化测试：在 MessageBoxBase 中使用完全相同的 TreeWidget 代码
"""
import sys
from PySide6.QtWidgets import QApplication, QTreeWidgetItem, QMainWindow
from PySide6.QtCore import Qt
from qfluentwidgets import TreeWidget, MessageBoxBase, SubtitleLabel, PushButton


class MinimalTestDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 标题
        self.titleLabel = SubtitleLabel("最小化测试")
        
        # 创建树形控件 - 完全复制 test_checkbox.py 的代码
        self.tree = TreeWidget()
        self.tree.setHeaderHidden(True)
        
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试主窗口")
        self.resize(800, 600)
        
        # 创建按钮
        btn = PushButton("打开对话框", self)
        btn.move(50, 50)
        btn.clicked.connect(self.show_dialog)
    
    def show_dialog(self):
        dialog = MinimalTestDialog(self)
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
