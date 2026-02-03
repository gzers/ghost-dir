from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import TreeWidget
from src.data.user_manager import UserManager
from src.data.category_manager import CategoryManager


class CategoryTree(TreeWidget):
    """分类树组件"""
    
    # 信号
    category_selected = Signal(str)  # 分类被选中，发送分类 ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_manager = UserManager()
        self.category_manager = CategoryManager()
        self._init_ui()
        self._connect_signals()
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
    
    def _on_item_clicked(self, item, column):
        """树节点被点击"""
        # 提取分类 ID (UserRole)
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        if category_id:
            self.category_selected.emit(category_id)
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setMaximumWidth(250)
        # 设置背景色和移除边框
        self._update_theme_style()
        from src.common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _update_theme_style(self):
        """更新主题样式"""
        from src.gui.styles.utils import color_utils
        text_color = color_utils.get_text_primary()
        selected_bg = color_utils.get_item_selected_background()
        
        self.setStyleSheet(f"""
            CategoryTree {{
                background: transparent;
                border: none;
                outline: none;
                padding: 12px 0;
                color: {text_color};
            }}
            QTreeWidget::item {{
                padding: 8px 12px;
                background: transparent;
                border-radius: 4px;
                margin: 2px 8px;
            }}
            QTreeWidget::item:hover {{
                background: {selected_bg};
            }}
            QTreeWidget::item:selected {{
                background: {selected_bg};
                color: {text_color};
            }}
        """)

    def _on_theme_changed(self, theme):
        """主题变更"""
        self._update_theme_style()
    
    def load_categories(self):
        """加载分类列表"""
        self.clear()
        
        # 1. 添加"全部"节点
        total_count = len(self.user_manager.get_all_links())
        all_item = QTreeWidgetItem([f"全部 ({total_count})"])
        all_item.setData(0, Qt.ItemDataRole.UserRole, "all")
        self.addTopLevelItem(all_item)
        
        # 2. 递归加载分类树
        root_nodes = self.category_manager.get_category_tree()
        for node in root_nodes:
            self._add_category_item(node, None)
            
    def _add_category_item(self, node, parent_item):
        """递归添加分类项"""
        count = len(self.user_manager.get_links_by_category(node.id))
        item = QTreeWidgetItem([f"{node.name} ({count})"])
        item.setData(0, Qt.ItemDataRole.UserRole, node.id)
        
        if parent_item:
            parent_item.addChild(item)
        else:
            self.addTopLevelItem(item)
            
        # 递归处理子分类
        children = self.category_manager.get_children(node.id)
        for child in children:
            self._add_category_item(child, item)
