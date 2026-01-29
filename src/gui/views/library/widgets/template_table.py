from typing import List, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from qfluentwidgets import TableWidget, FluentIcon, RoundMenu, Action
from src.data.model import Template
from ....styles import get_font_style, get_text_primary, apply_transparent_style, get_text_secondary


class TemplateTableWidget(TableWidget):
    """模板表格组件 - 基于 QFluentWidgets 原生组件重构"""
    
    template_selected = Signal(str)  # 模板被选中时发出信号 (template_id)
    edit_template_requested = Signal(str)  # 请求编辑模板 (template_id)
    delete_template_requested = Signal(str)  # 请求删除模板 (template_id)
    
    def __init__(self, parent=None, user_manager=None):
        """初始化模板表格组件"""
        super().__init__(parent)
        self.templates: Dict[str, Template] = {}
        self.sort_states: Dict[str, tuple] = {}
        self.current_category_id: str = ""
        self.user_manager = user_manager
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 设置列
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            '名称', '源路径', '目标路径', '描述', '类型', '操作'
        ])
        
        # 使用原生特性：圆角和边框控制
        self.setBorderRadius(8)
        self.setBorderVisible(False)
        self.setSelectRightClickedRow(True)
        
        # 设置列宽
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        # 优化行高
        self.verticalHeader().setDefaultSectionSize(40)
        header.setFixedHeight(36)
        
        # 设置表格属性
        self.setEditTriggers(TableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(TableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(TableWidget.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(False)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setShowGrid(False)
        
        # 应用透明背景以透出 Mica
        apply_transparent_style(self)
        
        font_style = get_font_style(size="md", weight="normal")
        header_text_color = get_text_secondary()
        text_primary = get_text_primary()
        
        qss = f"""
            QTableWidget {{
                background: transparent;
                border: none;
                outline: none;
                {font_style}
            }}
            QHeaderView::section {{
                background-color: transparent;
                border: none;
                padding-left: 12px;
                color: {header_text_color};
                font-size: 13px;
                font-weight: 600;
            }}
            /* 基本文字颜色定义 */
            QTableWidget::item {{
                color: {text_primary};
                padding-left: 12px;
            }}
        """
        self.setStyleSheet(qss)
        self.verticalHeader().setVisible(False)
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        self.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
    
    def set_templates(self, templates: List[Template], category_id: str = ""):
        """设置模板列表"""
        self.current_category_id = category_id
        self.templates = {t.id: t for t in templates}
        
        self.setSortingEnabled(False)
        self.setRowCount(0)
        
        self.setRowCount(len(templates))
        for i, template in enumerate(templates):
            name_item = QTableWidgetItem(template.name)
            name_item.setData(Qt.ItemDataRole.UserRole, template.id)
            self.setItem(i, 0, name_item)
            
            src_item = QTableWidgetItem(template.default_src)
            self.setItem(i, 1, src_item)
            
            target = getattr(template, 'default_target', None) or '(使用全局默认)'
            target_item = QTableWidgetItem(target)
            self.setItem(i, 2, target_item)
            
            desc = template.description or ''
            desc_item = QTableWidgetItem(desc)
            self.setItem(i, 3, desc_item)
            
            type_text = '自定义' if template.is_custom else '官方'
            type_item = QTableWidgetItem(type_text)
            self.setItem(i, 4, type_item)
            
            action_item = QTableWidgetItem('')
            self.setItem(i, 5, action_item)
        
        if category_id in self.sort_states:
            column, order = self.sort_states[category_id]
            self.sortByColumn(column, order)
        
        self.setSortingEnabled(True)
    
    def _on_item_clicked(self, item: QTableWidgetItem):
        """表项被点击"""
        row = item.row()
        id_item = self.item(row, 0)
        if id_item:
            template_id = id_item.data(Qt.ItemDataRole.UserRole)
            if template_id:
                self.template_selected.emit(template_id)
    
    def _on_context_menu(self, pos):
        """显示右键菜单"""
        item = self.itemAt(pos)
        if not item: return
        
        row = item.row()
        id_item = self.item(row, 0)
        if not id_item: return
        
        template_id = id_item.data(Qt.ItemDataRole.UserRole)
        if not template_id: return
        
        menu = RoundMenu(parent=self)
        edit_action = Action(FluentIcon.EDIT, '编辑')
        edit_action.triggered.connect(lambda: self.edit_template_requested.emit(template_id))
        menu.addAction(edit_action)
        
        delete_action = Action(FluentIcon.DELETE, '删除')
        delete_action.triggered.connect(lambda: self.delete_template_requested.emit(template_id))
        menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(pos))
    
    def _on_header_clicked(self, column: int):
        """表头被点击"""
        if self.current_category_id:
            order = self.horizontalHeader().sortIndicatorOrder()
            self.sort_states[self.current_category_id] = (column, order)
    
    def get_selected_template_id(self) -> str:
        """获取当前选中的模板ID"""
        items = self.selectedItems()
        if items:
            row = items[0].row()
            id_item = self.item(row, 0)
            return id_item.data(Qt.ItemDataRole.UserRole) if id_item else None
        return None
    
    def get_selected_templates(self) -> List[str]:
        """获取所有选中的模板ID"""
        selected_rows = set(item.row() for item in self.selectedItems())
        ids = []
        for row in selected_rows:
            id_item = self.item(row, 0)
            if id_item:
                ids.append(id_item.data(Qt.ItemDataRole.UserRole))
        return ids
    
    def get_selected_templates(self) -> List[str]:
        """获取所有选中的模板ID"""
        selected_rows = set(item.row() for item in self.selectedItems())
        return [
            self.item(row, 0).data(Qt.ItemDataRole.UserRole)
            for row in selected_rows
        ]
