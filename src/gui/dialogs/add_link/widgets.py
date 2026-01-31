from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    BodyLabel, LineEdit, PushButton, ComboBox, CheckBox
)
from src.data.template_manager import TemplateManager
from src.data.user_manager import UserManager

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
        
        # 搜索框
        search_layout = QHBoxLayout()
        self.searchBox = LineEdit()
        self.searchBox.setPlaceholderText("搜索模版...")
        self.searchBox.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(self.searchBox)
        layout.addLayout(search_layout)
        
        # 模版列表
        self.templateList = QListWidget()
        self.templateList.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.templateList)
        
        # 详情区域
        details_layout = QVBoxLayout()
        
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText("名称")
        details_layout.addWidget(BodyLabel("名称:"))
        details_layout.addWidget(self.nameEdit)
        
        self.sourceEdit = LineEdit()
        self.sourceEdit.setPlaceholderText("源路径 (C 盘)")
        details_layout.addWidget(BodyLabel("源路径:"))
        details_layout.addWidget(self.sourceEdit)
        
        self.targetEdit = LineEdit()
        self.targetEdit.setPlaceholderText("目标路径 (D 盘)")
        details_layout.addWidget(BodyLabel("目标路径:"))
        details_layout.addWidget(self.targetEdit)
        
        self.categoryCombo = ComboBox()
        
        # 分类选择行
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.categoryCombo)
        
        self.manageCategoryBtn = PushButton("管理分类")
        self.manageCategoryBtn.clicked.connect(self.manage_categories_requested.emit)
        category_layout.addWidget(self.manageCategoryBtn)
        
        details_layout.addWidget(BodyLabel("分类:"))
        details_layout.addLayout(category_layout)
        
        layout.addLayout(details_layout)
        self.refresh_categories()

    def _load_templates(self):
        self.templateList.clear()
        templates = self.template_manager.get_all_templates()
        all_cats = {c.id: c.name for c in self.user_manager.get_all_categories()}
        for template in templates:
            cat_name = all_cats.get(template.category_id, "未知分类")
            item = QListWidgetItem(f"{template.name} ({cat_name})")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)

    def _on_search_changed(self, text: str):
        self.templateList.clear()
        templates = self.template_manager.search_templates(text) if text else self.template_manager.get_all_templates()
        all_cats = {c.id: c.name for c in self.user_manager.get_all_categories()}
        for template in templates:
            cat_name = all_cats.get(template.category_id, "未知分类")
            item = QListWidgetItem(f"{template.name} ({cat_name})")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem):
        template = item.data(Qt.ItemDataRole.UserRole)
        self.template_selected_signal.emit(template)
        
        # 填充
        self.nameEdit.setText(template.name)
        source_path = self.template_manager.expand_path(template.default_src)
        self.sourceEdit.setText(source_path)
        target_path = "D:\\" + source_path[3:]
        self.targetEdit.setText(target_path)
        
        # 根据 category_id 寻找分类名称
        all_cats = {c.id: c.name for c in self.user_manager.get_all_categories()}
        cat_name = all_cats.get(template.category_id, "")
        index = self.categoryCombo.findText(cat_name)
        if index >= 0:
            self.categoryCombo.setCurrentIndex(index)

    def refresh_categories(self):
        current_text = self.categoryCombo.currentText()
        self.categoryCombo.clear()
        categories = self.user_manager.get_all_categories()
        for category in categories:
            self.categoryCombo.addItem(category.name)
        index = self.categoryCombo.findText(current_text)
        if index >= 0:
            self.categoryCombo.setCurrentIndex(index)

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
        
        self.customNameEdit = LineEdit()
        self.customNameEdit.setPlaceholderText("软件名称")
        layout.addWidget(BodyLabel("名称:"))
        layout.addWidget(self.customNameEdit)
        
        self.customSourceEdit = LineEdit()
        self.customSourceEdit.setPlaceholderText("C:\\...")
        layout.addWidget(BodyLabel("源路径 (C 盘):"))
        layout.addWidget(self.customSourceEdit)
        
        self.customTargetEdit = LineEdit()
        self.customTargetEdit.setPlaceholderText("D:\\...")
        layout.addWidget(BodyLabel("目标路径 (D 盘):"))
        layout.addWidget(self.customTargetEdit)
        
        self.customCategoryCombo = ComboBox()
        
        custom_category_layout = QHBoxLayout()
        custom_category_layout.addWidget(self.customCategoryCombo)
        
        self.customManageCategoryBtn = PushButton("管理分类")
        self.customManageCategoryBtn.clicked.connect(self.manage_categories_requested.emit)
        custom_category_layout.addWidget(self.customManageCategoryBtn)
        
        layout.addWidget(BodyLabel("分类:"))
        layout.addLayout(custom_category_layout)
        
        self.saveAsTemplateBtn = CheckBox("保存为自定义模版")
        layout.addWidget(self.saveAsTemplateBtn)
        
        layout.addStretch()
        self.refresh_categories()

    def refresh_categories(self):
        current_text = self.customCategoryCombo.currentText()
        self.customCategoryCombo.clear()
        categories = self.user_manager.get_all_categories()
        for category in categories:
            self.customCategoryCombo.addItem(category.name)
        index = self.customCategoryCombo.findText(current_text)
        if index >= 0:
            self.customCategoryCombo.setCurrentIndex(index)
