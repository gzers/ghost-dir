"""
模板预览对话框
显示分类下的模板列表，用于添加子分类前的确认
"""
from typing import List
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel
from src.models.template import Template  # 新架构


class TemplatePreviewDialog(MessageBoxBase):
    """模板预览对话框"""
    
    def __init__(self, category_name: str, templates: List[Template], parent=None):
        """
        初始化模板预览对话框
        
        Args:
            category_name: 分类名称
            templates: 模板列表
            parent: 父窗口
        """
        super().__init__(parent)
        self.category_name = category_name
        self.templates = templates
        self.should_move = False
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel('该分类下有模板', self)
        
        # 说明文本
        desc_text = f"分类 '{self.category_name}' 下有 {len(self.templates)} 个模板\n"
        desc_text += "添加子分类前需要先移动这些模板"
        self.descLabel = BodyLabel(desc_text, self)
        self.descLabel.setWordWrap(True)
        
        # 模板列表表格
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['名称', '路径'])
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setFixedHeight(200)
        
        # 填充数据
        self.tableWidget.setRowCount(len(self.templates))
        for i, template in enumerate(self.templates):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(template.name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(template.default_src))
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.descLabel)
        self.viewLayout.addWidget(self.tableWidget)
        
        # 按钮文本
        self.yesButton.setText('移动模板')
        self.cancelButton.setText('取消')
        
        # 设置对话框大小
        self.widget.setMinimumWidth(500)
    
    def validate(self) -> bool:
        """验证（总是返回 True，由用户决定）"""
        self.should_move = True
        return True
    
    def should_move_templates(self) -> bool:
        """是否应该移动模板"""
        return self.should_move
