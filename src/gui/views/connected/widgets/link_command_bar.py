"""
连接命令栏组件
顶部命令栏，包含操作按钮、搜索框和视图切换器
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Signal
from qfluentwidgets import (
    PushButton, ToolButton, SearchLineEdit, Pivot,
    FluentIcon
)
from src.gui.i18n import t


class LinkCommandBar(QWidget):
    """连接命令栏"""
    
    # 信号
    add_link_clicked = Signal()        # 新建链接
    search_changed = Signal(str)       # 搜索文本改变
    view_changed = Signal(int)         # 视图切换 (0=列表, 1=分类)
    refresh_clicked = Signal()         # 刷新
    
    def __init__(self, parent=None):
        """初始化命令栏"""
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """设置 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)
        
        # 左侧：操作按钮
        self.add_btn = PushButton(FluentIcon.ADD, t("connected.add_link"))
        
        layout.addWidget(self.add_btn)
        
        layout.addStretch()
        
        # 中间：搜索框
        self.search_box = SearchLineEdit()
        self.search_box.setPlaceholderText(t("connected.search_placeholder"))
        self.search_box.setFixedWidth(300)
        layout.addWidget(self.search_box)
        
        layout.addStretch()
        
        # 右侧：视图切换器
        self.view_pivot = Pivot()
        self.view_pivot.addItem(
            routeKey='list',
            text=t("connected.view_list"),
            onClick=lambda: self.view_changed.emit(0)
        )
        self.view_pivot.addItem(
            routeKey='category',
            text=t("connected.view_category"),
            onClick=lambda: self.view_changed.emit(1)
        )
        self.view_pivot.setCurrentItem('category')  # 默认分类视图
        
        layout.addWidget(self.view_pivot)
        
        # 刷新按钮
        self.refresh_btn = ToolButton(FluentIcon.SYNC)
        self.refresh_btn.setToolTip(t("common.refresh"))
        layout.addWidget(self.refresh_btn)
    
    def _connect_signals(self):
        """连接信号"""
        self.add_btn.clicked.connect(self.add_link_clicked)
        self.search_box.textChanged.connect(self.search_changed)
        self.refresh_btn.clicked.connect(self.refresh_clicked)
    

    
    def get_search_text(self) -> str:
        """获取搜索文本"""
        return self.search_box.text()
    
    def clear_search(self):
        """清空搜索框"""
        self.search_box.clear()
    
    def set_current_view(self, index: int):
        """
        设置当前视图
        
        Args:
            index: 0=列表, 1=分类
        """
        if index == 0:
            self.view_pivot.setCurrentItem('list')
        else:
            self.view_pivot.setCurrentItem('category')
