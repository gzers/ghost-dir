"""
分类选择器组件
支持层级展示和只选叶子分类
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLineEdit, QPushButton, QHBoxLayout, QFrame
)
from PySide6.QtGui import QCursor
from qfluentwidgets import LineEdit, TransparentToolButton, FluentIcon, setCustomStyleSheet, TreeWidget
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode


class CategoryTreeDropdown(QFrame):
    """分类树下拉框"""
    
    item_selected = Signal(str, str)  # category_id, category_name
    
    def __init__(self, category_manager: CategoryManager, parent=None):
        super().__init__(parent)
        self.category_manager = category_manager
        self.category_items = {}
        self.setObjectName("CategoryTreeDropdown")
        
        # 核心修复：移除 WA_TranslucentBackground，它在某些系统上会导致全透明
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self._init_ui()
        self.load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)
        
        # 树形视图 - 使用官方 TreeWidget
        self.tree = TreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setFixedHeight(300)
        self.tree.setFixedWidth(360)
        
        # 核心：设置统一行高，并遵循 selectRows 行为
        self.tree.setUniformRowHeights(True)
        
        layout.addWidget(self.tree)
        
        self._apply_style()
        
        # 连接信号
        self.tree.itemClicked.connect(self._on_item_clicked)
    
    def _apply_style(self):
        """应用样式"""
        from ..styles import get_font_style, get_text_primary, get_text_secondary, get_accent_color
        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QPalette
        
        font_style = get_font_style(size="md", weight="normal")
        text_primary = get_text_primary()
        
        palette = QApplication.palette()
        is_dark = palette.color(QPalette.ColorRole.Window).lightness() < 128
        
        if is_dark:
            bg_color = "rgba(45, 45, 45, 0.95)"
            border_color = "rgba(255, 255, 255, 0.1)"
        else:
            bg_color = "rgba(255, 255, 255, 0.95)"
            border_color = "rgba(0, 0, 0, 0.15)"
        
        # 注意：这里移除了对 ::item:selected 的自定义颜色设置，
        # 让 qfluentwidgets.TreeWidget 的原生 Delegate 来处理选中状态和强调条
        qss = f"""
            #CategoryTreeDropdown {{
                background: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
            TreeWidget {{
                background: transparent;
                border: none;
                outline: none;
                {font_style}
            }}
            TreeWidget::item {{
                color: {text_primary};
                height: 36px;
                padding-left: 12px;
                margin: 0px;
            }}
            TreeWidget::branch {{
                background: transparent;
                width: 24px;
            }}
        """
        setCustomStyleSheet(self.tree, qss, qss)
        self.setStyleSheet(f"#CategoryTreeDropdown {{ background: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; }}")
    
    def load_categories(self):
        """加载分类树"""
        self.tree.clear()
        self.category_items.clear()
        
        root_categories = self.category_manager.get_category_tree()
        
        for category in sorted(root_categories, key=lambda x: x.order):
            self._add_category_item(category, None)
        
        self.tree.expandAll()
    
    def _add_category_item(self, category: CategoryNode, parent_item: Optional[QTreeWidgetItem] = None):
        """添加分类项"""
        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self.tree)
        
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        item.setText(0, category.name)
        self.category_items[category.id] = item
        
        # 检查是否为叶子节点
        all_categories = list(self.category_manager.categories.values())
        is_leaf = category.is_leaf(all_categories)
        
        if not is_leaf:
            # 非叶子节点：禁用选择
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            item.setToolTip(0, "此分类包含子分类，请选择具体的子分类")
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
        if category_id and self.category_manager.is_leaf(category_id):
            category_name = item.text(0)
            self.item_selected.emit(category_id, category_name)
            self.hide()


class CategorySelector(QWidget):
    """分类选择器组件（带下拉树形视图）"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_manager = None
        self.dropdown = None
        self.selected_category_id = None
        self.selected_category_name = None
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 输入框（显示选中的分类）
        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText('选择分类')
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 核心交互修复：LineEdit 会消费 mousePressEvent，因此需要安装事件过滤器或重写
        self.lineEdit.installEventFilter(self)
        layout.addWidget(self.lineEdit)
    
    def eventFilter(self, obj, event):
        if obj == self.lineEdit and event.type() == QEvent.Type.MouseButtonPress:
            self._show_dropdown()
            return True
        return super().eventFilter(obj, event)

    def set_manager(self, category_manager: CategoryManager):
        """设置分类管理器"""
        self.category_manager = category_manager
        
        # 创建下拉框
        if self.dropdown:
            self.dropdown.deleteLater()
        
        self.dropdown = CategoryTreeDropdown(self.category_manager, self)
        self.dropdown.item_selected.connect(self._on_category_selected)
    
    def _show_dropdown(self):
        """显示下拉框"""
        if not self.dropdown:
            return
        
        # 定位下拉框
        pos = self.mapToGlobal(self.lineEdit.rect().bottomLeft())
        self.dropdown.move(pos)
        self.dropdown.show()
    
    def _on_category_selected(self, category_id: str, category_name: str):
        """分类被选中"""
        self.selected_category_id = category_id
        self.selected_category_name = category_name
        self.lineEdit.setText(category_name)
    
    def refresh(self):
        """刷新分类列表"""
        if self.dropdown:
            self.dropdown.load_categories()
    
    def set_value(self, category_id: str):
        """设置选中的分类 ID"""
        if not category_id or not self.category_manager:
            return
        
        category = self.category_manager.get_category_by_id(category_id)
        if category:
            self.selected_category_id = category_id
            self.selected_category_name = category.name
            self.lineEdit.setText(category.name)
    
    def get_value(self) -> Optional[str]:
        """获取当前选中的分类 ID"""
        return self.selected_category_id
    
    def currentData(self) -> Optional[str]:
        """兼容 ComboBox 接口"""
        return self.get_value()
    
    def setFixedWidth(self, width: int):
        """设置固定宽度"""
        # 设置整个组件的宽度
        super().setFixedWidth(width)
        self.lineEdit.setFixedWidth(width)

