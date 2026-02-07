# coding:utf-8
from PySide6.QtWidgets import QFileDialog, QWidget
from qfluentwidgets import PushSettingCard, FluentIcon, InfoBar
from src.gui.i18n import t
from src.common.validators import PathValidator

class TargetRootCard(PushSettingCard):
    """ 默认仓库路径设置卡片 """

    def __init__(self, config_service, parent=None):
        self.config_service = config_service

        super().__init__(
            t("settings.select_path"),
            FluentIcon.FOLDER,
            t("settings.default_target_root"),
            self.config_service.get_default_target_root(),
            parent
        )

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        """ 选择路径 """
        # 获取最上层窗口作为父窗口，防止模态阻塞问题
        parent_window = self.window()

        path = QFileDialog.getExistingDirectory(
            parent_window,
            t("settings.select_path"),
            self.config_service.get_default_target_root()
        )

        if path:
            if self.config_service.set_default_target_root(path):
                self.setContent(path)
                InfoBar.success(
                    t("common.success"),
                    t("settings.path_updated"),
                    duration=2000,
                    position='TopCenter',
                    parent=parent_window
                )
