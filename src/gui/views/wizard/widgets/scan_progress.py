"""
扫描进度组件
显示扫描进度和状态信息
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QThread
from qfluentwidgets import (
    ProgressBar, BodyLabel, PrimaryPushButton, PushButton,
    StrongBodyLabel, FluentIcon, CardWidget
)


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


from ....components import Card
from ....styles import (
    apply_font_style, apply_muted_text_style,
    get_spacing, get_radius, get_content_width
)

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
        self.update_style()

    def update_style(self, theme=None):
        """更新样式"""
        super().update_style(theme)
        if hasattr(self, 'title_label'):
            self._refresh_content_styles()

    def _init_ui(self):
        """初始化 UI"""
        # 限制卡片宽度为窄（560px），使其在向导页居中且不铺满
        self.setFixedWidth(get_content_width("narrow"))
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)

        # 标题区域
        title_layout = QHBoxLayout()
        # 图标
        self.icon_label = BodyLabel("🔍")
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet(f"background: rgba(0,0,0,0.05); border-radius: {get_radius('md')}px; font-size: 20px;")
        title_layout.addWidget(self.icon_label)

        title_layout.addSpacing(12)

        title_text = QVBoxLayout()
        self.title_label = StrongBodyLabel("智能扫描")
        title_text.addWidget(self.title_label)
        self.status_label = BodyLabel("自动发现本机可管理的软件")
        self.status_label.setWordWrap(True)
        title_text.addWidget(self.status_label)
        title_layout.addLayout(title_text)
        title_layout.addStretch()

        self.main_layout.addLayout(title_layout)

        # 进度条
        self.progress_bar = ProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.main_layout.addWidget(self.progress_bar)

        # 详细状态
        self.detail_label = BodyLabel("点击扫描开始")
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.detail_label)

        # 结果统计
        self.result_label = BodyLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setVisible(False)
        self.main_layout.addWidget(self.result_label)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.scan_button = PrimaryPushButton(FluentIcon.SEARCH, "开始扫描")
        self.scan_button.clicked.connect(self._on_scan_clicked)
        button_layout.addWidget(self.scan_button)

        self.import_button = PrimaryPushButton(FluentIcon.DOWNLOAD, "一键导入")
        self.import_button.setEnabled(False)
        self.import_button.setVisible(False)
        self.import_button.clicked.connect(self._on_import_clicked)
        button_layout.addWidget(self.import_button)

        self.refresh_button = PushButton(FluentIcon.SYNC, "重新扫描")
        self.refresh_button.setEnabled(False)
        self.refresh_button.setVisible(False)
        self.refresh_button.clicked.connect(self._on_refresh_clicked)
        button_layout.addWidget(self.refresh_button)

        self.cancel_button = PushButton(FluentIcon.CLOSE, "取消")
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(button_layout)

    def _refresh_content_styles(self):
        """刷新文字样式"""
        apply_font_style(self.title_label, size="lg", weight="semibold")
        apply_muted_text_style(self.status_label, size="sm")
        apply_font_style(self.detail_label, weight="medium")


    def _on_scan_clicked(self):
        """扫描按钮点击"""
        if self.scanning:
            return
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
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.scan_button.setEnabled(False)
        self.import_button.setVisible(False)
        self.refresh_button.setVisible(False)
        self.result_label.setVisible(False)
        self.detail_label.setText("正在扫描本机，请稍候...")

    def update_progress(self, current, total):
        """更新进度"""
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
        if total > 0:
            self.detail_label.setText(f"正在扫描: {current}/{total}")

    def scan_finished(self, discovered_count, selected_count):
        """扫描完成"""
        self.scanning = False
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.discovered_count = discovered_count
        self.selected_count = selected_count

        if discovered_count > 0:
            self.detail_label.setText(f"扫描完成！发现 {discovered_count} 个可管理的软件")
            self.result_label.setText(f"已选中 {selected_count} 项")
            self.result_label.setVisible(True)
            self.scan_button.setVisible(False)
            self.import_button.setVisible(True)
            self.import_button.setEnabled(selected_count > 0)
            self.refresh_button.setVisible(True)
            self.refresh_button.setEnabled(True)
            self.cancel_button.setVisible(True)
        else:
            self.detail_label.setText("未发现可管理的软件")
            self.scan_button.setEnabled(True)
            self.refresh_button.setVisible(False)
            self.cancel_button.setVisible(False)

        self.progress_bar.setVisible(False)

    def scan_error(self, error_msg):
        """扫描出错"""
        self.scanning = False
        self.progress_bar.setVisible(False)
        self.detail_label.setText(f"扫描失败: {error_msg}")
        self.scan_button.setEnabled(True)

    def reset(self):
        """重置状态"""
        self.scanning = False
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)
        self.detail_label.setText("点击扫描开始")
        self.result_label.setVisible(False)
        self.scan_button.setVisible(True)
        self.scan_button.setEnabled(True)
        self.import_button.setVisible(False)
        self.import_button.setEnabled(False)
        self.refresh_button.setVisible(False)
        self.refresh_button.setEnabled(False)
        self.cancel_button.setVisible(False)

    def set_import_enabled(self, enabled):
        """设置导入按钮状态"""
        if self.import_button.isVisible():
            self.import_button.setEnabled(enabled)
