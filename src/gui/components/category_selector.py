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
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode
from src.gui.i18n import t, get_category_text


class CategoryTreeDropdown(QFrame):
    """分类树下拉框"""
    
    item_selected = Signal(object, str)  # category_id, category_name (id 可能是 None 表示根)
    
    def __init__(
        self, 
        category_manager: CategoryManager, 
        only_leaf: bool = True,
        root_visible: bool = False,
        exclude_ids: Optional[list] = None,
        parent=None
    ):
        super().__init__(parent)
        self.category_manager = category_manager
        self.only_leaf = only_leaf
        self.root_visible = root_visible
        self.exclude_ids = exclude_ids or []
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
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)
        
        # 树形视图 - 使用官方 TreeWidget
        self.tree = TreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setFixedHeight(300)
        # 移除硬编码宽度，由 _show_dropdown 动态控制
        
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
        
        # 修复：在 f-string 中，CSS 的大括号必须写成双大括号 {{ }}
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
                margin: 0px;
                padding: 0px;
                {font_style}
            }}
            TreeWidget::item {{
                color: {text_primary};
                height: 36px;
                padding-left: 12px;
                margin: 0px;
                border: none;
            }}
            TreeWidget::branch {{
                background: transparent;
                width: 24px;
            }}
        """
        # 对内部树和外壳都应用样式
        setCustomStyleSheet(self.tree, qss, qss)
        self.setStyleSheet(qss)
    
    def load_categories(self):
        """加载分类树"""
        self.tree.clear()
        self.category_items.clear()
        
        # 如果需要显示根分类
        if self.root_visible:
            from ..styles import get_text_secondary
            root_item = QTreeWidgetItem(self.tree)
            root_item.setData(0, Qt.ItemDataRole.UserRole, None)
            from ...gui.i18n import t
            root_name = t("library.label_root_category")
            # 如果翻译缺失，回退到默认文案
            if "[Missing:" in root_name:
                root_name = "无 (根分类)"
            root_item.setText(0, root_name)
            # 强调条装饰
            root_item.setForeground(0, self.palette().link())
            root_item.setToolTip(0, "点击选择此项作为根分类")
        
        root_categories = self.category_manager.get_category_tree()
        
        for category in sorted(root_categories, key=lambda x: x.order):
            self._add_category_item(category, None)
        
        self.tree.expandAll()
    
    def _add_category_item(self, category: CategoryNode, parent_item: Optional[QTreeWidgetItem] = None):
        """添加分类项"""
        # 递归检查排除列表（如果分类本身或其祖先在排除列表中，则不显示）
        if category.id in self.exclude_ids:
            return

        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self.tree)
        
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        
        # 核心修复：使用公共获取函数，兼顾配置名称与多语言
        display_name = get_category_text(category.id)
        item.setText(0, display_name)
        
        self.category_items[category.id] = item
        
        # 检查是否可选择
        all_categories = list(self.category_manager.categories.values())
        is_leaf = category.is_leaf(all_categories)
        
        if self.only_leaf:
            if not is_leaf:
                # 仅叶子模式：非叶子节点不可选
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                item.setToolTip(0, "此分类包含子分类，请选择具体的子分类")
                item.setForeground(0, self.palette().placeholderText())
            else:
                item.setToolTip(0, "点击选择此分类")
        else:
            # 全节点模式：所有节点皆可选
            item.setToolTip(0, f"点击选择 '{category.name}'")
        
        # 递归添加子分类
        children = self.category_manager.get_children(category.id)
        for child in sorted(children, key=lambda x: x.order):
            self._add_category_item(child, item)
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """树项被点击"""
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        
        # 判定是否可选
        selectable = True
        if self.only_leaf and category_id is not None:
            selectable = self.category_manager.is_leaf(category_id)
        
        if selectable:
            display_name = get_category_text(category_id)
            self.item_selected.emit(category_id, display_name)
            self.hide()


class CategorySelector(QWidget):
    """分类选择器组件（带下拉树形视图）"""
    
    def __init__(self, parent=None, only_leaf: bool = True, root_visible: bool = False):
        super().__init__(parent)
        self.category_manager = None
        self.dropdown = None
        self.only_leaf = only_leaf
        self.root_visible = root_visible
        self.exclude_ids = []
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

    def set_manager(self, category_manager: CategoryManager, exclude_ids: Optional[list] = None):
        """设置分类管理器"""
        self.category_manager = category_manager
        self.exclude_ids = exclude_ids or []
        
        # 创建下拉框
        if self.dropdown:
            self.dropdown.deleteLater()
        
        self.dropdown = CategoryTreeDropdown(
            self.category_manager, 
            only_leaf=self.only_leaf,
            root_visible=self.root_visible,
            exclude_ids=self.exclude_ids,
            parent=self
        )
        self.dropdown.item_selected.connect(self._on_category_selected)
    
    def _show_dropdown(self):
        """显示下拉框"""
        if not self.dropdown:
            return
        
        # 1. 同步宽度：下拉框总宽度与当前组件一致
        self.dropdown.setFixedWidth(self.width())
        # 同步内部树视图宽度 (减去布局边距左右各1, 共2)
        self.dropdown.tree.setFixedWidth(self.width() - 2)
        
        # 2. 定位并增加间距
        # 标准 Fluent 下拉间距通常为 4px
        pos = self.mapToGlobal(self.rect().bottomLeft())
        pos.setY(pos.y() + 4) 
        
        self.dropdown.move(pos)
        self.dropdown.show()
        self.dropdown.tree.setFocus()
    
    def _on_category_selected(self, category_id: str, category_name: str):
        """分类被选中"""
        self.selected_category_id = category_id
        self.selected_category_name = category_name
        self.lineEdit.setText(category_name)
    
    def refresh(self):
        """刷新分类列表"""
        if self.dropdown:
            self.dropdown.load_categories()
    
    def set_value(self, category_id: Optional[str]):
        """设置选中的分类 ID"""
        if category_id is None:
            if self.root_visible:
                from ...gui.i18n import t
                root_name = t("library.label_root_category")
                if "[Missing:" in root_name:
                    root_name = "无 (根分类)"
                self.selected_category_id = None
                self.selected_category_name = root_name
                self.lineEdit.setText(root_name)
            return

        if not self.category_manager:
            return
        
        category = self.category_manager.get_category_by_id(category_id)
        if category:
            display_name = get_category_text(category_id)
            self.selected_category_id = category_id
            self.selected_category_name = display_name
            self.lineEdit.setText(display_name)
    
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

