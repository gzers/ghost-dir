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
from ..i18n import t
import uuid


class CategoryManagerDialog(MessageBoxBase):
    """分类管理对话框 - 树形结构"""
    
    categories_changed = Signal()  # 分类变更信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.user_manager = UserManager()
        self.category_manager = CategoryManager()
        
        self.setWindowTitle(t("library.category_manager_title"))
        self._init_ui()
        self._load_categories()
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        from PySide6.QtCore import Qt
        
        # F2 快捷键：重命名
        if event.key() == Qt.Key.Key_F2:
            if self.renameButton.isEnabled():
                self._on_rename_category()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel(t("library.category_manager_title"))
        
        # 工具栏 (CommandBar)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(8)
        
        # 左侧编辑按钮组
        self.addButton = PushButton(FluentIcon.ADD, t("library.btn_new"))
        self.addButton.clicked.connect(self._on_add_category)
        toolbar_layout.addWidget(self.addButton)
        
        self.renameButton = PushButton(FluentIcon.EDIT, t("library.btn_rename"))
        self.renameButton.clicked.connect(self._on_rename_category)
        self.renameButton.setEnabled(False)
        toolbar_layout.addWidget(self.renameButton)
        
        self.deleteButton = PushButton(FluentIcon.DELETE, t("library.btn_delete"))
        self.deleteButton.clicked.connect(self._on_delete_category)
        self.deleteButton.setEnabled(False)
        toolbar_layout.addWidget(self.deleteButton)
        
        # 分隔符
        toolbar_layout.addStretch()
        
        # 右侧功能按钮
        from qfluentwidgets import TogglePushButton
        self.sortButton = TogglePushButton(t("library.btn_sort"))
        self.sortButton.setIcon(FluentIcon.SYNC)
        self.sortButton.toggled.connect(self._on_sort_toggled)
        toolbar_layout.addWidget(self.sortButton)
        
        self.helpButton = PushButton(FluentIcon.INFO, t("library.btn_help"))
        self.helpButton.clicked.connect(self._show_help)
        toolbar_layout.addWidget(self.helpButton)
        
        # 分类树
        self.categoryTree = TreeWidget()
        self.categoryTree.setHeaderHidden(True)
        self.categoryTree.setMinimumHeight(300)
        self.categoryTree.setMinimumWidth(500)
        
        # 禁用双击编辑
        from PySide6.QtWidgets import QAbstractItemView
        self.categoryTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # 初始禁用拖拽
        self.categoryTree.setDragEnabled(False)
        self.categoryTree.setAcceptDrops(False)
        self.categoryTree.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        
        # 单选模式
        self.categoryTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        # 启用右键菜单
        self.categoryTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.categoryTree.customContextMenuRequested.connect(self._show_context_menu)
        
        # 添加到视图
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(toolbar_layout)
        self.viewLayout.addWidget(self.categoryTree)
        
        # 连接信号
        self.categoryTree.itemSelectionChanged.connect(self._on_selection_changed)
        self.categoryTree.itemChanged.connect(self._on_item_changed)
        
        # 按钮
        self.yesButton.setText(t("library.btn_done"))
        self.cancelButton.setText(t("library.btn_cancel"))
        self.cancelButton.show()  # 显示取消按钮
        
        self.widget.setMinimumWidth(550)
        
        # 初始化模式状态
        self._is_sort_mode = False
    
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
        
        # 重命名按钮：只有选中一个项时启用
        self.renameButton.setEnabled(len(selected_items) == 1 and not self._is_sort_mode)
        
        # 删除按钮：检查是否有勾选的项
        self._update_delete_button_state()
    
    def _update_delete_button_state(self):
        """更新删除按钮状态"""
        # 检查是否有勾选的项
        checked_categories = []
        self._collect_checked_items(self.categoryTree.invisibleRootItem(), checked_categories)
        self.deleteButton.setEnabled(len(checked_categories) > 0)
    
    def _on_add_category(self):
        """新建分类"""
        from qfluentwidgets import InputDialog
        
        selected_items = self.categoryTree.selectedItems()
        
        # 弹出输入对话框
        dialog = InputDialog(t("library.dialog_new_category"), t("library.input_category_name"), self)
        
        if dialog.exec():
            name = dialog.textValue().strip()
            if not name:
                return
            
            # 确定父分类
            parent_id = None
            if selected_items:
                parent_category = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
                parent_id = parent_category.id
                
                # 检查是否可以添加子分类
                can_add, msg = self.category_manager.can_add_child_category(parent_id)
                if not can_add:
                    MessageBox(t("library.dialog_hint"), msg, self).exec()
                    return
            
            # 获取下一个 order 值
            children = self.category_manager.get_children(parent_id)
            next_order = len(children)
            
            # 创建分类
            category = CategoryNode(
                id=f"cat_{uuid.uuid4().hex[:8]}",
                name=name,
                icon="Folder",
                parent_id=parent_id,
                order=next_order
            )
            
            # 添加并立即保存
            success, msg = self.category_manager.add_category(category)
            
            if success:
                self._load_categories()
                self.categories_changed.emit()
                signal_bus.categories_changed.emit()
                InfoBar.success(
                    title=t("common.success"),
                    content=msg,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
            else:
                MessageBox(t("common.failed"), msg, self).exec()
    
    def _on_rename_category(self):
        """重命名分类"""
        from qfluentwidgets import InputDialog
        
        selected_items = self.categoryTree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        category = item.data(0, Qt.ItemDataRole.UserRole)
        
        # 弹出输入对话框
        dialog = InputDialog(t("library.dialog_rename_category"), t("library.input_new_name"), self)
        dialog.setTextValue(category.name)
        
        if dialog.exec():
            new_name = dialog.textValue().strip()
            if not new_name or new_name == category.name:
                return
            
            # 调用后端重命名方法
            success, msg = self.category_manager.rename_category(category.id, new_name)
            
            if success:
                self._load_categories()
                self.categories_changed.emit()
                signal_bus.categories_changed.emit()
                InfoBar.success(
                    title=t("common.success"),
                    content=msg,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
            else:
                MessageBox(t("common.failed"), msg, self).exec()
    
    def _on_delete_category(self):
        """删除分类"""
        # 收集所有被勾选的分类
        checked_categories = []
        self._collect_checked_items(self.categoryTree.invisibleRootItem(), checked_categories)
        
        if not checked_categories:
            MessageBox(t("library.dialog_hint"), t("library.error_empty_delete_selection", default="请勾选要删除的分类"), self).exec()
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
            # 有模板的情况，使用 i18n
            category_names = ", ".join([cat.name for cat in checked_categories])
            template_info = []
            for category, templates in categories_with_templates:
                template_names = [t_obj.name for t_obj in templates[:5]]
                if len(templates) > 5:
                    template_names.append(f"... 还有 {len(templates) - 5} 个")
                template_info.append(f"\n• {category.name} ({len(templates)} 模板):\n  - " + "\n  - ".join(template_names))
            
            message = t("library.confirm_delete_with_templates", 
                        count=len(checked_categories), 
                        names=category_names, 
                        template_count=total_templates, 
                        template_info="".join(template_info))
        else:
            # 没有模板的情况，使用 i18n
            message = t("library.confirm_delete_batch", 
                        count=len(checked_categories), 
                        names=", ".join([cat.name for cat in checked_categories]))
        
        reply = MessageBox(t("library.dialog_confirm_delete"), message, self).exec()
        
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
                title=t("common.success"),
                content=t("library.msg_delete_success", count=success_count, default=f"已成功删除 {success_count} 个分类"),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            MessageBox(t("common.partial_success", default="部分成功"), 
                       t("library.msg_delete_partial", success=success_count, failed=failed_count, default=f"成功删除 {success_count} 个分类，失败 {failed_count} 个"), 
                       self).exec()
    
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
    
    # ========== 双模式交互 ==========
    
    def _enter_browse_mode(self):
        """进入浏览模式"""
        self._is_sort_mode = False
        
        # 恢复复选框显示
        self._set_checkboxes_visible(True)
        
        # 禁用拖拽
        from PySide6.QtWidgets import QAbstractItemView
        self.categoryTree.setDragEnabled(False)
        self.categoryTree.setAcceptDrops(False)
        self.categoryTree.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        
        # 恢复按钮状态
        self.addButton.setEnabled(True)
        self._on_selection_changed()  # 更新重命名和删除按钮状态
        
        # 恢复对话框按钮
        self.yesButton.setEnabled(True)
        self.cancelButton.setEnabled(True)
        
        # 更新标题和排序按钮
        self.titleLabel.setText(t("library.category_manager_title"))
        self.sortButton.setText(t("library.btn_sort"))
        self.sortButton.setChecked(False)
    
    def _enter_sort_mode(self):
        """进入排序模式"""
        self._is_sort_mode = True
        
        # 隐藏所有复选框
        self._set_checkboxes_visible(False)
        
        # 启用拖拽
        from PySide6.QtWidgets import QAbstractItemView
        self.categoryTree.setDragEnabled(True)
        self.categoryTree.setAcceptDrops(True)
        self.categoryTree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        
        # 禁用所有编辑按钮
        self.addButton.setEnabled(False)
        self.renameButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        
        # 禁用对话框按钮（防止在排序模式下关闭）
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        
        # 更新标题和排序按钮
        self.titleLabel.setText(t("library.category_manager_sort_mode"))
        self.sortButton.setText(t("library.btn_exit_sort"))
        self.sortButton.setChecked(True)
    
    def _exit_sort_mode(self):
        """退出排序模式"""
        # 保存新的排序到数据库
        self._save_current_order()
        
        # 返回浏览模式
        self._enter_browse_mode()
    
    def _on_sort_toggled(self, checked: bool):
        """排序按钮切换"""
        if checked:
            self._enter_sort_mode()
        else:
            self._exit_sort_mode()
    
    def _set_checkboxes_visible(self, visible: bool):
        """显示/隐藏所有复选框"""
        def update_item(item):
            if visible:
                item.setFlags(
                    item.flags() | 
                    Qt.ItemFlag.ItemIsEnabled | 
                    Qt.ItemFlag.ItemIsUserCheckable |
                    Qt.ItemFlag.ItemIsSelectable
                )
            else:
                item.setFlags(
                    item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable
                )
            
            # 递归处理子项
            for i in range(item.childCount()):
                update_item(item.child(i))
        
        root = self.categoryTree.invisibleRootItem()
        for i in range(root.childCount()):
            update_item(root.child(i))
    
    def _save_current_order(self):
        """保存当前排序"""
        category_orders = []
        
        # 递归遍历树，收集所有分类的新 order
        def collect_orders(parent_item, parent_id):
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                category = child.data(0, Qt.ItemDataRole.UserRole)
                if category:
                    category_orders.append((category.id, i))
                    # 递归处理子分类
                    collect_orders(child, category.id)
        
        collect_orders(self.categoryTree.invisibleRootItem(), None)
        
        # 批量更新到数据库
        success, msg = self.category_manager.reorder_categories(category_orders)
        
        if success:
            InfoBar.success(
                title=t("common.success"),
                content=t("library.msg_sort_saved"),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            MessageBox(t("common.failed"), msg, self).exec()
    
    # ========== 右键菜单和帮助 ==========
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        from PySide6.QtGui import QAction
        from PySide6.QtWidgets import QMenu
        
        item = self.categoryTree.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)
        
        # 重命名
        rename_action = QAction(FluentIcon.EDIT.icon(), t("library.menu_rename"), self)
        rename_action.triggered.connect(self._on_rename_category)
        menu.addAction(rename_action)
        
        # 在此新建
        add_child_action = QAction(FluentIcon.ADD.icon(), t("library.menu_add_child"), self)
        add_child_action.triggered.connect(self._on_add_category)
        menu.addAction(add_child_action)
        
        menu.addSeparator()
        
        # 删除此项
        delete_action = QAction(FluentIcon.DELETE.icon(), t("library.menu_delete"), self)
        delete_action.triggered.connect(lambda: self._delete_single_category(item))
        menu.addAction(delete_action)
        
        menu.exec(self.categoryTree.viewport().mapToGlobal(pos))
    
    def _delete_single_category(self, item):
        """删除单个分类（用于右键菜单）"""
        category = item.data(0, Qt.ItemDataRole.UserRole)
        if not category:
            return
        
        # 检查是否为系统分类
        from ...common.config import SYSTEM_CATEGORIES
        if category.id in SYSTEM_CATEGORIES:
            MessageBox(t("library.dialog_hint"), t("library.error_system_category_delete"), self).exec()
            return
        
        # 确认删除
        reply = MessageBox(
            t("library.dialog_confirm_delete"),
            t("library.confirm_delete_single", name=category.name),
            self
        ).exec()
        
        if not reply:
            return
        
        # 删除分类
        success, msg = self.category_manager.delete_category(category.id)
        
        if success:
            self._load_categories()
            self.categories_changed.emit()
            signal_bus.categories_changed.emit()
            InfoBar.success(
                title=t("common.success"),
                content=msg,
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            MessageBox(t("common.failed"), msg, self).exec()
    
    def _show_help(self):
        """显示帮助提示"""
        help_content = (
            t("library.help_title") + "\n\n" +
            t("library.help_browse_mode") + "\n" +
            t("library.help_browse_1") + "\n" +
            t("library.help_browse_2") + "\n" +
            t("library.help_browse_3") + "\n" +
            t("library.help_browse_4") + "\n\n" +
            t("library.help_sort_mode") + "\n" +
            t("library.help_sort_1") + "\n" +
            t("library.help_sort_2") + "\n" +
            t("library.help_sort_3") + "\n" +
            t("library.help_sort_4") + "\n\n" +
            t("library.help_shortcuts") + "\n" +
            t("library.help_shortcuts_1") + "\n\n" +
            t("library.help_notes") + "\n" +
            t("library.help_notes_1") + "\n" +
            t("library.help_notes_2") + "\n" +
            t("library.help_notes_3")
        )
        
        MessageBox(t("library.btn_help"), help_content, self).exec()
    
    # ========== 工具方法 ==========
    
    def _on_expand_all(self):
        """全部展开"""
        self.categoryTree.expandAll()
    
    def _on_collapse_all(self):
        """全部折叠"""
        self.categoryTree.collapseAll()
    
    def validate(self):
        """验证（用户点击完成按钮时调用）"""
        return True


