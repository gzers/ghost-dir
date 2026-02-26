"""
分类选择器组件
支持层级展示和只选叶子分类
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidgetItem,
    QPushButton, QHBoxLayout, QFrame
)
from PySide6.QtGui import QCursor
from qfluentwidgets import LineEdit, TreeWidget, setCustomStyleSheet
from src.common.managers import CategoryManager  # TODO: 迁移到 CategoryService
from src.models.category import CategoryNode  # 新架构: 使用 models 层
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

        # 核心：监听主题变化信号以便及时更新样式
        from qfluentwidgets import qconfig
        qconfig.themeChanged.connect(self._apply_style)

    def showEvent(self, event):
        """弹出时强制刷新样式，防止主题滞后"""
        self._apply_style()
        super().showEvent(event)

    def _apply_style(self):
        """应用样式 (严重警告：禁止自定义 TreeWidget 内部项样式，否则会导致背景渲染分块冲突)"""
        from qfluentwidgets import setCustomStyleSheet, isDarkTheme

        # 仅定义容器样式，内部 TreeWidget 项交给官方原生处理以确保渲染一致性
        def get_container_qss(bg_color, border_color, text_color):
            return f"""
                CategoryTreeDropdown {{
                    background: {bg_color};
                    border: 1px solid {border_color};
                    border-radius: 8px;
                }}
                TreeWidget {{
                    background: transparent;
                    border: none;
                    outline: none;
                    color: {text_color};
                }}
                TreeWidget::item {{
                    color: {text_color};
                }}
            """

        light_qss = get_container_qss("rgba(255, 255, 255, 0.98)", "rgba(0, 0, 0, 0.1)", "black")
        dark_qss = get_container_qss("rgba(45, 45, 45, 0.98)", "rgba(255, 255, 255, 0.1)", "white")

        # 1. 设置响应式 QSS
        setCustomStyleSheet(self, light_qss, dark_qss)

        # 2. 核心补丁：对于顶级窗口强制刷新
        target_qss = dark_qss if isDarkTheme() else light_qss
        self.setStyleSheet(target_qss)

    def load_categories(self):
        """加载分类树"""
        self.tree.clear()
        self.category_items.clear()

        # 如果需要显示根分类
        if self.root_visible:
            from src.gui.styles import get_text_secondary
            root_item = QTreeWidgetItem(self.tree)
            root_item.setData(0, Qt.ItemDataRole.UserRole, None)
            from src.gui.i18n import t
            root_name = t("library.label_root_category")
            # 如果翻译缺失，回退到默认文案
            if "[Missing:" in root_name:
                root_name = "无 (根分类)"
            root_item.setText(0, root_name)
            # 强调条装饰
            root_item.setForeground(0, self.palette().link())
            root_item.setToolTip(0, "点击选择此项作为根分类")

        # 修正方法名：CategoryManager 中获取根节点的正确方法是 get_category_tree
        root_nodes = self.category_manager.get_category_tree()
        for node in sorted(root_nodes, key=lambda x: x.order):
            self._add_category_item(node)

        self.tree.expandAll()

    def _add_category_item(self, category: CategoryNode, parent_item: QTreeWidgetItem = None):
        """添加分类项"""
        # 递归检查排除列表（如果分类本身或其祖先在排除列表中，则不显示）
        if self.exclude_ids and category.id in self.exclude_ids:
            return

        if parent_item:
            item = QTreeWidgetItem(parent_item)
        else:
            item = QTreeWidgetItem(self.tree)

        item.setData(0, Qt.ItemDataRole.UserRole, category.id)

        # 直接使用节点的名称（已包含国际化后的文案）
        display_name = category.name
        item.setText(0, display_name)

        self.category_items[category.id] = item

        # 检查是否可选择
        is_leaf = self.category_manager.is_leaf(category.id)

        # 提取或补全全路径信息用于 Tooltip
        full_path_name = getattr(category, 'full_path_name', "") or display_name

        if self.only_leaf:
            if not is_leaf:
                # 仅叶子模式：非叶子节点不可选
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                item.setToolTip(0, f"[{full_path_name}]\n此分类包含子分类，请选择具体的子分类")
            else:
                item.setToolTip(0, f"选择分类: {full_path_name}")
        else:
            # 全节点模式：所有节点皆可选
            item.setToolTip(0, f"选择分类: {full_path_name}")

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

    value_changed = Signal(str)  # 添加对外信号

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

        # 核心：添加清除按钮（仿官方设计）
        from qfluentwidgets import TransparentToolButton, FluentIcon
        self.clearButton = TransparentToolButton(FluentIcon.CLOSE, self.lineEdit)
        self.clearButton.setFixedSize(28, 28)
        self.clearButton.setCursor(Qt.CursorShape.ArrowCursor)
        self.clearButton.setVisible(False)  # 初始隐藏
        self.clearButton.clicked.connect(self.clear)

        # 覆写 lineEdit 的 margins，给右侧下拉图标和清除按钮留出位置
        # 官方 LineEdit 右侧通常有 30px 的按钮空间，我们要留出更多一点
        self.lineEdit.setTextMargins(0, 0, 24, 0)

        layout.addWidget(self.lineEdit)

        # 安装过滤器
        self.lineEdit.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.lineEdit and event.type() == QEvent.Type.MouseButtonPress:
            self._show_dropdown()
            return True
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 将清除按钮定位在右侧（避开自带的下拉箭头位置，或与自带位置对齐）
        # 官方 ComboBox 风格通常清除按钮在下拉箭头左边
        self.clearButton.move(self.width() - 62, (self.height() - self.clearButton.height()) // 2)

    def clear(self):
        """清除选中"""
        self.set_value(None)
        # 触发清除信号
        self.value_changed.emit(None)

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

        # 设置全路径 Tooltip
        if self.category_manager and category_id:
            cat = self.category_manager.get_category_by_id(category_id)
            full_path = getattr(cat, 'full_path_name', None) if cat else None
            self.lineEdit.setToolTip(full_path if full_path else category_name)
        else:
            self.lineEdit.setToolTip(category_name)

        # 联动更新清除按钮状态
        if hasattr(self, 'clearButton'):
            self.clearButton.setVisible(bool(category_id))

        # 触发对外信号
        self.value_changed.emit(category_id)

    def refresh(self):
        """刷新分类列表"""
        if self.dropdown:
            self.dropdown.load_categories()

    def set_value(self, category_id: Optional[str]):
        """设置选中的分类 ID (不触发对外信号以防止循环)"""
        # 1. 处理清除逻辑 (category_id 为 None)
        if category_id is None:
            self.selected_category_id = None
            self.selected_category_name = None
            self.lineEdit.clear()
            self.lineEdit.setToolTip("")
            if hasattr(self, 'clearButton'):
                self.clearButton.setVisible(False)
            return

        # 2. 正常设置逻辑
        if not self.category_manager:
            return

        category = self.category_manager.get_category_by_id(category_id)
        if category:
            display_name = get_category_text(category_id)
            self.selected_category_id = category_id
            self.selected_category_name = display_name
            self.lineEdit.setText(display_name)

            # 设置全路径 Tooltip (防御属性缺失)
            full_path = getattr(category, 'full_path_name', None)
            self.lineEdit.setToolTip(full_path if full_path else display_name)

            # 联动显示清除按钮
            if hasattr(self, 'clearButton'):
                self.clearButton.setVisible(True)

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

