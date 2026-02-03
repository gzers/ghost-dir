"""
通用表格基类组件
提供统一的视觉呈现、表头全选逻辑和主题自适应
"""
from typing import Optional, List, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHeaderView, QWidget, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import TableWidget, CheckBox, setCustomStyleSheet
from src.gui.styles import (
    get_font_style, get_text_primary, apply_transparent_style, 
    get_text_secondary
)


class BaseTableWidget(TableWidget):
    """表格基类 - 封装统一样式和全选逻辑"""
    
    checked_changed = Signal(int)  # 勾选状态改变信号 (选中的数量)
    
    def __init__(self, parent=None, enable_checkbox: bool = True):
        """
        初始化表格基类
        :param enable_checkbox: 是否在第一列启用全选复选框
        """
        super().__init__(parent)
        self.enable_checkbox = enable_checkbox
        self.checkboxes: Dict[int, CheckBox] = {}
        self.header_checkbox: Optional[CheckBox] = None
        self.header_checkbox_container: Optional[QWidget] = None
        
        self._init_base_ui()
        self._connect_base_signals()

    def _init_base_ui(self):
        """初始化基础 UI 属性"""
        self.setBorderRadius(8)
        self.setBorderVisible(False)
        self.setSelectRightClickedRow(True)
        
        # 默认表格属性
        self.setEditTriggers(TableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(TableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(TableWidget.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(False)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setShowGrid(False)
        
        # 隐藏垂直表头以对齐视觉
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(40)
        self.horizontalHeader().setFixedHeight(36)
        
        apply_transparent_style(self)
        
        if self.enable_checkbox:
            self._setup_header_checkbox()
            
        self._apply_base_style()

    def _setup_header_checkbox(self):
        """设置表头全选复选框并实现动态对齐"""
        header = self.horizontalHeader()
        
        # 创建容器和布局
        self.header_checkbox_container = QWidget(header)
        container_layout = QHBoxLayout(self.header_checkbox_container)
        self.header_checkbox = CheckBox()
        container_layout.addWidget(self.header_checkbox)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # 连接状态信号
        self.header_checkbox.stateChanged.connect(self._on_header_checked_changed)
        # 连接尺寸同步信号，确保列宽变动时依然居中
        header.sectionResized.connect(self._on_header_section_resized)
        
        # 初始对齐
        self._update_header_checkbox_pos()

    def _on_header_section_resized(self, index, old_size, new_size):
        """当表头列宽改变时重新对齐"""
        if index == 0:
            self._update_header_checkbox_pos()
            
    def _update_header_checkbox_pos(self):
        """精确计算并更新复选框容器位置和大小"""
        if not self.header_checkbox_container:
            return
        width = self.columnWidth(0)
        height = self.horizontalHeader().height()
        # 基准偏移 8px 以适应 Fluent UI 风格
        self.header_checkbox_container.setGeometry(8, 0, width - 8, height)

    def _apply_base_style(self):
        """应用主题敏感样式 - 全局统一标准"""
        header_text_color = get_text_secondary()
        text_primary = get_text_primary()
        font_style = get_font_style(size="md", weight="normal")
        
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
                color: {header_text_color};
                font-size: 13px;
                font-weight: 600;
                padding-left: 8px;
            }}
            QTableWidget::item {{
                color: {text_primary};
                border: none;
                padding: 0 8px;
            }}
        """
        setCustomStyleSheet(self, qss, qss)

    def _connect_base_signals(self):
        """连接全局信号"""
        from src.common.signals import signal_bus
        signal_bus.theme_color_changed.connect(self._apply_base_style)
        signal_bus.theme_changed.connect(self._apply_base_style)

    def create_checkbox_cell(self, row: int, enabled: bool = True) -> CheckBox:
        """为特定行创建并设置复选框单元格，返回该复选框对象"""
        cb_container = QWidget()
        cb_container.setObjectName("checkboxContainer") # 方便查找
        cb_container.setFixedHeight(40)
        cb_container.setStyleSheet("background: transparent; border: none;")
        cb_layout = QHBoxLayout(cb_container)
        cb = CheckBox()
        cb.setEnabled(enabled)
        cb.setText("")
        cb_layout.addWidget(cb)
        cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cb_layout.setContentsMargins(0, 0, 0, 0)
        cb_layout.setSpacing(0)
        
        self.setCellWidget(row, 0, cb_container)
        
        # 不再按行号存字典，直接连接信号
        cb.stateChanged.connect(self._on_row_checked_changed)
        return cb

    def _on_row_checked_changed(self):
        """处理行勾选状态改变"""
        checked_rows = self.get_checked_rows()
        count = len(checked_rows)
        self.checked_changed.emit(count)
        
        # 同步表头复选框状态
        if self.header_checkbox:
            self.header_checkbox.blockSignals(True)
            total = self.rowCount()
            if count == 0:
                self.header_checkbox.setChecked(False)
            elif count == total and total > 0:
                self.header_checkbox.setChecked(True)
            else:
                self.header_checkbox.setChecked(False)
            self.header_checkbox.blockSignals(False)

    def _on_header_checked_changed(self, state):
        """处理表头勾选状态改变"""
        is_checked = state == Qt.CheckState.Checked.value
        for row in range(self.rowCount()):
            container = self.cellWidget(row, 0)
            if container:
                cb = container.findChild(CheckBox)
                if cb and cb.isEnabled(): # 仅处理启用的复选框
                    cb.blockSignals(True)
                    cb.setChecked(is_checked)
                    cb.blockSignals(False)
        self._on_row_checked_changed()

    def get_checked_rows(self) -> List[int]:
        """获取所有已勾选的行索引 (支持排序后的动态获取)"""
        checked = []
        for row in range(self.rowCount()):
            container = self.cellWidget(row, 0)
            if container:
                cb = container.findChild(CheckBox)
                if cb and cb.isChecked():
                    checked.append(row)
        return checked

    def reset_checkbox_state(self):
        """重置所有复选框状态"""
        self.checkboxes.clear()
        if self.header_checkbox:
            self.header_checkbox.blockSignals(True)
            self.header_checkbox.setChecked(False)
            self.header_checkbox.blockSignals(False)
        self.checked_changed.emit(0)

    def clear_selection(self):
        """取消勾选所有行"""
        for row in range(self.rowCount()):
            container = self.cellWidget(row, 0)
            if container:
                cb = container.findChild(CheckBox)
                if cb:
                    cb.blockSignals(True)
                    cb.setChecked(False)
                    cb.blockSignals(False)
        if self.header_checkbox:
            self.header_checkbox.blockSignals(True)
            self.header_checkbox.setChecked(False)
            self.header_checkbox.blockSignals(False)
        self.checked_changed.emit(0)

    def ensure_row_height(self):
        """强制对齐行高"""
        self.verticalHeader().setDefaultSectionSize(40)
