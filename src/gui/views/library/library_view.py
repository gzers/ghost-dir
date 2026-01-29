"""
模板库视图
浏览所有官方和自定义模板，使用树表布局
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PySide6.QtCore import Qt
from qfluentwidgets import (
    SearchLineEdit, PushButton, DropDownPushButton, FluentIcon,
    InfoBar, InfoBarPosition, MessageBox, RoundMenu, Action
)
from ...i18n import t
from src.data.user_manager import UserManager
from src.data.template_manager import TemplateManager
from src.data.category_manager import CategoryManager
from src.data.model import Template, CategoryNode
from ...components import BasePageView
from .widgets import CategoryTreeWidget, TemplateTableWidget
from ...dialogs import (
    CategoryEditDialog, TemplateEditDialog, TemplatePreviewDialog,
    BatchMoveDialog, ExportDialog, ImportDialog, CategoryManagerDialog
)


class LibraryView(BasePageView):
    """模板库视图"""

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("library.title"),
            show_toolbar=True,
            enable_scroll=False  # 不需要滚动，由组件自己处理
        )

        # 初始化数据管理器
        self.category_manager = CategoryManager()
        self.template_manager = TemplateManager(self.category_manager)
        self.user_manager = UserManager()
        
        # 双向引用
        self.category_manager.set_template_manager(self.template_manager)
        self.template_manager.set_category_manager(self.category_manager)

        # 当前选中的分类
        self.current_category_id = None

        # 设置页面内容
        self._setup_toolbar()
        self._setup_content()
        self._connect_signals()

        # 验证模板并加载
        self._validate_and_load()

    def _setup_toolbar(self):
        """设置工具栏"""
        toolbar = self.get_toolbar_layout()

        # 搜索框
        self.search_edit = SearchLineEdit()
        self.search_edit.setPlaceholderText('搜索模板...')
        self.search_edit.setFixedWidth(250)
        self.search_edit.textChanged.connect(self._on_search_changed)
        toolbar.addWidget(self.search_edit)

        toolbar.addSpacing(10)

        # 刷新按钮
        self.refresh_btn = PushButton(FluentIcon.SYNC, '刷新')
        self.refresh_btn.clicked.connect(self._on_refresh_clicked)
        toolbar.addWidget(self.refresh_btn)

        # 批量删除按钮
        self.batch_delete_btn = PushButton(FluentIcon.DELETE, '批量删除')
        self.batch_delete_btn.clicked.connect(self._on_batch_delete_clicked)
        self.batch_delete_btn.setEnabled(False)  # 默认禁用
        toolbar.addWidget(self.batch_delete_btn)

        toolbar.addStretch()

        # 新建模板按钮
        self.add_template_btn = PushButton(FluentIcon.ADD, '新建模板')
        self.add_template_btn.clicked.connect(self._on_add_template_clicked)
        toolbar.addWidget(self.add_template_btn)

        # 管理分类按钮（合并新建分类+编辑分类）
        self.manage_category_btn = PushButton(FluentIcon.FOLDER, '管理分类')
        self.manage_category_btn.clicked.connect(self._on_manage_category_clicked)
        toolbar.addWidget(self.manage_category_btn)

        # 导入/导出下拉菜单按钮
        self.import_export_btn = DropDownPushButton(FluentIcon.SYNC, '导入/导出')
        self.import_export_menu = RoundMenu(parent=self)
        
        # 导出操作
        self.export_action = Action(FluentIcon.SHARE, '导出')
        self.export_action.triggered.connect(self._on_export_clicked)
        self.import_export_menu.addAction(self.export_action)
        
        # 导入操作
        self.import_action = Action(FluentIcon.DOWNLOAD, '导入')
        self.import_action.triggered.connect(self._on_import_clicked)
        self.import_export_menu.addAction(self.import_action)
        
        self.import_export_btn.setMenu(self.import_export_menu)
        toolbar.addWidget(self.import_export_btn)

        # 右侧统计标签
        right_toolbar = self.get_right_toolbar_layout()
        self.count_label = PushButton()
        self.count_label.setEnabled(False)
        self.count_label.setText('加载中...')
        right_toolbar.addWidget(self.count_label)

    def _setup_content(self):
        """设置内容区域"""
        # 创建分割器
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：分类树
        self.category_tree = CategoryTreeWidget(self.category_manager, self.user_manager)
        self.category_tree.setMinimumWidth(200)
        self.category_tree.setMaximumWidth(400)
        
        # 右侧：模板表格
        self.template_table = TemplateTableWidget()
        
        # 添加到分割器
        self.splitter.addWidget(self.category_tree)
        self.splitter.addWidget(self.template_table)
        
        # 设置分割比例（1:3）
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)
        
        # 彻底解决高度撑满问题：移除 BasePageView 默认添加的所有底部弹簧
        content_layout = self.get_content_layout()
        main_layout = self.layout()
        
        # 1. 移除内容布局末尾的弹簧
        for i in range(content_layout.count() - 1, -1, -1):
            item = content_layout.itemAt(i)
            if item and item.spacerItem():
                content_layout.removeItem(item)
        
        # 2. 移除主布局末尾的弹簧
        if main_layout:
            for i in range(main_layout.count() - 1, -1, -1):
                item = main_layout.itemAt(i)
                if item and item.spacerItem():
                    main_layout.removeItem(item)
                    
        # 3. 设置最高拉伸优先级并添加
        from PySide6.QtWidgets import QSizePolicy
        self.splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.addWidget(self.splitter, 1)
        
        # 应用透明背景并隐藏分割线条（黑条）
        from ...styles import apply_transparent_style
        apply_transparent_style(self.splitter)
        self.splitter.setStyleSheet("QSplitter::handle { background: transparent; border: none; }")

    def _connect_signals(self):
        """连接信号"""
        # 分类树信号
        self.category_tree.category_selected.connect(self._on_category_selected)
        self.category_tree.add_category_requested.connect(self._on_add_category_requested)
        self.category_tree.edit_category_requested.connect(self._on_edit_category_requested)
        self.category_tree.delete_category_requested.connect(self._on_delete_category_requested)
        
        # 模板表格信号
        self.template_table.template_selected.connect(self._on_template_selected)
        self.template_table.edit_template_requested.connect(self._on_edit_template_requested)
        self.template_table.delete_template_requested.connect(self._on_delete_template_requested)
        self.template_table.checked_changed.connect(self._on_checked_count_changed)
        
        # 全局信号
        from ....common.signals import signal_bus
        signal_bus.categories_changed.connect(self._on_categories_changed)


    def _validate_and_load(self):
        """验证模板并加载"""
        # 验证所有模板
        orphaned = self.template_manager.validate_all_templates()
        
        if orphaned:
            InfoBar.warning(
                title='发现孤儿模板',
                content=f'有 {len(orphaned)} 个模板的分类不存在，已自动归入"未分类"',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self
            )
        
        # 更新统计
        self._update_count()

    # ========== 事件处理 ==========

    def _on_category_selected(self, category_id: str):
        """分类被选中"""
        self.current_category_id = category_id
        
        # 加载该分类下的模板
        templates = self.template_manager.get_templates_by_category(category_id)
        self.template_table.set_templates(templates, category_id)
        
        # 更新统计
        category = self.category_manager.get_category_by_id(category_id)
        if category:
            self.count_label.setText(t("library.stats_category", name=category.name, count=len(templates)))

    def _on_template_selected(self, template_id: str):
        """模板被选中"""
        pass  # 可以在这里添加预览等功能

    def _on_search_changed(self, text: str):
        """搜索文本改变"""
        search_text = text.strip().lower()
        
        # 如果搜索框为空，显示当前分类的所有模板
        if not search_text:
            if self.current_category_id:
                self._on_category_selected(self.current_category_id)
            return
        
        # 获取当前分类的模板
        if self.current_category_id:
            templates = self.template_manager.get_templates_by_category(self.current_category_id)
        else:
            templates = list(self.template_manager.templates.values())
        
        # 过滤模板：按名称、描述、标签搜索
        filtered_templates = []
        for template in templates:
            # 搜索名称
            if search_text in template.name.lower():
                filtered_templates.append(template)
                continue
            
            # 搜索描述
            if hasattr(template, 'description') and template.description and search_text in template.description.lower():
                filtered_templates.append(template)
                continue
            
            # 搜索标签
            if hasattr(template, 'tags') and template.tags:
                tags_str = ' '.join(template.tags).lower()
                if search_text in tags_str:
                    filtered_templates.append(template)
        
        # 更新表格显示
        self.template_table.set_templates(filtered_templates, self.current_category_id or "")
        
        # 更新统计
        self.count_label.setText(t("library.stats_search", count=len(filtered_templates)))

    def _on_refresh_clicked(self):
        """刷新按钮被点击"""
        self.category_tree.load_categories()
        if self.current_category_id:
            self._on_category_selected(self.current_category_id)
        self._update_count()
        
        InfoBar.success(
            title='刷新成功',
            content='已重新加载所有数据',
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    # ========== 分类操作 ==========

    def _on_manage_category_clicked(self):
        """管理分类按钮被点击"""
        dialog = CategoryManagerDialog(self)
        dialog.categories_changed.connect(self._on_categories_changed)
        dialog.exec()
    
    def _on_categories_changed(self):
        """分类发生变化"""
        # 记录当前选中的分类
        last_selected = self.current_category_id
        
        # 重新从磁盘加载数据
        self.category_manager.load_categories()
        
        # 刷新分类树
        self.category_tree.load_categories()
        
        # 恢复选中状态
        if last_selected:
            self.category_tree.select_category(last_selected)
            self._on_category_selected(last_selected)
        
        # 刷新统计
        self._update_count()

    def _on_add_category_requested(self, parent_id: str):
        """请求添加分类"""
        # 如果有父分类，检查是否可以添加子分类
        if parent_id:
            can_add, msg = self.category_manager.can_add_child_category(parent_id)
            if not can_add:
                # 显示模板预览对话框
                templates = self.template_manager.get_templates_by_category(parent_id)
                parent = self.category_manager.get_category_by_id(parent_id)
                
                preview_dialog = TemplatePreviewDialog(parent.name, templates, self)
                if preview_dialog.exec():
                    if preview_dialog.should_move_templates():
                        # 打开批量移动对话框
                        move_dialog = BatchMoveDialog(self.category_manager, templates, self)
                        if move_dialog.exec():
                            target_category_id = move_dialog.get_target_category_id()
                            # 移动模板
                            for template in templates:
                                template.category_id = target_category_id
                            
                            InfoBar.success(
                                title='移动成功',
                                content=f'已移动 {len(templates)} 个模板',
                                orient=Qt.Orientation.Horizontal,
                                isClosable=True,
                                position=InfoBarPosition.TOP,
                                duration=3000,
                                parent=self
                            )
                        else:
                            return
                else:
                    return
        
        # 打开分类编辑对话框
        dialog = CategoryEditDialog(self.category_manager, mode="create", parent=self)
        if parent_id:
            # 设置父分类
            for i in range(dialog.parentCombo.count()):
                if dialog.parentCombo.itemData(i) == parent_id:
                    dialog.parentCombo.setCurrentIndex(i)
                    break
        
        if dialog.exec():
            if dialog.validate():
                category = dialog.get_category()
                success, msg = self.category_manager.add_category(category)
                
                if success:
                    self._on_categories_changed()
                    signal_bus.categories_changed.emit()
                    InfoBar.success(
                        title='添加成功',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                else:
                    InfoBar.error(
                        title='添加失败',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )



    def _on_edit_category_requested(self, category_id: str):
        """请求编辑分类"""
        category = self.category_manager.get_category_by_id(category_id)
        if not category:
            return
        
        dialog = CategoryEditDialog(
            self.category_manager,
            category=category,
            mode="edit",
            parent=self
        )
        
        if dialog.exec():
            if dialog.validate():
                updated_category = dialog.get_category()
                success, msg = self.category_manager.update_category(updated_category)
                
                if success:
                    self._on_categories_changed()
                    signal_bus.categories_changed.emit()
                    InfoBar.success(
                        title='更新成功',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                else:
                    InfoBar.error(
                        title='更新失败',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )

    def _on_delete_category_requested(self, category_id: str):
        """请求删除分类"""
        category = self.category_manager.get_category_by_id(category_id)
        if not category:
            return
        
        # 确认对话框
        msg_box = MessageBox(
            '确认删除',
            f'确定要删除分类 "{category.name}" 吗？',
            self
        )
        
        if msg_box.exec():
            success, msg = self.category_manager.delete_category(category_id)
            
            if success:
                self._on_categories_changed()
                self.current_category_id = None
                # self.edit_category_btn.setEnabled(False) # 这行可能有误，BasePageView 没这个
                self.template_table.set_templates([], "")
                
                signal_bus.categories_changed.emit()
                InfoBar.success(
                    title='删除成功',
                    content=msg,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title='删除失败',
                    content=msg,
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )

    # ========== 模板操作 ==========

    def _on_add_template_clicked(self):
        """新建模板按钮被点击"""
        dialog = TemplateEditDialog(
            self.template_manager,
            self.category_manager,
            mode="create",
            default_category_id=self.current_category_id,
            parent=self
        )
        
        if dialog.exec():
            if dialog.validate():
                template = dialog.get_template()
                self.template_manager.templates[template.id] = template
                
                # 刷新当前分类
                if self.current_category_id:
                    self._on_category_selected(self.current_category_id)
                
                InfoBar.success(
                    title='添加成功',
                    content=f'已添加模板 "{template.name}"',
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )

    def _on_edit_template_requested(self, template_id: str):
        """请求编辑模板"""
        template = self.template_manager.templates.get(template_id)
        if not template:
            return
        
        dialog = TemplateEditDialog(
            self.template_manager,
            self.category_manager,
            template=template,
            mode="edit",
            parent=self
        )
        
        if dialog.exec():
            if dialog.validate():
                updated_template = dialog.get_template()
                self.template_manager.templates[template_id] = updated_template
                
                # 刷新当前分类
                if self.current_category_id:
                    self._on_category_selected(self.current_category_id)
                
                InfoBar.success(
                    title='更新成功',
                    content=f'已更新模板 "{updated_template.name}"',
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )

    def _on_delete_template_requested(self, template_id: str):
        """请求删除模板"""
        template = self.template_manager.templates.get(template_id)
        if not template:
            return
        
        # 确认对话框
        msg_box = MessageBox(
            '确认删除',
            f'确定要删除模板 "{template.name}" 吗？',
            self
        )
        
        if msg_box.exec():
            del self.template_manager.templates[template_id]
            
            # 刷新当前分类
            if self.current_category_id:
                self._on_category_selected(self.current_category_id)
            
            InfoBar.success(
                title='删除成功',
                content=f'已删除模板 "{template.name}"',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

    def _on_batch_delete_clicked(self):
        """批量删除被点击"""
        checked_ids = self.template_table.get_checked_template_ids()
        
        if not checked_ids:
            InfoBar.warning(
                title='操作提示',
                content='请先勾选需要删除的模板',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
            
        # 确认对话框
        msg_box = MessageBox(
            '确认批量删除',
            f'确定要删除选中的 {len(checked_ids)} 个模板吗？此操作不可撤销。',
            self
        )
        
        if msg_box.exec():
            # 执行删除
            for tid in checked_ids:
                if tid in self.template_manager.templates:
                    del self.template_manager.templates[tid]
            
            # 刷新当前分类
            if self.current_category_id:
                self._on_category_selected(self.current_category_id)
            else:
                # 如果没有选中分类，可能是在搜索结果中批量删除
                self._on_search_changed(self.search_edit.text())
            
            # 刷新全库统计
            self._update_count()
            
            InfoBar.success(
                title='删除成功',
                content=f'已成功删除 {len(checked_ids)} 个模板',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

    # ========== 导入/导出 ==========

    def _on_export_clicked(self):
        """导出按钮被点击"""
        dialog = ExportDialog(self.template_manager, self.category_manager, self)
        
        if dialog.exec():
            if dialog.validate():
                options = dialog.get_export_options()
                success, msg = self.template_manager.export_to_file(**options)
                
                if success:
                    InfoBar.success(
                        title='导出成功',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                else:
                    InfoBar.error(
                        title='导出失败',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )

    def _on_import_clicked(self):
        """导入按钮被点击"""
        dialog = ImportDialog(self.template_manager, self.category_manager, self)
        
        if dialog.exec():
            if dialog.validate():
                options = dialog.get_import_options()
                success, msg = self.template_manager.import_from_file(**options)
                
                if success:
                    # 刷新界面
                    self.category_tree.load_categories()
                    if self.current_category_id:
                        self._on_category_selected(self.current_category_id)
                    self._update_count()
                    
                    InfoBar.success(
                        title='导入成功',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                else:
                    InfoBar.error(
                        title='导入失败',
                        content=msg,
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )

    def _on_checked_count_changed(self, count: int):
        """勾选数量改变"""
        self.batch_delete_btn.setEnabled(count > 0)
        
        # 如果需要，可以在按钮文字上显示数量
        if count > 0:
            self.batch_delete_btn.setText(f'批量删除 ({count})')
        else:
            self.batch_delete_btn.setText('批量删除')

    # ========== 辅助方法 ==========

    def _update_count(self):
        """更新统计信息"""
        total_categories = len(self.category_manager.get_all_categories())
        total_templates = len(self.template_manager.templates)
        self.count_label.setText(t("library.stats_total", categories=total_categories, templates=total_templates))
