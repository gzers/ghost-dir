"""
新增连接对话框
"""
from PySide6.QtCore import Signal
from qfluentwidgets import MessageBoxBase
from src.data.template_manager import TemplateManager
from src.data.user_manager import UserManager
from src.data.model import UserLink, Template
from src.gui.dialogs.add_link.widgets import TemplateTabWidget, CustomTabWidget
import uuid


class AddLinkDialog(MessageBoxBase):
    """新增连接对话框"""
    
    link_added = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.template_manager = TemplateManager()
        self.user_manager = UserManager()
        self.selected_template = None
        
        self.setWindowTitle("新增连接")
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        from PySide6.QtWidgets import QVBoxLayout, QStackedWidget
        from qfluentwidgets import SegmentedWidget
        
        # 创建主布局容器
        container = QVBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        container.setSpacing(12)
        
        # 创建分段导航栏（官方组件）
        self.pivot = SegmentedWidget()
        
        # 创建堆栈视图
        self.stackedWidget = QStackedWidget()
        
        # Tab 1: 从模版库选择
        self.templateTab = TemplateTabWidget(self.template_manager, self.user_manager)
        self.templateTab.template_selected_signal.connect(self._on_template_selected)
        self.templateTab.manage_categories_requested.connect(self._on_manage_categories)
        
        # Tab 2: 自定义
        self.customTab = CustomTabWidget(self.user_manager)
        self.customTab.manage_categories_requested.connect(self._on_manage_categories)
        
        # 添加到堆栈和导航栏
        self.stackedWidget.addWidget(self.templateTab)
        self.stackedWidget.addWidget(self.customTab)
        self.pivot.addItem(routeKey='template', text='从模版库选择')
        self.pivot.addItem(routeKey='custom', text='自定义')
        
        # 连接导航切换信号
        self.pivot.currentItemChanged.connect(self._on_pivot_changed)
        self.pivot.setCurrentItem('template')
        
        # 添加到容器
        container.addWidget(self.pivot)
        container.addWidget(self.stackedWidget)
        
        # 创建包装器 widget
        from PySide6.QtWidgets import QWidget
        wrapper = QWidget()
        wrapper.setLayout(container)
        
        # 添加到视图
        self.viewLayout.addWidget(wrapper)
        
        # 按钮
        self.yesButton.setText("添加")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(600)
        self.widget.setMinimumHeight(500)
    
    def _on_pivot_changed(self, key):
        """导航切换回调"""
        index = 0 if key == 'template' else 1
        self.stackedWidget.setCurrentIndex(index)
    
    def _on_template_selected(self, template):
        """模版选中回调"""
        self.selected_template = template
    
    def _on_manage_categories(self):
        """打开分类管理对话框"""
        from src.gui.dialogs.category_manager import CategoryManagerDialog
        dialog = CategoryManagerDialog(self)
        dialog.categories_changed.connect(self._refresh_categories)
        dialog.exec()
    
    def _refresh_categories(self):
        """刷新分类列表"""
        self.templateTab.refresh_categories()
        self.customTab.refresh_categories()
    
    def validate(self):
        """验证并添加"""
        from qfluentwidgets import InfoBar, InfoBarPosition
        from PySide6.QtCore import Qt
        from src.common.validators import PathValidator
        from src.data.category_manager import CategoryManager
        
        # 1. 提取数据
        if self.stackedWidget.currentIndex() == 0:  # 从模版添加
            name = self.templateTab.nameEdit.text().strip()
            source = self.templateTab.sourceEdit.text().strip()
            target = self.templateTab.targetEdit.text().strip()
            category_id = self.templateTab.categorySelector.get_value()
        else:  # 自定义添加
            name = self.customTab.customNameEdit.text().strip()
            source = self.customTab.customSourceEdit.text().strip()
            target = self.customTab.customTargetEdit.text().strip()
            category_id = self.customTab.customCategorySelector.get_value()
            
        # 2. 必填项校验与统一 UI 提示
        def show_warning(content):
            InfoBar.warning(
                title="验证失败",
                content=content,
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

        if not name:
            show_warning("连接名称不能为空")
            return False
        if not source:
            show_warning("源路径不能为空")
            return False
        if not target:
            show_warning("目标路径不能为空")
            return False
        if not category_id:
            show_warning("请选择所属分类")
            return False
            
        # 3. 验证分类是否为叶子节点 (如果业务要求)
        cm = CategoryManager()
        if not cm.is_leaf(category_id):
            show_warning(f"分类 '{cm.get_category_by_id(category_id).name}' 不是末级分类，请选择子分类")
            return False

        # 4. 标准化路径
        source = PathValidator().normalize(source)
        target = PathValidator().normalize(target)
        
        # 5. 执行添加
        link = UserLink(
            id=str(uuid.uuid4()),
            name=name,
            source_path=source,
            target_path=target,
            category=category_id,
            template_id=self.selected_template.id if self.selected_template else None,
            icon=self.selected_template.icon if self.selected_template else None
        )
        
        if self.user_manager.add_link(link):
            # 处理保存为模版
            if self.stackedWidget.currentIndex() == 1 and self.customTab.saveAsTemplateBtn.isChecked():
                new_template = Template(
                    id=str(uuid.uuid4()),
                    name=name,
                    default_src=source,
                    category_id=category_id, # 修正字段名保持一致
                    is_custom=True
                )
                self.user_manager.add_custom_template(new_template)
            
            self.link_added.emit()
            return True
        else:
            show_warning("添加连接失败，请检查路径是否合法或冲突")
        
        return False
