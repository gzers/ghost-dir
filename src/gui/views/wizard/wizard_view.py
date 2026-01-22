"""
智能向导视图
引导式操作，快速完成常见任务
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import ScrollArea, SubtitleLabel, MessageBox
from ...i18n import t
from ....data.user_manager import UserManager
from ....data.template_manager import TemplateManager
from ....core.scanner import SmartScanner
from .widgets import ScanProgressCard, ScanWorker, ScanResultCard


class WizardView(QWidget):
    """智能向导视图"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 初始化数据管理器
        self.template_manager = TemplateManager()
        self.user_manager = UserManager()
        self.scanner = SmartScanner(self.template_manager, self.user_manager)

        # 扫描状态
        self.discovered_templates = []
        self.scan_result_cards = {}

        # 初始化 UI
        self._init_ui()

        # 连接信号
        self._connect_signals()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题
        title_layout = QHBoxLayout()
        from ...styles import apply_page_layout
        apply_page_layout(title_layout, spacing="section")
        title_layout.setContentsMargins(24, 24, 24, 8)
        self.title_label = SubtitleLabel(t("wizard.title"))
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 扫描进度卡片
        self.scan_progress = ScanProgressCard()
        layout.addWidget(self.scan_progress, 0, Qt.AlignmentFlag.AlignTop)

        # 结果区域
        self.result_scroll = ScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.result_container = QWidget()
        self.result_layout = QVBoxLayout(self.result_container)
        apply_page_layout(self.result_layout, spacing="group")  # 列表项间距 20px
        self.result_layout.setContentsMargins(24, 12, 24, 24)
        self.result_layout.addStretch()

        self.result_scroll.setWidget(self.result_container)
        layout.addWidget(self.result_scroll)

        # 初始隐藏结果区域
        self.result_scroll.setVisible(False)

        # 设置背景色（亮色主题下需要）
        self._update_theme_style()
        from ....common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _update_theme_style(self):
        """更新主题样式"""
        from ...styles import apply_container_style
        apply_container_style(self.result_container)


    def _on_theme_changed(self, theme):
        """主题变更"""
        self._update_theme_style()

    def _connect_signals(self):
        """连接信号"""
        self.scan_progress.scan_clicked.connect(self._on_scan_clicked)
        self.scan_progress.import_clicked.connect(self._on_import_clicked)
        self.scan_progress.refresh_clicked.connect(self._on_refresh_clicked)

    def _on_scan_clicked(self):
        """开始扫描"""
        self.scan_progress.start_scanning()

        # 清空之前的结果
        self.discovered_templates.clear()
        for card in self.scan_result_cards.values():
            card.deleteLater()
        self.scan_result_cards.clear()

        # 开始扫描
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
            for template in discovered:
                card = ScanResultCard(template)
                card.selected_changed.connect(self._on_selection_changed)
                card.import_requested.connect(self._on_single_import)
                card.ignore_requested.connect(self._on_ignore_template)

                # 插入到 stretch 之前
                self.result_layout.insertWidget(
                    self.result_layout.count() - 1,
                    card
                )
                self.scan_result_cards[template.id] = card
                if card.is_selected():
                    selected_count += 1

            self.result_scroll.setVisible(True)
            self.scan_progress.scan_finished(len(discovered), selected_count)
        else:
            self.result_scroll.setVisible(False)
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
            self.result_scroll.setVisible(False)
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
