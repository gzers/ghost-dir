"""
分类视图组件
左树右表布局，复用现有的 CategoryTree 和 LinkTable 组件
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt, Signal
from .category_tree import CategoryTree
from ....components.link_table import LinkTable
from .....data.user_manager import UserManager


class CategoryLinkView(QWidget):
    """分类视图 - 左侧分类树，右侧连接表格"""
    
    # 信号
    category_selected = Signal(str)  # 分类被选中
    link_selected = Signal(list)     # 连接被选中
    action_clicked = Signal(str, str)  # (link_id, action)
    
    def __init__(self, parent=None):
        """初始化分类视图"""
        super().__init__(parent)
        self.user_manager = UserManager()
        self._current_category = None
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：分类树
        self.category_tree = CategoryTree()
        splitter.addWidget(self.category_tree)
        
        # 右侧：连接表格
        self.link_table = LinkTable()
        splitter.addWidget(self.link_table)
        
        # 设置分割比例（1:3）
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        layout.addWidget(splitter)
    
    def _connect_signals(self):
        """连接信号"""
        # 分类树信号
        self.category_tree.category_selected.connect(self._on_category_selected)
        
        # 连接表格信号
        self.link_table.link_selected.connect(self.link_selected)
        self.link_table.action_clicked.connect(self.action_clicked)
    
    def _on_category_selected(self, category_name: str):
        """分类被选中"""
        self._current_category = category_name
        self.category_selected.emit(category_name)
        
        # 加载该分类下的连接
        if category_name == "全部":
            links = self.user_manager.get_all_links()
        else:
            links = self.user_manager.get_links_by_category(category_name)
        
        self.link_table.load_links(links)
    
    def load_data(self):
        """加载数据"""
        # 加载分类树
        self.category_tree.load_categories()
        
        # 默认加载所有连接
        links = self.user_manager.get_all_links()
        self.link_table.load_links(links)
    
    def refresh_data(self):
        """刷新数据"""
        # 刷新分类树
        self.category_tree.load_categories()
        
        # 刷新当前分类的连接
        if self._current_category:
            self._on_category_selected(self._current_category)
        else:
            links = self.user_manager.get_all_links()
            self.link_table.load_links(links)
    
    def update_statuses(self, statuses: dict):
        """
        更新连接状态
        
        Args:
            statuses: {link_id: LinkStatus} 字典
        """
        # LinkTable 会通过 link.status 动态计算状态，所以只需重新加载当前视图
        self.refresh_data()
    
    def get_selected_links(self) -> list:
        """获取选中的连接 ID 列表"""
        return self.link_table.get_selected_links()
    
    def clear_selection(self):
        """清除选择"""
        self.link_table.clear_selection()
