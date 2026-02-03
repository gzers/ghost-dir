"""
编辑链接对话框
"""
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal
from qfluentwidgets import MessageBoxBase, LineEdit, BodyLabel, PushButton
from src.data.user_manager import UserManager
from src.data.category_manager import CategoryManager
from src.gui.components import CategorySelector
from src.data.model import UserLink, LinkStatus
from src.gui.i18n import t


class EditLinkDialog(MessageBoxBase):
    """编辑链接对话框"""
    
    link_updated = Signal()
    
    def __init__(self, link: UserLink, parent=None):
        super().__init__(parent)
        self.link = link
        self.user_manager = UserManager()
        
        self.setWindowTitle(t("connected.edit_link"))
        self.is_connected = self.link.status == LinkStatus.CONNECTED
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = self.viewLayout
        
        # 软件名称
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText(t("connected.link_name_placeholder"))
        layout.addWidget(BodyLabel(t("connected.link_name")))
        layout.addWidget(self.nameEdit)
        
        # 源路径
        self.sourceEdit = LineEdit()
        self.sourceEdit.setPlaceholderText("C:\\...")
        self.sourceEdit.setReadOnly(self.is_connected)
        layout.addWidget(BodyLabel(t("connected.source_path")))
        layout.addWidget(self.sourceEdit)
        
        # 目标路径
        self.targetEdit = LineEdit()
        self.targetEdit.setPlaceholderText("D:\\...")
        self.targetEdit.setReadOnly(self.is_connected)
        layout.addWidget(BodyLabel(t("connected.target_path")))
        layout.addWidget(self.targetEdit)

        # 锁定提示
        if self.is_connected:
            tip_label = BodyLabel(t("connected.edit_path_locked_tip"))
            tip_label.setStyleSheet("color: #666; font-size: 12px;")
            layout.addWidget(tip_label)
        
        # 分类
        self.categorySelector = CategorySelector()
        self.category_manager = CategoryManager()
        self.categorySelector.set_manager(self.category_manager)
        
        layout.addWidget(BodyLabel(t("connected.category")))
        layout.addWidget(self.categorySelector)
        
        # 按钮
        self.yesButton.setText(t("common.save"))
        self.cancelButton.setText(t("common.cancel"))
        
        self.widget.setMinimumWidth(500)

    # 移除旧的 _refresh_categories，CategorySelector 自带管理功能

    def _load_data(self):
        """加载现有数据"""
        self.nameEdit.setText(self.link.name)
        self.sourceEdit.setText(self.link.source_path)
        self.targetEdit.setText(self.link.target_path)
        
        # 匹配分类 (回显 ID)
        self.categorySelector.set_value(self.link.category)

    def validate(self):
        """提交验证"""
        name = self.nameEdit.text().strip()
        category = self.categorySelector.get_value() or "uncategorized"
        
        if not name:
            return False
        
        # 更新对象
        self.link.name = name
        self.link.category = category
        
        # 如果未连接，允许更新路径
        if not self.is_connected:
            self.link.source_path = self.sourceEdit.text().strip()
            self.link.target_path = self.targetEdit.text().strip()
        
        # 保存到数据库
        if self.user_manager.update_link(self.link):
            self.link_updated.emit()
            return True
        
        return False
