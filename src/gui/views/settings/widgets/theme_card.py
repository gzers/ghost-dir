# coding:utf-8
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, OptionsConfigItem, OptionsValidator
from .....common.signals import signal_bus
from ....i18n import t

class ThemeCard(ComboBoxSettingCard):
    """ 主题模式设置卡片 """

    def __init__(self, user_manager, parent=None):
        self.user_manager = user_manager
        
        # 映射字典
        self.theme_map = {
            t("settings.theme_system"): "system",
            t("settings.theme_light"): "light",
            t("settings.theme_dark"): "dark"
        }
        self.rev_theme_map = {v: k for k, v in self.theme_map.items()}

        # 选项文本列表
        texts = list(self.theme_map.keys())

        # Config Item
        config_item = OptionsConfigItem(
            "Appearance", "Theme", "system",
            OptionsValidator(list(self.theme_map.values())),
        )

        super().__init__(
            config_item,
            FluentIcon.BRUSH,
            t("settings.theme"),
            t("settings.theme_desc"),
            texts=texts,
            parent=parent
        )

        # 初始化值
        self._init_value()
        
        # 连接信号
        self.comboBox.currentTextChanged.connect(self._on_theme_changed)
    
    def _init_value(self):
        """ 初始化当前选中项 """
        theme = self.user_manager.get_theme()
        text = self.rev_theme_map.get(theme, t("settings.theme_system"))
        self.comboBox.setCurrentText(text)

    def _on_theme_changed(self, text):
        """ 主题变更回调 """
        theme = self.theme_map.get(text, "system")
        
        if self.user_manager.set_theme(theme):
            signal_bus.theme_changed.emit(theme)
