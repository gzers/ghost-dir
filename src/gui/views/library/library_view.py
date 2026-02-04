import os
from typing import List, Optional, Set
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QFrame
)
from qfluentwidgets import (
    SearchLineEdit, TransparentToolButton, FluentIcon as FIF,
    InfoBar, MessageBox, RoundMenu, Action
)
from src.gui.i18n import t
from src.core.services.context import service_bus
from src.common.signals import signal_bus
from src.data.model import Template, CategoryNode
from src.gui.components import BasePageView, CategoryTreeWidget, BatchToolbar
from src.gui.views.library.widgets import TemplateTableWidget
from src.gui.dialogs import (
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
            enable_scroll=False,
            content_padding=False,
            add_stretch=False
        )

        # 注入服务
        self.category_service = service_bus.category_service
        self.template_service = service_bus.template_service
        
        self.current_category_id: Optional[str] = None

        # 设置页面内容
        self._setup_content()
        self._connect_signals()
        
        # 初始加载
        self._validate_and_load()
        self._filter_templates()

    def _setup_content(self):
        """设置页面内容"""
        content_layout = self.get_content_layout()
        
        # 顶部工具栏 (由 BasePageView 提供容器)
        toolbar_layout = self.get_toolbar_layout()
        
        # 1. 标题和统计
        self.count_label = QLabel(self)
        self.count_label.setStyleSheet("color: gray;")
        toolbar_layout.addWidget(self.count_label)
        toolbar_layout.addStretch(1)

        # 2. 搜索框
        self.search_edit = SearchLineEdit(self)
        self.search_edit.setPlaceholderText(t("library.search_placeholder"))
        self.search_edit.setFixedWidth(300)
        toolbar_layout.addWidget(self.search_edit)

        # 3. 操作按钮
        self.add_template_btn = TransparentToolButton(FIF.ADD, self)
        self.add_template_btn.setToolTip(t("library.add_template_tooltip"))
        toolbar_layout.addWidget(self.add_template_btn)

        self.refresh_btn = TransparentToolButton(FIF.SYNC, self)
        self.refresh_btn.setToolTip(t("common.refresh"))
        toolbar_layout.addWidget(self.refresh_btn)

        self.more_btn = TransparentToolButton(FIF.MORE, self)
        toolbar_layout.addWidget(self.more_btn)

        # 主要内容区：左侧分类树 + 右侧模板表格
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        content_layout.addLayout(main_layout, 1)

        # 左侧分类树
        self.category_tree = CategoryTreeWidget(
            service_bus.category_manager, 
            service_bus.user_manager, 
            parent=self
        )
        self.category_tree.setFixedWidth(240)
        main_layout.addWidget(self.category_tree)

        # 右侧堆栈/容器
        self.right_container = QFrame(self)
        self.right_container.setObjectName("rightContainer")
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.right_container, 1)

        # 模板表格
        self.template_table = TemplateTableWidget(self, service_bus.user_manager)
        right_layout.addWidget(self.template_table)

        # 批量操作栏
        self.batch_toolbar = BatchToolbar(self)
        self.batch_toolbar.set_mode("library")
        self.batch_toolbar.hide()
        content_layout.addWidget(self.batch_toolbar)

    def _connect_signals(self):
        """连接信号"""
        # 分类树信号
        self.category_tree.category_selected.connect(self._on_category_selected)
        self.category_tree.add_category_requested.connect(self._on_add_category_requested)
        self.category_tree.edit_category_requested.connect(self._on_edit_category_requested)
        self.category_tree.delete_category_requested.connect(self._on_delete_category_requested)

        # 搜索和按钮信号
        self.search_edit.textChanged.connect(self._on_search_changed)
        self.add_template_btn.clicked.connect(self._on_add_template_clicked)
        self.refresh_btn.clicked.connect(self._on_refresh_clicked)
        self.more_btn.clicked.connect(self._on_show_more_menu)

        # 表格信号
        self.template_table.edit_template_requested.connect(self._on_edit_template_requested)
        self.template_table.delete_template_requested.connect(self._on_delete_template_requested)
        self.template_table.checked_changed.connect(self._on_checked_count_changed)

        # 批量操作栏信号
        self.batch_toolbar.batch_delete_clicked.connect(self._on_batch_delete_clicked)
        self.batch_toolbar.clear_selection_clicked.connect(self._clear_all_selection)

        # 信号总线监听
        signal_bus.categories_changed.connect(self._on_categories_changed)

    def _validate_and_load(self):
        """验证模板并加载"""
        orphaned = self.template_service.manager.validate_all_templates()
        if orphaned:
            InfoBar.warning(
                title=t("library.orphaned_warning_title"),
                content=t("library.orphaned_warning_content", count=len(orphaned)),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position='TopCenter',
                duration=5000,
                parent=self
            )

    def _on_category_selected(self, category_id: str):
        """分类选择回调"""
        self.current_category_id = category_id
        self._filter_templates()

    def _on_search_changed(self, text: str):
        """搜索内容改变回调"""
        self._filter_templates()

    def _filter_templates(self):
        """调用 Service 层执行统一过滤"""
        search_text = self.search_edit.text()
        category_id = self.current_category_id or "all"
        
        view_models = self.template_service.get_filtered_templates(category_id, search_text)
        
        is_leaf = self.category_service.manager.is_leaf(category_id) if category_id != "all" else False
        allow_ops = (category_id == "all") or is_leaf
        self.add_template_btn.setEnabled(allow_ops)
        self.template_table.set_templates(view_models, category_id, allow_operations=allow_ops)
        
        if search_text:
            all_templates = self.template_service.manager.get_all_templates()
            matched_categories = set()
            for tpl in all_templates:
                if (search_text in tpl.name.lower() or 
                    (tpl.description and search_text in tpl.description.lower())):
                    matched_categories.add(tpl.category_id)
            self.category_tree.highlight_categories(matched_categories)
            self.count_label.setText(t("library.stats_search", count=len(view_models)))
        else:
            self.category_tree.clear_highlights()
            if category_id == "all":
                total_categories = len(self.category_service.manager.get_all_categories())
                self.count_label.setText(t("library.stats_total", categories=total_categories, templates=len(view_models)))
            else:
                category = self.category_service.manager.get_category_by_id(category_id)
                name = category.name if category else "未知"
                self.count_label.setText(t("library.stats_category", name=name, count=len(view_models)))

    def _on_refresh_clicked(self):
        """刷新按钮被点击"""
        self.template_service.manager.load_templates()
        self.category_service.manager.load_categories()
        self.category_tree.load_categories()
        self._filter_templates()
        InfoBar.success(t("common.success"), t("library.refresh_success"), duration=2000, position='TopCenter', parent=self)

    def _on_show_more_menu(self):
        """显示更多菜单"""
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.DOWNLOAD, t("library.export"), self, triggered=self._on_export_requested))
        menu.addAction(Action(FIF.UP, t("library.import"), self, triggered=self._on_import_clicked))
        menu.addSeparator()
        menu.addAction(Action(FIF.SETTING, t("library.manage_categories"), self, triggered=self._on_manage_categories))
        
        pos = self.more_btn.mapToGlobal(QPoint(0, self.more_btn.height()))
        menu.exec(pos, ani=True)

    def _on_manage_categories(self):
        """管理分类"""
        dialog = CategoryManagerDialog(self)
        dialog.exec()
        self._on_categories_changed()

    def _on_categories_changed(self):
        """分类数据变更回调"""
        last_selected = self.current_category_id
        self.category_service.manager.load_categories()
        self.category_tree.load_categories()
        if last_selected:
            self.category_tree.select_category(last_selected)
        self._filter_templates()

    def _on_add_category_requested(self, parent_id: Optional[str] = None):
        """请求添加分类"""
        if parent_id:
            can_add, msg = self.category_service.manager.can_add_child_category(parent_id)
            if not can_add:
                templates = self.template_service.manager.get_templates_by_category(parent_id)
                parent = self.category_service.manager.get_category_by_id(parent_id)
                preview_dialog = TemplatePreviewDialog(parent.name, templates, self)
                if preview_dialog.exec():
                    move_dialog = BatchMoveDialog(self.category_service.manager, templates, self)
                    if move_dialog.exec():
                        target_category_id = move_dialog.get_target_category_id()
                        for t in templates:
                            t.category_id = target_category_id
                        self.template_service.manager.load_templates()
                    else:
                        return
                else:
                    return
        
        from src.gui.dialogs.category_manager import CategoryEditDialog
        dialog = CategoryEditDialog(self.category_service.manager, mode="create", parent=self)
        if parent_id:
            for i in range(dialog.parentCombo.count()):
                if dialog.parentCombo.itemData(i) == parent_id:
                    dialog.parentCombo.setCurrentIndex(i)
                    break
        
        if dialog.exec():
            if dialog.validate():
                category = dialog.get_category()
                success, msg = self.category_service.add_category(category.name, category.parent_id)
                if success:
                    self._on_categories_changed()
                    InfoBar.success(t("common.success"), msg, duration=2000, position='TopCenter', parent=self)
                else:
                    InfoBar.error(t("common.error"), msg, duration=3000, position='TopCenter', parent=self)

    def _on_edit_category_requested(self, category_id: str):
        """请求编辑分类"""
        category = self.category_service.manager.get_category_by_id(category_id)
        if not category: return
        dialog = CategoryEditDialog(self.category_service.manager, category=category, mode="edit", parent=self)
        if dialog.exec():
            if dialog.validate():
                updated_category = dialog.get_category()
                success, msg = self.category_service.update_category(updated_category)
                if success:
                    self._on_categories_changed()
                    InfoBar.success(t("common.success"), msg, duration=2000, position='TopCenter', parent=self)
                else:
                    InfoBar.error(t("common.error"), msg, duration=3000, position='TopCenter', parent=self)

    def _on_delete_category_requested(self, category_id: str):
        """请求删除分类"""
        status, context = self.category_service.validate_delete(category_id)
        if status == "ERROR":
            InfoBar.error("错误", context["message"], duration=3000, position='TopCenter', parent=self)
            return

        if status == "REQUIRED_CONFIRM":
            msg_box = MessageBox("确认删除", context["message"], self)
            if not msg_box.exec(): return

        success, msg = self.category_service.execute_delete(category_id, force=True)
        if success:
            self._on_categories_changed()
            self.current_category_id = None
            self.template_table.set_templates([], "")
            InfoBar.success("删除成功", msg, duration=2000, position='TopCenter', parent=self)
        else:
            InfoBar.error("删除失败", msg, duration=3000, position='TopCenter', parent=self)

    def _on_add_template_clicked(self):
        """新建模板按钮被点击"""
        dialog = TemplateEditDialog(
            mode="create",
            default_category_id=self.current_category_id,
            parent=self
        )
        if dialog.exec():
            # 由于验证成功后逻辑已在 Service 完成，此处只需刷新 UI
            if self.current_category_id:
                self._on_category_selected(self.current_category_id)
            else:
                self._filter_templates()
            InfoBar.success('处理成功', '模板已创建', duration=2000, position='TopCenter', parent=self)

    def _on_edit_template_requested(self, template_id: str):
        """请求编辑模板"""
        template = self.template_service.manager.templates.get(template_id)
        if not template: return
        dialog = TemplateEditDialog(
            template=template,
            mode="edit",
            parent=self
        )
        if dialog.exec():
            # 业务持久化已在对话框 validate() 调用 Service 完成
            self._filter_templates()
            InfoBar.success('处理成功', '模板已更新', duration=2000, position='TopCenter', parent=self)

    def _on_delete_template_requested(self, template_id: str):
        """请求删除模板"""
        template = self.template_service.manager.templates.get(template_id)
        if not template: return
        msg_box = MessageBox('确认删除', f'确定要删除模板 "{template.name}" 吗？', self)
        if msg_box.exec():
            success, msg = self.template_service.delete_template(template_id)
            if success:
                self._filter_templates()
                InfoBar.success('删除成功', f'已删除模板 "{template.name}"', duration=2000, position='TopCenter', parent=self)
            else:
                InfoBar.error('删除失败', msg, duration=2000, position='TopCenter', parent=self)

    def _on_batch_delete_clicked(self):
        """批量删除被点击"""
        checked_ids = self.template_table.get_checked_template_ids()
        if not checked_ids: return
        msg_box = MessageBox('确认批量删除', f'确定要删除选中的 {len(checked_ids)} 个模板吗？', self)
        if msg_box.exec():
            success, msg = self.template_service.batch_delete_templates(checked_ids)
            if success:
                self._filter_templates()
                self._update_count()
                self._clear_all_selection()
                InfoBar.success('删除成功', msg, duration=2000, position='TopCenter', parent=self)
            else:
                InfoBar.error('删除失败', msg, duration=2000, position='TopCenter', parent=self)

    def _on_export_requested(self):
        """导出请求"""
        dialog = ExportDialog(self.template_service.manager, self.category_service.manager, self)
        if dialog.exec() and dialog.validate():
            options = dialog.get_export_options()
            # 从 options 中取出文件路径（假设 dialog 的 key 是 file_path）
            path = options.pop('file_path', None)
            if path:
                success, msg = self.template_service.export_to_file(path, options)
                if success: InfoBar.success("成功", msg, duration=2000, position='TopCenter', parent=self)
                else: InfoBar.error("失败", msg, duration=3000, position='TopCenter', parent=self)

    def _on_import_clicked(self):
        """导入请求"""
        dialog = ImportDialog(self.template_service.manager, self.category_service.manager, self)
        if dialog.exec() and dialog.validate():
            options = dialog.get_import_options()
            path = options.pop('file_path', None)
            if path:
                success, msg = self.template_service.import_from_file(path, options)
                if success:
                    self._on_categories_changed()
                    InfoBar.success("成功", msg, duration=2000, position='TopCenter', parent=self)
                else: InfoBar.error("失败", msg, duration=3000, position='TopCenter', parent=self)

    def _on_checked_count_changed(self, count: int):
        """勾选数量改变"""
        if count > 0:
            self.batch_toolbar.update_count(count)
            self.batch_toolbar.show()
        else:
            self.batch_toolbar.hide()

    def _clear_all_selection(self):
        """清除选择"""
        self.template_table.clear_selection()
        self.batch_toolbar.hide()

    def _update_count(self):
        """更新全局统计"""
        total_categories = len(self.category_service.manager.get_all_categories())
        total_templates = len(self.template_service.manager.get_all_templates())
        self.count_label.setText(t("library.stats_total", categories=total_categories, templates=total_templates))
