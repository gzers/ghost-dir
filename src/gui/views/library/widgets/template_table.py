from typing import List, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout
from qfluentwidgets import FluentIcon, RoundMenu, Action, TransparentToolButton, InfoBar, InfoBarPosition, CheckBox
from src.data.model import Template
from src.gui.components import BaseTableWidget


class TemplateTableWidget(BaseTableWidget):
    """模板表格组件 - 增强版（基于通用基类重构）"""
    
    template_selected = Signal(str)
    edit_template_requested = Signal(str)
    delete_template_requested = Signal(str)
    
    def __init__(self, parent=None, user_manager=None):
        """初始化模板表格组件"""
        super().__init__(parent, enable_checkbox=True)
        self.templates: Dict[str, Template] = {}
        self.sort_states: Dict[str, tuple] = {}
        self.current_category_id: str = ""
        self.user_manager = user_manager
        self.allow_operations = True
        
        self._setup_columns()
        self._connect_signals()
    
    def _setup_columns(self):
        """配置模板表特有的列信息"""
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            '', '名称', '源路径', '目标路径', '描述', '类型', '操作'
        ])
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 48)
        
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(6, 100)
        
        # 居中对齐特定列
        for col in [0, 5, 6]:
            self.model().setHeaderData(col, Qt.Orientation.Horizontal, 
                                       Qt.AlignmentFlag.AlignCenter, 
                                       Qt.ItemDataRole.TextAlignmentRole)
        
        self._update_header_checkbox_pos()

    def _connect_signals(self):
        """连接业务相关的信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        self.horizontalHeader().sectionClicked.connect(self._on_header_clicked)

    def set_templates(self, templates: List[Template], category_id: str = "", allow_operations: bool = True):
        """设置模板列表"""
        self.current_category_id = category_id
        self.allow_operations = allow_operations
        self.templates = {t.id: t for t in templates}
        
        self.setSortingEnabled(False)
        self.setRowCount(0)
        self.reset_checkbox_state()
        
        self.setRowCount(len(templates))
        for i, template in enumerate(templates):
            # 0. 同时在第 0 列设置数据项用于存储 ID (必须在 setCellWidget 之前，否则可能由于重新创建项导致 Widget 被清除)
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.UserRole, template.id)
            self.setItem(i, 0, id_item)
            
            # 1. 复选框容器 (使用基类)
            # v7.4.1: 如果是内置模板且 allow_operations 为 True (普通视图模式)，禁用复选框
            is_selectable = template.is_custom if allow_operations else False
            cb = self.create_checkbox_cell(i, enabled=is_selectable)
            cb.setProperty("template_id", template.id) 
            if not template.is_custom:
                cb.setToolTip("系统内置模板，无法删除或修改")
            
            # 1. 名称
            name_item = QTableWidgetItem(template.name)
            name_item.setData(Qt.ItemDataRole.UserRole, template.id)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            name_item.setToolTip(template.name)
            self.setItem(i, 1, name_item)
            
            # 2. 源路径
            src_item = QTableWidgetItem(template.default_src)
            src_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            src_item.setToolTip(template.default_src)
            self.setItem(i, 2, src_item)
            
            # 3. 目标路径
            target = getattr(template, 'default_target', None) or '跟随全局配置'

            target_item = QTableWidgetItem(target)
            target_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            target_item.setToolTip(target)
            self.setItem(i, 3, target_item)
            
            # 4. 描述
            desc = template.description or ''
            desc_item = QTableWidgetItem(desc)
            desc_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            desc_item.setToolTip(desc if desc else None)
            self.setItem(i, 4, desc_item)
            
            # 5. 类型 (使用主题感知的标签)
            from qfluentwidgets import CaptionLabel
            from src.gui.styles import apply_muted_text_style
            
            type_text = '自定义' if template.is_custom else '官方'
            type_container = self.create_alignment_container()
            type_label = CaptionLabel(type_text)
            # 应用统一样式：弱化显示以区分主标题
            apply_muted_text_style(type_label)
            
            type_container.layout().addWidget(type_label)
            self.setCellWidget(i, 5, type_container)
            
            # 6. 操作按钮
            btn_container = QWidget()
            btn_container.setStyleSheet("background: transparent; border: none;")
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(4)
            
            edit_btn = TransparentToolButton(FluentIcon.EDIT, btn_container)
            edit_btn.setToolTip('编辑')
            edit_btn.setFixedSize(32, 32)
            edit_btn.setEnabled(allow_operations)
            edit_btn.clicked.connect(lambda checked=False, tid=template.id: self.edit_template_requested.emit(tid))
            
            del_btn = TransparentToolButton(FluentIcon.DELETE, btn_container)
            del_btn.setToolTip('删除')
            del_btn.setFixedSize(32, 32)
            del_btn.setEnabled(allow_operations)
            del_btn.clicked.connect(lambda checked=False, tid=template.id: self.delete_template_requested.emit(tid))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setCellWidget(i, 6, btn_container)
        
        if category_id in self.sort_states:
            column, order = self.sort_states[category_id]
            self.sortByColumn(column, order)
        
        self.setSortingEnabled(True)
        self.ensure_row_height()
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
        
        if item and item.text():
            copy_action = Action(FluentIcon.COPY, '复制')
            def copy_text():
                QGuiApplication.clipboard().setText(item.text())
                InfoBar.success(
                    title="已复制",
                    content=f"内容: {item.text()[:20]}...",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_CENTER,
                    duration=2000,
                    parent=self.window()
                )
            copy_action.triggered.connect(copy_text)
            menu.addAction(copy_action)
            menu.addSeparator()

        edit_action = Action(FluentIcon.EDIT, '编辑')
        edit_action.setEnabled(self.allow_operations)
        edit_action.triggered.connect(lambda: self.edit_template_requested.emit(template_id))
        menu.addAction(edit_action)
        
        delete_action = Action(FluentIcon.DELETE, '删除')
        delete_action.setEnabled(self.allow_operations)
        delete_action.triggered.connect(lambda: self.delete_template_requested.emit(template_id))
        menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(pos))
    
    def _on_header_clicked(self, column: int):
        """记录排序状态"""
        if self.current_category_id:
            order = self.horizontalHeader().sortIndicatorOrder()
            self.sort_states[self.current_category_id] = (column, order)

    def get_checked_template_ids(self) -> List[str]:
        """获取所有已勾选的模板ID (增强版：双重校验确保 ID 准确)"""
        ids = []
        for row in self.get_checked_rows():
            # 1. 优先从 CheckBox 属性获取 (最可靠，不受 Item 覆盖影响)
            container = self.cellWidget(row, 0)
            if container:
                cb = container.findChild(CheckBox)
                if cb and cb.property("template_id"):
                    ids.append(cb.property("template_id"))
                    continue
            
            # 2. 备选方案：从 QTableWidgetItem 获取
            id_item = self.item(row, 0)
            if id_item:
                ids.append(id_item.data(Qt.ItemDataRole.UserRole))
        return ids
