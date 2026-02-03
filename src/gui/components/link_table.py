"""
连接表格组件
主控制台的核心表格视图，继承自通用表格基类
"""
from typing import List
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import PushButton, TransparentToolButton, FluentIcon, IndeterminateProgressRing
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

        # 3. 状态 (使用标准对齐容器包装 StatusBadge)
        from .status_badge import StatusBadge
        container = self.create_alignment_container()
        badge = StatusBadge(link.status)
        container.layout().addWidget(badge)
        self.setCellWidget(row, 3, container)
        
        # 4. 占用空间
        size_text = format_size(link.last_known_size) if link.last_known_size > 0 else "未计算"
        size_item = QTableWidgetItem(size_text)
        size_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 4, size_item)
        
        # 记录映射，方便后续动态更新加载状态
        name_item.setData(Qt.ItemDataRole.UserRole + 1, row) 
        
        # 5. 操作按钮
        action_widget = self._create_action_buttons(link)
        self.setCellWidget(row, 5, action_widget)

    def _create_action_buttons(self, link: UserLink) -> QWidget:
        """创建操作按钮组"""
        container = self.create_alignment_container()
        layout = container.layout()
        layout.setSpacing(8)
        
        # 获取状态字符串值进行比较
        status_val = link.status.value if hasattr(link.status, 'value') else link.status
        
        # 使用更轻量的按钮样式以匹配视觉
        # 交互逻辑统一化：失效、就绪、断开均视为“待建立”
        to_connect_statues = [
            LinkStatus.DISCONNECTED.value if hasattr(LinkStatus.DISCONNECTED, 'value') else LinkStatus.DISCONNECTED,
            LinkStatus.READY.value if hasattr(LinkStatus.READY, 'value') else LinkStatus.READY,
            LinkStatus.INVALID.value if hasattr(LinkStatus.INVALID, 'value') else LinkStatus.INVALID
        ]
        
        if status_val in to_connect_statues:
            btn = TransparentToolButton(FluentIcon.PLAY_SOLID, container)
            btn.setToolTip("建立连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "establish"))
            layout.addWidget(btn)
        elif status_val == (LinkStatus.CONNECTED.value if hasattr(LinkStatus.CONNECTED, 'value') else LinkStatus.CONNECTED):
            btn = TransparentToolButton(FluentIcon.CLOSE, container)
            btn.setToolTip("断开连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "disconnect"))
            layout.addWidget(btn)

        
        # 通用编辑按钮
        edit_btn = TransparentToolButton(FluentIcon.EDIT, container)
        edit_btn.setToolTip("编辑连接信息")
        edit_btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "edit"))
        layout.addWidget(edit_btn)
        
        # 通用删除按钮
        del_btn = TransparentToolButton(FluentIcon.DELETE, container)
        del_btn.setToolTip("删除链接记录")
        del_btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "delete"))
        layout.addWidget(del_btn)
        
        return container

    def _on_row_checked_changed(self):
        """处理行勾选状态改变 - 鲁棒性增强版本"""
        # 获取选中的 ID 列表
        selected_ids = self.get_selected_links()
        count = len(selected_ids)
        self.checked_changed.emit(count)
        
        # 同步表头复选框状态
        if self.header_checkbox:
            self.header_checkbox.blockSignals(True)
            total = self.rowCount()
            # 只有当选中数量等于总行数且总行数大于 0 时，表头才勾选
            self.header_checkbox.setChecked(count == total and total > 0)
            self.header_checkbox.blockSignals(False)

        # 发射业务信号
        self.link_selected.emit(selected_ids)

    def get_selected_links(self) -> list:
        """获取当前勾选的连接 ID 列表 - 强鲁棒版本"""
        selected_ids = []
        for row in range(self.rowCount()):
            container = self.cellWidget(row, 0)
            if container:
                from qfluentwidgets import CheckBox
                cb = container.findChild(CheckBox)
                if cb and cb.isChecked():
                    lid = cb.property("link_id")
                    if lid:
                        selected_ids.append(lid)
        return selected_ids

    def set_all_sizes_loading(self):
        """将所有行设置为加载状态"""
        for row in range(self.rowCount()):
            self.set_row_size_loading(row, True)

    def set_row_size_loading(self, row: int, is_loading: bool):
        """设置某一行空间占用列的加载状态"""
        if is_loading:
            # 1. 先清空原本的文字内容，避免并存
            size_item = self.item(row, 4)
            if size_item:
                size_item.setText("")
            
            # 2. 插入进度环 (使用标准对齐容器)
            container = self.create_alignment_container()
            ring = IndeterminateProgressRing(container)
            ring.setFixedSize(16, 16)
            ring.setStrokeWidth(2)
            container.layout().addWidget(ring)
            self.setCellWidget(row, 4, container)
        else:
            # 清除单元格中的 Widget (ProgressRing)
            self.removeCellWidget(row, 4)
