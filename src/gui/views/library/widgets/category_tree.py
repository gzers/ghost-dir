"""
分类树组件
显示分类树结构
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu
from PySide6.QtGui import QAction
from qfluentwidgets import FluentIcon, RoundMenu, Action
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode


class CategoryTreeWidget(QTreeWidget):
    """分类树组件"""
    
    category_selected = Signal(str)  # 分类被选中时发出信号 (category_id)
    add_category_requested = Signal(str)  # 请求添加分类 (parent_id)
    edit_category_requested = Signal(str)  # 请求编辑分类 (category_id)
    delete_category_requested = Signal(str)  # 请求删除分类 (category_id)
    
    def __init__(self, category_manager: CategoryManager, parent=None):
        """
        初始化分类树组件
        
        Args:
            category_manager: 分类管理器
            parent: 父窗口
        """
        super().__init__(parent)
        self.category_manager = category_manager
        self.category_items = {}  # category_id -> QTreeWidgetItem
        
        self._init_ui()
        self._connect_signals()
        self.load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setAnimated(True)
        self.setIndentation(20)
    
    def _connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
    
    def load_categories(self):
        """加载分类树"""
        self.clear()
        self.category_items.clear()
        
        # 获取根分类
        root_categories = self.category_manager.get_category_tree()
        
        # 递归构建树
        for category in sorted(root_categories, key=lambda x: x.order):
            self._add_category_item(category, None)
        
        # 展开所有节点
        self.expandAll()
    
    def _add_category_item(self, category: CategoryNode, parent_item: Optional[QTreeWidgetItem]):
        """
        添加分类项
        
        Args:
            category: 分类对象
            parent_item: 父项（None 表示根节点）
        """
        # 创建树项
        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self)
        
        # 设置文本和图标
        item.setText(0, category.name)
        
        # 设置图标
        try:
            icon_enum = getattr(FluentIcon, category.icon, FluentIcon.FOLDER)
            item.setIcon(0, icon_enum.icon())
        except:
            item.setIcon(0, FluentIcon.FOLDER.icon())
        
        # 存储分类ID
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        
        # 保存到字典
        self.category_items[category.id] = item
        
        # 递归添加子分类
        children = self.category_manager.get_children(category.id)
        for child in sorted(children, key=lambda x: x.order):
            self._add_category_item(child, item)
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """树项被点击"""
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        if category_id:
            self.category_selected.emit(category_id)
    
    def _on_context_menu(self, pos):
        """显示右键菜单"""
        item = self.itemAt(pos)
        
        menu = RoundMenu(parent=self)
        
        if item:
            # 有选中项
            category_id = item.data(0, Qt.ItemDataRole.UserRole)
            category = self.category_manager.get_category_by_id(category_id)
            
            if category:
                # 添加子分类
                add_child_action = Action(FluentIcon.ADD, '添加子分类')
                add_child_action.triggered.connect(lambda: self.add_category_requested.emit(category_id))
                menu.addAction(add_child_action)
                
                menu.addSeparator()
                
                # 编辑
                edit_action = Action(FluentIcon.EDIT, '编辑')
                edit_action.triggered.connect(lambda: self.edit_category_requested.emit(category_id))
                menu.addAction(edit_action)
                
                # 删除（系统分类不可删除）
                from ....common.config import SYSTEM_CATEGORIES
                if category_id not in SYSTEM_CATEGORIES:
                    delete_action = Action(FluentIcon.DELETE, '删除')
                    delete_action.triggered.connect(lambda: self.delete_category_requested.emit(category_id))
                    menu.addAction(delete_action)
        else:
            # 无选中项，显示添加根分类
            add_root_action = Action(FluentIcon.ADD, '添加根分类')
            add_root_action.triggered.connect(lambda: self.add_category_requested.emit(None))
            menu.addAction(add_root_action)
        
        menu.exec(self.mapToGlobal(pos))
    
    def get_selected_category_id(self) -> Optional[str]:
        """获取当前选中的分类ID"""
        item = self.currentItem()
        if item:
            return item.data(0, Qt.ItemDataRole.UserRole)
        return None
    
    def select_category(self, category_id: str):
        """选中指定分类"""
        if category_id in self.category_items:
            item = self.category_items[category_id]
            self.setCurrentItem(item)
            self.scrollToItem(item)
