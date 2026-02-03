"""
已连接视图 (Connected View)
管理所有已建立或待处理的链接，支持分类查看、列表搜索及批量操作
"""
import os
import typing
from typing import List, Optional
from PySide6.QtWidgets import QSplitter, QWidget, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import (
    PushButton, ToolButton, FluentIcon as FIF, MessageBox, 
    InfoBar, InfoBarPosition, Pivot, SearchLineEdit, PrimaryPushButton, 
    TransparentPushButton, StateToolTip, IndeterminateProgressRing
)
from src.gui.common import operation_runner
from src.gui.i18n import t
from src.core.services.context import service_bus
from src.common.signals import signal_bus
from src.gui.components import BasePageView, CategoryTreeWidget, BatchToolbar, LinkTable
from src.gui.styles import apply_transparent_style
from src.gui.views.connected.widgets import FlatLinkView


class ConnectedView(BasePageView):
    """已连接视图 - 管理所有连接状态"""

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("connected.title"),
            show_toolbar=True,
            enable_scroll=False,
            content_padding=False,
            add_stretch=False
        )

        # 注入服务
        self.connection_service = service_bus.connection_service
        self.config_service = service_bus.config_service
        self.category_manager = service_bus.category_manager
        self.user_manager = service_bus.user_manager
        
        self.current_category_id: str = "all"
        self._state_tooltip: Optional[StateToolTip] = None

        # 构建界面
        self._setup_toolbar()
        self._setup_content()
        self._connect_signals()

        # 初始化视图状态
        default_view = self.config_service.get_config("default_link_view", "list")
        self.view_pivot.setCurrentItem(default_view)
        self._on_view_pivot_changed(default_view)

        # 加载数据
        self._load_data()

    def _setup_toolbar(self):
        """设置工具栏"""
        toolbar = self.get_toolbar_layout()

        # 添加按钮
        self.add_btn = PrimaryPushButton(FIF.ADD, t("connected.add_link"))
        self.scan_btn = TransparentPushButton(FIF.SEARCH, t("connected.scan_apps"))
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.scan_btn)

        toolbar.addStretch(1)

        # 搜索与切换
        self.search_edit = SearchLineEdit()
        self.search_edit.setPlaceholderText(t("connected.search_placeholder"))
        self.search_edit.setFixedWidth(260)
        
        self.view_pivot = Pivot()
        self.view_pivot.addItem("list", t("connected.view_list"))
        self.view_pivot.addItem("category", t("connected.view_category"))
        
        self.refresh_btn = ToolButton(FIF.SYNC)
        self.refresh_btn.setToolTip(t("connected.refresh_status"))
        self.refresh_btn.clicked.connect(lambda: self._load_data(refresh_size=True))

        toolbar.addWidget(self.search_edit)
        toolbar.addSpacing(8)
        toolbar.addWidget(self.view_pivot)
        toolbar.addWidget(self.refresh_btn)

    def _setup_content(self):
        """设置主内容区"""
        content_layout = self.get_content_layout()

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 分类树
        self.category_tree = CategoryTreeWidget(self.category_manager, service_bus.user_manager)
        self.category_tree.setFixedWidth(240)
        
        # 堆栈视图
        self.view_stack = QStackedWidget()
        self.category_link_table = LinkTable()
        self.list_view = FlatLinkView()
        self.view_stack.addWidget(self.category_link_table)
        self.view_stack.addWidget(self.list_view)
        
        self.splitter.addWidget(self.category_tree)
        self.splitter.addWidget(self.view_stack)
        self.splitter.setStretchFactor(1, 1)
        apply_transparent_style(self.splitter)
        
        content_layout.addWidget(self.splitter, 1)

        # 批量工具栏
        self.batch_toolbar = BatchToolbar(self)
        self.batch_toolbar.set_mode("connected")
        self.batch_toolbar.hide()
        content_layout.addWidget(self.batch_toolbar)

    def _connect_signals(self):
        """信号绑定"""
        self.add_btn.clicked.connect(self._on_add_link)
        self.scan_btn.clicked.connect(self._on_scan)
        self.search_edit.textChanged.connect(self._on_search_changed)
        self.view_pivot.currentItemChanged.connect(self._on_view_pivot_changed)
        # 刷新按钮已在 _setup_toolbar 中绑定 explicit refresh_size=True
        
        self.category_tree.category_selected.connect(self._on_category_selected)
        
        # 表格操作
        for view in [self.category_link_table, self.list_view]:
            view.link_selected.connect(self._on_links_selected)
            view.action_clicked.connect(self._on_action_clicked)

        # 批量操作
        self.batch_toolbar.batch_establish_clicked.connect(self._on_batch_establish)
        self.batch_toolbar.batch_disconnect_clicked.connect(self._on_batch_disconnect)
        self.batch_toolbar.batch_remove_clicked.connect(self._on_batch_remove)
        self.batch_toolbar.clear_selection_clicked.connect(self._clear_all_selection)

        # 全局信号
        signal_bus.data_refreshed.connect(self._load_data)
        signal_bus.config_changed.connect(self._on_config_changed)


    def _load_data(self, refresh_size: bool = False):
        """加载数据"""
        view_models = self.connection_service.get_all_links(self.current_category_id)
        
        # 即使数据项目前暂时不支持 ViewModel，但在 View 层通过 DTO 桥接或强制转换适配
        # 这里演示注入 ViewModel 列表
        self.category_link_table.load_links(view_models)
        self.list_view.load_links(view_models)
        
        # 触发空间统计 (仅在需要时)
        if refresh_size and view_models:
            # 🆕 UI 反馈：通知表格进入加载状态
            self.category_link_table.set_all_sizes_loading()
            
            # 显示状态提示
            self._state_tooltip = StateToolTip(
                "正在统计空间占用",
                "计算中，请稍候...",
                self.window()
            )
            self._state_tooltip.show()

            # 注意：FlatLinkView 也需要这个支持，如果它是基于列表的视图
            if hasattr(self.list_view, 'table'):
                self.list_view.table.set_all_sizes_loading()
            elif hasattr(self.list_view, 'set_all_sizes_loading'):
                 self.list_view.set_all_sizes_loading()

            ids = [vm.id for vm in view_models]
            self.connection_service.calculate_sizes_async(ids, self._on_size_calculated)

    def _on_size_calculated(self, results: dict):
        """统计完成回调"""
        if self._state_tooltip:
            self._state_tooltip.setContent("统计更新完成 ✓")
            self._state_tooltip.setState(True)
            self._state_tooltip = None
        
        # 🆕 提示：此处不再手动 load_links，因为 ConnectionService 
        # 会通过 signal_bus 发射 data_refreshed 信号，驱动 _load_data 执行。

    def _on_category_selected(self, category_id: str):
        self.current_category_id = category_id
        self._load_data()

    def _on_view_pivot_changed(self, item_or_key):
        route_key = item_or_key if isinstance(item_or_key, str) else item_or_key.objectName()
        if route_key == "list":
            self.category_tree.hide()
            self.view_stack.setCurrentIndex(1)
            self.current_category_id = "all"
        else:
            self.category_tree.show()
            self.view_stack.setCurrentIndex(0)
        self._load_data()

    def _on_search_changed(self, text: str):
        # 简单的内存过滤逻辑，实际应调用 service
        self._load_data()

    def _on_links_selected(self, selected_ids: list):
        count = len(selected_ids)
        self.batch_toolbar.update_count(count)
        self.batch_toolbar.setVisible(count > 0)

    def _on_action_clicked(self, link_id: str, action: str):
        """单项操作"""
        if action == "establish":
            operation_runner.run_task_async(
                self.connection_service.establish_connection_by_id, 
                link_id, 
                title="正在建立连接",
                parent=self,
                on_finished=lambda s, m, d: self._load_data() if s else None
            )
        elif action == "disconnect":
            operation_runner.run_task_async(
                self.connection_service.disconnect_connection, 
                link_id, 
                title="正在断开连接",
                parent=self,
                on_finished=lambda s, m, d: self._load_data() if s else None
            )
        elif action == "reconnect":
            operation_runner.run_task_async(
                self.connection_service.reconnect_connection, 
                link_id, 
                title="正在重新连接",
                parent=self,
                on_finished=lambda s, m, d: self._load_data() if s else None
            )
        elif action == "edit":
            link = service_bus.user_manager.get_link_by_id(link_id)
            if link:
                from src.gui.dialogs.edit_link.dialog import EditLinkDialog
                dialog = EditLinkDialog(link, self)
                if dialog.exec():
                    self._load_data()
            return 
        elif action == "delete":
            link = service_bus.user_manager.get_link_by_id(link_id)
            if not link: return
            
            title = t("connected.confirm_remove_title")
            msg = t("connected.msg_delete_confirm").format(name=link.name)
            if MessageBox(title, msg, self).exec():
                service_bus.user_manager.remove_link(link_id)
                InfoBar.success(t("common.success"), t("connected.batch_remove"), duration=2000, position='TopCenter', parent=self)
                self._load_data()
            return


    def _on_batch_establish(self):
        checked_ids = self._get_checked_ids()
        if not checked_ids: return
        
        operation_runner.run_batch_task_async(
            checked_ids,
            self.connection_service.establish_connection_by_id,
            "批量建立连接",
            lambda lid: f"正在建立: {self.user_manager.get_link_by_id(lid).name}",
            parent=self,
            on_finished=lambda s, m, d: (self._load_data(), self._clear_all_selection())
        )

    def _on_batch_disconnect(self):
        checked_ids = self._get_checked_ids()
        if not checked_ids: return
        
        operation_runner.run_batch_task_async(
            checked_ids,
            self.connection_service.disconnect_connection,
            "批量断开连接",
            lambda lid: f"正在断开: {self.user_manager.get_link_by_id(lid).name}",
            parent=self,
            on_finished=lambda s, m, d: (self._load_data(), self._clear_all_selection())
        )

    def _on_batch_remove(self):
        checked_ids = self._get_checked_ids()
        if not checked_ids: return
        if MessageBox("确认移除", f"确定要移除选中的 {len(checked_ids)} 个连接配置吗？", self).exec():
            operation_runner.run_batch_task_async(
                checked_ids,
                self.user_manager.remove_link,
                "批量移除配置",
                lambda lid: f"正在移除: {self.user_manager.get_link_by_id(lid).name}",
                parent=self,
                on_finished=lambda s, m, d: (self._load_data(), self._clear_all_selection())
            )

    def _get_checked_ids(self) -> List[str]:
        if self.view_stack.currentIndex() == 0:
            return self.category_link_table.get_selected_links()
        return self.list_view.get_selected_links()

    def _clear_all_selection(self):
        self.category_link_table.clear_selection()
        self.list_view.clear_selection()
        self.batch_toolbar.hide()

    def _on_config_changed(self, key, value):
        if key == "default_link_view":
            self.view_pivot.setCurrentItem(str(value))

    def _on_add_link(self):
        from src.gui.dialogs import AddLinkDialog
        dialog = AddLinkDialog(self)
        if dialog.exec(): self._load_data()

    def _on_scan(self):
        from src.gui.dialogs import ScanFlowDialog
        dialog = ScanFlowDialog(self.category_manager, self)
        if dialog.exec(): self._load_data()
