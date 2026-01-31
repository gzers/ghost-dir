"""
连接表格组件
主控制台的核心表格视图，继承自通用表格基类
"""
from typing import List
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import PushButton, TransparentToolButton, FluentIcon
from .base_table import BaseTableWidget
from ...data.model import UserLink, LinkStatus
from ...common.config import format_size
from ..i18n import get_status_text


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
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["", "软件信息", "状态", "占用空间", "操作"])
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 48)  # 标准复选框宽度
        
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(2, 120)
        
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(3, 120)
        
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(4, 180) # 调窄操作列，保持紧凑

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
        self.create_checkbox_cell(row)
        
        # 1. 软件信息
        name_item = QTableWidgetItem(link.name)
        name_item.setData(Qt.ItemDataRole.UserRole, link.id)
        name_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.setItem(row, 1, name_item)

        # 2. 状态 (封装容器确保居中)
        status_widget = QWidget()
        status_widget.setStyleSheet("background: transparent; border: none;")
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_text = get_status_text(link.status.value)
        from qfluentwidgets import BodyLabel
        label = BodyLabel(status_text)
        status_layout.addWidget(label)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCellWidget(row, 2, status_widget)
        
        # 3. 占用空间
        size_text = format_size(link.last_known_size) if link.last_known_size > 0 else "未计算"
        size_item = QTableWidgetItem(size_text)
        size_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 3, size_item)
        
        # 4. 操作按钮
        action_widget = self._create_action_buttons(link)
        self.setCellWidget(row, 4, action_widget)

    def _create_action_buttons(self, link: UserLink) -> QWidget:
        """创建操作按钮组"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 使用更轻量的按钮样式以匹配视觉
        if link.status == LinkStatus.DISCONNECTED:
            btn = TransparentToolButton(FluentIcon.LINK, widget)
            btn.setToolTip("建立连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "establish"))
            layout.addWidget(btn)
        elif link.status == LinkStatus.CONNECTED:
            btn = TransparentToolButton(FluentIcon.CLOSE, widget)
            btn.setToolTip("断开连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "disconnect"))
            layout.addWidget(btn)
        elif link.status == LinkStatus.READY:
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
        """重写基类信号处理，转发业务信号"""
        super()._on_row_checked_changed()
        selected_ids = []
        for row, cb in self.checkboxes.items():
            if cb.isChecked():
                id_item = self.item(row, 1) # 这里 ID 存在第 1 列
                if id_item:
                    selected_ids.append(id_item.data(Qt.ItemDataRole.UserRole))
        self.link_selected.emit(selected_ids)

    def get_selected_links(self) -> list:
        """获取当前勾选的连接 ID 列表"""
        selected_ids = []
        for row, cb in self.checkboxes.items():
            if cb.isChecked():
                id_item = self.item(row, 1)
                if id_item:
                    selected_ids.append(id_item.data(Qt.ItemDataRole.UserRole))
        return selected_ids
