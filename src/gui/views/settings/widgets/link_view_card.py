# coding:utf-8
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, OptionsConfigItem, OptionsValidator
from .....common.config import LINK_VIEW_OPTIONS, DEFAULT_LINK_VIEW
from ....i18n import t

class LinkViewCard(ComboBoxSettingCard):
    """ 默认连接视图设置卡片 """

    def __init__(self, user_manager, parent=None):
        self.user_manager = user_manager
        
        # 从配置构建映射字典
        self.view_map = {
            t(option["i18n_key"]): option["value"]
            for option in LINK_VIEW_OPTIONS
        }
        self.rev_view_map = {v: k for k, v in self.view_map.items()}

        # 选项文本列表
        texts = list(self.view_map.keys())

        # Config Item (用于 ComboBoxSettingCard 的标准架构)
        config_item = OptionsConfigItem(
            "Personalization", "DefaultLinkView", DEFAULT_LINK_VIEW,
            OptionsValidator(list(self.view_map.values())),
        )

        super().__init__(
            config_item,
            FluentIcon.LAYOUT,
            t("settings.view_mode"),
            t("settings.view_mode_desc"),
            texts=texts,
            parent=parent
        )

        # 初始化值
        self._init_value()
        
        # 连接信号
        self.comboBox.currentTextChanged.connect(self._on_view_changed)
    
    def _init_value(self):
        """ 初始化当前选中项 """
        view = self.user_manager.get_default_link_view()
        text = self.rev_view_map.get(view, list(self.view_map.keys())[0])
        self.comboBox.setCurrentText(text)

    def _on_view_changed(self, text):
        """ 视图模式变更回调 """
        view = self.view_map.get(text, DEFAULT_LINK_VIEW)
        self.user_manager.set_default_link_view(view)
