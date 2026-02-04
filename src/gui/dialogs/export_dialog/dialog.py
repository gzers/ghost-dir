"""
导出对话框
用于导出模板和分类
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QFileDialog, QCheckBox, QButtonGroup
)
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, PushButton,
    CheckBox, InfoBar
)
from src.data.template_manager import TemplateManager
from src.data.category_manager import CategoryManager


class ExportDialog(MessageBoxBase):
    """导出对话框"""
    
    def __init__(
        self,
        template_manager: TemplateManager,
        category_manager: CategoryManager,
        parent=None
    ):
        """
        初始化导出对话框
        
        Args:
            template_manager: 模板管理器
            category_manager: 分类管理器
            parent: 父窗口
        """
        super().__init__(parent)
        self.template_manager = template_manager
        self.category_manager = category_manager
        self.export_path = ""
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel('导出模板库', self)
        
        # 表单
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)
        
        # 导出选项
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(8)
        
        self.exportCategoriesCheck = CheckBox('导出所有分类', self)
        self.exportCategoriesCheck.setChecked(True)
        
        self.exportTemplatesCheck = CheckBox('导出所有模板', self)
        self.exportTemplatesCheck.setChecked(True)
        
        options_layout.addWidget(self.exportCategoriesCheck)
        options_layout.addWidget(self.exportTemplatesCheck)
        
        form_layout.addRow('导出内容:', options_widget)
        
        # 文件路径
        path_widget = QWidget()
        path_layout = QHBoxLayout(path_widget)
        path_layout.setContentsMargins(0, 0, 0, 0)
        path_layout.setSpacing(8)
        
        self.pathEdit = LineEdit(self)
        self.pathEdit.setPlaceholderText('选择导出文件路径')
        self.pathEdit.setFixedWidth(300)
        self.pathEdit.setReadOnly(True)
        
        self.browseBtn = PushButton('浏览', self)
        self.browseBtn.setFixedWidth(60)
        
        path_layout.addWidget(self.pathEdit)
        path_layout.addWidget(self.browseBtn)
        
        form_layout.addRow('保存到*:', path_widget)
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(form_widget)
        
        # 按钮文本
        self.yesButton.setText('导出')
        self.cancelButton.setText('取消')
        
        # 设置对话框大小
        self.widget.setMinimumWidth(450)
    
    def _connect_signals(self):
        """连接信号"""
        self.browseBtn.clicked.connect(self._on_browse_clicked)
    
    def _on_browse_clicked(self):
        """浏览按钮被点击"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "选择导出文件",
            "",
            "JSON Files (*.json)"
        )
        if file_path:
            if not file_path.endswith('.json'):
                file_path += '.json'
            self.export_path = file_path
            self.pathEdit.setText(file_path)
    
    def validate(self) -> bool:
        """验证输入"""
        if not self.export_path:
            InfoBar.warning(
                title='验证失败',
                content='请选择导出文件路径',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
        
        if not self.exportCategoriesCheck.isChecked() and not self.exportTemplatesCheck.isChecked():
            InfoBar.warning(
                title='验证失败',
                content='请至少选择一项导出内容',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
        
        return True
    
    def get_export_options(self):
        """获取导出选项"""
        return {
            'file_path': self.export_path,
            'include_categories': self.exportCategoriesCheck.isChecked(),
            'include_templates': self.exportTemplatesCheck.isChecked()
        }
