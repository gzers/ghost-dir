"""
通用分类树组件
显示分类树结构，支持展开/收缩工具栏
"""
from typing import Optional, List
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QLabel, QWidget
from qfluentwidgets import FluentIcon, RoundMenu, Action, setCustomStyleSheet, TreeWidget
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode
from src.gui.styles import get_font_style, get_text_primary, apply_transparent_style


class InternalCategoryTree(TreeWidget):
    """内部分类树 - 仅包含树逻辑"""
    
    category_selected = Signal(str)
    add_category_requested = Signal(str)
    edit_category_requested = Signal(str)
    delete_category_requested = Signal(str)
    
    def __init__(self, category_manager: CategoryManager, user_manager: Optional['UserManager'] = None, 
                 show_count: bool = False, count_provider: Optional[callable] = None, parent=None):
        super().__init__(parent)
        self.category_manager = category_manager
        self.user_manager = user_manager
        self.show_count = show_count
        self.count_provider = count_provider
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
        self.setIndentation(20)  # 设置缩进,为展开/收缩指示器留出空间
        self.setSelectionBehavior(QTreeWidget.SelectionBehavior.SelectRows)
        apply_transparent_style(self)
        self._apply_style()

    def _apply_style(self, theme_color: str = None):
        """应用统一样式 - 使用明暗分离的 QSS"""
        from src.gui.styles import get_font_family, get_font_size, get_font_weight
        
        font_family = get_font_family()
        font_size = get_font_size("md")
        font_weight = get_font_weight("normal")
        
        # 基础样式模板
        qss_base = f"""
            TreeWidget {{
                background: transparent;
                border: none;
                outline: none;
                font-family: {font_family};
                font-size: {font_size}px;
                font-weight: {font_weight};
            }}
            TreeWidget::item {{
                height: 36px;
                padding-left: 12px;
                margin: 0px;
                background: transparent;
                border: none;
            }}
            TreeWidget::branch {{
                background: transparent;
                width: 24px;
            }}
        """
        
        # 明亮主题样式
        light_qss = qss_base + """
            TreeWidget { color: #1F1F1F; }
            TreeWidget::item { color: #1F1F1F; }
            TreeWidget::item:hover, TreeWidget::item:selected { background: rgba(0, 0, 0, 0.05); }
            TreeWidget::item:selected { color: #1F1F1F; }
        """
        
        # 暗黑主题样式
        dark_qss = qss_base + """
            TreeWidget { color: #FFFFFF; }
            TreeWidget::item { color: #FFFFFF; }
            TreeWidget::item:hover, TreeWidget::item:selected { background: rgba(255, 255, 255, 0.08); }
            TreeWidget::item:selected { color: #FFFFFF; }
        """
        
        setCustomStyleSheet(self, light_qss, dark_qss)
        
        # 关键: 设置统一行高,避免展开/折叠时的布局抖动
        self.setUniformRowHeights(True)

    def _connect_signals(self):
        """连接内部和外部信号"""
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        
        from src.common.signals import signal_bus
        signal_bus.theme_color_changed.connect(self._apply_style)
        signal_bus.theme_changed.connect(self._apply_style)  # 修复主题切换 Bug
    
    def load_categories(self):
        """加载分类树"""
        self.clear()
        self.category_items.clear()
        
        root_categories = self.category_manager.get_category_tree()
        
        # 1. 手动添加"全部"根节点
        all_item = QTreeWidgetItem(self)
        all_item.setData(0, Qt.ItemDataRole.UserRole, "all")
        
        # 根据配置决定是否显示数量
        if self.show_count and self.count_provider:
            count = self.count_provider("all")
            all_item.setText(0, f"全部 ({count})")
        else:
            all_item.setText(0, "全部")
        
        self.category_items["all"] = all_item

        # 默认选中“全部”
        self.setCurrentItem(all_item)

        # 2. 递归构建现有分类树
        for category in sorted(root_categories, key=lambda x: x.order):
            self._add_category_item(category, None)
        
        # 展开所有节点
        self.expandAll()
    
    def _add_category_item(self, category, parent_item=None, depth=0):
        """添加分类项"""
        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self)
        
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        
        # 根据配置决定是否显示数量
        if self.show_count and self.count_provider:
            count = self.count_provider(category.id)
            item.setText(0, f"{category.name} ({count})")
        else:
            item.setText(0, category.name)
        
        self.category_items[category.id] = item
        
        # 为非叶子节点添加工具提示
        all_categories = list(self.category_manager.categories.values())
        is_leaf = category.is_leaf(all_categories)
        if not is_leaf:
            item.setToolTip(0, "此分类包含子分类。点击查看所有子分类下的项。")
        
        children = self.category_manager.get_children(category.id)
        for child in sorted(children, key=lambda x: x.order):
            self._add_category_item(child, item, depth + 1)
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """树项被点击"""
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        # 这里为了兼容性，如果 category_id 是 "all"，我们发送 None 或 "全部" 取决于外部逻辑
        # 但组件本身应该发送原始 ID
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
                
                from src.common.config import SYSTEM_CATEGORIES
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
        from src.gui.styles import get_text_primary, get_accent_color, get_text_secondary
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
        from src.gui.styles import get_text_primary
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
    
    def __init__(self, category_manager: CategoryManager, user_manager: Optional['UserManager'] = None, 
                 show_count: bool = False, count_provider: Optional[callable] = None, 
                 title: str = "分类", parent=None):
        super().__init__(parent)
        self.category_manager = category_manager
        self.user_manager = user_manager
        self.show_count = show_count
        self.count_provider = count_provider
        self.title_text = title
        
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """初始化 UI"""
        from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
        from qfluentwidgets import TransparentToolButton, StrongBodyLabel
        from src.gui.styles import get_text_secondary
        from src.gui.styles.constants.icons import ICON_SIZES
        from src.gui.styles.constants.components import COMPONENT_STYLES
        
        btn_size = COMPONENT_STYLES["button"]["height_sm"]
        icon_size = ICON_SIZES["sm"]

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)

        # 1. 顶部工具栏
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setContentsMargins(4, 0, 4, 0)
        self.toolbar_layout.setSpacing(2)

        self.title_label = StrongBodyLabel(self.title_text)
        self.title_label.setStyleSheet(f"color: {get_text_secondary()}; font-weight: bold;")
        self.toolbar_layout.addWidget(self.title_label)
        self.toolbar_layout.addStretch()

        # 展开按钮
        self.expand_btn = TransparentToolButton(FluentIcon.DOWN, self)
        self.expand_btn.setToolTip("展开全部")
        self.expand_btn.setFixedSize(btn_size, btn_size)
        self.expand_btn.setIconSize(QSize(icon_size, icon_size))
        self.toolbar_layout.addWidget(self.expand_btn)

        # 收起按钮
        self.collapse_btn = TransparentToolButton(FluentIcon.UP, self)
        self.collapse_btn.setToolTip("收起全部")
        self.collapse_btn.setFixedSize(btn_size, btn_size)
        self.collapse_btn.setIconSize(QSize(icon_size, icon_size))
        self.toolbar_layout.addWidget(self.collapse_btn)

        self.main_layout.addLayout(self.toolbar_layout)

        # 2. 内部树视图
        self.tree = InternalCategoryTree(
            self.category_manager, 
            self.user_manager, 
            show_count=self.show_count,
            count_provider=self.count_provider,
            parent=self
        )
        self.main_layout.addWidget(self.tree)

    def _connect_signals(self):
        """信号转发和处理"""
        self.expand_btn.clicked.connect(self.tree.expandAll)
        self.collapse_btn.clicked.connect(self.tree.collapseAll)
        
        self.tree.category_selected.connect(self.category_selected.emit)
        self.tree.add_category_requested.connect(self.add_category_requested.emit)
        self.tree.edit_category_requested.connect(self.edit_category_requested.emit)
        self.tree.delete_category_requested.connect(self.delete_category_requested.emit)

    def load_categories(self):
        self.tree.load_categories()

    def select_category(self, category_id: str):
        self.tree.select_category(category_id)

    def highlight_categories(self, category_ids: List[str]):
        self.tree.highlight_categories(category_ids)

    def clear_highlights(self):
        self.tree.clear_highlights()

    def expandAll(self):
        self.tree.expandAll()

    def collapseAll(self):
        self.tree.collapseAll()
