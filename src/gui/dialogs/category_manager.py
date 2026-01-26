"""
分类管理对话框 - 树形结构版本
支持层叠弹窗模式，显示分类树形结构
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, PushButton, 
    MessageBox, BodyLabel, TreeWidget, FluentIcon,
    InfoBar, InfoBarPosition
)
from ...data.user_manager import UserManager
from ...data.category_manager import CategoryManager
from ...data.model import Category, CategoryNode
from ...common.signals import signal_bus
import uuid


class CategoryManagerDialog(MessageBoxBase):
    """分类管理对话框 - 树形结构"""
    
    categories_changed = Signal()  # 分类变更信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.user_manager = UserManager()
        self.category_manager = CategoryManager()
        
        self.setWindowTitle("管理分类")
        self._init_ui()
        self._load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel("分类管理")
        
        # 分类树
        self.categoryTree = TreeWidget()
        self.categoryTree.setHeaderHidden(True)
        self.categoryTree.setMinimumHeight(300)
        self.categoryTree.setMinimumWidth(400)
        
        # 输入区域
        input_layout = QHBoxLayout()
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText("输入新分类名称...")
        input_layout.addWidget(self.nameEdit)
        
        self.addButton = PushButton(FluentIcon.ADD, "添加根分类")
        self.addButton.clicked.connect(self._on_add_root_category)
        input_layout.addWidget(self.addButton)
        
        # 操作按钮行
        button_layout = QHBoxLayout()
        
        self.addChildButton = PushButton(FluentIcon.FOLDER_ADD, "添加子分类")
        self.addChildButton.clicked.connect(self._on_add_child_category)
        self.addChildButton.setEnabled(False)
        button_layout.addWidget(self.addChildButton)
        
        self.deleteButton = PushButton(FluentIcon.DELETE, "删除选中")
        self.deleteButton.clicked.connect(self._on_delete_category)
        self.deleteButton.setEnabled(False)
        button_layout.addWidget(self.deleteButton)
        
        button_layout.addStretch()
        
        self.expandAllButton = PushButton(FluentIcon.DOWN, "全部展开")
        self.expandAllButton.clicked.connect(self._on_expand_all)
        button_layout.addWidget(self.expandAllButton)
        
        self.collapseAllButton = PushButton(FluentIcon.UP, "全部折叠")
        self.collapseAllButton.clicked.connect(self._on_collapse_all)
        button_layout.addWidget(self.collapseAllButton)
        
        # 添加到视图
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(BodyLabel("分类树（支持多层级）："))
        self.viewLayout.addWidget(self.categoryTree)
        self.viewLayout.addLayout(input_layout)
        self.viewLayout.addLayout(button_layout)
        
        # 连接信号
        self.categoryTree.itemSelectionChanged.connect(self._on_selection_changed)
        self.categoryTree.itemChanged.connect(self._on_item_changed)
        
        # 按钮
        self.yesButton.setText("完成")
        self.cancelButton.setText("取消")
        self.cancelButton.show()  # 显示取消按钮
        
        self.widget.setMinimumWidth(500)
    
    def _load_categories(self):
        """加载分类树"""
        self.categoryTree.clear()
        
        # 获取根分类
        root_categories = self.category_manager.get_category_tree()
        
        # 递归构建树
        for category in root_categories:
            self._add_category_item(None, category)
    
    def _on_item_changed(self, item, column):
        """Item 变化时的回调 - 实现父子复选框联动"""
        if column != 0:
            return
        
        # 暂时断开信号，避免递归触发
        self.categoryTree.itemChanged.disconnect(self._on_item_changed)
        
        # 获取当前项的勾选状态
        check_state = item.checkState(0)
        
        # 递归设置所有子项的勾选状态
        self._set_children_check_state(item, check_state)
        
        # 重新连接信号
        self.categoryTree.itemChanged.connect(self._on_item_changed)
        
        # 更新删除按钮状态
        self._update_delete_button_state()
    
    def _set_children_check_state(self, parent_item, check_state):
        """递归设置所有子项的勾选状态"""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            child.setCheckState(0, check_state)
            # 递归设置子项的子项
            self._set_children_check_state(child, check_state)
    
    def _add_category_item(self, parent_item, category: CategoryNode):
        """递归添加分类项"""
        # 创建树节点
        if parent_item is None:
            item = QTreeWidgetItem(self.categoryTree)
        else:
            item = QTreeWidgetItem(parent_item)
        
        # 设置显示文本
        item.setText(0, category.name)
        
        # 设置复选框
        item.setFlags(
            item.flags() | 
            Qt.ItemFlag.ItemIsEnabled | 
            Qt.ItemFlag.ItemIsUserCheckable |
            Qt.ItemFlag.ItemIsSelectable
        )
        item.setCheckState(0, Qt.CheckState.Unchecked)
        
        # 设置数据
        item.setData(0, Qt.ItemDataRole.UserRole, category)
        
        # 设置图标
        if category.icon:
            try:
                icon = getattr(FluentIcon, category.icon.upper(), FluentIcon.FOLDER)
                item.setIcon(0, icon.icon())
            except:
                item.setIcon(0, FluentIcon.FOLDER.icon())
        else:
            item.setIcon(0, FluentIcon.FOLDER.icon())
        
        # 系统分类显示为灰色
        if category.is_builtin:
            item.setForeground(0, Qt.GlobalColor.gray)
        
        # 递归添加子分类
        children = self.category_manager.get_children(category.id)
        for child in children:
            self._add_category_item(item, child)

    
    def _on_selection_changed(self):
        """选择改变"""
        selected_items = self.categoryTree.selectedItems()
        has_selection = len(selected_items) > 0
        
        # 添加子分类按钮：只要有选中项就启用
        self.addChildButton.setEnabled(has_selection)
        
        # 删除按钮：检查是否有勾选的项
        self._update_delete_button_state()
    
    def _update_delete_button_state(self):
        """更新删除按钮状态"""
        # 检查是否有勾选的项
        checked_categories = []
        self._collect_checked_items(self.categoryTree.invisibleRootItem(), checked_categories)
        self.deleteButton.setEnabled(len(checked_categories) > 0)
    
    def _on_add_root_category(self):
        """添加根分类"""
        name = self.nameEdit.text().strip()
        
        if not name:
            MessageBox("提示", "请输入分类名称", self).exec()
            return
        
        # 检查是否已存在
        categories = self.category_manager.get_all_categories()
        if any(c.name == name for c in categories):
            MessageBox("提示", "分类已存在", self).exec()
            return
        
        # 添加分类
        category = CategoryNode(
            id=f"cat_{uuid.uuid4().hex[:8]}",
            name=name,
            icon="Folder",
            parent_id=None,
            order=len(self.category_manager.get_category_tree())
        )
        
        success, msg = self.category_manager.add_category(category)
        
        if success:
            self.nameEdit.clear()
            self._load_categories()
            self.categories_changed.emit()
            signal_bus.categories_changed.emit()
            InfoBar.success(
                title='成功',
                content=msg,
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            MessageBox("失败", msg, self).exec()
    
    def _on_add_child_category(self):
        """添加子分类"""
        selected_items = self.categoryTree.selectedItems()
        if not selected_items:
            MessageBox("提示", "请先选择父分类", self).exec()
            return
        
        parent_category = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        
        # 检查是否可以添加子分类
        can_add, msg = self.category_manager.can_add_child_category(parent_category.id)
        if not can_add:
            MessageBox("提示", msg, self).exec()
            return
        
        name = self.nameEdit.text().strip()
        if not name:
            MessageBox("提示", "请输入分类名称", self).exec()
            return
        
        # 检查是否已存在
        categories = self.category_manager.get_all_categories()
        if any(c.name == name for c in categories):
            MessageBox("提示", "分类已存在", self).exec()
            return
        
        # 添加子分类
        children = self.category_manager.get_children(parent_category.id)
        category = CategoryNode(
            id=f"cat_{uuid.uuid4().hex[:8]}",
            name=name,
            icon="Folder",
            parent_id=parent_category.id,
            order=len(children)
        )
        
        success, msg = self.category_manager.add_category(category)
        
        if success:
            self.nameEdit.clear()
            self._load_categories()
            self.categories_changed.emit()
            signal_bus.categories_changed.emit()
            InfoBar.success(
                title='成功',
                content=msg,
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            MessageBox("失败", msg, self).exec()
    
    def _on_delete_category(self):
        """删除分类"""
        # 收集所有被勾选的分类
        checked_categories = []
        self._collect_checked_items(self.categoryTree.invisibleRootItem(), checked_categories)
        
        if not checked_categories:
            MessageBox("提示", "请勾选要删除的分类", self).exec()
            return
        
        # 检查每个分类下的模板
        from ...data.template_manager import TemplateManager
        template_manager = TemplateManager()
        
        categories_with_templates = []
        total_templates = 0
        
        for category in checked_categories:
            # 获取该分类下的所有模板
            templates = template_manager.get_templates_by_category(category.id)
            if templates:
                categories_with_templates.append((category, templates))
                total_templates += len(templates)
        
        # 构建确认消息
        category_names = ", ".join([cat.name for cat in checked_categories])
        
        if categories_with_templates:
            # 有模板的情况，显示详细信息
            template_info = []
            for category, templates in categories_with_templates:
                template_names = [t.name for t in templates[:5]]  # 最多显示5个
                if len(templates) > 5:
                    template_names.append(f"... 还有 {len(templates) - 5} 个")
                template_info.append(f"\n• {category.name} ({len(templates)} 个模板):\n  - " + "\n  - ".join(template_names))
            
            message = (
                f"确定要删除以下 {len(checked_categories)} 个分类吗？\n"
                f"{category_names}\n\n"
                f"⚠️ 警告：这些分类下共有 {total_templates} 个模板：\n"
                + "\n".join(template_info) +
                "\n\n删除分类后，这些模板也会一并删除！"
            )
        else:
            # 没有模板的情况
            message = (
                f"确定要删除以下 {len(checked_categories)} 个分类吗？\n"
                f"{category_names}\n\n"
                f"这些分类下没有模板。"
            )
        
        reply = MessageBox("确认删除", message, self).exec()
        
        if not reply:
            return
        
        # 批量删除分类
        success_count = 0
        failed_count = 0
        
        for category in checked_categories:
            success, msg = self.category_manager.delete_category(category.id)
            if success:
                success_count += 1
            else:
                failed_count += 1
        
        # 刷新界面
        self._load_categories()
        self.categories_changed.emit()
        signal_bus.categories_changed.emit()
        
        # 显示结果
        if failed_count == 0:
            InfoBar.success(
                title='成功',
                content=f"已成功删除 {success_count} 个分类",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            MessageBox("部分成功", f"成功删除 {success_count} 个分类，失败 {failed_count} 个", self).exec()
    
    def _collect_checked_items(self, parent_item, checked_list):
        """递归收集所有被勾选的分类"""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child.checkState(0) == Qt.CheckState.Checked:
                category = child.data(0, Qt.ItemDataRole.UserRole)
                if category:
                    checked_list.append(category)
            # 递归检查子项
            self._collect_checked_items(child, checked_list)
    
    def _on_expand_all(self):
        """全部展开"""
        self.categoryTree.expandAll()
    
    def _on_collapse_all(self):
        """全部折叠"""
        self.categoryTree.collapseAll()
    
    def validate(self):
        """验证（用户点击完成按钮时调用）"""
        return True


