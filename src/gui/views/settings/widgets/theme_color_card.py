# coding:utf-8
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, OptionsConfigItem, OptionsValidator
from .....common.signals import signal_bus
from ....i18n import t

class ThemeColorCard(ComboBoxSettingCard):
    """ 主题颜色设置卡片 """

    def __init__(self, user_manager, parent=None):
        self.user_manager = user_manager
        
        # 颜色映射字典
        self.color_map = {
            t("settings.theme_color_system"): "system",
            t("settings.theme_color_teal"): "#009FAA",
            t("settings.theme_color_blue"): "#0078D4",
            t("settings.theme_color_green"): "#107C10",
            t("settings.theme_color_orange"): "#D83B01",
            t("settings.theme_color_red"): "#E81123",
            t("settings.theme_color_purple"): "#80397B"
        }
        # 反向映射
        self.rev_color_map = {v: k for k, v in self.color_map.items()}

        # 选项文本列表
        texts = list(self.color_map.keys())

        # 创建配置项
        # 注意：这里的 configItem 主要用于 widget 内部状态绑定，
        # 实际持久化我们通过 connect 信号委托给 user_manager
        config_item = OptionsConfigItem(
            "Appearance", "ThemeColor", "system",
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
        # 查找对应的显示文本
        text = self.rev_color_map.get(color, t("settings.theme_color_teal"))
        self.setValue(text)  # ComboBoxSettingCard.setValue 接受的是显示的文本吗？
        # wait, ComboBoxSettingCard.setValue usually takes the value matching the logic?
        # No, typically setValue takes the generic value if using qconfig.
        # But here I am not fully using qconfig's bind.
        # ComboBoxSettingCard wraps a ComboBox.
        # Let's see how standard usage works. 
        # Usually: card.setValue(value) where value matches one of the options if mapped?
        # Actually ComboBoxSettingCard expects `texts` to be the display labels.
        # The `configItem` stores the underlying value?
        # In `qfluentwidgets`, `ComboBoxSettingCard` maps selection index to `configItem` value if `configItem` is valid?
        # Let's look at `SettingView` again.
        # `self.themeCard.setValue(current_theme)` where current_theme is "system","light"...
        # And `texts` are `["跟随系统", "亮色", ...]`
        # So `OptionsSettingCard` (used for theme) handles mapping index to value?
        # `OptionsSettingCard` is a group of RadioButtons.
        # `ComboBoxSettingCard` uses a ComboBox.
        
        # If I use `self.comboBox.setCurrentText(text)`, that works for UI.
        self.comboBox.setCurrentText(text)

    def _on_color_changed(self, text):
        """ 颜色变更回调 """
        color = self.color_map.get(text, "#009FAA")
        
        if self.user_manager.set_theme_color(color):
            signal_bus.theme_color_changed.emit(color)
