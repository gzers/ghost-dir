"""
模板表格组件
显示模板列表
"""
from typing import List, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMenu
from PySide6.QtGui import QAction
from qfluentwidgets import FluentIcon, RoundMenu, Action
from src.data.model import Template


class TemplateTableWidget(QTableWidget):
    """模板表格组件"""
    
    template_selected = Signal(str)  # 模板被选中时发出信号 (template_id)
    edit_template_requested = Signal(str)  # 请求编辑模板 (template_id)
    delete_template_requested = Signal(str)  # 请求删除模板 (template_id)
    
    def __init__(self, parent=None):
        """初始化模板表格组件"""
        super().__init__(parent)
        self.templates: Dict[str, Template] = {}
        self.sort_states: Dict[str, tuple] = {}  # category_id -> (column, order)
        self.current_category_id: str = ""
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 设置列
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            '名称', '源路径', '目标路径', '描述', '类型', '操作'
        ])
        
        # 设置列宽
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        # 设置表格属性
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # 垂直表头
        self.verticalHeader().setVisible(False)
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        self.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
    
    def set_templates(self, templates: List[Template], category_id: str = ""):
        """
        设置模板列表
        
        Args:
            templates: 模板列表
            category_id: 分类ID（用于恢复排序状态）
        """
        self.current_category_id = category_id
        self.templates = {t.id: t for t in templates}
        
        # 清空表格
        self.setSortingEnabled(False)
        self.setRowCount(0)
        
        # 填充数据
        self.setRowCount(len(templates))
        for i, template in enumerate(templates):
            # 名称
            name_item = QTableWidgetItem(template.name)
            name_item.setData(Qt.ItemDataRole.UserRole, template.id)
            self.setItem(i, 0, name_item)
            
            # 源路径
            src_item = QTableWidgetItem(template.default_src)
            self.setItem(i, 1, src_item)
            
            # 目标路径
            target = getattr(template, 'default_target', None) or '(使用全局默认)'
            target_item = QTableWidgetItem(target)
            self.setItem(i, 2, target_item)
            
            # 描述
            desc = template.description or ''
            desc_item = QTableWidgetItem(desc)
            self.setItem(i, 3, desc_item)
            
            # 类型
            type_text = '自定义' if template.is_custom else '官方'
            type_item = QTableWidgetItem(type_text)
            self.setItem(i, 4, type_item)
            
            # 操作（暂时留空，可以添加按钮）
            action_item = QTableWidgetItem('')
            self.setItem(i, 5, action_item)
        
        # 恢复排序状态
        if category_id in self.sort_states:
            column, order = self.sort_states[category_id]
            self.sortByColumn(column, order)
        
        self.setSortingEnabled(True)
    
    def _on_item_clicked(self, item: QTableWidgetItem):
        """表项被点击"""
        row = item.row()
        template_id = self.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if template_id:
            self.template_selected.emit(template_id)
    
    def _on_context_menu(self, pos):
        """显示右键菜单"""
        item = self.itemAt(pos)
        
        if not item:
            return
        
        row = item.row()
        template_id = self.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        if not template_id:
            return
        
        menu = RoundMenu(parent=self)
        
        # 编辑
        edit_action = Action(FluentIcon.EDIT, '编辑')
        edit_action.triggered.connect(lambda: self.edit_template_requested.emit(template_id))
        menu.addAction(edit_action)
        
        # 删除
        delete_action = Action(FluentIcon.DELETE, '删除')
        delete_action.triggered.connect(lambda: self.delete_template_requested.emit(template_id))
        menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(pos))
    
    def _on_header_clicked(self, column: int):
        """表头被点击（排序）"""
        # 保存排序状态
        if self.current_category_id:
            order = self.horizontalHeader().sortIndicatorOrder()
            self.sort_states[self.current_category_id] = (column, order)
    
    def get_selected_template_id(self) -> str:
        """获取当前选中的模板ID"""
        item = self.currentItem()
        if item:
            row = item.row()
            return self.item(row, 0).data(Qt.ItemDataRole.UserRole)
        return None
    
    def get_selected_templates(self) -> List[str]:
        """获取所有选中的模板ID"""
        selected_rows = set(item.row() for item in self.selectedItems())
        return [
            self.item(row, 0).data(Qt.ItemDataRole.UserRole)
            for row in selected_rows
        ]
