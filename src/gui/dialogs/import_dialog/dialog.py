"""
导入对话框
用于导入模板和分类
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QFileDialog, QRadioButton, QButtonGroup, QLabel
)
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, PushButton,
    BodyLabel, InfoBar
)
import json
from src.data.template_manager import  # TODO: 迁移到 TemplateService TemplateManager
from src.data.category_manager import  # TODO: 迁移到 CategoryService CategoryManager
from src.common.validators import PathValidator


class ImportDialog(MessageBoxBase):
    """导入对话框"""
    
    def __init__(
        self,
        template_manager: TemplateManager,
        category_manager: CategoryManager,
        parent=None
    ):
        """
        初始化导入对话框
        
        Args:
            template_manager: 模板管理器
            category_manager: 分类管理器
            parent: 父窗口
        """
        super().__init__(parent)
        self.template_manager = template_manager
        self.category_manager = category_manager
        self.import_path = ""
        self.preview_data = None
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel('导入模板库', self)
        
        # 表单
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)
        
        # 文件路径
        path_widget = QWidget()
        path_layout = QHBoxLayout(path_widget)
        path_layout.setContentsMargins(0, 0, 0, 0)
        path_layout.setSpacing(8)
        
        self.pathEdit = LineEdit(self)
        self.pathEdit.setPlaceholderText('选择导入文件')
        self.pathEdit.setFixedWidth(300)
        self.pathEdit.setReadOnly(True)
        
        self.browseBtn = PushButton('浏览', self)
        self.browseBtn.setFixedWidth(60)
        
        path_layout.addWidget(self.pathEdit)
        path_layout.addWidget(self.browseBtn)
        
        form_layout.addRow('文件路径*:', path_widget)
        
        # 预览信息
        self.previewLabel = BodyLabel('', self)
        self.previewLabel.setWordWrap(True)
        form_layout.addRow('预览:', self.previewLabel)
        
        # 冲突处理策略
        strategy_widget = QWidget()
        strategy_layout = QVBoxLayout(strategy_widget)
        strategy_layout.setContentsMargins(0, 0, 0, 0)
        strategy_layout.setSpacing(8)
        
        self.strategyGroup = QButtonGroup(self)
        
        self.skipRadio = QRadioButton('跳过已存在的', self)
        self.skipRadio.setChecked(True)
        self.strategyGroup.addButton(self.skipRadio, 0)
        
        self.overwriteRadio = QRadioButton('覆盖已存在的', self)
        self.strategyGroup.addButton(self.overwriteRadio, 1)
        
        self.renameRadio = QRadioButton('重命名导入的', self)
        self.strategyGroup.addButton(self.renameRadio, 2)
        
        strategy_layout.addWidget(self.skipRadio)
        strategy_layout.addWidget(self.overwriteRadio)
        strategy_layout.addWidget(self.renameRadio)
        
        form_layout.addRow('冲突处理:', strategy_widget)
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(form_widget)
        
        # 按钮文本
        self.yesButton.setText('导入')
        self.cancelButton.setText('取消')
        
        # 设置对话框大小
        self.widget.setMinimumWidth(450)
    
    def _connect_signals(self):
        """连接信号"""
        self.browseBtn.clicked.connect(self._on_browse_clicked)
    
    def _on_browse_clicked(self):
        """浏览按钮被点击"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择导入文件",
            "",
            "ZIP Files (*.zip)"
        )
        if file_path:
            # 标准化路径，移除 \\?\ 等前缀
            file_path = PathValidator().normalize(file_path)
            self.import_path = file_path
            self.pathEdit.setText(file_path)
            self._load_preview()
    
    def _load_preview(self):
        """加载预览信息"""
        try:
            import zipfile
            
            # 从 ZIP 文件读取元数据
            with zipfile.ZipFile(self.import_path, 'r') as zf:
                # 读取元数据
                if 'metadata.json' in zf.namelist():
                    metadata_json = zf.read('metadata.json').decode('utf-8')
                    metadata = json.loads(metadata_json)
                    
                    category_count = metadata.get('categories_count', 0)
                    template_count = metadata.get('templates_count', 0)
                    export_date = metadata.get('export_date', '未知')
                    
                    preview_text = f"将导入 {category_count} 个分类和 {template_count} 个模板\n"
                    preview_text += f"导出时间: {export_date}"
                    
                    self.previewLabel.setText(preview_text)
                    self.preview_data = metadata
                else:
                    # 没有元数据,尝试读取分类和模板数据
                    categories_data = []
                    templates_data = []
                    
                    if 'categories.json' in zf.namelist():
                        categories_json = zf.read('categories.json').decode('utf-8')
                        categories_data = json.loads(categories_json)
                    
                    if 'templates.json' in zf.namelist():
                        templates_json = zf.read('templates.json').decode('utf-8')
                        templates_data = json.loads(templates_json)
                    
                    preview_text = f"将导入 {len(categories_data)} 个分类和 {len(templates_data)} 个模板"
                    self.previewLabel.setText(preview_text)
                    self.preview_data = {'categories_count': len(categories_data), 'templates_count': len(templates_data)}
            
        except Exception as e:
            self.previewLabel.setText(f'读取文件失败: {str(e)}')
            self.preview_data = None
    
    def validate(self) -> bool:
        """验证输入"""
        if not self.import_path:
            InfoBar.warning(
                title='验证失败',
                content='请选择导入文件',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
        
        if not self.preview_data:
            InfoBar.warning(
                title='验证失败',
                content='无法读取导入文件',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
        
        return True
    
    def get_import_options(self):
        """获取导入选项"""
        strategy_map = {
            0: 'skip',
            1: 'overwrite',
            2: 'rename'
        }
        
        return {
            'file_path': self.import_path,
            'conflict_strategy': strategy_map[self.strategyGroup.checkedId()]
        }
