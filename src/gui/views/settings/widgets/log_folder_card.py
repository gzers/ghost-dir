# coding:utf-8
import os
from qfluentwidgets import PushSettingCard, FluentIcon
from src.gui.i18n import t
from src.common.config import LOG_DIR

class LogFolderCard(PushSettingCard):
    """ 日志目录设置卡片 """

    def __init__(self, parent=None):
        super().__init__(
            t("settings.view_log"),
            FluentIcon.DOCUMENT,
            t("settings.log_folder"),
            str(LOG_DIR),
            parent
        )

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        """ 打开日志文件夹 """
        if os.path.exists(LOG_DIR):
            os.startfile(LOG_DIR)
        else:
            # 如果不存在则创建并打开
            os.makedirs(LOG_DIR, exist_ok=True)
            os.startfile(LOG_DIR)
