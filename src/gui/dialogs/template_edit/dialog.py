from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QFileDialog
)
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, ComboBox,
    PushButton, TextEdit, FluentIcon, TransparentToolButton,
    InfoBar, BodyLabel
)
from src.gui.components import CategorySelector, ValidatedLineEdit
from src.gui.styles import format_required_label
# TODO: 通过 app 实例访问 Service,而不是 service_bus
from src.models.template import Template  # 新架构
from src.common.validators import PathValidator, NameValidator
from src.common.service_bus import service_bus


class TemplateEditDialog(MessageBoxBase):
    """模板编辑对话框"""

    def __init__(
        self,
        template: Optional[Template] = None,
        default_category_id: Optional[str] = None,
        mode: str = "create",
        parent=None
    ):
        """
        初始化模板编辑对话框
        """
        super().__init__(parent)
        self.template_service = service_bus.template_service
        self.category_manager = service_bus.category_manager

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

        # 统一样式常量
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

        self.widget.setMinimumWidth(500)

    def _load_data(self):
        """加载数据"""
        self.categoryCombo.set_manager(self.category_manager)

        if self.mode == "edit" and self.template:
            self.nameEdit.setText(self.template.name)
            self.srcEdit.setText(self.template.default_src)
            if hasattr(self.template, 'default_target') and self.template.default_target:
                self.targetEdit.setText(self.template.default_target)
            if self.template.description:
                self.descEdit.setPlainText(self.template.description)

            category_id = getattr(self.template, 'category_id', getattr(self.template, 'category', None))
            if category_id:
                self.categoryCombo.set_value(category_id)

        elif self.mode == "create" and self.default_category_id:
            if self.category_manager.is_leaf(self.default_category_id):
                self.categoryCombo.set_value(self.default_category_id)

    def _connect_signals(self):
        """连接信号"""
        self.srcBrowseBtn.clicked.connect(self._on_src_browse_clicked)
        self.targetBrowseBtn.clicked.connect(self._on_target_browse_clicked)

    def _on_src_browse_clicked(self):
        """浏览源路径"""
        folder = QFileDialog.getExistingDirectory(self, "选择源文件夹", "", QFileDialog.Option.ShowDirsOnly)
        if folder:
            self.srcEdit.setText(folder)

    def _on_target_browse_clicked(self):
        """浏览目标路径"""
        folder = QFileDialog.getExistingDirectory(self, "选择目标文件夹", "", QFileDialog.Option.ShowDirsOnly)
        if folder:
            self.targetEdit.setText(folder)

    def validate(self) -> bool:
        """
        提交验证并持久化
        """
        data = {
            "name": self.nameEdit.text(),
            "default_src": self.srcEdit.text(),
            "default_target": self.targetEdit.text(),
            "category_id": self.categoryCombo.currentData(),
            "description": self.descEdit.toPlainText()
        }

        if self.mode == "edit":
            success, msg = self.template_service.update_template_from_data(self.template.id, data)
        else:
            success, msg = self.template_service.add_template_from_data(data)

        if success:
            return True
        else:
            InfoBar.warning(
                title='验证失败',
                content=msg,
                orient=Qt.Orientation.Horizontal,
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
