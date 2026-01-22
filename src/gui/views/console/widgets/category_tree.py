"""
分类树组件
左侧分类导航树
"""
from PySide6.QtWidgets import QTreeWidgetItem
from qfluentwidgets import TreeWidget
from .....data.user_manager import UserManager


class CategoryTree(TreeWidget):
    """分类树组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_manager = UserManager()
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setHeaderHidden(True)
        self.setMaximumWidth(250)
        # 设置背景色和移除边框
        self._update_theme_style()
        from .....common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _update_theme_style(self):
        """更新主题样式"""
        from ....styles import StyleManager
        bg_color = StyleManager.get_container_background()
        self.setStyleSheet(f"QTreeWidget {{ background-color: {bg_color}; border-right: none; }}")

    def _on_theme_changed(self, theme):
        """主题变更"""
        self._update_theme_style()
    
    def load_categories(self):
        """加载分类列表"""
        self.clear()
        
        # 添加"全部"节点
        all_item = QTreeWidgetItem(["全部"])
        self.addTopLevelItem(all_item)
        
        # 添加分类节点
        categories = self.user_manager.get_all_categories()
        for category in categories:
            count = len(self.user_manager.get_links_by_category(category.name))
            item = QTreeWidgetItem([f"{category.name} ({count})"])
            self.addTopLevelItem(item)
