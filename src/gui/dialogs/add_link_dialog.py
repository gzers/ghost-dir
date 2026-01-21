"""
新增连接对话框
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, BodyLabel, LineEdit,
    PushButton, ComboBox
)
from ...data.template_manager import TemplateManager
from ...data.user_manager import UserManager
from ...data.model import UserLink, Template
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
        from PySide6.QtWidgets import QTabWidget
        
        # 创建标签页
        self.tabWidget = QTabWidget()
        
        # Tab 1: 从模版库选择
        self.templateTab = self._create_template_tab()
        self.tabWidget.addTab(self.templateTab, "从模版库选择")
        
        # Tab 2: 自定义
        self.customTab = self._create_custom_tab()
        self.tabWidget.addTab(self.customTab, "自定义")
        
        # 添加到视图
        self.viewLayout.addWidget(self.tabWidget)
        
        # 按钮
        self.yesButton.setText("添加")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(600)
        self.widget.setMinimumHeight(500)
    
    def _create_template_tab(self) -> QWidget:
        """创建模版选择标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
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
        self.templateList.itemClicked.connect(self._on_template_selected)
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
        self._load_categories()
        
        # 分类选择行（下拉框 + 管理按钮）
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.categoryCombo)
        
        self.manageCategoryBtn = PushButton("管理分类")
        self.manageCategoryBtn.clicked.connect(self._on_manage_categories)
        category_layout.addWidget(self.manageCategoryBtn)
        
        details_layout.addWidget(BodyLabel("分类:"))
        details_layout.addLayout(category_layout)
        
        layout.addLayout(details_layout)
        
        # 加载模版
        self._load_templates()
        
        return widget
    
    def _create_custom_tab(self) -> QWidget:
        """创建自定义标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
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
        self._load_categories(self.customCategoryCombo)
        
        # 分类选择行
        custom_category_layout = QHBoxLayout()
        custom_category_layout.addWidget(self.customCategoryCombo)
        
        self.customManageCategoryBtn = PushButton("管理分类")
        self.customManageCategoryBtn.clicked.connect(self._on_manage_categories)
        custom_category_layout.addWidget(self.customManageCategoryBtn)
        
        layout.addWidget(BodyLabel("分类:"))
        layout.addLayout(custom_category_layout)
        
        layout.addStretch()
        
        return widget
    
    def _load_templates(self):
        """加载模版列表"""
        self.templateList.clear()
        templates = self.template_manager.get_all_templates()
        
        for template in templates:
            item = QListWidgetItem(f"{template.name} ({template.category})")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)
    
    def _load_categories(self, combo=None):
        """加载分类列表"""
        if combo is None:
            combo = self.categoryCombo
        
        combo.clear()
        categories = self.user_manager.get_all_categories()
        for category in categories:
            combo.addItem(category.name)
    
    def _on_search_changed(self, text: str):
        """搜索变更"""
        if not text:
            self._load_templates()
            return
        
        self.templateList.clear()
        templates = self.template_manager.search_templates(text)
        
        for template in templates:
            item = QListWidgetItem(f"{template.name} ({template.category})")
            item.setData(Qt.ItemDataRole.UserRole, template)
            self.templateList.addItem(item)
    
    def _on_template_selected(self, item: QListWidgetItem):
        """模版选中"""
        template = item.data(Qt.ItemDataRole.UserRole)
        self.selected_template = template
        
        # 自动填充
        self.nameEdit.setText(template.name)
        
        source_path = self.template_manager.expand_path(template.default_src)
        self.sourceEdit.setText(source_path)
        
        # 自动生成目标路径
        target_path = "D:\\" + source_path[3:]  # C:\xxx -> D:\xxx
        self.targetEdit.setText(target_path)
        
        # 设置分类
        index = self.categoryCombo.findText(template.category)
        if index >= 0:
            self.categoryCombo.setCurrentIndex(index)
    
    def _on_manage_categories(self):
        """打开分类管理对话框（层叠弹窗）"""
        from .category_manager import CategoryManagerDialog
        
        # 创建层叠对话框
        dialog = CategoryManagerDialog(self)
        
        # 连接信号：分类变更时刷新下拉框
        dialog.categories_changed.connect(self._refresh_categories)
        
        # 显示对话框（模态）
        dialog.exec()
    
    def _refresh_categories(self):
        """刷新分类下拉框（保持当前选择）"""
        # 保存当前选择
        current_text = self.categoryCombo.currentText()
        custom_current_text = self.customCategoryCombo.currentText()
        
        # 重新加载
        self._load_categories(self.categoryCombo)
        self._load_categories(self.customCategoryCombo)
        
        # 恢复选择
        index = self.categoryCombo.findText(current_text)
        if index >= 0:
            self.categoryCombo.setCurrentIndex(index)
        
        custom_index = self.customCategoryCombo.findText(custom_current_text)
        if custom_index >= 0:
            self.customCategoryCombo.setCurrentIndex(custom_index)
    
    def validate(self):
        """验证并添加"""
        # 判断当前标签页
        if self.tabWidget.currentIndex() == 0:  # 从模版添加
            name = self.nameEdit.text().strip()
            source = self.sourceEdit.text().strip()
            target = self.targetEdit.text().strip()
            category = self.categoryCombo.currentText()
        else:  # 自定义添加
            name = self.customNameEdit.text().strip()
            source = self.customSourceEdit.text().strip()
            target = self.customTargetEdit.text().strip()
            category = self.customCategoryCombo.currentText()
        
        # 验证
        if not name or not source or not target:
            return False
        
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
            self.link_added.emit()
            return True
        
        return False
