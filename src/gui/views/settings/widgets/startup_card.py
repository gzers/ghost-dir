# coding:utf-8
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, OptionsConfigItem, OptionsValidator
from ....i18n import t

class StartupCard(ComboBoxSettingCard):
    """ 启动页面设置卡片 """

    def __init__(self, user_manager, parent=None):
        self.user_manager = user_manager
        
        # 映射字典
        self.page_map = {
            t("settings.startup_wizard"): "wizard",
            t("settings.startup_console"): "console",
            t("settings.startup_library"): "library"
        }
        self.rev_page_map = {v: k for k, v in self.page_map.items()}

        # 选项文本列表
        texts = list(self.page_map.keys())

        # Config Item
        config_item = OptionsConfigItem(
            "Startup", "Page", "wizard",
            OptionsValidator(list(self.page_map.values())),
        )

        super().__init__(
            config_item,
            FluentIcon.GAME,
            t("settings.startup_page"),
            t("settings.startup_page_desc"),
            texts=texts,
            parent=parent
        )

        # 初始化值
        self._init_value()
        
        # 连接信号
        self.comboBox.currentTextChanged.connect(self._on_page_changed)
    
    def _init_value(self):
        """ 初始化当前选中项 """
        page = self.user_manager.get_startup_page()
        text = self.rev_page_map.get(page, t("settings.startup_wizard"))
        self.comboBox.setCurrentText(text)

    def _on_page_changed(self, text):
        """ 启动页变更回调 """
        page = self.page_map.get(text, "wizard")
        self.user_manager.set_startup_page(page)
