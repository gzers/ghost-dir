# coding:utf-8
"""
配置文件编辑器卡片组件
允许用户通过外部编辑器修改配置文件，并提供实时校验与热重载
重构版本：所有业务逻辑调用 ConfigFileService
"""
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import Qt, QFileSystemWatcher, QUrl
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PySide6.QtGui import QDesktopServices
from qfluentwidgets import (
    CardWidget, BodyLabel, IconWidget, ToolButton, PushButton,
    FluentIcon, InfoBar, MessageBox
)

from src.gui.i18n import t
from src.gui.styles import apply_font_style, apply_muted_text_style
from src.common.config import USER_CONFIG_FILE, USER_CATEGORIES_FILE, USER_LINKS_FILE
# TODO: ConfigFileService 尚未实现，暂时注释掉
# from src.core.services.config_file_service import ConfigFileService


class ConfigFileRow(QWidget):
    """单个配置文件行组件"""

    def __init__(self, file_path: Path, icon: FluentIcon, color: str,
                 name_key: str, desc_key: str, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.name_key = name_key
        self.desc_key = desc_key

        self._init_ui(icon, color)
        self._update_status(True)  # 初始状态为正常

    def _init_ui(self, icon: FluentIcon, color: str):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # 左侧图标
        self.icon_widget = IconWidget(icon, self)
        self.icon_widget.setFixedSize(32, 32)
        layout.addWidget(self.icon_widget)

        # 中间信息区
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        # 文件名（加粗）
        self.name_label = BodyLabel(t(f"wizard.{self.name_key}"))
        apply_font_style(self.name_label, weight="semibold")
        info_layout.addWidget(self.name_label)

        # 用途说明（灰色小字）
        self.desc_label = BodyLabel(t(f"wizard.{self.desc_key}"))
        apply_muted_text_style(self.desc_label, size="sm")
        info_layout.addWidget(self.desc_label)

        # 文件路径（更小的灰色字体）
        self.path_label = BodyLabel(str(self.file_path))
        apply_muted_text_style(self.path_label, size="xs")
        info_layout.addWidget(self.path_label)

        layout.addLayout(info_layout, stretch=1)

        # 右侧操作区
        # 编辑按钮
        self.edit_button = ToolButton(FluentIcon.EDIT, self)
        self.edit_button.setToolTip(t("wizard.config_editor.edit"))
        self.edit_button.clicked.connect(self._on_edit_clicked)
        layout.addWidget(self.edit_button)

        # 状态指示器
        self.status_label = BodyLabel()
        self.status_label.setFixedWidth(80)
        layout.addWidget(self.status_label)

    def _on_edit_clicked(self):
        """编辑按钮点击事件"""
        url = QUrl.fromLocalFile(str(self.file_path))
        if QDesktopServices.openUrl(url):
            InfoBar.info(
                t("wizard.config_editor.opened"),
                t("wizard.config_editor.save_to_reload"),
                duration=3000,
                position='TopCenter',
                parent=self.window()
            )
        else:
            InfoBar.error(
                t("common.error"),
                t("wizard.config_editor.open_failed"),
                duration=3000,
                position='TopCenter',
                parent=self.window()
            )

    def _update_status(self, is_valid: bool):
        """更新状态指示器"""
        if is_valid:
            self.status_label.setText(f"✅ {t('wizard.config_editor.status_ok')}")
            self.status_label.setStyleSheet("color: #27AE60;")
        else:
            self.status_label.setText(f"❌ {t('wizard.config_editor.status_error')}")
            self.status_label.setStyleSheet("color: #E74C3C;")

    def validate_and_update(self, config_service) -> bool:
        """
        校验文件并更新状态（调用服务层）

        Args:
            config_service: 配置文件服务实例

        Returns:
            是否校验通过
        """
        # TODO: ConfigFileService 尚未实现，暂时返回 True
        if config_service is None:
            self._update_status(True)
            return True

        # 调用服务层校验
        is_valid, error_msg = config_service.validate_config_file(self.file_path)
        self._update_status(is_valid)

        if not is_valid:
            MessageBox(
                t("wizard.config_editor.validation_failed"),
                error_msg,
                self.window()
            ).exec()

        return is_valid


class ConfigEditorCard(CardWidget):
    """配置文件编辑器卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO: ConfigFileService 尚未实现，暂时注释掉
        # self.config_service = ConfigFileService()
        self.config_service = None  # 临时占位

        # 配置文件映射
        self.config_rows = {}

        self._init_ui()
        self._setup_file_watcher()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 标题栏（标题 + 操作按钮）
        header_layout = QHBoxLayout()

        title_label = BodyLabel(t("wizard.config_editor.title"))
        apply_font_style(title_label, size="lg", weight="semibold")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # 导出按钮
        self.export_button = PushButton(FluentIcon.SAVE, t("wizard.config_editor.export"))
        self.export_button.clicked.connect(self._on_export_clicked)
        header_layout.addWidget(self.export_button)

        # 还原按钮
        self.restore_button = PushButton(FluentIcon.FOLDER, t("wizard.config_editor.restore"))
        self.restore_button.clicked.connect(self._on_restore_clicked)
        header_layout.addWidget(self.restore_button)

        layout.addLayout(header_layout)

        # 警告横幅
        self.warning_banner = self._create_warning_banner()
        layout.addWidget(self.warning_banner)

        # 说明文字 (正常字体)
        desc_label = BodyLabel(t("wizard.config_editor.description"))
        layout.addWidget(desc_label)

        # 分隔线
        layout.addSpacing(8)

        # 配置文件列表
        config_files = [
            (USER_CONFIG_FILE, FluentIcon.SETTING, "#2F6BFF",
             "config_editor.config_json", "config_editor.config_json_desc"),
            (USER_CATEGORIES_FILE, FluentIcon.FOLDER_ADD, "#9A7BFF",
             "config_editor.categories_json", "config_editor.categories_json_desc"),
            (USER_LINKS_FILE, FluentIcon.LINK, "#27AE60",
             "config_editor.links_json", "config_editor.links_json_desc"),
        ]

        for file_path, icon, color, name_key, desc_key in config_files:
            row = ConfigFileRow(file_path, icon, color, name_key, desc_key, self)
            layout.addWidget(row)
            self.config_rows[str(file_path)] = row

    def _create_warning_banner(self) -> QWidget:
        """创建警告横幅"""
        banner = QWidget(self)
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(12, 8, 12, 8)
        banner_layout.setSpacing(8)

        # 警告图标
        warning_icon = IconWidget(FluentIcon.INFO, banner)
        warning_icon.setFixedSize(20, 20)
        banner_layout.addWidget(warning_icon)

        # 警告文本 (小字体)
        warning_text = BodyLabel("警告: 直接修改配置文件可能导致应用异常，建议在修改前先备份配置", banner)
        apply_font_style(warning_text, size="xs")
        apply_muted_text_style(warning_text)
        banner_layout.addWidget(warning_text, stretch=1)

        return banner

    def _setup_file_watcher(self):
        """设置文件监控"""
        self.file_watcher = QFileSystemWatcher(self)

        # 添加监控路径
        for file_path in self.config_rows.keys():
            self.file_watcher.addPath(file_path)

        # 连接文件变更信号
        self.file_watcher.fileChanged.connect(self._on_file_changed)

    def _on_file_changed(self, file_path: str):
        """文件变更回调"""
        row = self.config_rows.get(file_path)
        if not row:
            return

        # TODO: ConfigFileService 尚未实现，暂时跳过校验和重载
        if self.config_service is None:
            InfoBar.info(
                t("common.info"),
                "配置文件已更改，但校验功能尚未实现",
                duration=2000,
                position='TopCenter',
                parent=self.window()
            )
            return

        # 调用服务层校验
        is_valid = row.validate_and_update(self.config_service)

        if is_valid:
            # 调用服务层重载
            success, error_msg = self.config_service.reload_config(Path(file_path))

            if not success:
                InfoBar.error(
                    t("common.error"),
                    error_msg,
                    duration=3000,
                    position='TopCenter',
                    parent=self.window()
                )

            # 重新添加监控（某些编辑器保存时会删除重建文件）
            if not self.file_watcher.files() or file_path not in self.file_watcher.files():
                self.file_watcher.addPath(file_path)

    def _on_export_clicked(self):
        """导出按钮点击"""
        # TODO: ConfigFileService 尚未实现
        if self.config_service is None:
            InfoBar.warning(
                t("common.warning"),
                "配置导出功能尚未实现",
                duration=2000,
                position='TopCenter',
                parent=self.window()
            )
            return

        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self.window(),
            t("wizard.config_editor.export_title"),
            f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            "ZIP 文件 (*.zip)"
        )

        if file_path:
            success, result = self.config_service.export_configs(Path(file_path))
            if success:
                InfoBar.success(
                    t("common.success"),
                    t("wizard.config_editor.export_success").format(path=result),
                    duration=3000,
                    position='TopCenter',
                    parent=self.window()
                )
            else:
                InfoBar.error(
                    t("common.error"),
                    result,
                    duration=3000,
                    position='TopCenter',
                    parent=self.window()
                )

    def _on_restore_clicked(self):
        """还原按钮点击"""
        # TODO: ConfigFileService 尚未实现
        if self.config_service is None:
            InfoBar.warning(
                t("common.warning"),
                "配置还原功能尚未实现",
                duration=2000,
                position='TopCenter',
                parent=self.window()
            )
            return

        # 选择备份文件
        file_path, _ = QFileDialog.getOpenFileName(
            self.window(),
            t("wizard.config_editor.restore_title"),
            "",
            "ZIP 文件 (*.zip)"
        )

        if file_path:
            # 确认对话框
            msg_box = MessageBox(
                t("wizard.config_editor.restore_confirm_title"),
                t("wizard.config_editor.restore_confirm_message"),
                self.window()
            )

            if msg_box.exec():
                success, error_msg = self.config_service.restore_configs(Path(file_path))
                if success:
                    InfoBar.success(
                        t("common.success"),
                        t("wizard.config_editor.restore_success"),
                        duration=3000,
                        position='TopCenter',
                        parent=self.window()
                    )

                    # 更新所有状态指示器
                    for row in self.config_rows.values():
                        row._update_status(True)
                else:
                    InfoBar.error(
                        t("common.error"),
                        error_msg,
                        duration=3000,
                        position='TopCenter',
                        parent=self.window()
                    )
