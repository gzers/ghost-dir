from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QFormLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    BodyLabel, SubtitleLabel, LineEdit, PushButton, CheckBox, 
    HorizontalSeparator, ListWidget, FluentIcon, StrongBodyLabel
)
from src.data.template_manager import TemplateManager
from src.data.user_manager import UserManager
from src.data.category_manager import CategoryManager
from src.gui.components import CategorySelector, ValidatedLineEdit
from src.gui.i18n import get_category_text
from src.common.validators import PathValidator, NameValidator
from src.gui.styles import get_spacing, get_layout_margins

class TemplateTabWidget(QWidget):
    """从模版库选择标签页"""
    template_selected_signal = Signal(object)
    manage_categories_requested = Signal()

    def __init__(self, template_manager: TemplateManager, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.template_manager = template_manager
        self.user_manager = user_manager
        self.category_manager = CategoryManager()
        self._init_ui()
        self.refresh_categories()
        # 初始加载所有模板
        self._load_templates_by_category("all")

    def _init_ui(self):
        layout = QVBoxLayout(self)
        # 使用 LAYOUT_MARGINS["compact"]
        margin = get_layout_margins().get("compact", 12)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(0)
        
        # --- 1. 选择模板区域 ---
        # 官方风格标题
        layout.addWidget(SubtitleLabel("1. 选择模板"))
        layout.addSpacing(get_spacing("xs"))
        layout.addWidget(HorizontalSeparator())
        layout.addSpacing(get_spacing("md"))
        
        # 搜索行
        search_layout = QHBoxLayout()
        search_layout.setSpacing(get_spacing("md"))
        self.searchBox = LineEdit()
        self.searchBox.setPlaceholderText("在此搜索模版关键词...")
        self.searchBox.setClearButtonEnabled(True)
        self.searchBox.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(StrongBodyLabel("搜索: "))
        search_layout.addWidget(self.searchBox)
        layout.addLayout(search_layout)
        layout.addSpacing(get_spacing("sm"))
        
        # 筛选行
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(get_spacing("md"))
        self.categoryFilter = CategorySelector()
        self.categoryFilter.set_manager(self.category_manager)
        self.categoryFilter.value_changed.connect(self._on_category_filter_changed)
        filter_layout.addWidget(StrongBodyLabel("筛选: "))
        filter_layout.addWidget(self.categoryFilter, 1)
        layout.addLayout(filter_layout)
        layout.addSpacing(get_spacing("md"))
        
        # 模板列表
        self.templateList = ListWidget()
        self.templateList.setFixedHeight(150) # 保持紧凑
        self.templateList.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.templateList)
        
        # --- 2. 配置详情区域 ---
        layout.addSpacing(get_spacing("xl"))
        layout.addWidget(SubtitleLabel("2. 配置详情"))
        layout.addSpacing(get_spacing("xs"))
        layout.addWidget(HorizontalSeparator())
        layout.addSpacing(get_spacing("md"))
        
        # 使用 QFormLayout 以实现最标准的 Label 对齐
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        # 固定左右间距，确保视觉整齐
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.nameEdit = ValidatedLineEdit()
        self.nameEdit.addValidator(NameValidator())
        self.nameEdit.setPlaceholderText("输入链接名称")
        form_layout.addRow(BodyLabel("名称:"), self.nameEdit)
        
        self.sourceEdit = ValidatedLineEdit()
        self.sourceEdit.addValidator(PathValidator())
        self.sourceEdit.setPlaceholderText("选择或输入源路径")
        form_layout.addRow(BodyLabel("源路径:"), self.sourceEdit)
        
        self.targetEdit = ValidatedLineEdit()
        self.targetEdit.addValidator(PathValidator())
        self.targetEdit.setPlaceholderText("将根据源路径进行映射")
        form_layout.addRow(BodyLabel("目标路径:"), self.targetEdit)
        
        # 分类行封装
        cat_edit_widget = QWidget()
        cat_edit_layout = QHBoxLayout(cat_edit_widget)
        cat_edit_layout.setContentsMargins(0, 0, 0, 0)
        cat_edit_layout.setSpacing(get_spacing("sm"))
        
        self.categorySelector = CategorySelector()
        self.categorySelector.set_manager(self.category_manager)
        cat_edit_layout.addWidget(self.categorySelector, 1)
        
        self.manageCategoryBtn = PushButton("管理")
        self.manageCategoryBtn.setFixedWidth(60)
        self.manageCategoryBtn.clicked.connect(self.manage_categories_requested.emit)
        cat_edit_layout.addWidget(self.manageCategoryBtn)
        
        form_layout.addRow(BodyLabel("所属分类:"), cat_edit_widget)
        
        layout.addWidget(form_widget)
        layout.addStretch()

    def _on_category_filter_changed(self, category_id: str):
        self.current_category_id = category_id if category_id else "all"
        self._load_templates_by_category(self.current_category_id)
    
    def _load_templates_by_category(self, category_id: str):
        self.templateList.clear()
        if category_id == "all":
            templates = self.template_manager.get_all_templates()
        else:
            templates = self.template_manager.get_templates_by_category_recursive(category_id)
        
        for template in templates:
            item = QListWidgetItem()
            # 强化标题感
            item.setText(f"{template.name}\n路径: {template.default_src}")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)

    def _on_search_changed(self, text: str):
        if text:
            self.templateList.clear()
            templates = self.template_manager.search_templates(text)
            for template in templates:
                item = QListWidgetItem()
                cat_name = get_category_text(template.category_id)
                item.setText(f"{template.name} ({cat_name})\n路径: {template.default_src}")
                item.setData(Qt.ItemDataRole.UserRole, template)
                self.templateList.addItem(item)
        else:
            self._load_templates_by_category(getattr(self, 'current_category_id', 'all'))

    def _on_item_clicked(self, item: QListWidgetItem):
        template = item.data(Qt.ItemDataRole.UserRole)
        self.template_selected_signal.emit(template)
        
        self.nameEdit.setText(template.name)
        source_path = self.template_manager.expand_path(template.default_src)
        source_path = PathValidator().normalize(source_path)
        self.sourceEdit.setText(source_path)
        
        # 默认推断逻辑
        target_path = "D:\\" + source_path[3:]
        target_path = PathValidator().normalize(target_path)
        self.targetEdit.setText(target_path)
        
        cat_id = getattr(template, 'category_id', getattr(template, 'category', 'uncategorized'))
        self.categorySelector.set_value(cat_id)

    def refresh_categories(self):
        self.categoryFilter.refresh()
        self.categorySelector.refresh()

class CustomTabWidget(QWidget):
    """自定义标签页"""
    manage_categories_requested = Signal()

    def __init__(self, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.category_manager = CategoryManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        margin = get_layout_margins().get("compact", 12)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(get_spacing("md"))
        
        layout.addWidget(SubtitleLabel("配置详情"))
        layout.addSpacing(get_spacing("xs"))
        layout.addWidget(HorizontalSeparator())
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.customNameEdit = ValidatedLineEdit()
        self.customNameEdit.addValidator(NameValidator())
        self.customNameEdit.setPlaceholderText("例如: 我的项目")
        form_layout.addRow(BodyLabel("链接名称:"), self.customNameEdit)
        
        self.customSourceEdit = ValidatedLineEdit()
        self.customSourceEdit.addValidator(PathValidator())
        self.customSourceEdit.setPlaceholderText("源文件或文件夹的绝对路径...")
        form_layout.addRow(BodyLabel("源路径:"), self.customSourceEdit)
        
        self.customTargetEdit = ValidatedLineEdit()
        self.customTargetEdit.addValidator(PathValidator())
        self.customTargetEdit.setPlaceholderText("软链接将被创建的路径...")
        form_layout.addRow(BodyLabel("目标路径:"), self.customTargetEdit)
        
        # 分类行
        self.customCategorySelector = CategorySelector()
        self.customCategorySelector.set_manager(self.category_manager)
        
        cat_row_widget = QWidget()
        cat_row_layout = QHBoxLayout(cat_row_widget)
        cat_row_layout.setContentsMargins(0, 0, 0, 0)
        cat_row_layout.setSpacing(get_spacing("sm"))
        
        cat_row_layout.addWidget(self.customCategorySelector, 1)
        self.customManageBtn = PushButton("管理")
        self.customManageBtn.setFixedWidth(60)
        self.customManageBtn.clicked.connect(self.manage_categories_requested.emit)
        cat_row_layout.addWidget(self.customManageBtn)
        
        form_layout.addRow(BodyLabel("所属分类:"), cat_row_widget)
        
        layout.addWidget(form_widget)
        
        # 选项控制 - 保持跟输入框对齐
        self.saveAsTemplateBtn = CheckBox("保存为自定义模版以便下次快速使用")
        # 这里的 95px 是 QFormLayout 实现对齐的一个近似估值，如果由于动态字号导致对齐不准，后续通过 QFormLayout::labelForField 动态调整更稳
        form_layout.addRow("", self.saveAsTemplateBtn)
        
        layout.addStretch()
        self.refresh_categories()

    def refresh_categories(self):
        self.customCategorySelector.refresh()
