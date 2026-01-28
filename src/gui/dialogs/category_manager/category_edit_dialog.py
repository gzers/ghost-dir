"""
分类编辑对话框
用于添加或编辑分类
"""
from typing import Optional
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel
)
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, ComboBox,
    PushButton, SpinBox, FluentIcon, TransparentToolButton,
    InfoBar, InfoBarPosition
)
from src.data.model import CategoryNode
from src.data.category_manager import CategoryManager
from ..icon_picker import IconPickerDialog
from ...i18n import t


class CategoryEditDialog(MessageBoxBase):
    """分类编辑对话框"""
    
    def __init__(
        self,
        category_manager: CategoryManager,
        category: Optional[CategoryNode] = None,
        mode: str = "create",
        parent=None
    ):
        """
        初始化分类编辑对话框
        
        Args:
            category_manager: 分类管理器
            category: 要编辑的分类（None 表示新建）
            mode: 模式 ("create" 或 "edit")
            parent: 父窗口
        """
        super().__init__(parent)
        self.category_manager = category_manager
        self.category = category
        self.mode = mode
        self.selected_icon = category.icon if category else "Folder"
        
        self.setWindowTitle(t("library.dialog_rename_category") if self.mode == "edit" else t("library.dialog_new_category"))
        self._init_ui()
        self._load_data()
        self._connect_signals()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        title = t("library.dialog_rename_category") if self.mode == "edit" else t("library.dialog_new_category")
        self.titleLabel = SubtitleLabel(title, self)
        
        # 表单布局
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # 分类名称
        self.nameEdit = LineEdit(self)
        self.nameEdit.setPlaceholderText(t("library.placeholder_category_name"))
        self.nameEdit.setFixedWidth(300)
        form_layout.addRow(t("library.label_category_name"), self.nameEdit)
        
        # 父分类
        self.parentCombo = ComboBox(self)
        self.parentCombo.setFixedWidth(300)
        self.parentCombo.setPlaceholderText(t("library.placeholder_parent_category"))
        form_layout.addRow(t("library.label_parent_category"), self.parentCombo)
        
        # 图标选择
        icon_widget = QWidget()
        icon_layout = QHBoxLayout(icon_widget)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(8)
        
        self.iconButton = TransparentToolButton(FluentIcon.FOLDER, self)
        self.iconButton.setFixedSize(48, 48)
        self.iconButton.setIconSize(QSize(32, 32))
        self.iconButton.setToolTip(t("library.tooltip_select_icon"))
        
        self.iconLabel = QLabel(self.selected_icon, self)
        self.iconLabel.setStyleSheet('color: gray;')
        
        icon_layout.addWidget(self.iconButton)
        icon_layout.addWidget(self.iconLabel)
        icon_layout.addStretch()
        
        form_layout.addRow(t("library.label_icon"), icon_widget)
        
        # 排序权重
        self.orderSpin = SpinBox(self)
        self.orderSpin.setRange(0, 999)
        self.orderSpin.setValue(0)
        self.orderSpin.setFixedWidth(150)
        form_layout.addRow(t("library.label_order"), self.orderSpin)
        
        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(form_widget)
        
        # 按钮文本
        self.yesButton.setText(t("library.btn_save"))
        self.cancelButton.setText(t("library.btn_cancel"))
        
        # 设置对话框大小
        self.widget.setMinimumWidth(450)
    
    def _load_data(self):
        """加载数据"""
        # 加载父分类列表
        self.parentCombo.addItem(t("library.label_root_category"), None)
        
        for category in self.category_manager.get_all_categories():
            # 编辑模式下，不能选择自己作为父分类
            if self.mode == "edit" and self.category and category.id == self.category.id:
                continue
            
            # 不能选择自己的子孙分类作为父分类
            if self.mode == "edit" and self.category:
                descendants = self.category_manager._get_all_descendants(self.category.id)
                if any(d.id == category.id for d in descendants):
                    continue
            
            # 显示分类层级
            depth = category.get_depth(self.category_manager.categories)
            indent = "  " * (depth - 1)
            display_name = f"{indent}{category.name}"
            
            self.parentCombo.addItem(display_name, category.id)
        
        # 如果是编辑模式，填充现有数据
        if self.mode == "edit" and self.category:
            self.nameEdit.setText(self.category.name)
            self.orderSpin.setValue(self.category.order)
            self.selected_icon = self.category.icon
            self._update_icon_display()
            
            # 选中父分类
            if self.category.parent_id:
                for i in range(self.parentCombo.count()):
                    if self.parentCombo.itemData(i) == self.category.parent_id:
                        self.parentCombo.setCurrentIndex(i)
                        break
    
    def _connect_signals(self):
        """连接信号"""
        self.iconButton.clicked.connect(self._on_icon_button_clicked)
    
    def _on_icon_button_clicked(self):
        """图标按钮被点击"""
        dialog = IconPickerDialog(self.selected_icon, self)
        if dialog.exec():
            self.selected_icon = dialog.get_selected_icon()
            self._update_icon_display()
    
    def _update_icon_display(self):
        """更新图标显示"""
        try:
            icon = getattr(FluentIcon, self.selected_icon, FluentIcon.FOLDER)
            self.iconButton.setIcon(icon)
            self.iconLabel.setText(self.selected_icon)
        except:
            self.iconButton.setIcon(FluentIcon.FOLDER)
            self.iconLabel.setText("Folder")
    
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
                title=t("common.failed"),
                content=t("library.error_empty_name"),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        # 获取父分类ID
        parent_id = self.parentCombo.currentData()
        
        # 如果选择了父分类，验证是否可以添加子分类
        if parent_id and self.mode == "create":
            can_add, msg = self.category_manager.can_add_child_category(parent_id)
            if not can_add:
                InfoBar.warning(
                    title=t("common.failed"),
                    content=msg,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                return False
        
        # 验证深度（如果是新建或修改了父分类）
        if self.mode == "create" or (self.category and self.category.parent_id != parent_id):
            # 创建临时分类对象来计算深度
            temp_category = CategoryNode(
                id=self.category.id if self.category else "temp",
                name=name,
                parent_id=parent_id,
                icon=self.selected_icon,
                order=self.orderSpin.value()
            )
            
            depth = temp_category.get_depth(self.category_manager.categories)
            from ....common.config import MAX_CATEGORY_DEPTH
            
            if depth > MAX_CATEGORY_DEPTH:
                InfoBar.warning(
                    title=t("common.failed"),
                    content=t("library.help_notes_3"), # 复用层级限制说明或者建新key，这里复用
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                return False
        
        return True
    
    def get_category(self) -> CategoryNode:
        """
        获取分类对象
        
        Returns:
            分类对象
        """
        if self.mode == "edit" and self.category:
            # 更新现有分类
            self.category.name = self.nameEdit.text().strip()
            self.category.parent_id = self.parentCombo.currentData()
            self.category.icon = self.selected_icon
            self.category.order = self.orderSpin.value()
            return self.category
        else:
            # 创建新分类
            # 生成ID
            import re
            category_id = re.sub(r'[^\w\s-]', '', self.nameEdit.text().strip())
            category_id = re.sub(r'[-\s]+', '_', category_id).lower()
            
            # 如果有父分类，添加父分类前缀
            parent_id = self.parentCombo.currentData()
            if parent_id:
                category_id = f"{parent_id}.{category_id}"
            
            # 确保ID唯一
            original_id = category_id
            counter = 1
            while category_id in self.category_manager.categories:
                category_id = f"{original_id}_{counter}"
                counter += 1
            
            return CategoryNode(
                id=category_id,
                name=self.nameEdit.text().strip(),
                parent_id=parent_id,
                icon=self.selected_icon,
                order=self.orderSpin.value(),
                is_builtin=False
            )
