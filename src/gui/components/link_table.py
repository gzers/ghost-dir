"""
连接表格组件
主控制台的核心表格视图
"""
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import PushButton, TableWidget
from ...data.model import UserLink, LinkStatus
from ...common.config import format_size
from .status_badge import StatusBadge


class LinkTable(TableWidget):
    """连接表格组件"""
    
    # 信号
    link_selected = Signal(list)  # 选中的连接 ID 列表
    action_clicked = Signal(str, str)  # (link_id, action)
    
    def __init__(self, parent=None):
        """初始化表格"""
        super().__init__(parent)
        self._init_ui()
        self.links = []
        self.checkboxes = {}
    
    def _init_ui(self):
        """初始化 UI"""
        # 设置列
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["", "软件信息", "状态", "占用空间", "操作"])

        # 设置主题样式
        self._update_theme_style()
        from ...common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _update_theme_style(self):
        """更新主题样式"""
        from ..styles import StyleManager
        bg_color = StyleManager.get_container_background()
        alternate_bg = StyleManager.get_hover_background()
        border_color = StyleManager.get_border_color()
        
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {bg_color};
                alternate-background-color: {alternate_bg};
                gridline-color: transparent;
                border: none;
            }}
            QHeaderView::section {{
                background-color: {bg_color};
                border: none;
                border-bottom: 1px solid {border_color};
            }}
        """)

    def _on_theme_changed(self, theme):
        """主题变更"""
        self._update_theme_style()
        
        # 设置列宽
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 复选框
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 软件信息
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # 状态
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # 空间
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # 操作
        
        self.setColumnWidth(0, 50)
        self.setColumnWidth(2, 120)
        self.setColumnWidth(3, 120)
        self.setColumnWidth(4, 200)
        
        # 设置表格属性
        self.setWordWrap(False)
        self.setRowCount(0)
        self.setAlternatingRowColors(True)  # 启用交替行背景色
        
        # 启用排序
        self.setSortingEnabled(True)
    
    def load_links(self, links: list):
        """加载连接列表"""
        self.links = links
        self.setRowCount(len(links))
        self.checkboxes.clear()
        
        for row, link in enumerate(links):
            self._create_row(row, link)
    
    def _create_row(self, row: int, link: UserLink):
        """创建表格行"""
        # 列 0: 复选框
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(self._on_checkbox_changed)
        checkbox_layout.addWidget(checkbox)
        
        self.setCellWidget(row, 0, checkbox_widget)
        self.checkboxes[link.id] = checkbox
        
        # 列 1: 软件信息
        name_item = QTableWidgetItem(link.name)
        name_item.setData(Qt.ItemDataRole.UserRole, link.id)
        self.setItem(row, 1, name_item)
        
        # 列 2: 状态
        status_badge = StatusBadge(link.status)
        self.setCellWidget(row, 2, status_badge)
        
        # 列 3: 占用空间
        size_text = format_size(link.last_known_size) if link.last_known_size > 0 else "未计算"
        size_item = QTableWidgetItem(size_text)
        size_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 3, size_item)
        
        # 列 4: 操作按钮
        action_widget = self._create_action_buttons(link)
        self.setCellWidget(row, 4, action_widget)
    
    def _create_action_buttons(self, link: UserLink) -> QWidget:
        """创建操作按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # 根据状态显示不同的按钮
        if link.status == LinkStatus.DISCONNECTED:
            btn = PushButton("🔗 建立连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "establish"))
            layout.addWidget(btn)
            
        elif link.status == LinkStatus.CONNECTED:
            btn = PushButton("🔌 断开连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "disconnect"))
            layout.addWidget(btn)
            
        elif link.status == LinkStatus.READY:
            btn = PushButton("🔗 重新连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "reconnect"))
            layout.addWidget(btn)
            
        else:  # INVALID
            btn = PushButton("🗑️ 删除")
            btn.clicked.connect(lambda: self.action_clicked.emit(link.id, "delete"))
            layout.addWidget(btn)
        
        layout.addStretch()
        return widget
    
    def _on_checkbox_changed(self):
        """复选框状态变更"""
        selected_ids = []
        for link_id, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected_ids.append(link_id)
        
        self.link_selected.emit(selected_ids)
    
    def get_selected_links(self) -> list:
        """获取选中的连接 ID"""
        selected_ids = []
        for link_id, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected_ids.append(link_id)
        return selected_ids
    
    def clear_selection(self):
        """清除所有选择"""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
