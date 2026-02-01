"""
模板编辑对话框
用于添加或编辑模板
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QFileDialog
)
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, ComboBox,
    PushButton, TextEdit, FluentIcon, TransparentToolButton,
    InfoBar, InfoBarPosition, BodyLabel
)
from ...components import CategorySelector, ValidatedLineEdit
from ...styles import format_required_label
from src.data.template_manager import TemplateManager
from src.data.category_manager import CategoryManager
from src.data.model import Template
from src.common.validators import PathValidator, NameValidator


class TemplateEditDialog(MessageBoxBase):
    """模板编辑对话框"""
    
    def __init__(
        self,
        template_manager: TemplateManager,
        category_manager: CategoryManager,
        template: Optional[Template] = None,
        default_category_id: Optional[str] = None,
        mode: str = "create",
        parent=None
    ):
        """
        初始化模板编辑对话框
        
        Args:
            template_manager: 模板管理器
            category_manager: 分类管理器
            template: 要编辑的模板（None 表示新建）
            mode: 模式 ("create" 或 "edit")
            parent: 父窗口
        """
        super().__init__(parent)
        self.template_manager = template_manager
        self.category_manager = category_manager
        self.template = template
        self.default_category_id = default_category_id
        self.mode = mode
        
        self._init_ui()
        self._load_data()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        title = "编辑模板" if self.mode == "edit" else "新建模板"
        self.titleLabel = SubtitleLabel(title, self)
        
        # 表单布局
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # 统一样式常量（非硬编码，引用自组件逻辑）
        LABEL_WIDTH = 100
        CONTENT_WIDTH = 380
        
        # 模板名称
        self.nameLabel = BodyLabel(format_required_label('模板名称'), self)
        self.nameEdit = ValidatedLineEdit(self)
        self.nameEdit.addValidator(NameValidator())
        self.nameEdit.setPlaceholderText('输入模板名称')
        self.nameEdit.setFixedWidth(CONTENT_WIDTH)
        form_layout.addRow(self.nameLabel, self.nameEdit)
        
        # 标源路径
        self.srcLabel = BodyLabel(format_required_label('源路径'), self)
        src_widget = QWidget()
        src_layout = QHBoxLayout(src_widget)
        src_layout.setContentsMargins(0, 0, 0, 0)
        src_layout.setSpacing(8)
        
        self.srcEdit = ValidatedLineEdit(self)
        self.srcEdit.addValidator(PathValidator())
        self.srcEdit.setPlaceholderText('C:\\路径\\到\\源文件夹 (支持环境变量)')
        # 自动计算宽度：CONTENT_WIDTH - 按钮宽度(60) - 间距(8) = 312
        self.srcEdit.setFixedWidth(CONTENT_WIDTH - 68)
        
        self.srcBrowseBtn = PushButton('浏览', self)
        self.srcBrowseBtn.setFixedWidth(60)
        
        src_layout.addWidget(self.srcEdit)
        src_layout.addWidget(self.srcBrowseBtn)
        form_layout.addRow(self.srcLabel, src_widget)
        
        # 目标路径
        self.targetLabel = BodyLabel('目标路径', self)
        target_widget = QWidget()
        target_layout = QHBoxLayout(target_widget)
        target_layout.setContentsMargins(0, 0, 0, 0)
        target_layout.setSpacing(8)
        
        self.targetEdit = ValidatedLineEdit(self)
        self.targetEdit.addValidator(PathValidator())
        self.targetEdit.setPlaceholderText('D:\\路径\\到\\目标文件夹 (可选，留空使用全局默认)')
        self.targetEdit.setFixedWidth(CONTENT_WIDTH - 68)
        
        self.targetBrowseBtn = PushButton('浏览', self)
        self.targetBrowseBtn.setFixedWidth(60)
        
        target_layout.addWidget(self.targetEdit)
        target_layout.addWidget(self.targetBrowseBtn)
        form_layout.addRow(self.targetLabel, target_widget)
        
        # 分类选择 (使用公共组件)
        self.categoryLabel = BodyLabel(format_required_label('分类'), self)
        self.categoryCombo = CategorySelector(self)
        self.categoryCombo.setFixedWidth(CONTENT_WIDTH)
        form_layout.addRow(self.categoryLabel, self.categoryCombo)
        
        # 描述
        self.descLabel = BodyLabel('描述', self)
        self.descEdit = TextEdit(self)
        self.descEdit.setPlaceholderText('输入模板描述（可选）')
        self.descEdit.setFixedHeight(80)
        self.descEdit.setFixedWidth(CONTENT_WIDTH)
        form_layout.addRow(self.descLabel, self.descEdit)
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(form_widget)
        
        # 按钮文本
        self.yesButton.setText('保存')
        self.cancelButton.setText('取消')
        
        # 设置对话框大小
        self.widget.setMinimumWidth(500)
    
    def _load_data(self):
        """加载数据"""
        # 1. 使用公共组件加载分类列表
        self.categoryCombo.set_manager(self.category_manager)
        
        # 2. 如果是编辑模式，填充现有数据
        if self.mode == "edit" and self.template:
            self.nameEdit.setText(self.template.name)
            
            # 使用标准化路径回显
            source_path = PathValidator().normalize(self.template.default_src)
            self.srcEdit.setText(source_path)
            
            # 目标路径（可选）
            if hasattr(self.template, 'default_target') and self.template.default_target:
                target_path = PathValidator().normalize(self.template.default_target)
                self.targetEdit.setText(target_path)
            
            # 描述
            if self.template.description:
                self.descEdit.setPlainText(self.template.description)
            
            # 3. 选中分类 (通过组件方法精准选中)
            category_id = getattr(self.template, 'category_id', getattr(self.template, 'category', None))
            print(f"[DEBUG] Raw category_id from template object: '{category_id}'")
            if category_id:
                self.categoryCombo.set_value(category_id)
        
        # 3. 如果是新建模式且有默认分类
        elif self.mode == "create" and self.default_category_id:
            # 只有当它是叶子节点时才预选（符合业务逻辑）
            if self.category_manager.is_leaf(self.default_category_id):
                self.categoryCombo.set_value(self.default_category_id)

    
    def _connect_signals(self):
        """连接信号"""
        self.srcBrowseBtn.clicked.connect(self._on_src_browse_clicked)
        self.targetBrowseBtn.clicked.connect(self._on_target_browse_clicked)
    
    def _on_src_browse_clicked(self):
        """浏览源路径"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择源文件夹",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            # 标准化路径
            folder = PathValidator().normalize(folder)
            self.srcEdit.setText(folder)
    
    def _on_target_browse_clicked(self):
        """浏览目标路径"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择目标文件夹",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            # 标准化路径
            folder = PathValidator().normalize(folder)
            self.targetEdit.setText(folder)
    
    def validate(self) -> bool:
        """
        验证输入
        
        Returns:
            True 如果验证通过
        """
        # 验证名称
        name = self.nameEdit.text().strip()
        if not name:
            InfoBar.warning(
                title='验证失败',
                content='模板名称不能为空',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        # 验证源路径
        src_path = self.srcEdit.text().strip()
        if not src_path:
            InfoBar.warning(
                title='验证失败',
                content='源路径不能为空',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        # 验证分类
        category_id = self.categoryCombo.currentData()
        if not category_id:
            InfoBar.warning(
                title='验证失败',
                content='请选择分类',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        # 验证分类是否为叶子分类
        if not self.category_manager.is_leaf(category_id):
            category_name = self.category_manager.get_category_by_id(category_id).name
            InfoBar.warning(
                title='验证失败',
                content=f'分类 "{category_name}" 不是叶子分类，无法添加模板',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        return True
    
    def get_template(self) -> Template:
        """
        获取模板对象
        
        Returns:
            模板对象
        """
        from datetime import datetime
        
        if self.mode == "edit" and self.template:
            # 更新现有模板
            self.template.name = self.nameEdit.text().strip()
            self.template.default_src = self.srcEdit.text().strip()
            self.template.category_id = self.categoryCombo.currentData()
            self.template.default_target = self.targetEdit.text().strip() or None
            self.template.description = self.descEdit.toPlainText().strip() or None
            self.template.updated_at = datetime.now().isoformat()
            return self.template
        else:
            # 创建新模板
            # 生成ID
            import re
            name = self.nameEdit.text().strip()
            template_id = re.sub(r'[^\w\s-]', '', name)
            template_id = re.sub(r'[-\s]+', '_', template_id).lower()
            
            # 确保ID唯一
            original_id = template_id
            counter = 1
            while template_id in self.template_manager.templates:
                template_id = f"{original_id}_{counter}"
                counter += 1
            
            return Template(
                id=template_id,
                name=name,
                default_src=self.srcEdit.text().strip(),
                category_id=self.categoryCombo.currentData(),
                default_target=self.targetEdit.text().strip() or None,
                description=self.descEdit.toPlainText().strip() or None,
                is_custom=True,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
