# coding:utf-8
"""
测试 TreeWidget 复选框功能
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import TreeWidget, PushButton


class TestCheckboxTree(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TreeWidget Checkbox Test")
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # 创建树形控件
        self.tree = TreeWidget()
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)
        
        # 添加测试按钮
        btn = PushButton("检查勾选项")
        btn.clicked.connect(self.check_items)
        layout.addWidget(btn)
        
        # 添加测试项
        self.add_test_items()
    
    def add_test_items(self):
        """添加测试项"""
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
            
            # 添加子项
            for j in range(2):
                child = QTreeWidgetItem(item)
                child.setText(0, f"子分类 {i+1}-{j+1}")
                child.setFlags(
                    child.flags() | 
                    Qt.ItemFlag.ItemIsEnabled | 
                    Qt.ItemFlag.ItemIsUserCheckable |
                    Qt.ItemFlag.ItemIsSelectable
                )
                child.setCheckState(0, Qt.CheckState.Unchecked)
    
    def check_items(self):
        """检查勾选的项"""
        checked = []
        self.collect_checked(self.tree.invisibleRootItem(), checked)
        print(f"勾选的项: {[item.text(0) for item in checked]}")
    
    def collect_checked(self, parent, checked_list):
        """递归收集勾选的项"""
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.checkState(0) == Qt.CheckState.Checked:
                checked_list.append(child)
            self.collect_checked(child, checked_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TestCheckboxTree()
    w.show()
    sys.exit(app.exec())
