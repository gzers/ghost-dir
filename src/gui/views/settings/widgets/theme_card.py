# coding:utf-8
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, OptionsConfigItem, OptionsValidator
from src.common.signals import signal_bus
from src.common.config import THEME_OPTIONS, DEFAULT_THEME
from src.gui.i18n import t

class ThemeCard(ComboBoxSettingCard):
    """ 主题模式设置卡片 """

    def __init__(self, config_service, parent=None):
        self.config_service = config_service

        # 从配置构建映射字典
        self.theme_map = {
            t(option["i18n_key"]): option["value"]
            for option in THEME_OPTIONS
        }
        self.rev_theme_map = {v: k for k, v in self.theme_map.items()}

        # 选项文本列表
        texts = list(self.theme_map.keys())

        # Config Item
        config_item = OptionsConfigItem(
            "Appearance", "Theme", DEFAULT_THEME,
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
        theme = self.config_service.get_theme()
        text = self.rev_theme_map.get(theme, list(self.theme_map.keys())[0])
        self.comboBox.setCurrentText(text)

    def _on_theme_changed(self, text):
        """ 主题变更回调 """
        theme = self.theme_map.get(text, DEFAULT_THEME)

        if self.config_service.set_theme(theme):
            signal_bus.theme_changed.emit(theme)
            # 同时也发送通用的配置变更信号
