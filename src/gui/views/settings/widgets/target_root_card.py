# coding:utf-8
from PySide6.QtWidgets import QFileDialog, QWidget
from qfluentwidgets import PushSettingCard, FluentIcon
from ....i18n import t
from src.common.validators import PathValidator

class TargetRootCard(PushSettingCard):
    """ 默认仓库路径设置卡片 """

    def __init__(self, user_manager, parent=None):
        self.user_manager = user_manager
        
        super().__init__(
            t("settings.select_path"),
            FluentIcon.FOLDER,
            t("settings.default_target_root"),
            self.user_manager.get_default_target_root(),
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
            self.user_manager.get_default_target_root()
        )
        
        if path:
            # 使用 PathValidator 标准化路径，移除 \\?\ 等前缀并统一分隔符
            path = PathValidator().normalize(path)
            if self.user_manager.set_default_target_root(path):
                self.setContent(path)
