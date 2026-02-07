"""
列表视图组件 (View A)
极简风格显示全量连接，支持自定义 Delegate
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QStyledItemDelegate, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPainter, QIcon
from qfluentwidgets import BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon, IndeterminateProgressRing
from src.models import UserLink, LinkStatus  # 新架构
from src.common.managers import UserManager
from src.gui.i18n import t, get_category_text
from src.gui.components.status_badge import StatusBadge
from src.common.validators import PathValidator

class FlatLinkView(QListWidget):
    """智能列表视图 - 极简/宽屏模式"""

    link_selected = Signal(list)
    action_clicked = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_manager = UserManager()
        self.loading_ids = set() # 正在计算大小的 ID 集合
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        self.setObjectName("FlatLinkView")
        self.setSpacing(8)
        self.setViewportMargins(0, 0, 0, 0)
        self.setStyleSheet("""
            #FlatLinkView {
                background: transparent;
                border: none;
                outline: none;
            }
            #FlatLinkView::item {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin-bottom: 4px;
            }
            #FlatLinkView::item:selected {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid palette(highlight);
            }
        """)

        # 连接选择变化信号
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def load_links(self, links: list):
        """加载连接列表"""
        self.clear()
        for link in links:
            item = QListWidgetItem(self)
            item.setSizeHint(QSize(0, 72))  # 固定行高 72px
            self.addItem(item)

            # 创建自定义小部件
            widget = LinkItemWidget(link, self)
            widget.action_clicked.connect(self.action_clicked.emit)
            self.setItemWidget(item, widget)
            
            # 恢复加载状态
            if link.id in self.loading_ids:
                widget.set_size_loading(True)

    def set_all_sizes_loading(self):
        """全量设置空间大小加载状态"""
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if isinstance(widget, LinkItemWidget):
                self.loading_ids.add(widget.link.id) # 这里 loading_ids 语义保持计算大小
                widget.set_size_loading(True)

    def set_all_status_loading(self):
        """全量设置状态探测加载状态"""
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if isinstance(widget, LinkItemWidget):
                widget.set_status_loading(True)

    def update_row_status(self, link_id: str, status: LinkStatus):
        """同步更新探测状态"""
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if isinstance(widget, LinkItemWidget) and widget.link.id == link_id:
                widget.update_status(status)
                break

    def update_row_size(self, link_id: str, size_text: str):
        """更新单行大小"""
        if link_id in self.loading_ids:
            self.loading_ids.remove(link_id)
        
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if isinstance(widget, LinkItemWidget) and widget.link.id == link_id:
                widget.set_size_loading(False)
                # 刷新路径标签处的占用提示
                widget.update_size_info(size_text)
                break

    def clear_selection(self):
        """清除选择"""
        self.clearSelection()

    def _on_selection_changed(self):
        """处理选择变化并发出业务信号"""
        selected_ids = []
        for item in self.selectedItems():
            widget = self.itemWidget(item)
            if isinstance(widget, LinkItemWidget):
                selected_ids.append(widget.link.id)
        self.link_selected.emit(selected_ids)

    def get_selected_links(self) -> list:
        """获取当前选中的连接 ID 列表"""
        selected_ids = []
        for item in self.selectedItems():
            widget = self.itemWidget(item)
            if isinstance(widget, LinkItemWidget):
                selected_ids.append(widget.link.id)
        return selected_ids

class LinkItemWidget(QWidget):
    """列表项小部件"""
    action_clicked = Signal(str, str)

    def __init__(self, link: UserLink, parent=None):
        super().__init__(parent)
        self.link = link
        # 实时标准化路径显示
        self.display_path = PathValidator().normalize(self.link.target_path)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        # 图标
        icon_btn = TransparentToolButton(FluentIcon.APPLICATION, self)
        icon_btn.setIconSize(QSize(32, 32))
        layout.addWidget(icon_btn)

        # 信息区
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        # 第一行：名称 + 分类
        title_layout = QHBoxLayout()
        self.name_label = BodyLabel(self.link.name, self)

        # 优先使用全路径名称 (尝试引用 ViewModel 的 category_path 或 DataModel 的 category_path_name)
        full_path = getattr(self.link, 'category_path', "") or getattr(self.link, 'category_path_name', "")
        cat_name = full_path or get_category_text(self.link.category)
        self.category_label = CaptionLabel(cat_name, self)

        # 设置分类全路径 Tooltip
        if full_path:
            self.category_label.setToolTip(full_path)
        else:
            self.category_label.setToolTip(get_category_text(self.link.category))

        # 使用 QGraphicsOpacityEffect 实现透明度
        op = QGraphicsOpacityEffect(self.category_label)
        op.setOpacity(0.7)
        self.category_label.setGraphicsEffect(op)

        title_layout.addWidget(self.name_label)
        title_layout.addSpacing(4)
        title_layout.addWidget(self.category_label)
        title_layout.addStretch()

        # 第二行：路径
        self.path_label = CaptionLabel(self.display_path, self)
        self.path_label.setToolTip(self.display_path)

        path_op = QGraphicsOpacityEffect(self.path_label)
        path_op.setOpacity(0.6)
        self.path_label.setGraphicsEffect(path_op)

        info_layout.addLayout(title_layout)
        info_layout.addWidget(self.path_label)
        layout.addLayout(info_layout)

        layout.addStretch(1)

        # 🆕 空间占用显示区 (调整至状态左侧)
        self.size_container = QWidget(self)
        size_layout = QHBoxLayout(self.size_container)
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(4)

        self.size_label = CaptionLabel("", self.size_container)
        self.size_label.setStyleSheet("color: palette(highlight); font-weight: bold;")
        
        self.size_loading_ring = IndeterminateProgressRing(self.size_container)
        self.size_loading_ring.setFixedSize(14, 14)
        self.size_loading_ring.setStrokeWidth(2)
        
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_loading_ring)
        layout.addWidget(self.size_container)

        self.size_label.setVisible(False)
        self.size_loading_ring.setVisible(False)
        self.size_container.setVisible(False)

        # 状态徽章 (标准可视化组件)
        self.status_badge = StatusBadge(self.link.status, self)
        layout.addWidget(self.status_badge)

        # 🆕 状态加载环 (放在徽章位置)
        self.status_loading_ring = IndeterminateProgressRing(self)
        self.status_loading_ring.setFixedSize(16, 16)
        self.status_loading_ring.setStrokeWidth(2)
        self.status_loading_ring.setVisible(False)
        layout.addWidget(self.status_loading_ring)

        # 操作按钮组
        self.setup_actions(layout)

        # 🆕 [核心修复] 初始化时自动回填已有的空间数据
        if self.link.last_known_size > 0:
            from src.common.config import format_size
            self.update_size_info(format_size(self.link.last_known_size))

    def set_size_loading(self, is_loading: bool):
        """切换空间计算加载状态"""
        self.size_container.setVisible(True)
        self.size_loading_ring.setVisible(is_loading)
        if is_loading:
            self.size_label.setVisible(False)
        else:
            # 只有在非加载状态下且没有数值时才隐藏容器
            if not self.size_label.text():
                self.size_container.setVisible(False)

    def set_status_loading(self, is_loading: bool):
        """切换状态探测加载状态"""
        self.status_loading_ring.setVisible(is_loading)
        if is_loading:
            self.status_badge.setVisible(False)
        else:
            self.status_badge.setVisible(True)

    def update_status(self, status: LinkStatus):
        """更新并显示状态"""
        self.status_loading_ring.setVisible(False)
        self.status_badge.update_status(status)
        self.status_badge.setVisible(True)

    def update_size_info(self, size_text: str):
        """[核心修复] 原子化更新空间信息：先清理圆圈，再显现文字"""
        # 1. 强制隐匿加载圆圈
        self.size_loading_ring.setVisible(False)
        # 2. 设置新文案
        self.size_label.setText(size_text)
        # 3. 驱动容器与标签显现
        self.size_label.setVisible(True)
        self.size_container.setVisible(True)

    def setup_actions(self, layout):
        """根据状态设置操作按钮"""
        # 建立连接：适用于“未连接”、“就绪”、“失效/异常”状态
        if self.link.status in [LinkStatus.DISCONNECTED, LinkStatus.READY, LinkStatus.INVALID]:
            btn = TransparentToolButton(FluentIcon.PLAY_SOLID, self)
            btn.setToolTip("建立连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(self.link.id, "establish"))
            layout.addWidget(btn)

        # 断开连接：仅适用于“已连接”状态
        elif self.link.status == LinkStatus.CONNECTED:
            btn = TransparentToolButton(FluentIcon.CLOSE, self)
            btn.setToolTip("断开连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(self.link.id, "disconnect"))
            layout.addWidget(btn)

        # 编辑按钮
        edit_btn = TransparentToolButton(FluentIcon.EDIT, self)
        edit_btn.setToolTip("编辑记录")
        edit_btn.clicked.connect(lambda: self.action_clicked.emit(self.link.id, "edit"))
        layout.addWidget(edit_btn)

        # 更多/删除按钮
        del_btn = TransparentToolButton(FluentIcon.DELETE, self)
        del_btn.setToolTip("移除记录")
        del_btn.clicked.connect(lambda: self.action_clicked.emit(self.link.id, "delete"))
        layout.addWidget(del_btn)
