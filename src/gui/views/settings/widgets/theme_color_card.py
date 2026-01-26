# coding:utf-8
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, OptionsConfigItem, OptionsValidator
from .....common.signals import signal_bus
from .....common.config import THEME_COLOR_OPTIONS, DEFAULT_THEME_COLOR
from ....i18n import t

class ThemeColorCard(ComboBoxSettingCard):
    """ 主题颜色设置卡片 """

    def __init__(self, user_manager, parent=None):
        self.user_manager = user_manager
        
        # 从配置构建颜色映射字典
        self.color_map = {
            t(option["i18n_key"]): option["value"]
            for option in THEME_COLOR_OPTIONS
        }
        # 反向映射
        self.rev_color_map = {v: k for k, v in self.color_map.items()}

        # 选项文本列表
        texts = list(self.color_map.keys())

        # 创建配置项
        # 注意：这里的 configItem 主要用于 widget 内部状态绑定，
        # 实际持久化我们通过 connect 信号委托给 user_manager
        config_item = OptionsConfigItem(
            "Appearance", "ThemeColor", DEFAULT_THEME_COLOR,
            OptionsValidator(list(self.color_map.values())),
        )

        super().__init__(
            config_item,
            FluentIcon.PALETTE,
            t("settings.theme_color"),
            t("settings.theme_color_desc"),
            texts=texts,
            parent=parent
        )

        # 初始化值
        self._init_value()
        
        # 连接信号
        self.comboBox.currentTextChanged.connect(self._on_color_changed)
    
    def _init_value(self):
        """ 初始化当前选中项 """
        color = self.user_manager.get_theme_color()
        # 查找对应的显示文本，如果找不到则使用第一个选项
        text = self.rev_color_map.get(color, list(self.color_map.keys())[0])
        self.comboBox.setCurrentText(text)

    def _on_color_changed(self, text):
        """ 颜色变更回调 """
        color = self.color_map.get(text, DEFAULT_THEME_COLOR)
        
        if self.user_manager.set_theme_color(color):
            signal_bus.theme_color_changed.emit(color)
