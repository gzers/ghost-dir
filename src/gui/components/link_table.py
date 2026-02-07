"""
连接表格组件
主控制台的核心表格视图，继承自通用表格基类
"""
from typing import List
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import PushButton, TransparentToolButton, FluentIcon, IndeterminateProgressRing
from src.gui.components.base_table import BaseTableWidget
from src.models.link import UserLink, LinkStatus  # 新架构: 使用 models 层
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
        self.loading_ids = set() # 正在计算大小的 ID 集合
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
            # 如果该 ID 正在加载列表中，恢复其加载动画
            if link.id in self.loading_ids:
                self.set_row_size_loading(row, True)

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
        
        # 记录实测指向 (如果有)
        if link.resolve_path:
            name_item.setToolTip(f"期望指向: {link.source_path}\n物理实测: {link.resolve_path}")
        else:
            name_item.setToolTip(f"期望指向: {link.source_path}")
            
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
        
        # 为 ERROR 状态增加详细提示
        if link.status == LinkStatus.ERROR:
            badge.setToolTip("路径存在冲突：目标位置已被普通文件占用，无法建立链接。")
            
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

        # 获取状态枚举（由于是 UserLink 对象，直接用 link.status）
        status = link.status

        # 4. 操作按钮设置
        # 只要是“未连接”、“就绪”或“错误”状态，均视为可修复项
        can_establish = [LinkStatus.DISCONNECTED, LinkStatus.READY, LinkStatus.ERROR]

        if status in can_establish:
            btn = TransparentToolButton(FluentIcon.PLAY_SOLID, container)
            # 根据具体情况调整 ToolTip
            tip = "建立连接" if status == LinkStatus.READY else "修复连接"
            btn.setToolTip(tip)
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "establish"))
            layout.addWidget(btn)
        elif status == LinkStatus.CONNECTED:
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
            item = self.item(row, 1)
            if item:
                lid = item.data(Qt.ItemDataRole.UserRole)
                if lid:
                    self.loading_ids.add(lid)
            self.set_row_size_loading(row, True)

    def set_all_status_loading(self):
        """将所有状态列设置为加载状态"""
        for row in range(self.rowCount()):
            self.set_row_status_loading(row, True)

    def set_row_status_loading(self, row: int, is_loading: bool):
        """设置某一行状态列的加载状态"""
        if is_loading:
            # 1. 插进度环
            container = self.create_alignment_container(Qt.AlignmentFlag.AlignCenter)
            ring = IndeterminateProgressRing(container)
            ring.setFixedSize(16, 16)
            ring.setStrokeWidth(2)
            container.layout().addWidget(ring)
            self.setCellWidget(row, 3, container)
        else:
            # 由 update_row_status 接管恢复工作，此处不用显式 remove，除非是中途停止
            pass

    def update_row_status(self, link_id: str, status: LinkStatus):
        """更新指定行的状态显示"""
        for row in range(self.rowCount()):
            item = self.item(row, 1)
            if item and item.data(Qt.ItemDataRole.UserRole) == link_id:
                # 1. 移除加载动画容器
                self.removeCellWidget(row, 3)
                
                # 2. 重新创建并设置 StatusBadge
                from .status_badge import StatusBadge
                container = self.create_alignment_container()
                badge = StatusBadge(status)
                
                # 保持之前的 Tooltip 逻辑映射（简单复现之前的核心逻辑）
                # 这里暂时省略复杂的 tooltip，为了快速恢复样式，后续可通过 reload 完成精细填色
                container.layout().addWidget(badge)
                self.setCellWidget(row, 3, container)
                break

    def set_row_size_loading(self, row: int, is_loading: bool):
        """设置某一行空间占用列的加载状态"""
        if is_loading:
            # 1. 先清空原本的文字内容，避免并存
            size_item = self.item(row, 4)
            if size_item:
                size_item.setText("")

            # 2. 插入进度环 (使用标准对齐容器)
            container = self.create_alignment_container(Qt.AlignmentFlag.AlignCenter)
            ring = IndeterminateProgressRing(container)
            ring.setFixedSize(16, 16)
            ring.setStrokeWidth(2)
            ring.start()  # 【关键】启动动画
            container.layout().addWidget(ring)
            self.setCellWidget(row, 4, container)
        else:
            # 【关键】停止并移除 ProgressRing
            old_widget = self.cellWidget(row, 4)
            if old_widget:
                # 找到 ProgressRing 并停止动画
                ring = old_widget.findChild(IndeterminateProgressRing)
                if ring:
                    ring.stop()
                old_widget.setParent(None)
                old_widget.deleteLater()
            self.removeCellWidget(row, 4)

    def update_row_size(self, link_id: str, size_text: str):
        """更新指定行的空间显示，并停止加载动画"""
        # 不再通过 loading_ids 集合拦截，只要收到信号就更新 UI
        if link_id in self.loading_ids:
            self.loading_ids.remove(link_id)

        for row in range(self.rowCount()):
            item = self.item(row, 1)
            if item and item.data(Qt.ItemDataRole.UserRole) == link_id:
                # 1. 物理移除并销毁 ProgressRing (关键修复)
                old_widget = self.cellWidget(row, 4)
                if old_widget:
                    # 【关键】找到并停止动画
                    ring = old_widget.findChild(IndeterminateProgressRing)
                    if ring:
                        ring.stop()
                    old_widget.setParent(None)
                    old_widget.deleteLater()
                self.removeCellWidget(row, 4)
                
                # 2. 补置数据项并同步
                size_item = self.item(row, 4)
                if not size_item:
                    size_item = QTableWidgetItem()
                    self.setItem(row, 4, size_item)
                
                size_item.setText(size_text)
                size_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                
                # 3. 立即重绘该单元格
                self.viewport().update()
                break
