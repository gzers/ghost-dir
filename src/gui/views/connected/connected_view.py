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
    InfoBar, Pivot, SearchLineEdit, PrimaryPushButton, 
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

        self.help_btn = ToolButton(FIF.HELP)
        self.help_btn.setToolTip(t("connected.status_help_title"))
        self.help_btn.clicked.connect(self._on_show_status_help)

        toolbar.addWidget(self.search_edit)
        toolbar.addSpacing(8)
        toolbar.addWidget(self.view_pivot)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.help_btn)

    def _setup_content(self):
        """设置主内容区"""
        content_layout = self.get_content_layout()

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 分类树（显示连接数量）
        self.category_tree = CategoryTreeWidget(
            self.category_manager, 
            service_bus.user_manager,
            show_count=True,
            count_provider=lambda cid: len(self.user_manager.get_links_by_category(cid)) if cid != "all" else len(self.user_manager.get_all_links())
        )
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
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("QSplitter::handle { background: transparent; }")
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
            
            # 🆕 统一使用 TopCenter InfoBar 代替左上角 StateToolTip
            InfoBar.info(
                "正在统计",
                "正在统计空间占用，请稍候...",
                duration=2000,
                position='TopCenter',
                parent=self.window()
            )

            # 注意：FlatLinkView 也需要这个支持，如果它是基于列表的视图
            if hasattr(self.list_view, 'table'):
                self.list_view.table.set_all_sizes_loading()
            elif hasattr(self.list_view, 'set_all_sizes_loading'):
                 self.list_view.set_all_sizes_loading()

            ids = [vm.id for vm in view_models]
            self.connection_service.calculate_sizes_async(ids, self._on_size_calculated)

    def _on_size_calculated(self, results: dict):
        """统计完成回调"""
        # 显示单次汇总通知
        InfoBar.success(
            "统计完成",
            "统计更新完成 ✓",
            duration=2000,
            position='TopCenter',
            parent=self.window()
        )
        
    def _on_show_status_help(self):
        """显示状态定义说明"""
        from src.gui.styles.utils.color_utils import get_status_colors, get_text_secondary, get_divider_color
        colors = get_status_colors()
        sec_color = get_text_secondary()
        border_color = get_divider_color()
        
        title = t("connected.status_help_title")
        
        # 封装表格行 html，使用 table 解决换行对齐问题，使用 SVG 圆点解决显示不全问题
        def get_row_html(status_key, label_key):
            color = colors.get(status_key, "#808080")
            status_name = t(f"connected.status_{status_key}")
            desc = t(f"connected.{label_key}")
            # 使用简单的 SVG 确保圆点在富文本中不被截断且居中
            dot_svg = f"""<svg width="12" height="12"><circle cx="6" cy="6" r="5" fill="{color}" /></svg>"""
            return f"""
                <tr>
                    <td style="padding: 10px 8px; vertical-align: top; width: 80px;">
                        <span style="white-space: nowrap;">{dot_svg} <b>{status_name}</b></span>
                    </td>
                    <td style="padding: 10px 8px; vertical-align: top; color: {sec_color};">
                        {desc}
                    </td>
                </tr>
            """

        content = f"""
            <table style="width: 100%; border-collapse: collapse;">
                {get_row_html('connected', 'status_connected_desc')}
                {get_row_html('disconnected', 'status_disconnected_desc')}
                {get_row_html('ready', 'status_ready_desc')}
                {get_row_html('invalid', 'status_invalid_desc')}
            </table>
            <div style="margin-top: 15px; border-top: 1px solid {border_color}; padding-top: 15px;">
                <b style="font-size: 14px;">{t('connected.edit_rule_title')}</b>
                <p style="margin-top: 8px; color: {sec_color}; line-height: 1.5;">{t('connected.edit_rule_desc')}</p>
            </div>
        """
        
        # 使用 MessageBox 并配置单一居中按钮
        msg = MessageBox(title, "", self)
        msg.titleLabel.setText(title)
        msg.contentLabel.setText(content) # QLabel 使用 setText 渲染 HTML
        msg.cancelButton.hide() # 隐藏取消按钮，使 OK 按钮自动居中
        msg.yesButton.setFixedWidth(120)
        msg.exec()

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
                title=t("connected.establish"),
                parent=self,
                on_start=lambda: self.category_link_table.show_loading(link_id, True),
                on_finished=lambda s, m, d: (
                    self.category_link_table.show_loading(link_id, False),
                    self._load_data() if s else None
                )
            )
        elif action == "disconnect":
            operation_runner.run_task_async(
                self.connection_service.disconnect_connection, 
                link_id, 
                title=t("connected.disconnect"),
                parent=self,
                on_start=lambda: self.category_link_table.show_loading(link_id, True),
                on_finished=lambda s, m, d: (
                    self.category_link_table.show_loading(link_id, False),
                    self._load_data() if s else None
                )
            )
        elif action == "reconnect":
            operation_runner.run_task_async(
                self.connection_service.reconnect_connection, 
                link_id, 
                title=t("connected.reconnect"),
                parent=self,
                on_start=lambda: self.category_link_table.show_loading(link_id, True),
                on_finished=lambda s, m, d: (
                    self.category_link_table.show_loading(link_id, False),
                    self._load_data() if s else None
                )
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
                InfoBar.success(
                    t("common.success"), 
                    t("connected.batch_remove"), 
                    duration=2000, 
                    position='TopCenter', 
                    parent=self
                )
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
