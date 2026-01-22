"""
智能向导视图
引导式操作，快速完成常见任务
"""
from PySide6.QtCore import Qt
from qfluentwidgets import MessageBox
from ...i18n import t
from ....data.user_manager import UserManager
from ....data.template_manager import TemplateManager
from ....core.scanner import SmartScanner
from ...components import BasePageView
from .widgets import ScanProgressCard, ScanWorker, ScanResultCard


class WizardView(BasePageView):
    """智能向导视图"""

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("wizard.title"),
            show_toolbar=False,
            enable_scroll=True
        )

        # 初始化数据管理器
        self.template_manager = TemplateManager()
        self.user_manager = UserManager()
        self.scanner = SmartScanner(self.template_manager, self.user_manager)

        # 扫描状态
        self.discovered_templates = []
        self.scan_result_cards = {}

        # 添加页面内容
        self._setup_content()

        # 连接信号
        self._connect_signals()

    def _setup_content(self):
        """设置页面内容"""
        # 扫描进度卡片（固定内容，始终可见）
        self.scan_progress = ScanProgressCard()
        self.add_fixed_content(self.scan_progress, before_scroll=True)

        # 结果滚动区域初始隐藏
        self.get_scroll_area().setVisible(False)

    def _on_theme_changed(self, theme: str):
        """主题变更处理"""
        super()._on_theme_changed(theme)

    def _connect_signals(self):
        """连接信号"""
        self.scan_progress.scan_clicked.connect(self._on_scan_clicked)
        self.scan_progress.import_clicked.connect(self._on_import_clicked)
        self.scan_progress.refresh_clicked.connect(self._on_refresh_clicked)
        self.scan_progress.cancel_clicked.connect(self._on_cancel_clicked)

    def _on_scan_clicked(self):
        """开始扫描"""
        self.scan_progress.start_scanning()

        # 清空之前的结果
        self.discovered_templates.clear()
        for card in self.scan_result_cards.values():
            card.deleteLater()
        self.scan_result_cards.clear()

        # 开始扫描（在后台线程中进行，不会阻塞 UI）
        self.worker = ScanWorker(self.scanner)
        self.worker.finished.connect(self._on_scan_finished)
        self.worker.error.connect(self._on_scan_error)
        self.worker.start()

    def _on_scan_finished(self, discovered):
        """扫描完成"""
        self.discovered_templates = discovered

        # 显示结果
        if discovered:
            # 创建结果卡片
            selected_count = 0
            content_layout = self.get_content_layout()

            for template in discovered:
                card = ScanResultCard(template)
                card.selected_changed.connect(self._on_selection_changed)
                card.import_requested.connect(self._on_single_import)
                card.ignore_requested.connect(self._on_ignore_template)

                # 插入到 stretch 之前
                content_layout.insertWidget(
                    content_layout.count() - 1,
                    card
                )
                self.scan_result_cards[template.id] = card
                if card.is_selected():
                    selected_count += 1

            self.get_scroll_area().setVisible(True)
            self.scan_progress.scan_finished(len(discovered), selected_count)
        else:
            self.get_scroll_area().setVisible(False)
            self.scan_progress.scan_finished(0, 0)

    def _on_scan_error(self, error_msg):
        """扫描出错"""
        self.scan_progress.scan_error(error_msg)

    def _on_selection_changed(self, template_id, selected):
        """选择状态改变"""
        # 更新选中计数
        selected_count = sum(
            1 for card in self.scan_result_cards.values()
            if card.is_selected()
        )
        self.scan_progress.result_label.setText(f"已选中 {selected_count} 项")
        self.scan_progress.set_import_enabled(selected_count > 0)

    def _on_import_clicked(self):
        """一键导入选中的软件"""
        # 获取选中的模版
        selected = [
            card.get_template()
            for card in self.scan_result_cards.values()
            if card.is_selected()
        ]

        if not selected:
            return

        # 确认对话框
        box = MessageBox(
            f"确定要导入 {len(selected)} 个软件吗？",
            "批量导入确认",
            self
        )
        if box.exec():
            # 导入
            count = self.scanner.import_templates(selected)
            if count > 0:
                # 通知主窗口更新
                # TODO: 发送信号通知主窗口
                self._show_import_success(count)
            else:
                self._show_import_failed()

    def _on_single_import(self, template_id):
        """导入单个软件"""
        template = self.scan_result_cards[template_id].get_template()
        count = self.scanner.import_templates([template])
        if count > 0:
            self._show_import_success(1)
        else:
            self._show_import_failed()

    def _on_ignore_template(self, template_id):
        """永久忽略软件"""
        template = self.scan_result_cards[template_id].get_template()
        self.user_manager.add_to_ignore_list(template_id)

        # 移除卡片
        card = self.scan_result_cards.pop(template_id)
        card.deleteLater()

        # 更新统计
        if not self.scan_result_cards:
            self.get_scroll_area().setVisible(False)
            self.scan_progress.result_label.setVisible(False)
        else:
            selected_count = sum(
                1 for card in self.scan_result_cards.values()
                if card.is_selected()
            )
            self.scan_progress.result_label.setText(f"已选中 {selected_count} 项")
            self.scan_progress.set_import_enabled(selected_count > 0)

    def _on_refresh_clicked(self):
        """重新扫描"""
        self._on_scan_clicked()

    def _on_cancel_clicked(self):
        """取消扫描结果，返回初始状态"""
        # 清空所有结果卡片
        self.discovered_templates.clear()
        for card in self.scan_result_cards.values():
            card.deleteLater()
        self.scan_result_cards.clear()

        # 隐藏滚动区域
        self.get_scroll_area().setVisible(False)

        # 重置扫描进度卡片
        self.scan_progress.reset()

    def _show_import_success(self, count):
        """显示导入成功"""
        box = MessageBox(
            f"成功导入 {count} 个软件！",
            "导入成功",
            self
        )
        box.yesButton.setText("确定")
        box.cancelButton.hide()
        box.exec()

        # 重置状态
        self._on_refresh_clicked()

    def _show_import_failed(self):
        """显示导入失败"""
        box = MessageBox(
            "导入失败，请重试！",
            "导入失败",
            self
        )
        box.yesButton.setText("确定")
        box.cancelButton.hide()
        box.exec()
