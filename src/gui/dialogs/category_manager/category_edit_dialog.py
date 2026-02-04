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
    MessageBoxBase, SubtitleLabel, LineEdit,
    PushButton, SpinBox, FluentIcon, TransparentToolButton,
    InfoBar, BodyLabel
)
from src.data.model import CategoryNode
from src.data.category_manager import CategoryManager
from src.gui.components.category_selector import CategorySelector
from src.gui.i18n import t
from src.gui.styles import format_required_label


class CategoryEditDialog(MessageBoxBase):
    """分类编辑对话框"""
    
    def __init__(
        self,
        category_manager: CategoryManager,
        category: Optional[CategoryNode] = None,
        mode: str = "create",
        parent=None,
        target_parent_id: Optional[str] = None
    ):
        """
        初始化分类编辑对话框
        
        Args:
            category_manager: 分类管理器
            category: 要编辑的分类（None 表示新建）
            mode: 模式 ("create" 或 "edit")
            parent: 父窗口
            target_parent_id: 预设的父分类ID（新建模式下有效）
        """
        super().__init__(parent)
        self.category_manager = category_manager
        self.category = category
        self.mode = mode
        self.target_parent_id = target_parent_id
        
        self.setWindowTitle(t("library.dialog_rename_category") if self.mode == "edit" else t("library.dialog_new_category"))
        self._init_ui()
        self._load_data()
    
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
        
        CONTENT_WIDTH = 380
        
        # 分类名称
        self.nameLabel = BodyLabel(format_required_label(t("library.label_category_name")), self)
        self.nameEdit = LineEdit(self)
        self.nameEdit.setPlaceholderText(t("library.placeholder_category_name"))
        self.nameEdit.setFixedWidth(CONTENT_WIDTH)
        form_layout.addRow(self.nameLabel, self.nameEdit)
        
        # 父分类 - 使用新的树形选择器
        self.parentLabel = BodyLabel(t("library.label_parent_category"), self)
        self.parentCombo = CategorySelector(self, only_leaf=False, root_visible=True)
        self.parentCombo.setFixedWidth(CONTENT_WIDTH)
        form_layout.addRow(self.parentLabel, self.parentCombo)
        
        # 排序权重
        self.orderLabel = BodyLabel(t("library.label_order"), self)
        self.orderSpin = SpinBox(self)
        self.orderSpin.setRange(0, 999)
        self.orderSpin.setValue(0)
        self.orderSpin.setFixedWidth(150)
        form_layout.addRow(self.orderLabel, self.orderSpin)
        
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
        # 确定需要预选的父分类 ID
        target_pid = None
        if self.mode == "edit" and self.category:
            target_pid = self.category.parent_id
        elif self.mode == "create" and self.target_parent_id:
            target_pid = self.target_parent_id

        # 构建排除列表（不能选自己及子孙）
        exclude_ids = []
        if self.mode == "edit" and self.category:
            exclude_ids.append(self.category.id)
            descendants = self.category_manager._get_all_descendants(self.category.id)
            exclude_ids.extend([d.id for d in descendants])
        
        # 配置树形选择器
        self.parentCombo.set_manager(self.category_manager, exclude_ids=exclude_ids)
        
        # 设置初始选中值
        self.parentCombo.set_value(target_pid)
        
        # 填充基本信息
        if self.mode == "edit" and self.category:
            self.nameEdit.setText(self.category.name)
            self.orderSpin.setValue(self.category.order)
    

    
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
                position='TopCenter',
                duration=3000,
                parent=self
            )
            return False
        
        # 获取父分类ID
        parent_id = self.parentCombo.get_value()
        
        # 如果选择了父分类，验证是否可以添加子分类
        if parent_id and self.mode == "create":
            can_add, msg = self.category_manager.can_add_child_category(parent_id)
            if not can_add:
                InfoBar.warning(
                    title=t("common.failed"),
                    content=msg,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position='TopCenter',
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
                order=self.orderSpin.value()
            )
            
            depth = temp_category.get_depth(self.category_manager.categories)
            from src.common.config import MAX_CATEGORY_DEPTH
            
            if depth > MAX_CATEGORY_DEPTH:
                InfoBar.warning(
                    title=t("common.failed"),
                    content=t("library.help_notes_3"), # 复用层级限制说明或者建新key，这里复用
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position='TopCenter',
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
            self.category.parent_id = self.parentCombo.get_value()
            self.category.order = self.orderSpin.value()
            return self.category
        else:
            # 创建新分类
            # 直接从输入框和父分类获取数据
            name = self.nameEdit.text().strip()
            parent_id = self.parentCombo.get_value()
            
            # 生成 ID：清理名称中的非法字符
            import re
            base_id = re.sub(r'[^\w\s-]', '', name)
            base_id = re.sub(r'[-\s]+', '_', base_id).lower()
            
            # 这里的关键点：如果是子分类，ID 应包含父 ID 前缀
            # 如果是 root，就是 base_id
            new_id = f"{parent_id}.{base_id}" if parent_id else base_id
            
            # 确保 ID 唯一
            category_id = new_id
            counter = 1
            while category_id in self.category_manager.categories:
                category_id = f"{new_id}_{counter}"
                counter += 1
            
            return CategoryNode(
                id=category_id,
                name=name,
                parent_id=parent_id,
                order=self.orderSpin.value(),
                is_builtin=False
            )
