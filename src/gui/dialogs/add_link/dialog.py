"""
新增连接对话框
"""
from PySide6.QtWidgets import QTabWidget
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
        # 创建标签页
        self.tabWidget = QTabWidget()
        
        # Tab 1: 从模版库选择
        self.templateTab = TemplateTabWidget(self.template_manager, self.user_manager)
        self.templateTab.template_selected_signal.connect(self._on_template_selected)
        self.templateTab.manage_categories_requested.connect(self._on_manage_categories)
        self.tabWidget.addTab(self.templateTab, "从模版库选择")
        
        # Tab 2: 自定义
        self.customTab = CustomTabWidget(self.user_manager)
        self.customTab.manage_categories_requested.connect(self._on_manage_categories)
        self.tabWidget.addTab(self.customTab, "自定义")
        
        # 添加到视图
        self.viewLayout.addWidget(self.tabWidget)
        
        # 按钮
        self.yesButton.setText("添加")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(600)
        self.widget.setMinimumHeight(500)
    
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
        if self.tabWidget.currentIndex() == 0:  # 从模版添加
            name = self.templateTab.nameEdit.text().strip()
            source = self.templateTab.sourceEdit.text().strip()
            target = self.templateTab.targetEdit.text().strip()
            category = self.templateTab.categorySelector.get_value() or "uncategorized"
        else:  # 自定义添加
            name = self.customTab.customNameEdit.text().strip()
            source = self.customTab.customSourceEdit.text().strip()
            target = self.customTab.customTargetEdit.text().strip()
            category = self.customTab.customCategorySelector.get_value() or "uncategorized"
        
        # 验证
        if not name or not source or not target:
            return False
            
        # 标准化路径
        from src.common.validators import PathValidator
        source = PathValidator().normalize(source)
        target = PathValidator().normalize(target)
        
        # 创建连接
        link = UserLink(
            id=str(uuid.uuid4()),
            name=name,
            source_path=source,
            target_path=target,
            category=category,
            template_id=self.selected_template.id if self.selected_template else None,
            icon=self.selected_template.icon if self.selected_template else None
        )
        
        # 添加到用户数据
        if self.user_manager.add_link(link):
            # 处理保存为模版
            if self.tabWidget.currentIndex() == 1 and self.customTab.saveAsTemplateBtn.isChecked():
                new_template = Template(
                    id=str(uuid.uuid4()),
                    name=name,
                    default_src=source,
                    category=category,
                    is_custom=True
                )
                self.user_manager.add_custom_template(new_template)
            
            self.link_added.emit()
            return True
        
        return False
