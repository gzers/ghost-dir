from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import MessageBoxBase, LineEdit, BodyLabel, PushButton, InfoBar, InfoBarPosition
from src.data.user_manager import UserManager
from src.data.category_manager import CategoryManager
from src.gui.components import CategorySelector
from src.data.model import UserLink, LinkStatus
from src.gui.i18n import t
from src.gui.styles import format_required_label
from src.common.validators import PathValidator

class EditLinkDialog(MessageBoxBase):
    """编辑链接对话框"""
    
    link_updated = Signal()
    
    def __init__(self, link: UserLink, parent=None):
        super().__init__(parent)
        self.link = link
        self.user_manager = UserManager()
        self.category_manager = CategoryManager()
        
        self.setWindowTitle(t("connected.edit_link"))
        self.is_connected = self.link.status == LinkStatus.CONNECTED
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = self.viewLayout
        layout.setSpacing(12)
        
        # 软件名称
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText(t("connected.link_name_placeholder"))
        layout.addWidget(BodyLabel(format_required_label(t("connected.link_name"))))
        layout.addWidget(self.nameEdit)
        
        # 源路径
        self.sourceEdit = LineEdit()
        self.sourceEdit.setPlaceholderText("C:\\...")
        self.sourceEdit.setReadOnly(self.is_connected)
        layout.addWidget(BodyLabel(format_required_label(t("connected.source_path"))))
        layout.addWidget(self.sourceEdit)
        
        # 目标路径
        self.targetEdit = LineEdit()
        self.targetEdit.setPlaceholderText("D:\\...")
        self.targetEdit.setReadOnly(self.is_connected)
        layout.addWidget(BodyLabel(format_required_label(t("connected.target_path"))))
        layout.addWidget(self.targetEdit)

        # 锁定提示
        if self.is_connected:
            tip_label = BodyLabel(t("connected.edit_path_locked_tip"))
            tip_label.setStyleSheet("color: #E21; font-size: 12px; font-weight: semibold;") # 强化警告
            layout.addWidget(tip_label)
        
        # 分类
        self.categorySelector = CategorySelector()
        self.categorySelector.set_manager(self.category_manager)
        
        layout.addWidget(BodyLabel(format_required_label(t("connected.category"))))
        layout.addWidget(self.categorySelector)
        
        # 按钮
        self.yesButton.setText(t("common.save"))
        self.cancelButton.setText(t("common.cancel"))
        
        self.widget.setMinimumWidth(500)

    def _load_data(self):
        """加载现有数据"""
        self.nameEdit.setText(self.link.name)
        self.sourceEdit.setText(self.link.source_path)
        self.targetEdit.setText(self.link.target_path)
        self.categorySelector.set_value(self.link.category)

    def validate(self):
        """提交验证"""
        name = self.nameEdit.text().strip()
        source = self.sourceEdit.text().strip()
        target = self.targetEdit.text().strip()
        category_id = self.categorySelector.get_value()
        
        def show_warning(content):
            InfoBar.warning(
                title="验证失败",
                content=content,
                orient=Qt.Orientation.Horizontal,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

        if not name:
            show_warning("连接名称不能为空")
            return False
        if not source:
            show_warning("源路径不能为空")
            return False
        if not target:
            show_warning("目标路径不能为空")
            return False
        if not category_id:
            show_warning("请选择所属分类")
            return False
            
        # 验证分类是否为叶子节点
        if not self.category_manager.is_leaf(category_id):
            show_warning("请选择具体的末级分类")
            return False
        
        # 更新对象
        self.link.name = name
        self.link.category = category_id
        
        # 如果未连接，允许更新路径
        if not self.is_connected:
            validator = PathValidator()
            self.link.source_path = validator.normalize(source)
            self.link.target_path = validator.normalize(target)
        
        # 保存到数据库
        if self.user_manager.update_link(self.link):
            self.link_updated.emit()
            return True
        else:
            show_warning("保存失败，请检查路径冲突")
        
        return False

