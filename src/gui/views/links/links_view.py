"""
链接视图 (Links View)
管理所有已建立或待处理的链接，支持分类查看、列表搜索及批量操作
"""
import os
import typing
from typing import List, Optional
from PySide6.QtWidgets import QSplitter, QWidget, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6 import QtCore
from qfluentwidgets import (
    PushButton, ToolButton, FluentIcon as FIF, MessageBox,
    InfoBar, Pivot, SearchLineEdit, PrimaryPushButton,
    TransparentPushButton, StateToolTip, IndeterminateProgressRing
)
from src.gui.common import operation_runner
from src.gui.i18n import t
from src.common.service_bus import service_bus
# TODO: 通过 app 实例访问 Service
from src.common.signals import signal_bus
from src.gui.components import BasePageView, CategoryTreeWidget, BatchToolbar, LinkTable
from src.gui.styles import apply_transparent_style
from src.gui.views.links.widgets import FlatLinkView
from src.models.link import LinkStatus


class LinksView(BasePageView):
    """链接视图 - 管理所有链接状态"""

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("links.title"),
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
        self._init_throttling()

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
        self.add_btn = PrimaryPushButton(FIF.ADD, t("links.add_link"))
        self.scan_btn = TransparentPushButton(FIF.SEARCH, t("links.scan_apps"))
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.scan_btn)

        toolbar.addStretch(1)

        # 搜索与切换
        self.search_edit = SearchLineEdit()
        self.search_edit.setPlaceholderText(t("links.search_placeholder"))
        self.search_edit.setFixedWidth(260)

        self.view_pivot = Pivot()
        self.view_pivot.addItem("list", t("links.view_list"))
        self.view_pivot.addItem("category", t("links.view_category"))

        self.refresh_btn = ToolButton(FIF.SYNC)
        self.refresh_btn.setToolTip(t("links.refresh_status"))
        self.refresh_btn.clicked.connect(lambda: self._load_data(refresh_size=True))

        self.help_btn = ToolButton(FIF.HELP)
        self.help_btn.setToolTip(t("links.status_help_title"))
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

        # 分类树（显示链接数量）
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
        self.batch_toolbar.set_mode("links")
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
        self.category_link_table.load_links(view_models)
        self.list_view.load_links(view_models)

        # 如果需要彻底刷新（点击同步按钮时）
        if refresh_size and view_models:
            ids = [vm.id for vm in view_models]
            
            # 【关键修复】先设置加载动画，再启动异步任务
            # 1. 同步启动视觉加载反馈（必须在异步任务前）
            self.category_link_table.set_all_status_loading()
            self.category_link_table.set_all_sizes_loading()
            self.list_view.set_all_status_loading()
            self.list_view.set_all_sizes_loading()
            
            # 2. 启动异步状态探测（在动画设置后）
            self.connection_service.refresh_status_async(
                ids,
                self._on_single_status_refreshed,
                None  # 状态探测完成不需要触发后续动作
            )
            
            # 3. 启动异步空间统计（在动画设置后）
            self.connection_service.calculate_sizes_async(
                ids, 
                self._on_single_size_calculated,
                self._on_all_sizes_finished
            )

    # --- 专题优化：UI 节流更新逻辑 ---
    def _init_throttling(self):
        """初始化 UI 刷新节流器"""
        self._update_queue = [] # [(type, id, data)]
        self._throttle_timer = QtCore.QTimer(self)
        self._throttle_timer.setInterval(50) # 缩短至 50ms，提升感知度
        self._throttle_timer.timeout.connect(self._process_update_batch)
        self._throttle_timer.start()

    def _process_update_batch(self):
        """原子化批量处理 UI 信号"""
        if not self._update_queue: return
        
        # 原子交换队列，防止处理期间 append 冲突
        batch = self._update_queue
        self._update_queue = []
        
        status_updates = {}
        size_updates = {}
        
        for u_type, lid, data in batch:
            if u_type == 'status': status_updates[lid] = data
            elif u_type == 'size': size_updates[lid] = data

        # 执行批量 UI 刷新
        from src.common.config import format_size
        for lid, status in status_updates.items():
            self.category_link_table.update_row_status(lid, status)
            if hasattr(self.list_view, 'update_row_status'):
                self.list_view.update_row_status(lid, status)
        
        for lid, size in size_updates.items():
            try:
                size_val = int(size) if size is not None else 0
                # 即使是 0 字节也应该格式化显示（如 0 B），而不是显示“未计算”
                size_text = format_size(size_val)
                
                self.category_link_table.update_row_size(lid, size_text)
                if hasattr(self.list_view, 'update_row_size'):
                    self.list_view.update_row_size(lid, size_text)
            except Exception as e:
                print(f"渲染组件更新失败 [{lid}]: {e}")

    @QtCore.Slot(str, object)
    def _on_single_status_refreshed(self, link_id: str, status: object):
        """单条状态刷新完成 - 入队节流"""
        self._update_queue.append(('status', link_id, status))

    @QtCore.Slot(str, object)
    def _on_single_size_calculated(self, link_id: str, size: object):
        """单行统计完成 - 入队节流"""
        self._update_queue.append(('size', link_id, size))

    @QtCore.Slot(dict)
    def _on_all_sizes_finished(self, results: dict):
        """全部统计完成：发送单一汇总通知"""
        InfoBar.success(
            "统计完成",
            f"已完成 {len(results)} 项空间占用统计项目流程图",
            duration=3000,
            position='TopCenter',
            parent=self.window()
        )

    def _on_show_status_help(self):
        """显示状态定义说明"""
        from src.gui.styles.utils.color_utils import get_status_colors, get_text_secondary, get_divider_color
        colors = get_status_colors()
        sec_color = get_text_secondary()
        border_color = get_divider_color()

        title = t("links.status_help_title")

        # 封装表格行 html，使用 table 解决换行对齐问题，使用 SVG 圆点解决显示不全问题
        def get_row_html(status_key, label_key):
            color = colors.get(status_key, "#808080")
            status_name = t(f"links.status_{status_key}")
            desc = t(f"links.{label_key}")
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
                <b style="font-size: 14px;">{t('links.edit_rule_title')}</b>
                <p style="margin-top: 8px; color: {sec_color}; line-height: 1.5;">{t('links.edit_rule_desc')}</p>
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

        if action == "establish" or action == "reconnect":
            title_text = t("links.establish") if action == "establish" else t("links.reconnect")
            runner_fn = self.connection_service.establish_connection_by_id if action == "establish" else self.connection_service.reconnect_connection
            
            def _on_establish_finished(success: bool, msg: str, data: dict):
                # 统一清理两方视图的加载状态
                self.category_link_table.show_loading(link_id, False)
                self.list_view.show_loading(link_id, False)
                
                print(f"[DEBUG] 操作结束: success={success}, msg={msg}")
                if success:
                    self._load_data()
                elif msg == "TARGET_EXISTS":
                    # ⚠️ 终于捕获到冲突，强制触发迁移流程
                    print(f"[DEBUG] 确认冲突，正在唤起迁移面板")
                    self._handle_action_migration(link_id, action)
                else:
                    # 其他错误已有 OperationRunner 弹 InfoBar
                    pass

            operation_runner.run_task_async(
                runner_fn, 
                link_id,
                title=title_text,
                parent=self,
                on_start=lambda: (
                    self.category_link_table.show_loading(link_id, True),
                    self.list_view.show_loading(link_id, True)
                ),
                on_finished=_on_establish_finished
            )
        elif action == "disconnect":
            # 询问用户是否需要逆向迁移
            link = self.user_manager.get_link_by_id(link_id)
            if not link:
                return
                
            from qfluentwidgets import MessageBox
            
            # 创建自定义对话框
            w = MessageBox(
                "断开连接",
                f"您要断开链接：{link.name}\n\n请选择断开方式：",
                self
            )
            w.contentLabel.setMinimumWidth(600)  # 设置内容区域宽度
            
            # 修改按钮文字和样式
            from qfluentwidgets import PushButton, PrimaryPushButton
            
            # 迁移回软件路径（推荐）- 第一个按钮，强调色
            w.yesButton.setText("迁移回软件路径（推荐）")
            w.yesButton.setObjectName("primaryButton")
            w.yesButton.setMinimumWidth(200)
            
            # 仅断开链接 - 第二个按钮，普通样式
            disconnect_btn = PushButton("仅断开链接", w)
            disconnect_btn.setMinimumWidth(140)
            w.buttonLayout.insertWidget(1, disconnect_btn)
            
            w.cancelButton.setText("取消")
            w.cancelButton.setMinimumWidth(100)
            
            result = None
            w.yesButton.clicked.connect(lambda: setattr(w, '_result', 'migrate') or w.accept())
            disconnect_btn.clicked.connect(lambda: setattr(w, '_result', 'disconnect') or w.accept())
            w.cancelButton.clicked.connect(lambda: setattr(w, '_result', 'cancel') or w.reject())
            
            if w.exec():
                result = getattr(w, '_result', 'cancel')
            else:
                result = 'cancel'
            
            if result == 'cancel':
                return
            elif result == 'migrate':
                # 逆向迁移：库路径 -> 软件路径
                self._handle_reverse_migration(link_id)
            else:
                # 仅断开链接
                operation_runner.run_task_async(
                    self.connection_service.disconnect_connection,
                    link_id,
                    title=t("links.disconnect"),
                    parent=self,
                    on_start=lambda: (
                        self.category_link_table.show_loading(link_id, True),
                        self.list_view.show_loading(link_id, True)
                    ),
                    on_finished=lambda s, m, d: (
                        self.category_link_table.show_loading(link_id, False),
                        self.list_view.show_loading(link_id, False),
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

            title = t("links.confirm_remove_title")
            msg = t("links.msg_delete_confirm").format(name=link.name)
            if MessageBox(title, msg, self).exec():
                service_bus.user_manager.remove_link(link_id)
                InfoBar.success(
                    t("common.success"),
                    t("links.batch_remove"),
                    duration=2000,
                    position='TopCenter',
                    parent=self
                )
                self._load_data()
            return

    def _handle_action_migration(self, link_id: str, action: str):
        """处理操作过程中的冲突：软件路径有真实数据"""
        link = self.user_manager.get_link_by_id(link_id)
        if not link: return

        from qfluentwidgets import MessageBox
        
        # 展开环境变量
        source_real = os.path.expandvars(link.source_path)  # 软件路径
        target_real = os.path.expandvars(link.target_path)  # 库路径

        # 创建冲突处理对话框
        w = MessageBox(
            "路径冲突",
            f"软件路径已存在数据：{source_real}\n\n请选择处理方式：",
            self
        )
        w.contentLabel.setMinimumWidth(550)
        
        from qfluentwidgets import PushButton, PrimaryPushButton
        
        # 保留软件路径数据（推荐）- 第一个按钮，强调色
        w.yesButton.setText("保留软件路径数据（推荐）")
        w.yesButton.setObjectName("primaryButton")
        w.yesButton.setMinimumWidth(200)
        
        # 用库数据覆盖 - 第二个按钮
        overwrite_btn = PushButton("用库数据覆盖", w)
        overwrite_btn.setMinimumWidth(140)
        w.buttonLayout.insertWidget(1, overwrite_btn)
        
        w.cancelButton.setText("取消")
        w.cancelButton.setMinimumWidth(100)
        
        result = None
        w.yesButton.clicked.connect(lambda: setattr(w, '_result', 'keep') or w.accept())
        overwrite_btn.clicked.connect(lambda: setattr(w, '_result', 'overwrite') or w.accept())
        w.cancelButton.clicked.connect(lambda: setattr(w, '_result', 'cancel') or w.reject())
        
        if w.exec():
            result = getattr(w, '_result', 'cancel')
        else:
            result = 'cancel'
        
        if result == 'cancel':
            return
        elif result == 'overwrite':
            # 覆盖：删除软件路径数据，用库数据建立链接
            self._handle_overwrite_and_connect(link_id, source_real)
        else:
            # 保留：将软件路径数据迁移到库，覆盖库中的旧数据
            self._handle_migrate_and_connect(link_id, source_real, target_real, action)

    def _handle_overwrite_and_connect(self, link_id: str, source_real: str):
        """覆盖现有数据并建立链接"""
        from qfluentwidgets import InfoBar
        
        # 获取库路径
        link = self.user_manager.get_link_by_id(link_id)
        if not link:
            return
        
        target_real = os.path.expandvars(link.target_path)  # 库路径
        
        # 关键检查：确保库路径有数据
        if not os.path.exists(target_real) or not os.listdir(target_real):
            InfoBar.error(
                "覆盖失败",
                f"库路径为空或不存在，无法覆盖。\n请先确保库路径有数据：{target_real}",
                duration=5000,
                position='TopCenter',
                parent=self
            )
            return
        
        try:
            import shutil
            if os.path.exists(source_real):
                if os.path.isfile(source_real):
                    os.remove(source_real)
                else:
                    shutil.rmtree(source_real)
            
            # 删除成功后，直接尝试建立连接（不走 _on_action_clicked 避免循环）
            conn_success, conn_msg = self.connection_service.establish_connection_by_id(link_id)
            if conn_success:
                self._load_data()
            else:
                InfoBar.error(
                    "建立连接失败",
                    f"覆盖后仍无法建立连接：{conn_msg}",
                    duration=5000,
                    position='TopCenter',
                    parent=self
                )
        except Exception as e:
            InfoBar.error(
                "删除失败",
                f"无法删除现有数据：{str(e)}",
                duration=3000,
                position='TopCenter',
                parent=self
            )

    def _handle_migrate_and_connect(self, link_id: str, source_real: str, target_real: str, action: str):
        """迁移数据到库路径并建立链接"""
        from src.gui.dialogs.migration import MigrationProgressDialog, MigrationResultDialog
        from src.services.migration_service import MigrationService

        # 显示进度对话框
        progress_dialog = MigrationProgressDialog(self)
        migration_service = MigrationService()

        def _on_migration_done(success: bool, error_msg: str):
            progress_dialog.close()
            # 弹出结果对话框
            result_dialog = MigrationResultDialog(success, error_msg, self)
            result_dialog.exec()
            
            if success:
                # 迁移成功后直接尝试建立连接，不再走 _on_action_clicked 避免无限循环
                conn_success, conn_msg = self.connection_service.establish_connection_by_id(link_id)
                if conn_success:
                    self._load_data()
                else:
                    # 清理失败（文件被锁定等），直接提示用户，不再弹迁移面板
                    InfoBar.error(
                        "建立连接失败",
                        f"原始路径可能包含被锁定的文件，请关闭相关程序后重试。\n{conn_msg}",
                        duration=5000,
                        position='TopCenter',
                        parent=self
                    )
                    self._load_data()

        migration_service.task_finished.connect(_on_migration_done)

        # 迁移方向：将软件路径（source）的数据迁移到库路径（target）
        migration_service.migrate_async(
            source=source_real,  # 软件路径（现有数据位置）
            target=target_real,  # 库路径（迁移目的地）
            mode="copy",
            on_progress=progress_dialog.update_progress
        )
        # 开启迁移后的物理清理
        if migration_service._worker:
            migration_service._worker.cleanup_source = True
        
        progress_dialog.cancel_requested.connect(migration_service.cancel_migration)
        progress_dialog.exec()

    def _handle_reverse_migration(self, link_id: str):
        """处理逆向迁移：库路径 -> 软件路径"""
        link = self.user_manager.get_link_by_id(link_id)
        if not link: return

        from src.gui.dialogs.migration import MigrationProgressDialog, MigrationResultDialog
        from src.services.migration_service import MigrationService
        from src.drivers.fs import is_junction, remove_junction

        # 展开环境变量
        source_real = os.path.expandvars(link.source_path)  # 软件路径
        target_real = os.path.expandvars(link.target_path)  # 库路径

        # 关键修正：先检查并断开链接
        if is_junction(source_real):
            # 如果软件路径是符号链接，先删除它
            if not remove_junction(source_real):
                from qfluentwidgets import InfoBar
                InfoBar.error(
                    "断开链接失败",
                    f"无法删除符号链接：{source_real}",
                    duration=3000,
                    position='TopCenter',
                    parent=self
                )
                return
        
        # 显示进度对话框
        progress_dialog = MigrationProgressDialog(self)
        migration_service = MigrationService()

        def _on_reverse_migration_done(success: bool, error_msg: str):
            from qfluentwidgets import InfoBar
            
            progress_dialog.close()
            # 弹出结果对话框
            result_dialog = MigrationResultDialog(success, error_msg, self)
            result_dialog.exec()
            
            if success:
                # 迁移成功，更新链接状态
                link.status = LinkStatus.READY
                self.user_manager.update_link(link)
                
                # 关键验证：检查软件路径是否真的有数据
                if not os.path.exists(source_real) or not os.listdir(source_real):
                    InfoBar.error(
                        "逆向迁移异常",
                        f"迁移报告成功，但软件路径为空！\n已保留库路径数据以防丢失。",
                        duration=5000,
                        position='TopCenter',
                        parent=self
                    )
                    self._load_data()
                    return
                
                # 清理库路径的数据
                try:
                    import shutil
                    if os.path.exists(target_real):
                        if os.path.isfile(target_real):
                            os.remove(target_real)
                        else:
                            shutil.rmtree(target_real)
                        InfoBar.success(
                            "逆向迁移完成",
                            f"数据已迁回软件路径，库路径已清理",
                            duration=3000,
                            position='TopCenter',
                            parent=self
                        )
                except Exception as e:
                    InfoBar.warning(
                        "清理库路径失败",
                        f"数据已迁回，但库路径清理失败：{str(e)}",
                        duration=3000,
                        position='TopCenter',
                        parent=self
                    )
                
                self._load_data()

        migration_service.task_finished.connect(_on_reverse_migration_done)

        # 添加调试日志
        print(f"[DEBUG] 开始逆向迁移:")
        print(f"[DEBUG]   源路径（库）: {target_real}, 存在: {os.path.exists(target_real)}")
        if os.path.exists(target_real):
            print(f"[DEBUG]   源路径文件数: {len(os.listdir(target_real)) if os.path.isdir(target_real) else '单文件'}")
        print(f"[DEBUG]   目标路径（软件）: {source_real}, 存在: {os.path.exists(source_real)}")

        # 逆向迁移：库路径 -> 软件路径
        migration_service.migrate_async(
            source=target_real,  # 库路径（现有数据位置）
            target=source_real,  # 软件路径（迁移目的地）
            mode="copy",
            on_progress=progress_dialog.update_progress
        )
        # 不需要清理源路径（库路径保留数据）
        
        progress_dialog.cancel_requested.connect(migration_service.cancel_migration)
        progress_dialog.exec()


    def _on_batch_establish(self):
        checked_ids = self._get_checked_ids()
        if not checked_ids: return

        operation_runner.run_batch_task_async(
            checked_ids,
            self.connection_service.establish_connection_by_id,
            "批量建立链接",
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
            "批量断开链接",
            lambda lid: f"正在断开: {self.user_manager.get_link_by_id(lid).name}",
            parent=self,
            on_finished=lambda s, m, d: (self._load_data(), self._clear_all_selection())
        )

    def _on_batch_remove(self):
        checked_ids = self._get_checked_ids()
        if not checked_ids: return
        
        # 使用 i18n 文案
        title = t("links.confirm_remove_title")
        msg = t("links.confirm_remove_msg", count=len(checked_ids))
        
        if MessageBox(title, msg, self).exec():
            operation_runner.run_task_async(
                self.user_manager.remove_links,
                checked_ids,
                title=t("links.batch_remove"),
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
