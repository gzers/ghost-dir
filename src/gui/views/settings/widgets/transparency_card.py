# coding:utf-8
from qfluentwidgets import SwitchSettingCard, FluentIcon, ConfigItem, BoolValidator
from src.common.signals import signal_bus
from src.gui.i18n import t

class TransparencyCard(SwitchSettingCard):
    """ 透明效果设置卡片 """

    def __init__(self, config_service, parent=None):
        self.config_service = config_service
        
        # 创建一个虚拟的 ConfigItem 用于绑定
        config_item = ConfigItem("Appearance", "EnableTransparency", True, BoolValidator())

        super().__init__(
            icon=FluentIcon.TRANSPARENT,
            title=t("settings.transparency"),
            content=t("settings.transparency_desc"),
            configItem=config_item,
            parent=parent
        )

        # 初始化值
        self._init_value()
        
        # 连接信号
        self.checkedChanged.connect(self._on_transparency_changed)
    
    def _init_value(self):
        """ 初始化当前选中状态 """
        enabled = self.config_service.get_transparency()
        self.setChecked(enabled)

    def _on_transparency_changed(self, is_checked: bool):
        """ 透明效果变更回调 """
        if self.config_service.set_transparency(is_checked):
            # 发送全局信号（复用 theme 变更信号，因为窗口效果通常随之刷新）
            signal_bus.theme_changed.emit(self.config_service.get_theme())
