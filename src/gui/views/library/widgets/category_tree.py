"""
分类树组件
显示分类树结构
"""
from typing import Optional, List
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QLabel, QWidget
from PySide6.QtGui import QAction
from qfluentwidgets import FluentIcon, RoundMenu, Action, setCustomStyleSheet, TreeWidget
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode
from ....styles import get_font_style, get_text_primary, apply_transparent_style


class InternalCategoryTree(TreeWidget):
    """内部分类树 - 仅包含树逻辑"""
    
    category_selected = Signal(str)
    add_category_requested = Signal(str)
    edit_category_requested = Signal(str)
    delete_category_requested = Signal(str)
    
    def __init__(self, category_manager: CategoryManager, user_manager: Optional['UserManager'] = None, parent=None):
        super().__init__(parent)
        self.category_manager = category_manager
        self.user_manager = user_manager
        self.category_items = {}
        
        self._init_ui()
        self._connect_signals()
        self.load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setAnimated(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setIndentation(0)
        self.setSelectionBehavior(QTreeWidget.SelectionBehavior.SelectRows)
        apply_transparent_style(self)
        self._apply_style()

    def _apply_style(self, theme_color: str = None):
        """应用统一样式"""
        from ....styles import get_accent_color, get_font_style, get_text_primary
        
        accent_color = theme_color
        if not accent_color and self.user_manager:
            accent_color = self.user_manager.get_theme_color()
        
        if not accent_color or accent_color == "system":
            accent_color = get_accent_color()
            
        font_style = get_font_style(size="md", weight="normal")
        text_primary = get_text_primary()
        
        qss = f"""
            TreeWidget {{
                background: transparent;
                border: none;
                outline: none;
                {font_style}
            }}
            TreeWidget::item {{
                color: {text_primary};
                height: 36px;
                padding: 0px;
                margin: 0px;
            }}
            TreeWidget::branch {{
                background: transparent;
            }}
        """
        setCustomStyleSheet(self, qss, qss)
        
        # 关键: 设置统一行高,避免展开/折叠时的布局抖动
        self.setUniformRowHeights(True)

    def _connect_signals(self):
        """连接内部和外部信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        
        from .....common.signals import signal_bus
        signal_bus.theme_color_changed.connect(self._apply_style)
    
    def load_categories(self):
        """加载分类树"""
        self.clear()
        self.category_items.clear()
        
        root_categories = self.category_manager.get_category_tree()
        
        # 1. 手动添加“全部”根节点
        all_item = QTreeWidgetItem(self)
        all_item.setData(0, Qt.ItemDataRole.UserRole, "all")
        self.category_items["all"] = all_item
        
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
        from ....styles.constants.icons import ICON_SIZES
        
        icon_size = ICON_SIZES["sm"]
        
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 0, 0, 0)  # 左边距为强调条留出空间
        layout.setSpacing(8)
        
        icon_label = QLabel()
        icon_label.setPixmap(FluentIcon.APPLICATION.icon().pixmap(icon_size, icon_size))
        layout.addWidget(icon_label)
        
        text_label = QLabel("全部")
        text_label.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(text_label)
        layout.addStretch()
        
        container.setFixedHeight(36)  # 设置固定高度,与树项高度一致
        container.setStyleSheet("background: transparent; border: none;")
        container.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setItemWidget(all_item, 0, container)
        
        # 默认选中“全部”
        self.setCurrentItem(all_item)

        # 2. 递归构建现有分类树
        for category in sorted(root_categories, key=lambda x: x.order):
            self._add_category_item(category, None)
        
        # 展开所有节点
        self.expandAll()
    
    def _add_category_item(self, category, parent_item=None, depth=0):
        """添加分类项"""
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
        
        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self)
        
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        self.category_items[category.id] = item
        
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 0, 0, 0)  # 左边距为强调条留出空间
        layout.setSpacing(8)
        
        if depth > 0:
            layout.addSpacing(depth * 24)
            
        from ....styles.constants.icons import ICON_SIZES
        icon_size = ICON_SIZES["sm"]
        
        icon_label = QLabel()
        
        # 根据是否为叶子节点选择图标
        all_categories = list(self.category_manager.categories.values())
        is_leaf = category.is_leaf(all_categories)
        
        try:
            # 优先使用自定义图标,如果没有则根据叶子状态选择默认图标
            if category.icon:
                icon_enum = getattr(FluentIcon, category.icon, None)
                if icon_enum:
                    icon_label.setPixmap(icon_enum.icon().pixmap(icon_size, icon_size))
                else:
                    # 自定义图标无效时使用默认图标
                    default_icon = FluentIcon.DOCUMENT if is_leaf else FluentIcon.FOLDER
                    icon_label.setPixmap(default_icon.icon().pixmap(icon_size, icon_size))
            else:
                # 没有自定义图标时根据叶子状态选择
                default_icon = FluentIcon.DOCUMENT if is_leaf else FluentIcon.FOLDER
                icon_label.setPixmap(default_icon.icon().pixmap(icon_size, icon_size))
        except Exception as e:
            # 异常情况下使用默认图标
            default_icon = FluentIcon.DOCUMENT if is_leaf else FluentIcon.FOLDER
            icon_label.setPixmap(default_icon.icon().pixmap(icon_size, icon_size))
        
        layout.addWidget(icon_label)
        
        # 创建文本标签
        text_label = QLabel(category.name)
        text_label.setStyleSheet("background: transparent; border: none;") 
        
        # 为非叶子节点添加工具提示
        if not is_leaf:
            text_label.setToolTip("此分类包含子分类,不能直接放置模板。点击查看所有子分类下的模板。")
        
        layout.addWidget(text_label)
        
        layout.addStretch()
        container.setFixedHeight(36)  # 设置固定高度,与树项高度一致
        container.setStyleSheet("background: transparent; border: none;")
        container.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) 
        self.setItemWidget(item, 0, container)
        
        children = self.category_manager.get_children(category.id)
        for child in sorted(children, key=lambda x: x.order):
            self._add_category_item(child, item, depth + 1)
    
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
            category_id = item.data(0, Qt.ItemDataRole.UserRole)
            category = self.category_manager.get_category_by_id(category_id)
            
            if category:
                add_child_action = Action(FluentIcon.ADD, '添加子分类')
                add_child_action.triggered.connect(lambda: self.add_category_requested.emit(category_id))
                menu.addAction(add_child_action)
                menu.addSeparator()
                edit_action = Action(FluentIcon.EDIT, '编辑')
                edit_action.triggered.connect(lambda: self.edit_category_requested.emit(category_id))
                menu.addAction(edit_action)
                
                from ....common.config import SYSTEM_CATEGORIES
                if category_id not in SYSTEM_CATEGORIES:
                    delete_action = Action(FluentIcon.DELETE, '删除')
                    delete_action.triggered.connect(lambda: self.delete_category_requested.emit(category_id))
                    menu.addAction(delete_action)
        else:
            add_root_action = Action(FluentIcon.ADD, '添加根分类')
            add_root_action.triggered.connect(lambda: self.add_category_requested.emit(None))
            menu.addAction(add_root_action)
        
        menu.exec(self.mapToGlobal(pos))
    
    def select_category(self, category_id: str):
        """选中指定分类"""
        if category_id in self.category_items:
            item = self.category_items[category_id]
            self.setCurrentItem(item)
            self.scrollToItem(item)

    def highlight_categories(self, category_ids: List[str]):
        """高亮并展开指定的分类"""
        from ....styles import get_text_primary, get_accent_color, get_text_secondary
        text_primary = get_text_primary()
        text_secondary = get_text_secondary()
        accent_color = get_accent_color()
        highlight_set = set(category_ids) if category_ids else set()

        for cid, item in self.category_items.items():
            widget = self.itemWidget(item, 0)
            if not widget:
                continue
            is_matched = cid in highlight_set
            for child in widget.findChildren(QLabel):
                if child.text() == "":
                    continue
                if is_matched:
                    child.setStyleSheet(f"background: transparent; border: none; font-weight: bold; color: {accent_color};")
                else:
                    color = text_secondary if category_ids else text_primary
                    child.setStyleSheet(f"background: transparent; border: none; font-weight: normal; color: {color};")
            if is_matched:
                parent = item.parent()
                while parent:
                    parent.setExpanded(True)
                    parent = parent.parent()
    
    def clear_highlights(self):
        """清除所有高亮样式"""
        from ....styles import get_text_primary
        text_primary = get_text_primary()
        for item in self.category_items.values():
            widget = self.itemWidget(item, 0)
            if widget:
                for child in widget.findChildren(QLabel):
                    if child.text() != "":
                        child.setStyleSheet(f"background: transparent; border: none; font-weight: normal; color: {text_primary};")


class CategoryTreeWidget(QWidget):
    """分类树容器组件 - 包含顶部控制按钮和树视图"""
    
    category_selected = Signal(str)
    add_category_requested = Signal(str)
    edit_category_requested = Signal(str)
    delete_category_requested = Signal(str)
    
    def __init__(self, category_manager: CategoryManager, user_manager: Optional['UserManager'] = None, parent=None):
        super().__init__(parent)
        self.category_manager = category_manager
        self.user_manager = user_manager
        
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """初始化 UI"""
        from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
        from qfluentwidgets import TransparentToolButton, StrongBodyLabel
        from ....styles import get_text_secondary
        
        from ....styles.constants.icons import ICON_SIZES
        from ....styles.constants.components import COMPONENT_STYLES
        
        btn_size = COMPONENT_STYLES["button"]["height_sm"] # 28
        icon_size = ICON_SIZES["sm"] # 16

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)

        # 1. 顶部工具栏
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setContentsMargins(4, 0, 4, 0)
        self.toolbar_layout.setSpacing(2)

        self.title_label = StrongBodyLabel("分类")
        self.title_label.setStyleSheet(f"color: {get_text_secondary()}; font-weight: bold;")
        self.toolbar_layout.addWidget(self.title_label)
        self.toolbar_layout.addStretch()

        # 展开按钮（对应展开全部）
        self.expand_btn = TransparentToolButton(FluentIcon.DOWN, self)
        self.expand_btn.setToolTip("展开全部")
        self.expand_btn.setFixedSize(btn_size, btn_size)
        self.expand_btn.setIconSize(QSize(icon_size, icon_size))
        self.toolbar_layout.addWidget(self.expand_btn)

        # 收起按钮（对应收起全部）
        self.collapse_btn = TransparentToolButton(FluentIcon.UP, self)
        self.collapse_btn.setToolTip("收起全部")
        self.collapse_btn.setFixedSize(btn_size, btn_size)
        self.collapse_btn.setIconSize(QSize(icon_size, icon_size))
        self.toolbar_layout.addWidget(self.collapse_btn)

        self.main_layout.addLayout(self.toolbar_layout)

        # 2. 内部树视图
        self.tree = InternalCategoryTree(self.category_manager, self.user_manager, self)
        self.main_layout.addWidget(self.tree)

    def _connect_signals(self):
        """信号转发和处理"""
        self.expand_btn.clicked.connect(self.tree.expandAll)
        self.collapse_btn.clicked.connect(self.tree.collapseAll)
        
        # 转发 InternalCategoryTree 的信号
        self.tree.category_selected.connect(self.category_selected.emit)
        self.tree.add_category_requested.connect(self.add_category_requested.emit)
        self.tree.edit_category_requested.connect(self.edit_category_requested.emit)
        self.tree.delete_category_requested.connect(self.delete_category_requested.emit)

    # 代理常用的 TreeWidget 方法到内部树
    def load_categories(self):
        self.tree.load_categories()

    def select_category(self, category_id: str):
        self.tree.select_category(category_id)

    def highlight_categories(self, category_ids: List[str]):
        self.tree.highlight_categories(category_ids)

    def clear_highlights(self):
        self.tree.clear_highlights()

    def get_selected_category_id(self) -> Optional[str]:
        return self.tree.get_selected_category_id()

    def expandAll(self):
        self.tree.expandAll()

    def collapseAll(self):
        self.tree.collapseAll()
