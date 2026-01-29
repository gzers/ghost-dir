"""
分类树组件
显示分类树结构
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QLabel
from PySide6.QtGui import QAction
from qfluentwidgets import FluentIcon, RoundMenu, Action, setCustomStyleSheet, TreeWidget
from src.data.category_manager import CategoryManager
from src.data.model import CategoryNode
from ....styles import get_font_style, get_text_primary, apply_transparent_style


class CategoryTreeWidget(TreeWidget):
    """分类树组件 - 使用 QFluentWidgets 官方 TreeWidget"""
    
    category_selected = Signal(str)  # 分类被选中时发出信号 (category_id)
    add_category_requested = Signal(str)  # 请求添加分类 (parent_id)
    edit_category_requested = Signal(str)  # 请求编辑分类 (category_id)
    delete_category_requested = Signal(str)  # 请求删除分类 (category_id)
    
    def __init__(self, category_manager: CategoryManager, user_manager: Optional['UserManager'] = None, parent=None):
        """
        初始化分类树组件
        
        Args:
            category_manager: 分类管理器
            user_manager: 用户数据管理器
            parent: 父窗口
        """
        super().__init__(parent)
        self.category_manager = category_manager
        self.user_manager = user_manager
        self.category_items = {}  # category_id -> QTreeWidgetItem
        
        self._init_ui()
        self._connect_signals()
        self.load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setAnimated(True)
        
        # 禁用原生的水平滚动条，防止边缘空隙
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 核心：必须禁用 Indentation，否则 branch 伪元素会导致多个指示条
        self.setIndentation(0)
        self.setSelectionBehavior(QTreeWidget.SelectionBehavior.SelectRows)
        
        # 应用透明背景
        apply_transparent_style(self)
        
        # 初始化样式
        self._apply_style()

    def _apply_style(self, theme_color: str = None):
        """
        应用统一样式
        
        Args:
            theme_color: 可选的主题色（Hex），如果不传则从 user_manager 或系统获取
        """
        from .....common.signals import signal_bus
        from ....styles import get_accent_color, get_font_style, get_text_primary
        
        # 获取颜色优先级：传参 > user_manager 配置 > 系统默认 (ACCENT_COLOR)
        accent_color = theme_color
        if not accent_color and self.user_manager:
            accent_color = self.user_manager.get_theme_color()
        
        # 如果是 "system"，回退到 get_accent_color() (内部处理了系统色)
        if not accent_color or accent_color == "system":
            accent_color = get_accent_color()
            
        font_style = get_font_style(size="md", weight="normal")
        text_primary = get_text_primary()
        
        # 使用 QFluentWidgets 官方默认样式，仅设置基础样式
        qss = f"""
            TreeWidget {{
                background: transparent;
                border: none;
                outline: none;
                {font_style}
            }}
            TreeWidget::item {{
                color: {text_primary};
            }}
        """
        setCustomStyleSheet(self, qss, qss)

    def _connect_signals(self):
        """连接内部和外部信号"""
        # 点击信号
        self.itemClicked.connect(self._on_item_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        
        # 监听全局主题色变更
        from .....common.signals import signal_bus
        signal_bus.theme_color_changed.connect(self._apply_style)
    
    def load_categories(self):
        """加载分类树"""
        self.clear()
        self.category_items.clear()
        
        # 获取根分类
        root_categories = self.category_manager.get_category_tree()
        
        # 1. 手动添加“全部”根节点
        all_item = QTreeWidgetItem(self)
        all_item.setData(0, Qt.ItemDataRole.UserRole, "all")
        self.category_items["all"] = all_item
        
        # 为“全部”节点创建 Widget
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        icon_label = QLabel()
        icon_label.setPixmap(FluentIcon.APPLICATION.icon().pixmap(16, 16))
        layout.addWidget(icon_label)
        
        text_label = QLabel("全部")
        text_label.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(text_label)
        layout.addStretch()
        
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
        """
        添加分类项
        
        Args:
            category: 分类对象
            parent_item: 父项（None 表示根节点）
            depth: 层级深度
        """
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
        
        # 创建项
        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self)
        
        # 存储分类ID
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        self.category_items[category.id] = item
        
        # --- 核心修复：使用 setItemWidget 配合 Spacer 手动实现物理层级感 ---
        # 这种方式不会触发 QTreeWidget 的 branch 渲染，从而保证只有最左侧一条指示条。
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 1. 缩进 Spacer
        if depth > 0:
            layout.addSpacing(depth * 24)
            
        # 2. 图标
        icon_label = QLabel()
        try:
            icon_enum = getattr(FluentIcon, category.icon, FluentIcon.FOLDER)
            icon_label.setPixmap(icon_enum.icon().pixmap(16, 16))
        except:
            icon_label.setPixmap(FluentIcon.FOLDER.icon().pixmap(16, 16))
        layout.addWidget(icon_label)
        
        # 3. 文本
        text_label = QLabel(category.name)
        text_label.setStyleSheet("background: transparent; border: none;") # 确保继承外层颜色
        layout.addWidget(text_label)
        
        layout.addStretch()
        
        # 关键：我们需要让 item 知道它有一个 Widget，同时 QSS 依然能控制背景
        # 为了让点击事件和悬停背景正常工作，我们将 container 设为透明
        container.setStyleSheet("background: transparent; border: none;")
        container.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # 让点击穿透到 item
        
        self.setItemWidget(item, 0, container)
        
        # 递归添加子分类
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
    
    def highlight_categories(self, category_ids: List[str]):
        """
        高亮并展开指定的分类
        
        Args:
            category_ids: 需要高亮的分类ID列表
        """
        from ....styles import get_text_primary, get_accent_color, get_text_secondary

        # 1. 重置所有项的样式（使用次级文字颜色，让未匹配项变暗但仍可见）
        text_primary = get_text_primary()
        text_secondary = get_text_secondary()
        accent_color = get_accent_color()

        for item in self.category_items.values():
            widget = self.itemWidget(item, 0)
            if widget:
                for child in widget.findChildren(QLabel):
                    if child.text() != "":
                        child.setStyleSheet(f"background: transparent; border: none; font-weight: normal; color: {text_secondary};")

        if not category_ids:
            # 如果没有搜索结果，恢复到主文字颜色
            self.clear_highlights()
            return

        # 2. 高亮指定的分类并展开父级
        for cid in category_ids:
            if cid in self.category_items:
                item = self.category_items[cid]
                
                # 高亮文本（使用主题强调色和加粗）
                widget = self.itemWidget(item, 0)
                if widget:
                    for child in widget.findChildren(QLabel):
                        if child.text() != "":
                            child.setStyleSheet(f"background: transparent; border: none; font-weight: bold; color: {accent_color};")
                
                # 展开父级
                parent = item.parent()
                while parent:
                    parent.setExpanded(True)
                    parent = parent.parent()
    
    def clear_highlights(self):
        """清除所有高亮样式，恢复到主文字颜色"""
        from ....styles import get_text_primary
        text_primary = get_text_primary()
        
        for item in self.category_items.values():
            widget = self.itemWidget(item, 0)
            if widget:
                for child in widget.findChildren(QLabel):
                    if child.text() != "":
                        child.setStyleSheet(f"background: transparent; border: none; font-weight: normal; color: {text_primary};")

    def select_category(self, category_id: str):
        """选中指定分类"""
        if category_id in self.category_items:
            item = self.category_items[category_id]
            self.setCurrentItem(item)
            self.scrollToItem(item)
