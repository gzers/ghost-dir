"""
主控制台视图
页面主体 - 负责布局和协调各组件
"""
from PySide6.QtWidgets import QSplitter, QWidget, QStackedWidget
from PySide6.QtCore import Qt
import os
from qfluentwidgets import PushButton, ToolButton, FluentIcon, MessageBox
from ...components.link_table import LinkTable
from ...i18n import t
from ....data.user_manager import UserManager
from ....data.template_manager import TemplateManager
from ....data.model import LinkStatus
from ....core.scanner import SmartScanner
from ....core.transaction import TransactionManager
from ....core.safety import ProcessGuard
from ....common.signals import signal_bus
from ...components import BasePageView, LinkTable, CategoryTreeWidget
from ...styles import apply_transparent_style
from .widgets import BatchToolbar, FlatLinkView


class ConnectedView(BasePageView):
    """已连接视图 - 管理所有连接状态"""

    def __init__(self, parent=None):
        """初始化已连接视图"""
        super().__init__(
            parent=parent,
            title=t("connected.title"),
            show_toolbar=True,      # 层级 2：启用工具栏
            enable_scroll=False,    # 不需要滚动，内容区自适应
            content_padding=False   # 内容铺满
        )

        # 初始化数据管理器
        self.user_manager = UserManager()
        self.template_manager = TemplateManager()
        from ....data.category_manager import CategoryManager
        self.category_manager = CategoryManager()
        self.scanner = SmartScanner(self.template_manager, self.user_manager)

        # 设置工具栏（层级 2）
        self._setup_toolbar()

        # 设置页面内容（层级 3）
        self._setup_content()

        # 连接信号
        self._connect_signals()

        # 加载数据
        self._load_data()

    def _setup_content(self):
        """设置页面内容（层级 3）"""
        content_layout = self.get_content_layout()

        # 创建分割器
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：通用分类树容器 (CategoryTreeWidget)
        self.category_tree = CategoryTreeWidget(self.category_manager, self.user_manager)
        self.category_tree.setMinimumWidth(200)
        self.category_tree.setMaximumWidth(400)
        
        # 右侧：主展示堆栈
        self.view_stack = QStackedWidget()
        
        # 视图堆栈包含：分类视图 B（用于左树右表模式）和全量列表视图 A
        # 这里为了满足用户“分类视图下有侧边栏，列表视图下无侧边栏”的要求，
        # 我们让 QSplitter 的第一个部件是侧边栏，第二个是堆栈。
        
        # 默认：分类视图对应的表格 (Index 0)
        self.category_link_table = LinkTable()
        self.view_stack.addWidget(self.category_link_table)
        
        # 智能列表视图 A (Index 1)
        self.list_view = FlatLinkView()
        self.view_stack.addWidget(self.list_view)
        
        self.splitter.addWidget(self.category_tree)
        self.splitter.addWidget(self.view_stack)
        
        # 设置分割比例（1:3）
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)
        
        # 应用 LibraryView 风格的样式优化：隐藏分割线手柄黑条
        self.splitter.setStyleSheet("QSplitter::handle { background: transparent; border: none; }")
        apply_transparent_style(self.splitter)
        
        # 彻底解决高度撑满问题：移除 BasePageView 默认添加的所有底部弹簧
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

        # 3. 设置最高拉伸优先级
        from PySide6.QtWidgets import QSizePolicy
        self.splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.addWidget(self.splitter, 1)

        # 批量操作工具栏组件（在最下方，但不占用剩余空间，除非需要）
        self.batch_toolbar = BatchToolbar()
        content_layout.addWidget(self.batch_toolbar)
        self.batch_toolbar.hide()

    def _setup_toolbar(self):
        """设置统一工具栏（层级 2）"""
        from qfluentwidgets import PrimaryPushButton, SearchLineEdit, Pivot, TransparentPushButton
        toolbar = self.get_toolbar_layout()

        # --- 左侧操作区 ---
        # 新增链接（主按钮）
        self.add_btn = PrimaryPushButton(FluentIcon.ADD, t("connected.add_link"))
        
        # 扫描（透明按钮）
        self.scan_btn = TransparentPushButton(FluentIcon.SEARCH, t("connected.scan_apps"))
        
        # 批量移除（透明按钮，默认禁用）
        self.batch_remove_btn = TransparentPushButton(FluentIcon.DELETE, t("connected.batch_remove"))
        self.batch_remove_btn.setEnabled(False)

        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.scan_btn)
        toolbar.addWidget(self.batch_remove_btn)

        # 弹簧撑开中间
        toolbar.addStretch(1)

        # --- 右侧功能区 ---
        # 搜索框
        self.search_edit = SearchLineEdit()
        self.search_edit.setPlaceholderText(t("connected.search_placeholder"))
        self.search_edit.setMaximumWidth(300)
        
        # 视图切换器
        self.view_pivot = Pivot()
        self.view_pivot.addItem("list", t("connected.view_list"))
        self.view_pivot.addItem("category", t("connected.view_category"))
        self.view_pivot.setCurrentItem("category") # 默认选分类视图
        
        # 刷新按钮
        self.refresh_btn = ToolButton(FluentIcon.SYNC)
        self.refresh_btn.setToolTip(t("connected.refresh_status"))

        toolbar.addWidget(self.search_edit)
        toolbar.addSpacing(8)
        toolbar.addWidget(self.view_pivot)
        toolbar.addWidget(self.refresh_btn)

        # 额外右侧工具区域（BasePageView 提供的右测布局）
        right_toolbar = self.get_right_toolbar_layout()
        self.refresh_size_btn = ToolButton(FluentIcon.SYNC)
        self.refresh_size_btn.setToolTip(t("connected.refresh_size"))
        # 只有在高度压缩时可能需要这个，暂时放着或保持为空以保持简洁
        # right_toolbar.addWidget(self.refresh_size_btn)

    def _connect_signals(self):
        """连接信号"""
        # 工具栏操作按钮
        self.add_btn.clicked.connect(self._on_add_link)
        self.scan_btn.clicked.connect(self._on_scan)
        self.batch_remove_btn.clicked.connect(self._on_batch_remove)
        
        # 搜索与切换
        self.search_edit.textChanged.connect(self._on_search_changed)
        self.view_pivot.currentItemChanged.connect(self._on_view_pivot_changed)
        self.refresh_btn.clicked.connect(self._refresh_status)
        
        # 分类树信号
        self.category_tree.category_selected.connect(self._on_category_selected)
        
        # 表格信号
        self.category_link_table.link_selected.connect(self._on_links_selected)
        self.category_link_table.action_clicked.connect(self._on_action_clicked)

        # 列表视图信号
        self.list_view.link_selected.connect(self._on_links_selected)
        self.list_view.action_clicked.connect(self._on_action_clicked)

        # 批量操作工具栏信号
        self.batch_toolbar.batch_establish_clicked.connect(self._on_batch_establish)
        self.batch_toolbar.batch_disconnect_clicked.connect(self._on_batch_disconnect)
        self.batch_toolbar.clear_selection_clicked.connect(self.category_link_table.clear_selection)
        self.batch_toolbar.clear_selection_clicked.connect(self.list_view.clear_selection)

        # 全局信号
        signal_bus.data_refreshed.connect(self._load_data)
        signal_bus.categories_changed.connect(self._load_data)

    def _load_data(self):
        """加载数据"""
        # 强制重载磁盘最新数据
        self.user_manager.reload()
        
        # 加载分类树
        self.category_tree.load_categories()
        
        # 默认选中“全部”并触发加载
        self.category_tree.select_category("all")
        self._on_category_selected("all")
        
        # 刷新状态
        self._refresh_status()
    
    def _refresh_status(self):
        """刷新所有连接的状态"""
        links = self.user_manager.get_all_links()
        for link in links:
            _ = link.status
        
        # 刷新表格显示
        self._on_category_selected(getattr(self, 'current_category_id', "all"))
    
    def _on_view_pivot_changed(self, route_key: str):
        """视图切换"""
        if route_key == "list":
            # 列表视图
            self.category_tree.hide()
            self.splitter.setSizes([0, 1000])
            self.view_stack.setCurrentIndex(1)
            self._on_category_selected("all")
        else:
            # 分类视图
            self.category_tree.show()
            self.splitter.setSizes([250, 750])
            self.view_stack.setCurrentIndex(0)
            self._on_category_selected(getattr(self, 'current_category_id', "all"))

    def _on_category_selected(self, category_id: str):
        """分类树节点被选中"""
        self.current_category_id = category_id
        
        if category_id == "all":
            links = self.user_manager.get_all_links()
        else:
            # 兼容性修复：现在全部按 ID 过滤
            links = self.user_manager.get_links_by_category(category_id)
            
        # 同时同步数据到两个视图
        self.category_link_table.load_links(links)
        self.list_view.load_links(links)
    
    def _on_view_changed(self, index: int):
        """视图切换"""
        self.view_stack.setCurrentIndex(index)
    
    def _on_search_changed(self, text: str):
        """搜索文本改变"""
        search_text = text.strip().lower()
        category_name = getattr(self, 'current_category', "全部")
        
        # 1. 获取基础数据集（基于分类）
        if category_name == "全部":
            base_links = self.user_manager.get_all_links()
        else:
            base_links = self.user_manager.get_links_by_category(category_name)
            
        # 2. 应用搜索过滤
        if not search_text:
            filtered_links = base_links
        else:
            filtered_links = [
                link for link in base_links 
                if search_text in link.name.lower() or search_text in link.target_path.lower()
            ]
            
        # 3. 更新视图
        self.category_link_table.load_links(filtered_links)
        self.list_view.load_links(filtered_links)
    
    def _on_batch_remove(self):
        """批量移除连接"""
        selected_ids = self.category_view.get_selected_links()
        if not selected_ids:
            return
        
        # 确认
        reply = MessageBox(
            "确认删除",
            f"确定要删除 {len(selected_ids)} 个连接吗？\n这不会删除实际文件。",
            self
        ).exec()
        
        if not reply:
            return
        
        # 执行删除
        for link_id in selected_ids:
            self.user_manager.remove_link(link_id)
        
        # 刷新数据
        self._load_data()
        self.category_view.clear_selection()

    def _on_links_selected(self, selected_ids: list):
        """连接选中事件"""
        count = len(selected_ids)

        if count > 0:
            self.batch_toolbar.update_count(count)
            self.batch_toolbar.show()
        else:
            self.batch_toolbar.hide()

    def _on_action_clicked(self, link_id: str, action: str):
        """操作按钮点击事件"""
        link = self.user_manager.get_link_by_id(link_id)
        if not link:
            return

        if action == "establish":
            self._establish_link(link)
        elif action == "disconnect":
            self._disconnect_link(link)
        elif action == "delete":
            self._delete_link(link)

    def _establish_link(self, link):
        """建立连接"""
        # 进程卫士检查
        guard = ProcessGuard()
        processes = guard.scan_handles(link.source_path)

        if processes:
            msg = "检测到以下进程正在占用文件：\n\n"
            for pid, name in processes:
                msg += f"• {name} (PID: {pid})\n"
            msg += "\n是否结束这些进程并继续？"

            reply = MessageBox("文件占用警告", msg, self).exec()
            if reply:
                guard.kill_processes(processes)
            else:
                return

        # 执行事务
        manager = TransactionManager(link.source_path, link.target_path, link.id)
        if manager.establish_link():
            MessageBox("成功", f"已成功建立连接：{link.name}", self).exec()
            self._load_data()
        else:
            MessageBox("失败", f"建立连接失败：{link.name}", self).exec()

    def _disconnect_link(self, link):
        """断开连接"""
        # 进程卫士检查（检查目标路径占用）
        guard = ProcessGuard()
        processes = guard.scan_handles(link.target_path)

        if processes:
            msg = "检测到以下进程正在占用目标文件：\n\n"
            for pid, name in processes:
                msg += f"• {name} (PID: {pid})\n"
            msg += "\n是否结束这些进程并继续？"

            reply = MessageBox("文件占用警告", msg, self).exec()
            if reply:
                guard.kill_processes(processes)
            else:
                return

        # 执行事务
        manager = TransactionManager(link.source_path, link.target_path, link.id)
        if manager.disconnect_link():
            MessageBox("成功", f"已成功断开连接：{link.name}", self).exec()
            self._load_data()
        else:
            MessageBox("失败", f"断开连接失败：{link.name}", self).exec()

    def _delete_link(self, link):
        """删除连接"""
        reply = MessageBox(
            "确认删除",
            f"确定要删除连接 {link.name} 吗？\n这不会删除实际文件。",
            self
        ).exec()

        if reply:
            self.user_manager.remove_link(link.id)
            self._load_data()

    def _on_batch_establish(self):
        """批量建立连接"""
        selected_ids = self.category_view.get_selected_links()
        if not selected_ids:
            return

        # 过滤出未连接的项目
        links_to_establish = []
        for link_id in selected_ids:
            link = self.user_manager.get_link_by_id(link_id)
            if link and link.status == LinkStatus.DISCONNECTED:
                links_to_establish.append(link)

        if not links_to_establish:
            MessageBox("提示", "没有可建立连接的项目", self).exec()
            return

        # 确认
        reply = MessageBox(
            "批量建立连接",
            f"将为 {len(links_to_establish)} 个软件建立连接，是否继续？",
            self
        ).exec()

        if not reply:
            return

        # 执行批量操作
        success_count = 0
        failed_items = []

        for link in links_to_establish:
            # 进程卫士检查
            guard = ProcessGuard()
            processes = guard.scan_handles(link.source_path)

            if processes:
                # 自动结束进程
                guard.kill_processes(processes)

            # 执行事务
            manager = TransactionManager(link.source_path, link.target_path, link.id)
            if manager.establish_link():
                success_count += 1
            else:
                failed_items.append(link.name)

        # 刷新数据
        self._load_data()
        self.category_view.clear_selection()

        # 显示结果
        if failed_items:
            msg = f"成功: {success_count}/{len(links_to_establish)}\n\n失败项目:\n"
            msg += "\n".join(f"• {name}" for name in failed_items)
            MessageBox("批量操作完成", msg, self).exec()
        else:
            MessageBox("成功", f"已成功建立 {success_count} 个连接", self).exec()

    def _on_batch_disconnect(self):
        """批量断开连接"""
        selected_ids = self.category_view.get_selected_links()
        if not selected_ids:
            return

        # 过滤出已连接的项目
        links_to_disconnect = []
        for link_id in selected_ids:
            link = self.user_manager.get_link_by_id(link_id)
            if link and link.status == LinkStatus.CONNECTED:
                links_to_disconnect.append(link)

        if not links_to_disconnect:
            MessageBox("提示", "没有可断开连接的项目", self).exec()
            return

        # 确认
        reply = MessageBox(
            "批量断开连接",
            f"将断开 {len(links_to_disconnect)} 个软件的连接，是否继续？",
            self
        ).exec()

        if not reply:
            return

        # 执行批量操作
        success_count = 0
        failed_items = []

        for link in links_to_disconnect:
            # 进程卫士检查（检查目标路径占用）
            guard = ProcessGuard()
            processes = guard.scan_handles(link.target_path)

            if processes:
                # 自动结束进程
                guard.kill_processes(processes)

            # 执行事务
            manager = TransactionManager(link.source_path, link.target_path, link.id)
            if manager.disconnect_link():
                success_count += 1
            else:
                failed_items.append(link.name)

        # 刷新数据
        self._load_data()
        self.category_view.clear_selection()

        # 显示结果
        if failed_items:
            msg = f"成功: {success_count}/{len(links_to_disconnect)}\n\n失败项目:\n"
            msg += "\n".join(f"• {name}" for name in failed_items)
            MessageBox("批量操作完成", msg, self).exec()
        else:
            MessageBox("成功", f"已成功断开 {success_count} 个连接", self).exec()

    def _on_add_link(self):
        """新增连接"""
        from ...dialogs import AddLinkDialog

        dialog = AddLinkDialog(self)
        dialog.link_added.connect(self._load_data)
        dialog.exec()

    def _on_scan(self):
        """扫描本机应用"""
        from ...dialogs import ScanWizardDialog

        dialog = ScanWizardDialog(self)
        dialog.scan_completed.connect(self._on_scan_completed)
        dialog.exec()

    def _on_scan_completed(self, count: int):
        """扫描完成"""
        MessageBox("扫描完成", f"成功导入 {count} 个软件", self).exec()
        self._load_data()

    def _on_refresh_size(self):
        """刷新空间统计"""
        from PySide6.QtCore import QThread, Signal
        from ...utils.space_analyzer import calculate_directory_size

        links = self.user_manager.get_all_links()

        if not links:
            MessageBox("提示", "没有需要统计的连接", self).exec()
            return

        # 确认操作
        reply = MessageBox(
            "刷新空间统计",
            f"将计算 {len(links)} 个连接的空间占用，可能需要一些时间。\n是否继续？",
            self
        ).exec()

        if not reply:
            return

        # 显示进度提示
        from qfluentwidgets import StateToolTip
        self.stateTooltip = StateToolTip("正在计算", "请稍候...", self.window())
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()

        # 后台计算
        class SizeCalculator(QThread):
            finished = Signal(dict)  # {link_id: size}

            def __init__(self, links):
                super().__init__()
                self.links = links

            def run(self):
                results = {}
                for link in self.links:
                    # 优先计算源路径，如果不存在则计算目标路径
                    if os.path.exists(link.source_path):
                        size = calculate_directory_size(link.source_path)
                    elif os.path.exists(link.target_path):
                        size = calculate_directory_size(link.target_path)
                    else:
                        size = 0

                    results[link.id] = size

                self.finished.emit(results)

        self.calculator = SizeCalculator(links)
        self.calculator.finished.connect(self._on_size_calculated)
        self.calculator.start()

    def _on_size_calculated(self, results: dict):
        """空间计算完成"""
        # 更新缓存
        for link_id, size in results.items():
            self.user_manager.update_link_size(link_id, size)

        # 关闭提示
        self.stateTooltip.setContent("计算完成 ✓")
        self.stateTooltip.setState(True)
        self.stateTooltip = None

        # 刷新列表
        self._load_data()

        MessageBox("完成", f"已更新 {len(results)} 个连接的空间统计", self).exec()
