"""
分类选择器组件
用于批量移动对话框中选择目标分类
只允许选择叶子节点
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from qfluentwidgets import TreeWidget, setCustomStyleSheet
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode


class CategorySelectorTree(TreeWidget):
    """分类选择器树 - 只允许选择叶子节点"""
    
    category_selected = Signal(str)  # 发射选中的分类ID
    
    def __init__(self, category_manager: CategoryManager, parent=None):
        super().__init__(parent)
        self.category_manager = category_manager
        self.category_items = {}
        
        self._init_ui()
        self._connect_signals()
        self.load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setIndentation(20)
        self.setSelectionBehavior(QTreeWidget.SelectionBehavior.SelectRows)
        self.setFixedHeight(300)
        self._apply_style()
    
    def _apply_style(self):
        """应用样式"""
        from ....styles import get_font_style, get_text_primary, get_text_secondary, get_accent_color
        
        font_style = get_font_style(size="md", weight="normal")
        text_primary = get_text_primary()
        text_secondary = get_text_secondary()
        accent_color = get_accent_color()
        
        qss = f"""
            TreeWidget {{
                background: transparent;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 6px;
                outline: none;
                {font_style}
            }}
            TreeWidget::item {{
                color: {text_primary};
                height: 32px;
                padding-left: 8px;
                margin: 2px 4px;
                border-radius: 4px;
            }}
            TreeWidget::item:hover {{
                background: rgba(0, 0, 0, 0.05);
            }}
            TreeWidget::item:selected {{
                background: {accent_color};
                color: white;
            }}
            TreeWidget::item:disabled {{
                color: {text_secondary};
                background: transparent;
            }}
            TreeWidget::branch {{
                background: transparent;
                width: 20px;
            }}
        """
        setCustomStyleSheet(self, qss, qss)
        self.setUniformRowHeights(True)
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
    
    def load_categories(self):
        """加载分类树"""
        self.clear()
        self.category_items.clear()
        
        root_categories = self.category_manager.get_category_tree()
        
        # 递归构建分类树
        for category in sorted(root_categories, key=lambda x: x.order):
            self._add_category_item(category, None)
        
        # 展开所有节点
        self.expandAll()
    
    def _add_category_item(self, category: CategoryNode, parent_item: Optional[QTreeWidgetItem] = None):
        """添加分类项"""
        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self)
        
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        item.setText(0, category.name)
        self.category_items[category.id] = item
        
        # 检查是否为叶子节点
        all_categories = list(self.category_manager.categories.values())
        is_leaf = category.is_leaf(all_categories)
        
        if not is_leaf:
            # 非叶子节点：禁用选择，添加提示
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            item.setToolTip(0, "此分类包含子分类，请选择具体的子分类")
            # 使用灰色文本显示
            item.setForeground(0, self.palette().placeholderText())
        else:
            # 叶子节点：可选择
            item.setToolTip(0, "点击选择此分类")
        
        # 递归添加子分类
        children = self.category_manager.get_children(category.id)
        for child in sorted(children, key=lambda x: x.order):
            self._add_category_item(child, item)
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """树项被点击"""
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        if category_id:
            # 检查是否为叶子节点
            if self.category_manager.is_leaf(category_id):
                self.category_selected.emit(category_id)
            else:
                # 非叶子节点，取消选择
                self.clearSelection()
    
    def get_selected_category_id(self) -> Optional[str]:
        """获取当前选中的分类ID"""
        selected_items = self.selectedItems()
        if selected_items:
            category_id = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
            # 确保是叶子节点
            if self.category_manager.is_leaf(category_id):
                return category_id
        return None
    
    def select_category(self, category_id: str):
        """选中指定分类"""
        if category_id in self.category_items:
            item = self.category_items[category_id]
            # 只有叶子节点才能被选中
            if self.category_manager.is_leaf(category_id):
                self.setCurrentItem(item)
                self.scrollToItem(item)
