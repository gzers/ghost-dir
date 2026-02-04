from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QWidget
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import MessageBoxBase, LineEdit, BodyLabel, PushButton, InfoBar, InfoBarPosition
from src.core.services.context import service_bus
from src.gui.components import CategorySelector
from src.data.model import UserLink, LinkStatus
from src.gui.i18n import t
from src.gui.styles import format_required_label

class EditLinkDialog(MessageBoxBase):
    """编辑链接对话框"""
    
    link_updated = Signal()
    
    def __init__(self, link: UserLink, parent=None):
        super().__init__(parent)
        self.link = link
        self.connection_service = service_bus.connection_service
        self.category_manager = service_bus.category_manager
        
        self.setWindowTitle(t("connected.edit_link"))
        self.is_connected = self.link.status == LinkStatus.CONNECTED
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """初始化 UI"""
        # 使用 QFormLayout 实现 Label 与 Input 水平并排对齐
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 软件名称
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText(t("connected.link_name_placeholder"))
        form_layout.addRow(BodyLabel(format_required_label(t("connected.link_name"))), self.nameEdit)
        
        # 源路径
        self.sourceEdit = LineEdit()
        self.sourceEdit.setPlaceholderText("C:\\...")
        self.sourceEdit.setReadOnly(self.is_connected)
        form_layout.addRow(BodyLabel(format_required_label(t("connected.source_path"))), self.sourceEdit)
        
        # 目标路径
        self.targetEdit = LineEdit()
        self.targetEdit.setPlaceholderText("D:\\...")
        self.targetEdit.setReadOnly(self.is_connected)
        form_layout.addRow(BodyLabel(format_required_label(t("connected.target_path"))), self.targetEdit)

        # 锁定提示
        if self.is_connected:
            tip_label = BodyLabel(t("connected.edit_path_locked_tip"))
            tip_label.setStyleSheet("color: #E21; font-size: 12px; font-weight: semibold;")
            form_layout.addRow("", tip_label)
        
        # 分类
        self.categorySelector = CategorySelector()
        self.categorySelector.set_manager(self.category_manager)
        form_layout.addRow(BodyLabel(format_required_label(t("connected.category"))), self.categorySelector)
        
        # 将表单添加到主视图
        self.viewLayout.addWidget(form_widget)
        
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
        """提交验证并更新业务"""
        data = {
            "name": self.nameEdit.text(),
            "source": self.sourceEdit.text(),
            "target": self.targetEdit.text(),
            "category_id": self.categorySelector.get_value()
        }
        
        success, msg = self.connection_service.validate_and_update_link(self.link.id, data)
        
        if success:
            self.link_updated.emit()
            return True
        else:
            InfoBar.warning(
                title="验证失败",
                content=msg,
                orient=Qt.Orientation.Horizontal,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
        
        return False

