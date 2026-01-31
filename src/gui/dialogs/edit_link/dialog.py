"""
编辑链接对话框
"""
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal
from qfluentwidgets import MessageBoxBase, LineEdit, BodyLabel, ComboBox, PushButton
from ....data.user_manager import UserManager
from ....data.model import UserLink
from ...i18n import t


class EditLinkDialog(MessageBoxBase):
    """编辑链接对话框"""
    
    link_updated = Signal()
    
    def __init__(self, link: UserLink, parent=None):
        super().__init__(parent)
        self.link = link
        self.user_manager = UserManager()
        
        self.setWindowTitle(t("connected.edit_link"))
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
        self.sourceEdit.setReadOnly(True)  # 源路径通常不建议修改，因为事务已建立
        layout.addWidget(BodyLabel(t("connected.source_path")))
        layout.addWidget(self.sourceEdit)
        
        # 目标路径
        self.targetEdit = LineEdit()
        self.targetEdit.setPlaceholderText("D:\\...")
        self.targetEdit.setReadOnly(True)  # 同上
        layout.addWidget(BodyLabel(t("connected.target_path")))
        layout.addWidget(self.targetEdit)
        
        # 分类
        self.categoryCombo = ComboBox()
        category_row = QHBoxLayout()
        category_row.addWidget(self.categoryCombo)
        
        layout.addWidget(BodyLabel(t("connected.category")))
        layout.addLayout(category_row)
        
        # 刷新并填充分类
        self._refresh_categories()
        
        # 按钮
        self.yesButton.setText(t("common.save"))
        self.cancelButton.setText(t("common.cancel"))
        
        self.widget.setMinimumWidth(500)

    def _refresh_categories(self):
        """加载分类列表"""
        self.categoryCombo.clear()
        categories = self.user_manager.get_all_categories()
        for cat in categories:
            self.categoryCombo.addItem(cat.name, cat.id)

    def _load_data(self):
        """加载现有数据"""
        self.nameEdit.setText(self.link.name)
        self.sourceEdit.setText(self.link.source_path)
        self.targetEdit.setText(self.link.target_path)
        
        # 匹配分类
        index = self.categoryCombo.findText(self.link.category)
        if index >= 0:
            self.categoryCombo.setCurrentIndex(index)

    def validate(self):
        """提交验证"""
        name = self.nameEdit.text().strip()
        category = self.categoryCombo.currentText()
        
        if not name:
            return False
        
        # 更新对象
        self.link.name = name
        self.link.category = category
        
        # 保存到数据库
        if self.user_manager.update_link(self.link):
            self.link_updated.emit()
            return True
        
        return False
