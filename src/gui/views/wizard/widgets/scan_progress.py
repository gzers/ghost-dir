"""
扫描进度组件
显示扫描进度和状态信息
"""
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    CardWidget, BodyLabel, CaptionLabel, PrimaryPushButton, PushButton,
    FluentIcon, ProgressBar, IconWidget
)

from src.gui.styles import get_spacing, apply_font_style, apply_muted_text_style
from src.gui.i18n import t


class ScanProgressCard(CardWidget):
    """扫描进度卡片组件 - 紧凑单行布局"""

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
        """初始化 UI - 单行紧凑布局"""
        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(16)

        # 左侧：图标
        self.icon_widget = IconWidget(FluentIcon.SEARCH, self)
        self.icon_widget.setFixedSize(40, 40)
        main_layout.addWidget(self.icon_widget)

        # 中间：标题 + 副标题 + 状态
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        # 标题
        self.title_label = BodyLabel(t("wizard.scan_card_title"))
        apply_font_style(self.title_label, weight="semibold")
        info_layout.addWidget(self.title_label)

        # 副标题
        self.subtitle_label = CaptionLabel(t("wizard.scan_card_subtitle"))
        apply_muted_text_style(self.subtitle_label, size="sm")
        info_layout.addWidget(self.subtitle_label)

        # 状态文本（小号，灰色）
        self.status_label = CaptionLabel(f"🟢 {t('wizard.scan_idle')}")
        apply_muted_text_style(self.status_label, size="xs")
        info_layout.addWidget(self.status_label)

        main_layout.addLayout(info_layout, stretch=1)

        # 进度条容器（初始隐藏）
        self.progress_container = QWidget()
        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(4)

        self.progress_bar = ProgressBar()
        self.progress_bar.setRange(0, 0)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = CaptionLabel("")
        apply_muted_text_style(self.progress_label, size="xs")
        progress_layout.addWidget(self.progress_label)

        self.progress_container.setVisible(False)
        main_layout.addWidget(self.progress_container)

        # 右侧：按钮区域
        self._init_buttons(main_layout)

    def _init_buttons(self, layout):
        """初始化按钮区域"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(8)

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

        layout.addWidget(button_container)

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

        # 更新状态
        self.status_label.setText(f"🔵 {t('wizard.scan_progress')}")

        # 显示进度条
        self.progress_container.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.progress_label.setText(t("wizard.scan_progress_detail"))

        # 更新按钮状态
        self.scan_button.setEnabled(False)
        self.import_button.setVisible(False)
        self.refresh_button.setVisible(False)

    def update_progress(self, current: int, total: int):
        """
        更新进度

        Args:
            current: 当前进度
            total: 总进度
        """
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
        if total > 0:
            self.progress_label.setText(
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

        # 隐藏进度条
        self.progress_container.setVisible(False)

        if discovered_count > 0:
            # 更新状态文本
            self.status_label.setText(
                f"✅ {t('wizard.scan_complete_detail', count=discovered_count)} | "
                f"{t('wizard.selected_count', count=selected_count)}"
            )

            # 更新按钮状态
            self.scan_button.setVisible(False)
            self.import_button.setVisible(True)
            self.import_button.setEnabled(selected_count > 0)
            self.refresh_button.setVisible(True)
            self.refresh_button.setEnabled(True)
            self.cancel_button.setVisible(True)
        else:
            # 未发现软件
            self.status_label.setText(f"⚠️ {t('wizard.no_apps_found')}")
            self.scan_button.setEnabled(True)
            self.refresh_button.setVisible(False)
            self.cancel_button.setVisible(False)

    def scan_error(self, error_msg: str):
        """
        扫描出错

        Args:
            error_msg: 错误信息
        """
        self.scanning = False

        # 隐藏进度条
        self.progress_container.setVisible(False)

        # 显示错误
        self.status_label.setText(
            f"❌ {t('wizard.scan_error', error=error_msg)}"
        )

        # 恢复扫描按钮
        self.scan_button.setEnabled(True)

    def reset(self):
        """重置状态"""
        self.scanning = False

        # 重置状态
        self.status_label.setText(f"🟢 {t('wizard.scan_idle')}")

        # 隐藏进度条
        self.progress_container.setVisible(False)

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
        if not self.scanning and self.discovered_count > 0:
            self.status_label.setText(
                f"✅ {t('wizard.scan_complete_detail', count=self.discovered_count)} | "
                f"{t('wizard.selected_count', count=count)}"
            )
        # 更新导入按钮状态
        self.set_import_enabled(count > 0)
