# coding:utf-8
"""
测试：使用 _add_category_item 方式添加items
"""
import sys
from PySide6.QtWidgets import QApplication, QTreeWidgetItem, QMainWindow
from PySide6.QtCore import Qt
from qfluentwidgets import TreeWidget, MessageBoxBase, SubtitleLabel, PushButton


class TestDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 标题
        self.titleLabel = SubtitleLabel("测试 _add_item 方式")
        
        # 创建树形控件
        self.tree = TreeWidget()
        self.tree.setHeaderHidden(True)
        
        # 添加到视图
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.tree)
        
        # 按钮
        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(400)
        
        # 加载items - 模拟 category_manager 的方式
        self._load_items()
    
    def _load_items(self):
        """加载items - 模拟 _load_categories"""
        self.tree.clear()
        
        # 添加3个根items
        for i in range(3):
            self._add_item(None, f"分类 {i+1}")
    
    def _add_item(self, parent_item, text):
        """递归添加item - 模拟 _add_category_item"""
        # 创建树节点
        if parent_item is None:
            item = QTreeWidgetItem(self.tree)
        else:
            item = QTreeWidgetItem(parent_item)
        
        # 设置显示文本
        item.setText(0, text)
        
        # 设置复选框
        item.setFlags(
            item.flags() | 
            Qt.ItemFlag.ItemIsEnabled | 
            Qt.ItemFlag.ItemIsUserCheckable |
            Qt.ItemFlag.ItemIsSelectable
        )
        item.setCheckState(0, Qt.CheckState.Unchecked)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试主窗口")
        self.resize(800, 600)
        
        btn = PushButton("打开对话框", self)
        btn.move(50, 50)
        btn.clicked.connect(self.show_dialog)
    
    def show_dialog(self):
        dialog = TestDialog(self)
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
