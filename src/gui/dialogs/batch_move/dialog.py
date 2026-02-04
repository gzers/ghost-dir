"""
批量移动对话框
用于批量移动模板到新分类
"""
from typing import List
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QListWidget, QListWidgetItem, QLabel
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, InfoBar
from src.data.model import Template
from src.data.category_manager import CategoryManager
from src.gui.components import CategorySelector


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
        self.templateList.setFixedHeight(120)
        for template in self.templates:
            item = QListWidgetItem(f"{template.name} ({template.default_src})")
            self.templateList.addItem(item)
        
        # 分类选择标签
        category_label = BodyLabel('目标分类*:', self)
        category_label.setStyleSheet("font-weight: bold;")
        
        # 分类选择器（树形）
        self.categorySelector = CategorySelector(self, only_leaf=True)
        self.categorySelector.set_manager(self.category_manager)
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.descLabel)
        self.viewLayout.addWidget(self.templateList)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(category_label)
        self.viewLayout.addWidget(self.categorySelector)
        
        # 按钮文本
        self.yesButton.setText('移动')
        self.cancelButton.setText('取消')
        
        # 设置对话框大小
        self.widget.setMinimumWidth(500)
    
    def validate(self) -> bool:
        """验证输入"""
        if not self.categorySelector.get_value():
            InfoBar.warning(
                title='验证失败',
                content='请选择目标分类（只能选择叶子分类）',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
        
        return True
    
    def get_target_category_id(self) -> str:
        """获取目标分类ID"""
        return self.categorySelector.get_value()
