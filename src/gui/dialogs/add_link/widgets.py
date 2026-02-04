from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    BodyLabel, LineEdit, PushButton, CheckBox
)
from src.data.template_manager import TemplateManager
from src.data.user_manager import UserManager
from src.data.category_manager import CategoryManager
from src.gui.components import CategorySelector, ValidatedLineEdit
from src.gui.i18n import get_category_text
from src.common.validators import PathValidator, NameValidator

class TemplateTabWidget(QWidget):
    """从模版库选择标签页"""
    template_selected_signal = Signal(object)
    manage_categories_requested = Signal()

    def __init__(self, template_manager: TemplateManager, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.template_manager = template_manager
        self.user_manager = user_manager
        self._init_ui()
        self._load_templates()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        
        # 顶部: 分类筛选 + 搜索
        top_layout = QHBoxLayout()
        
        # 分类筛选器
        self.categoryFilter = CategorySelector()
        self.category_manager = CategoryManager()
        self.categoryFilter.set_manager(self.category_manager)
        self.categoryFilter.value_changed.connect(self._on_category_filter_changed)
        top_layout.addWidget(BodyLabel("筛选:"))
        top_layout.addWidget(self.categoryFilter, 1)
        
        self.searchBox = LineEdit()
        self.searchBox.setPlaceholderText("搜索模版...")
        self.searchBox.textChanged.connect(self._on_search_changed)
        top_layout.addWidget(self.searchBox, 1)
        
        layout.addLayout(top_layout)
        
        # 模板列表
        from qfluentwidgets import ListWidget
        self.templateList = ListWidget()
        self.templateList.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.templateList)
        
        # 详情区域
        details_layout = QVBoxLayout()
        
        self.nameEdit = ValidatedLineEdit()
        self.nameEdit.addValidator(NameValidator())
        self.nameEdit.setPlaceholderText("名称")
        details_layout.addWidget(BodyLabel("名称:"))
        details_layout.addWidget(self.nameEdit)
        
        self.sourceEdit = ValidatedLineEdit()
        self.sourceEdit.addValidator(PathValidator())
        self.sourceEdit.setPlaceholderText("源路径")
        details_layout.addWidget(BodyLabel("源路径:"))
        details_layout.addWidget(self.sourceEdit)
        
        self.targetEdit = ValidatedLineEdit()
        self.targetEdit.addValidator(PathValidator())
        self.targetEdit.setPlaceholderText("目标路径")
        details_layout.addWidget(BodyLabel("目标路径:"))
        details_layout.addWidget(self.targetEdit)
        
        self.categorySelector = CategorySelector()
        self.category_manager = CategoryManager()
        self.categorySelector.set_manager(self.category_manager)
        
        # 分类选择行
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.categorySelector)
        
        self.manageCategoryBtn = PushButton("管理分类")
        self.manageCategoryBtn.clicked.connect(self.manage_categories_requested.emit)
        category_layout.addWidget(self.manageCategoryBtn)
        
        details_layout.addWidget(BodyLabel("分类:"))
        details_layout.addLayout(category_layout)
        
        layout.addLayout(details_layout)
        
        # 初始化数据
        self.current_category_id = "all"
        self.refresh_categories()
        self._load_templates_by_category("all")
    
    def _on_category_filter_changed(self, category_id: str):
        """分类筛选器切换回调"""
        self.current_category_id = category_id if category_id else "all"
        self._load_templates_by_category(self.current_category_id)
    
    
    def _load_templates_by_category(self, category_id: str):
        """根据分类加载模板"""
        self.templateList.clear()
        
        if category_id == "all":
            templates = self.template_manager.get_all_templates()
        else:
            templates = self.template_manager.get_templates_by_category_recursive(category_id)
        
        for template in templates:
            item = QListWidgetItem()
            # 两行显示: 名称 + 路径
            item.setText(f"{template.name}\n{template.default_src}")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)

    def _load_templates(self):
        self.templateList.clear()
        templates = self.template_manager.get_all_templates()
        for template in templates:
            cat_name = get_category_text(template.category_id)
            item = QListWidgetItem(f"{template.name} ({cat_name})")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)

    def _on_search_changed(self, text: str):
        if text:
            # 搜索模式
            self.templateList.clear()
            templates = self.template_manager.search_templates(text)
            for template in templates:
                item = QListWidgetItem()
                cat_name = get_category_text(template.category_id)
                item.setText(f"{template.name}\n{template.default_src}\n分类: {cat_name}")
                item.setData(Qt.ItemDataRole.UserRole, template)
                self.templateList.addItem(item)
        else:
            # 恢复分类浏览
            self._load_templates_by_category(self.current_category_id)

    def _on_item_clicked(self, item: QListWidgetItem):
        template = item.data(Qt.ItemDataRole.UserRole)
        self.template_selected_signal.emit(template)
        
        # 填充
        self.nameEdit.setText(template.name)
        source_path = self.template_manager.expand_path(template.default_src)
        # 使用 PathValidator 标准化路径回显
        source_path = PathValidator().normalize(source_path)
        self.sourceEdit.setText(source_path)
        
        target_path = "D:\\" + source_path[3:]
        target_path = PathValidator().normalize(target_path)
        self.targetEdit.setText(target_path)
        
        # 使用 category_id 精准匹配 (回显 ID)
        cat_id = getattr(template, 'category_id', getattr(template, 'category', 'uncategorized'))
        self.categorySelector.set_value(cat_id)

    def refresh_categories(self):
        """刷新分类列表"""
        self.categoryFilter.refresh()
        self.categorySelector.refresh()


class CustomTabWidget(QWidget):
    """自定义标签页"""
    manage_categories_requested = Signal()

    def __init__(self, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        
        self.customNameEdit = ValidatedLineEdit()
        self.customNameEdit.addValidator(NameValidator())
        self.customNameEdit.setPlaceholderText("软件名称")
        layout.addWidget(BodyLabel("名称:"))
        layout.addWidget(self.customNameEdit)
        
        self.customSourceEdit = ValidatedLineEdit()
        self.customSourceEdit.addValidator(PathValidator())
        self.customSourceEdit.setPlaceholderText("源路径...")
        layout.addWidget(BodyLabel("源路径:"))
        layout.addWidget(self.customSourceEdit)
        
        self.customTargetEdit = ValidatedLineEdit()
        self.customTargetEdit.addValidator(PathValidator())
        self.customTargetEdit.setPlaceholderText("目标路径...")
        layout.addWidget(BodyLabel("目标路径:"))
        layout.addWidget(self.customTargetEdit)
        
        self.customCategorySelector = CategorySelector()
        self.category_manager = CategoryManager()
        self.customCategorySelector.set_manager(self.category_manager)
        
        custom_category_layout = QHBoxLayout()
        custom_category_layout.addWidget(self.customCategorySelector)
        
        self.customManageCategoryBtn = PushButton("管理分类")
        self.customManageCategoryBtn.clicked.connect(self.manage_categories_requested.emit)
        custom_category_layout.addWidget(self.customManageCategoryBtn)
        
        layout.addWidget(BodyLabel("分类:"))
        layout.addLayout(custom_category_layout)
        
        self.saveAsTemplateBtn = CheckBox("保存为自定义模版")
        layout.addWidget(self.saveAsTemplateBtn)
        
        layout.addStretch()
        self.refresh_categories()
        
        # 为所有 BodyLabel 应用响应式主题
        from qfluentwidgets import setCustomStyleSheet
        setCustomStyleSheet(
            self,
            lightQss="BodyLabel { color: #1F1F1F; }",
            darkQss="BodyLabel { color: #FFFFFF; }"
        )

    def refresh_categories(self):
        """刷新分类列表"""
        self.customCategorySelector.refresh()
