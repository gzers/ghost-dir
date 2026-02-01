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
from qfluentwidgets import BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon
from src.data.model import UserLink, LinkStatus
from src.data.user_manager import UserManager
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

    def clear_selection(self):
        """清除选择"""
        self.clearSelection()

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
        
        cat_name = get_category_text(self.link.category)
        self.category_label = CaptionLabel(cat_name, self)
        
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
        
        # 状态徽章 (标准可视化组件)
        self.status_badge = StatusBadge(self.link.status, self)
        layout.addWidget(self.status_badge)
        
        # 操作按钮组
        self.setup_actions(layout)

    def setup_actions(self, layout):
        """根据状态设置操作按钮"""
        if self.link.status == LinkStatus.DISCONNECTED:
            btn = TransparentToolButton(FluentIcon.LINK, self)
            btn.setToolTip("建立连接")
            btn.clicked.connect(lambda: self.action_clicked.emit(self.link.id, "establish"))
            layout.addWidget(btn)
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
