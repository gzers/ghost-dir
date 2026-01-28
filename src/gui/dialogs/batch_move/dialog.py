"""
批量移动对话框
用于批量移动模板到新分类
"""
from typing import List
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QListWidget, QListWidgetItem
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ComboBox, BodyLabel, InfoBar, InfoBarPosition
from src.data.model import Template
from src.data.category_manager import CategoryManager


class BatchMoveDialog(MessageBoxBase):
    """批量移动对话框"""
    
    def __init__(
        self,
        category_manager: CategoryManager,
        templates: List[Template],
        parent=None
    ):
        """
        初始化批量移动对话框
        
        Args:
            category_manager: 分类管理器
            templates: 要移动的模板列表
            parent: 父窗口
        """
        super().__init__(parent)
        self.category_manager = category_manager
        self.templates = templates
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel('批量移动模板', self)
        
        # 说明
        desc_text = f"将 {len(self.templates)} 个模板移动到新分类"
        self.descLabel = BodyLabel(desc_text, self)
        
        # 模板列表
        self.templateList = QListWidget(self)
        self.templateList.setFixedHeight(150)
        for template in self.templates:
            item = QListWidgetItem(f"{template.name} ({template.default_src})")
            self.templateList.addItem(item)
        
        # 表单
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)
        
        # 目标分类选择
        self.categoryCombo = ComboBox(self)
        self.categoryCombo.setFixedWidth(300)
        self.categoryCombo.setPlaceholderText('选择目标分类')
        
        # 只显示叶子分类
        for category in self.category_manager.get_all_categories():
            if self.category_manager.is_leaf(category.id):
                depth = category.get_depth(self.category_manager.categories)
                indent = "  " * (depth - 1)
                display_name = f"{indent}{category.name}"
                self.categoryCombo.addItem(display_name, category.id)
        
        form_layout.addRow('目标分类*:', self.categoryCombo)
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.descLabel)
        self.viewLayout.addWidget(self.templateList)
        self.viewLayout.addWidget(form_widget)
        
        # 按钮文本
        self.yesButton.setText('移动')
        self.cancelButton.setText('取消')
        
        # 设置对话框大小
        self.widget.setMinimumWidth(450)
    
    def validate(self) -> bool:
        """验证输入"""
        if not self.categoryCombo.currentData():
            InfoBar.warning(
                title='验证失败',
                content='请选择目标分类',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        return True
    
    def get_target_category_id(self) -> str:
        """获取目标分类ID"""
        return self.categoryCombo.currentData()
