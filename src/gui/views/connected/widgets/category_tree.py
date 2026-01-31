"""
分类树组件
左侧分类导航树
"""
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Signal
from qfluentwidgets import TreeWidget
from .....data.user_manager import UserManager


class CategoryTree(TreeWidget):
    """分类树组件"""
    
    # 信号
    category_selected = Signal(str)  # 分类被选中，发送分类名称
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_manager = UserManager()
        self._init_ui()
        self._connect_signals()
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
    
    def _on_item_clicked(self, item, column):
        """树节点被点击"""
        # 提取分类名称（去掉计数部分）
        text = item.text(0)
        if " (" in text:
            category_name = text.split(" (")[0]
        else:
            category_name = text
        
        self.category_selected.emit(category_name)
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setMaximumWidth(250)
        # 设置背景色和移除边框
        self._update_theme_style()
        from .....common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _update_theme_style(self):
        """更新主题样式"""
        self.setStyleSheet("""
            CategoryTree {
                background: transparent;
                border: none;
                outline: none;
                padding: 12px 0;
            }
            QTreeWidget::item {
                padding: 8px 12px;
                background: transparent;
            }
        """)

    def _on_theme_changed(self, theme):
        """主题变更"""
        self._update_theme_style()
    
    def load_categories(self):
        """加载分类列表"""
        self.clear()
        
        # 添加"全部"节点
        all_item = QTreeWidgetItem(["全部"])
        self.addTopLevelItem(all_item)
        
        # 添加分类节点
        categories = self.user_manager.get_all_categories()
        for category in categories:
            count = len(self.user_manager.get_links_by_category(category.name))
            item = QTreeWidgetItem([f"{category.name} ({count})"])
            self.addTopLevelItem(item)
