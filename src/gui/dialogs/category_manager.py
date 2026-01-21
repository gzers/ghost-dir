"""
分类管理对话框
支持层叠弹窗模式
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, PushButton, 
    MessageBox, BodyLabel
)
from ...data.user_manager import UserManager
from ...data.model import Category
import uuid


class CategoryManagerDialog(MessageBoxBase):
    """分类管理对话框"""
    
    categories_changed = Signal()  # 分类变更信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.user_manager = UserManager()
        
        self.setWindowTitle("管理分类")
        self._init_ui()
        self._load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel("分类管理")
        
        # 分类列表
        self.categoryList = QListWidget()
        self.categoryList.setMinimumHeight(200)
        
        # 输入区域
        input_layout = QHBoxLayout()
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText("输入新分类名称...")
        input_layout.addWidget(self.nameEdit)
        
        self.addButton = PushButton("添加")
        self.addButton.clicked.connect(self._on_add_category)
        input_layout.addWidget(self.addButton)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        self.deleteButton = PushButton("删除选中")
        self.deleteButton.clicked.connect(self._on_delete_category)
        button_layout.addWidget(self.deleteButton)
        button_layout.addStretch()
        
        # 添加到视图
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(BodyLabel("现有分类："))
        self.viewLayout.addWidget(self.categoryList)
        self.viewLayout.addLayout(input_layout)
        self.viewLayout.addLayout(button_layout)
        
        # 按钮
        self.yesButton.setText("完成")
        self.cancelButton.hide()  # 隐藏取消按钮
        
        self.widget.setMinimumWidth(400)
    
    def _load_categories(self):
        """加载分类列表"""
        self.categoryList.clear()
        categories = self.user_manager.get_all_categories()
        
        for category in categories:
            item = QListWidgetItem(category.name)
            item.setData(Qt.ItemDataRole.UserRole, category)
            
            # 默认分类不可删除
            if category.name == "未分类":
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                item.setForeground(Qt.GlobalColor.gray)
            
            self.categoryList.addItem(item)
    
    def _on_add_category(self):
        """添加分类"""
        name = self.nameEdit.text().strip()
        
        if not name:
            MessageBox("提示", "请输入分类名称", self).exec()
            return
        
        # 检查是否已存在
        categories = self.user_manager.get_all_categories()
        if any(c.name == name for c in categories):
            MessageBox("提示", "分类已存在", self).exec()
            return
        
        # 添加分类
        category = Category(
            id=str(uuid.uuid4()),
            name=name
        )
        
        if self.user_manager.add_category(category):
            self.nameEdit.clear()
            self._load_categories()
            self.categories_changed.emit()
            MessageBox("成功", f"已添加分类：{name}", self).exec()
        else:
            MessageBox("失败", "添加分类失败", self).exec()
    
    def _on_delete_category(self):
        """删除分类"""
        current_item = self.categoryList.currentItem()
        
        if not current_item:
            MessageBox("提示", "请选择要删除的分类", self).exec()
            return
        
        category = current_item.data(Qt.ItemDataRole.UserRole)
        
        # 不允许删除默认分类
        if category.name == "未分类":
            MessageBox("提示", "不能删除默认分类", self).exec()
            return
        
        # 确认删除
        reply = MessageBox(
            "确认删除",
            f"确定要删除分类 {category.name} 吗？\n该分类下的连接将移到\"未分类\"。",
            self
        ).exec()
        
        if not reply:
            return
        
        # 删除分类
        if self.user_manager.remove_category(category.id):
            self._load_categories()
            self.categories_changed.emit()
            MessageBox("成功", f"已删除分类：{category.name}", self).exec()
        else:
            MessageBox("失败", "删除分类失败", self).exec()
    
    def validate(self):
        """验证（直接返回 True，因为没有取消按钮）"""
        return True
