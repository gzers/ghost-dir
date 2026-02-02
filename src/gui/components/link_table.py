"""
连接表格组件
主控制台的核心表格视图，继承自通用表格基类
"""
from typing import List
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import PushButton, TransparentToolButton, FluentIcon
from src.gui.components.base_table import BaseTableWidget
from src.data.model import UserLink, LinkStatus
from src.common.config import format_size
from src.gui.i18n import get_status_text, get_category_text


class LinkTable(BaseTableWidget):
    """连接表格组件 - 统一视觉版本"""
    
    # 信号
    link_selected = Signal(list)  # 选中的连接 ID 列表 (勾选的)
    action_clicked = Signal(str, str)  # (link_id, action)
    
    def __init__(self, parent=None):
        """初始化表格"""
        super().__init__(parent, enable_checkbox=True)
        self.links: List[UserLink] = []
        self._setup_columns()
    
    def _setup_columns(self):
        """配置列结构与拉伸模式"""
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["", "软件信息", "分类", "状态", "占用空间", "操作"])
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 48)  # 标准复选框宽度
        
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(2, 120)  # 分类列宽度
        
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(3, 100)
        
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(4, 100)
        
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(5, 180) # 调窄操作列，保持紧凑

        # 手动触发表头复选框位置更新
        self._update_header_checkbox_pos()

    def load_links(self, links: List[UserLink]):
        """加载连接列表"""
        self.links = links
        self.setSortingEnabled(False)
        self.setRowCount(0)
        self.reset_checkbox_state()
        
        self.setRowCount(len(links))
        for row, link in enumerate(links):
            self._create_row(row, link)
            
        self.setSortingEnabled(True)
        self.ensure_row_height()
        self.clearSelection()
    
    def _create_row(self, row: int, link: UserLink):
        """创建表格行细节"""
        # 0. 复选框 (使用基类工厂方法)
        cb = self.create_checkbox_cell(row)
        # 为复选框绑定 ID，防止排序后索引失效
        cb.setProperty("link_id", link.id)
        
        # 1. 软件信息
        name_item = QTableWidgetItem(link.name)
        name_item.setData(Qt.ItemDataRole.UserRole, link.id)
        name_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.setItem(row, 1, name_item)

        # 2. 分类 (标准化文案)
        cat_text = get_category_text(link.category)
        cat_item = QTableWidgetItem(cat_text)
        cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 2, cat_item)

        # 3. 状态 (使用可视化的 StatusBadge)
        from .status_badge import StatusBadge
        status_widget = QWidget()
        status_widget.setStyleSheet("background: transparent; border: none;")
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        badge = StatusBadge(link.status)
        status_layout.addWidget(badge)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCellWidget(row, 3, status_widget)
        
        # 4. 占用空间
        size_text = format_size(link.last_known_size) if link.last_known_size > 0 else "未计算"
        size_item = QTableWidgetItem(size_text)
        size_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 4, size_item)
        
        # 5. 操作按钮
        action_widget = self._create_action_buttons(link)
        self.setCellWidget(row, 5, action_widget)

    def _create_action_buttons(self, link: UserLink) -> QWidget:
        """创建操作按钮组"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 获取状态字符串值进行比较
        status_val = link.status.value if hasattr(link.status, 'value') else link.status
        
        # 使用更轻量的按钮样式以匹配视觉
        if status_val == LinkStatus.DISCONNECTED.value:
            btn = TransparentToolButton(FluentIcon.LINK, widget)
            btn.setToolTip("建立连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "establish"))
            layout.addWidget(btn)
        elif status_val == LinkStatus.CONNECTED.value:
            btn = TransparentToolButton(FluentIcon.CLOSE, widget)
            btn.setToolTip("断开连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "disconnect"))
            layout.addWidget(btn)
        elif status_val == LinkStatus.READY.value:
            btn = TransparentToolButton(FluentIcon.SYNC, widget)
            btn.setToolTip("重新连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "reconnect"))
            layout.addWidget(btn)

        
        # 通用编辑按钮
        edit_btn = TransparentToolButton(FluentIcon.EDIT, widget)
        edit_btn.setToolTip("编辑连接信息")
        edit_btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "edit"))
        layout.addWidget(edit_btn)
        
        # 通用删除按钮
        del_btn = TransparentToolButton(FluentIcon.DELETE, widget)
        del_btn.setToolTip("删除链接记录")
        del_btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "delete"))
        layout.addWidget(del_btn)
        
        return widget

    def _on_row_checked_changed(self):
        """处理行勾选状态改变 - 使用绑定数据而非物理索引"""
        # 注意：此处不再调用 super()._on_row_checked_changed()，因为我们要处理排序兼容性
        # 计算数量
        count = sum(1 for cb in self.checkboxes.values() if cb.isChecked())
        self.checked_changed.emit(count)
        
        # 同步表头
        if self.header_checkbox:
            self.header_checkbox.blockSignals(True)
            total = len(self.checkboxes)
            self.header_checkbox.setChecked(count == total and total > 0)
            self.header_checkbox.blockSignals(False)

        # 发射业务信号
        selected_ids = self.get_selected_links()
        self.link_selected.emit(selected_ids)

    def get_selected_links(self) -> list:
        """获取当前勾选的连接 ID 列表 - 强鲁棒版本"""
        selected_ids = []
        for cb in self.checkboxes.values():
            if cb.isChecked():
                lid = cb.property("link_id")
                if lid:
                    selected_ids.append(lid)
        return selected_ids
