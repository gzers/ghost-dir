"""
主控制台视图（重构版）
页面主体 - 负责布局和协调各组件
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PySide6.QtCore import Qt, Signal
import os
from qfluentwidgets import (
    PushButton, ToolButton, FluentIcon,
    TitleLabel, MessageBox
)
from ...components.link_table import LinkTable
from ....data.user_manager import UserManager
from ....data.template_manager import TemplateManager
from ....data.model import LinkStatus
from ....core.scanner import SmartScanner
from ....core.transaction import TransactionManager
from ....core.safety import ProcessGuard
from ....common.signals import signal_bus
from .category_tree import CategoryTree
from .batch_toolbar import BatchToolbar


class ConsoleView(QWidget):
    """主控制台视图"""
    
    def __init__(self, parent=None):
        """初始化控制台视图"""
        super().__init__(parent)
        
        # 初始化数据管理器
        self.user_manager = UserManager()
        self.template_manager = TemplateManager()
        self.scanner = SmartScanner(self.template_manager, self.user_manager)
        
        self._init_ui()
        self._connect_signals()
        self._load_data()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 标题栏
        title_layout = QHBoxLayout()
        title = TitleLabel("主控制台")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        # 工具栏按钮
        self.add_btn = PushButton(FluentIcon.ADD, "新增连接")
        self.scan_btn = PushButton(FluentIcon.SEARCH, "扫描本机应用")
        self.refresh_size_btn = PushButton(FluentIcon.SYNC, "刷新统计")
        self.refresh_btn = ToolButton(FluentIcon.SYNC)
        
        title_layout.addWidget(self.add_btn)
        title_layout.addWidget(self.scan_btn)
        title_layout.addWidget(self.refresh_size_btn)
        title_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(title_layout)
        
        # 主内容区：左树右表
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：分类树组件
        self.category_tree = CategoryTree()
        splitter.addWidget(self.category_tree)
        
        # 右侧：连接表格
        self.link_table = LinkTable()
        splitter.addWidget(self.link_table)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        layout.addWidget(splitter)
        
        # 批量操作工具栏组件（默认隐藏）
        self.batch_toolbar = BatchToolbar()
        layout.addWidget(self.batch_toolbar)
        self.batch_toolbar.hide()
    
    def _connect_signals(self):
        """连接信号"""
        # 按钮点击
        self.add_btn.clicked.connect(self._on_add_link)
        self.scan_btn.clicked.connect(self._on_scan)
        self.refresh_size_btn.clicked.connect(self._on_refresh_size)
        self.refresh_btn.clicked.connect(self._load_data)
        
        # 表格信号
        self.link_table.link_selected.connect(self._on_links_selected)
        self.link_table.action_clicked.connect(self._on_action_clicked)
        
        # 批量操作工具栏信号
        self.batch_toolbar.batch_establish_clicked.connect(self._on_batch_establish)
        self.batch_toolbar.batch_disconnect_clicked.connect(self._on_batch_disconnect)
        self.batch_toolbar.clear_selection_clicked.connect(self.link_table.clear_selection)
        
        # 全局信号
        signal_bus.data_refreshed.connect(self._load_data)
    
    def _load_data(self):
        """加载数据"""
        # 加载分类树
        self.category_tree.load_categories()
        
        # 加载连接表格
        links = self.user_manager.get_all_links()
        self.link_table.load_links(links)
    
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
        selected_ids = self.link_table.get_selected_links()
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
        self.link_table.clear_selection()
        
        # 显示结果
        if failed_items:
            msg = f"成功: {success_count}/{len(links_to_establish)}\n\n失败项目:\n"
            msg += "\n".join(f"• {name}" for name in failed_items)
            MessageBox("批量操作完成", msg, self).exec()
        else:
            MessageBox("成功", f"已成功建立 {success_count} 个连接", self).exec()
    
    def _on_batch_disconnect(self):
        """批量断开连接"""
        selected_ids = self.link_table.get_selected_links()
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
            manager = TransactionManager(link.source_path, link.target_path, link.id)
            if manager.disconnect_link():
                success_count += 1
            else:
                failed_items.append(link.name)
        
        # 刷新数据
        self._load_data()
        self.link_table.clear_selection()
        
        # 显示结果
        if failed_items:
            msg = f"成功: {success_count}/{len(links_to_disconnect)}\n\n失败项目:\n"
            msg += "\n".join(f"• {name}" for name in failed_items)
            MessageBox("批量操作完成", msg, self).exec()
        else:
            MessageBox("成功", f"已成功断开 {success_count} 个连接", self).exec()
    
    def _on_add_link(self):
        """新增连接"""
        from ...dialogs.add_link_dialog import AddLinkDialog
        
        dialog = AddLinkDialog(self)
        dialog.link_added.connect(self._load_data)
        dialog.exec()
    
    def _on_scan(self):
        """扫描本机应用"""
        from ...dialogs.scan_wizard_dialog import ScanWizardDialog
        
        dialog = ScanWizardDialog(self)
        dialog.scan_completed.connect(self._on_scan_completed)
        dialog.exec()
    
    def _on_scan_completed(self, count: int):
        """扫描完成"""
        MessageBox("扫描完成", f"成功导入 {count} 个软件", self).exec()
        self._load_data()
    
    def _on_refresh_size(self):
        """刷新空间统计"""
        from PySide6.QtCore import QThread
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
