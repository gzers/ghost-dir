"""
扫描进度组件
显示扫描进度和状态信息
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal, QThread
from qfluentwidgets import (
    BodyLabel, PrimaryPushButton, PushButton, FluentIcon
)

from ....components import Card, CardHeader, ProgressIndicator
from ....styles import (
    get_spacing, apply_font_style, apply_muted_text_style
)
from ....i18n import t


class ScanWorker(QThread):
    """扫描工作线程"""
    progress = Signal(int, int)  # current, total
    finished = Signal(list)  # discovered templates
    error = Signal(str)  # error message

    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner

    def run(self):
        """执行扫描"""
        try:
            discovered = self.scanner.scan()
            self.finished.emit(discovered)
        except Exception as e:
            self.error.emit(str(e))


class ScanProgressCard(Card):
    """扫描进度卡片组件"""

    # 信号定义
    scan_clicked = Signal()
    import_clicked = Signal()
    refresh_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanning = False
        self.discovered_count = 0
        self.selected_count = 0
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        # 设置卡片可扩展以占满一行
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            get_spacing("lg"),
            get_spacing("lg"),
            get_spacing("lg"),
            get_spacing("lg")
        )
        self.main_layout.setSpacing(get_spacing("md"))

        # 卡片头部
        self.header = CardHeader(
            icon=t("wizard.scan_card_icon"),
            title=t("wizard.scan_card_title"),
            subtitle=t("wizard.scan_card_subtitle")
        )
        self.main_layout.addWidget(self.header)

        # 进度指示器
        self.progress_indicator = ProgressIndicator()
        self.progress_indicator.set_status(t("wizard.scan_idle"))
        self.main_layout.addWidget(self.progress_indicator)

        # 结果统计标签
        self.result_label = BodyLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setVisible(False)
        apply_font_style(self.result_label, size="sm", color="secondary")
        self.main_layout.addWidget(self.result_label)

        # 按钮区域
        self._init_buttons()

    def _init_buttons(self):
        """初始化按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(get_spacing("sm"))
        button_layout.addStretch()

        # 扫描按钮
        self.scan_button = PrimaryPushButton(
            FluentIcon.SEARCH,
            t("wizard.start_scan")
        )
        self.scan_button.clicked.connect(self._on_scan_clicked)
        button_layout.addWidget(self.scan_button)

        # 导入按钮
        self.import_button = PrimaryPushButton(
            FluentIcon.DOWNLOAD,
            t("wizard.import_selected")
        )
        self.import_button.setEnabled(False)
        self.import_button.setVisible(False)
        self.import_button.clicked.connect(self._on_import_clicked)
        button_layout.addWidget(self.import_button)

        # 重新扫描按钮
        self.refresh_button = PushButton(
            FluentIcon.SYNC,
            t("wizard.rescan")
        )
        self.refresh_button.setEnabled(False)
        self.refresh_button.setVisible(False)
        self.refresh_button.clicked.connect(self._on_refresh_clicked)
        button_layout.addWidget(self.refresh_button)

        # 取消按钮
        self.cancel_button = PushButton(
            FluentIcon.CLOSE,
            t("wizard.cancel")
        )
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(button_layout)

    def _on_scan_clicked(self):
        """扫描按钮点击"""
        if not self.scanning:
            self.scan_clicked.emit()

    def _on_import_clicked(self):
        """导入按钮点击"""
        self.import_clicked.emit()

    def _on_refresh_clicked(self):
        """刷新按钮点击"""
        self.refresh_clicked.emit()

    def _on_cancel_clicked(self):
        """取消按钮点击"""
        self.cancel_clicked.emit()

    def start_scanning(self):
        """开始扫描状态"""
        self.scanning = True
        
        # 更新进度指示器
        self.progress_indicator.start_indeterminate()
        self.progress_indicator.set_status(t("wizard.scan_progress_detail"))
        
        # 更新按钮状态
        self.scan_button.setEnabled(False)
        self.import_button.setVisible(False)
        self.refresh_button.setVisible(False)
        self.result_label.setVisible(False)

    def update_progress(self, current: int, total: int):
        """
        更新进度
        
        Args:
            current: 当前进度
            total: 总进度
        """
        self.progress_indicator.set_progress(current, total)
        if total > 0:
            self.progress_indicator.set_status(
                t("wizard.scan_progress_count", current=current, total=total)
            )

    def scan_finished(self, discovered_count: int, selected_count: int):
        """
        扫描完成
        
        Args:
            discovered_count: 发现的软件数量
            selected_count: 选中的软件数量
        """
        self.scanning = False
        self.discovered_count = discovered_count
        self.selected_count = selected_count

        # 完成进度
        self.progress_indicator.complete()

        if discovered_count > 0:
            # 更新状态文本
            self.progress_indicator.set_status(
                t("wizard.scan_complete_detail", count=discovered_count)
            )
            
            # 显示选中统计
            self.result_label.setText(
                t("wizard.selected_count", count=selected_count)
            )
            self.result_label.setVisible(True)
            
            # 更新按钮状态
            self.scan_button.setVisible(False)
            self.import_button.setVisible(True)
            self.import_button.setEnabled(selected_count > 0)
            self.refresh_button.setVisible(True)
            self.refresh_button.setEnabled(True)
            self.cancel_button.setVisible(True)
        else:
            # 未发现软件
            self.progress_indicator.set_status(t("wizard.no_apps_found"))
            self.scan_button.setEnabled(True)
            self.refresh_button.setVisible(False)
            self.cancel_button.setVisible(False)

        # 隐藏进度条
        self.progress_indicator.hide_progress()

    def scan_error(self, error_msg: str):
        """
        扫描出错
        
        Args:
            error_msg: 错误信息
        """
        self.scanning = False
        
        # 隐藏进度条并显示错误
        self.progress_indicator.hide_progress()
        self.progress_indicator.set_status(
            t("wizard.scan_error", error=error_msg)
        )
        
        # 恢复扫描按钮
        self.scan_button.setEnabled(True)

    def reset(self):
        """重置状态"""
        self.scanning = False
        
        # 重置进度指示器
        self.progress_indicator.reset()
        self.progress_indicator.set_status(t("wizard.scan_idle"))
        
        # 重置结果标签
        self.result_label.setVisible(False)
        
        # 重置按钮状态
        self.scan_button.setVisible(True)
        self.scan_button.setEnabled(True)
        self.import_button.setVisible(False)
        self.import_button.setEnabled(False)
        self.refresh_button.setVisible(False)
        self.refresh_button.setEnabled(False)
        self.cancel_button.setVisible(False)

    def set_import_enabled(self, enabled: bool):
        """
        设置导入按钮状态
        
        Args:
            enabled: 是否启用
        """
        if self.import_button.isVisible():
            self.import_button.setEnabled(enabled)

    def update_selected_count(self, count: int):
        """
        更新选中数量
        
        Args:
            count: 选中数量
        """
        self.selected_count = count
        if self.result_label.isVisible():
            self.result_label.setText(
                t("wizard.selected_count", count=count)
            )
        # 更新导入按钮状态
        self.set_import_enabled(count > 0)

