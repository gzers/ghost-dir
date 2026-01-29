from typing import List, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout
from qfluentwidgets import TableWidget, FluentIcon, RoundMenu, Action, CheckBox, TransparentToolButton
from src.data.model import Template
from ....styles import get_font_style, get_text_primary, apply_transparent_style, get_text_secondary, get_accent_color


class TemplateTableWidget(TableWidget):
    """模板表格组件 - 增强版（含复选框与操作列）"""
    
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
        
        # 记录每行的复选框
        self.checkboxes: Dict[int, CheckBox] = {}
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 设置列：复选框, 名称, 源路径, 目标路径, 描述, 类型, 操作
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            '', '名称', '源路径', '目标路径', '描述', '类型', '操作'
        ])
        
        # 使用原生特性
        self.setBorderRadius(8)
        self.setBorderVisible(False)
        self.setSelectRightClickedRow(True)
        
        # 设置列宽与拉伸模式
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 48)  # 复选框列
        
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # 名称
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # 源路径
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)          # 目标路径
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # 描述
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # 类型
        
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)            # 操作
        self.setColumnWidth(6, 100)
        
        # 优化显示
        self.verticalHeader().setDefaultSectionSize(40)
        header.setFixedHeight(36)
        
        # 基本属性
        self.setEditTriggers(TableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(TableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(TableWidget.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(False)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setShowGrid(False)
        
        apply_transparent_style(self)
        
        self._apply_style()

    def _apply_style(self):
        """应用主题敏感样式 - 保持清爽原生感"""
        header_text_color = get_text_secondary()
        text_primary = get_text_primary()
        font_style = get_font_style(size="md", weight="normal")
        
        # 仅保留基础美化 QSS，不干涉 QFluentWidgets 的背景绘制
        qss = f"""
            QTableWidget {{
                background: transparent;
                outline: none;
                border: none;
                {font_style}
            }}
            QHeaderView::section {{
                background-color: transparent;
                border: none;
                padding-left: 8px;
                color: {header_text_color};
                font-size: 13px;
                font-weight: 600;
            }}
            QTableWidget::item {{
                color: {text_primary};
                padding-left: 8px;
                border: none;
            }}
        """
        self.setStyleSheet(qss)
        self.verticalHeader().setVisible(False)
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        self.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        
        # 连接主题/颜色变更信号
        from src.common.signals import signal_bus
        signal_bus.theme_color_changed.connect(self._apply_style)
        signal_bus.theme_changed.connect(self._apply_style)
    
    def set_templates(self, templates: List[Template], category_id: str = ""):
        """设置模板列表"""
        self.current_category_id = category_id
        self.templates = {t.id: t for t in templates}
        self.checkboxes.clear()
        
        self.setSortingEnabled(False)
        self.setRowCount(0)
        
        self.setRowCount(len(templates))
        for i, template in enumerate(templates):
            # 0. 复选框容器
            cb_container = QWidget()
            cb_layout = QHBoxLayout(cb_container)
            cb = CheckBox()
            cb_layout.addWidget(cb)
            cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            self.setCellWidget(i, 0, cb_container)
            self.checkboxes[i] = cb
            
            # 同时在第 0 列设置数据项用于存储 ID
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.UserRole, template.id)
            self.setItem(i, 0, id_item)
            
            # 1. 名称
            name_item = QTableWidgetItem(template.name)
            name_item.setData(Qt.ItemDataRole.UserRole, template.id)
            self.setItem(i, 1, name_item)
            
            # 2. 源路径
            src_item = QTableWidgetItem(template.default_src)
            self.setItem(i, 2, src_item)
            
            # 3. 目标路径
            target = getattr(template, 'default_target', None) or '(使用全局默认)'
            target_item = QTableWidgetItem(target)
            self.setItem(i, 3, target_item)
            
            # 4. 描述
            desc = template.description or ''
            desc_item = QTableWidgetItem(desc)
            self.setItem(i, 4, desc_item)
            
            # 5. 类型
            type_text = '自定义' if template.is_custom else '官方'
            type_item = QTableWidgetItem(type_text)
            self.setItem(i, 5, type_item)
            
            # 6. 操作按钮
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(4, 0, 4, 0)
            btn_layout.setSpacing(4)
            
            edit_btn = TransparentToolButton(FluentIcon.EDIT, btn_container)
            edit_btn.setToolTip('编辑')
            edit_btn.clicked.connect(lambda checked=False, tid=template.id: self.edit_template_requested.emit(tid))
            
            del_btn = TransparentToolButton(FluentIcon.DELETE, btn_container)
            del_btn.setToolTip('删除')
            del_btn.clicked.connect(lambda checked=False, tid=template.id: self.delete_template_requested.emit(tid))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setCellWidget(i, 6, btn_container)
        
        if category_id in self.sort_states:
            column, order = self.sort_states[category_id]
            self.sortByColumn(column, order)
        
        self.setSortingEnabled(True)
        self.clearSelection()
    
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
    
