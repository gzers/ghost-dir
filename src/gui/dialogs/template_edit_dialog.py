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
    InfoBar, InfoBarPosition
)
from src.data.model import Template
from src.data.template_manager import TemplateManager
from src.data.category_manager import CategoryManager


class TemplateEditDialog(MessageBoxBase):
    """模板编辑对话框"""
    
    def __init__(
        self,
        template_manager: TemplateManager,
        category_manager: CategoryManager,
        template: Optional[Template] = None,
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
        
        # 模板名称
        self.nameEdit = LineEdit(self)
        self.nameEdit.setPlaceholderText('输入模板名称')
        self.nameEdit.setFixedWidth(350)
        form_layout.addRow('模板名称*:', self.nameEdit)
        
        # 源路径
        src_widget = QWidget()
        src_layout = QHBoxLayout(src_widget)
        src_layout.setContentsMargins(0, 0, 0, 0)
        src_layout.setSpacing(8)
        
        self.srcEdit = LineEdit(self)
        self.srcEdit.setPlaceholderText('C:\\路径\\到\\源文件夹 (支持环境变量)')
        self.srcEdit.setFixedWidth(300)
        
        self.srcBrowseBtn = PushButton('浏览', self)
        self.srcBrowseBtn.setFixedWidth(60)
        
        src_layout.addWidget(self.srcEdit)
        src_layout.addWidget(self.srcBrowseBtn)
        
        form_layout.addRow('源路径*:', src_widget)
        
        # 目标路径
        target_widget = QWidget()
        target_layout = QHBoxLayout(target_widget)
        target_layout.setContentsMargins(0, 0, 0, 0)
        target_layout.setSpacing(8)
        
        self.targetEdit = LineEdit(self)
        self.targetEdit.setPlaceholderText('D:\\路径\\到\\目标文件夹 (可选，留空使用全局默认)')
        self.targetEdit.setFixedWidth(300)
        
        self.targetBrowseBtn = PushButton('浏览', self)
        self.targetBrowseBtn.setFixedWidth(60)
        
        target_layout.addWidget(self.targetEdit)
        target_layout.addWidget(self.targetBrowseBtn)
        
        form_layout.addRow('目标路径:', target_widget)
        
        # 分类选择
        self.categoryCombo = ComboBox(self)
        self.categoryCombo.setFixedWidth(350)
        self.categoryCombo.setPlaceholderText('选择分类')
        form_layout.addRow('分类*:', self.categoryCombo)
        
        # 描述
        self.descEdit = TextEdit(self)
        self.descEdit.setPlaceholderText('输入模板描述（可选）')
        self.descEdit.setFixedHeight(80)
        self.descEdit.setFixedWidth(350)
        form_layout.addRow('描述:', self.descEdit)
        
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
        # 加载分类列表（只显示叶子分类）
        for category in self.category_manager.get_all_categories():
            if self.category_manager.is_leaf(category.id):
                # 显示分类层级
                depth = category.get_depth(self.category_manager.categories)
                indent = "  " * (depth - 1)
                display_name = f"{indent}{category.name}"
                
                self.categoryCombo.addItem(display_name, category.id)
        
        # 如果是编辑模式，填充现有数据
        if self.mode == "edit" and self.template:
            self.nameEdit.setText(self.template.name)
            self.srcEdit.setText(self.template.default_src)
            
            # 目标路径（可选）
            if hasattr(self.template, 'default_target') and self.template.default_target:
                self.targetEdit.setText(self.template.default_target)
            
            # 描述
            if self.template.description:
                self.descEdit.setPlainText(self.template.description)
            
            # 选中分类
            category_id = getattr(self.template, 'category_id', self.template.category)
            for i in range(self.categoryCombo.count()):
                if self.categoryCombo.itemData(i) == category_id:
                    self.categoryCombo.setCurrentIndex(i)
                    break
    
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
            template_id = re.sub(r'[^\w\s-]', '', self.nameEdit.text().strip())
            template_id = re.sub(r'[-\s]+', '_', template_id).lower()
            
            # 确保ID唯一
            original_id = template_id
            counter = 1
            while template_id in self.template_manager.templates:
                template_id = f"{original_id}_{counter}"
                counter += 1
            
            return Template(
                id=template_id,
                name=self.nameEdit.text().strip(),
                default_src=self.srcEdit.text().strip(),
                category_id=self.categoryCombo.currentData(),
                default_target=self.targetEdit.text().strip() or None,
                description=self.descEdit.toPlainText().strip() or None,
                is_custom=True,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
