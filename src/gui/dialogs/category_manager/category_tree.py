from PySide6.QtWidgets import QAbstractItemView, QTreeWidgetItem
from PySide6.QtCore import Qt
from qfluentwidgets import TreeWidget
from src.common.config import MAX_CATEGORY_DEPTH, SYSTEM_CATEGORIES
from src.common.signals import signal_bus
from src.gui.styles import get_accent_color, get_text_primary, get_font_style

class CategoryTreeWidget(TreeWidget):
    """自定义分类树，支持拖拽验证"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_manager = None  # 将从外部设置
        
        # 初始化样式
        self.setIndentation(28)  # 增加缩进空间
        self._apply_style()
        
        # 连接主题变更信号
        signal_bus.theme_color_changed.connect(self._apply_style)
        signal_bus.theme_changed.connect(self._apply_style)  # 修复主题切换 Bug


    def _apply_style(self):
        """应用主题敏感样式 - 确保垂直居中对齐"""
        from qfluentwidgets import setCustomStyleSheet
        text_primary = get_text_primary()
        font_style = get_font_style(size="md")
        
        # 设置合适的行高和对齐方式,确保复选框、图标和文字垂直居中
        # 使用固定尺寸避免展开/折叠时的布局抖动
        qss = f"""
            TreeWidget {{
                outline: none;
                {font_style}
                background: transparent;
                border: none;
            }}
            TreeWidget::indicator {{
                width: 18px;
                height: 18px;
                margin-left: 2px;
                margin-right: 8px;
            }}
            TreeWidget::item {{
                color: {text_primary};
                height: 32px;
                padding-left: 12px;
                margin: 0px;
            }}
            TreeWidget::branch {{
                background: transparent;
                width: 24px;
            }}
        """
        setCustomStyleSheet(self, qss, qss)
        
        # 设置统一的行高,避免动态调整
        self.setUniformRowHeights(True)

    def dragMoveEvent(self, event):
        """拖拽移动过程中的验证"""
        if self._validate_drag(event):
            super().dragMoveEvent(event)
        else:
            event.ignore()

    def dropEvent(self, event):
        """放置时的验证"""
        if self._validate_drag(event):
            super().dropEvent(event)
        else:
            event.ignore()

    def _validate_drag(self, event) -> bool:
        """
        验证拖拽操作是否合法
        规则：
        1. 不能移动内置分类（可选，目前允许排序但不允许改变父子关系）
        2. 目标父分类不能包含模板
        3. 移动后的总深度不能超过 MAX_CATEGORY_DEPTH
        """
        # 获取被拖拽的项
        dragged_item = self.currentItem()
        if not dragged_item:
            return False
            
        category = dragged_item.data(0, Qt.ItemDataRole.UserRole)
        if not category:
            return False

        # 获取放置的目标项和放置位置
        target_item = self.itemAt(event.pos())
        
        # 这里的简化逻辑：如果我们是 InternalMove，我们主要关注放置到某项内部的情况
        # Qt 的默认行为：如果鼠标在项的正中间，是作为子项；如果是项的上边缘或下边缘，是作为同级。
        
        # 我们可以通过计算深度来做初步预防
        # 如果是作为子项移动：
        if target_item and target_item != dragged_item:
            # 1. 检查是否为子孙关系 (Qt 已拦截，但我们加固一下)
            if self._is_descendant(dragged_item, target_item):
                return False
                
            # 2. 检查放置深度
            target_depth = self._get_item_depth(target_item)
            subtree_depth = self._get_subtree_max_depth(dragged_item)
            if target_depth + subtree_depth > MAX_CATEGORY_DEPTH:
                return False
                
            # 3. 检查商务逻辑：目标父项是否有模板
            target_cat = target_item.data(0, Qt.ItemDataRole.UserRole)
            if target_cat:
                can_add, _ = self.category_manager.can_add_child_category(target_cat.id)
                if not can_add:
                    return False
            
            # 4. 系统分类保护：系统分类不允许作为子分类 (通常保持在根部)
            if category.id in SYSTEM_CATEGORIES:
                return False
                    
        return True

    def _get_item_depth(self, item) -> int:
        """计算项的当前深度"""
        depth = 1
        current = item
        while current.parent():
            current = current.parent()
            depth += 1
        return depth

    def _get_subtree_max_depth(self, item) -> int:
        """获取子树的最大相对深度"""
        if item.childCount() == 0:
            return 1
        max_child_depth = 0
        for i in range(item.childCount()):
            max_child_depth = max(max_child_depth, self._get_subtree_max_depth(item.child(i)))
        return 1 + max_child_depth

    def _is_descendant(self, parent, child) -> bool:
        """检查 child 是否是 parent 的子孙"""
        current = child.parent()
        while current:
            if current == parent:
                return True
            current = current.parent()
        return False
