# coding:utf-8
"""
配置恢复卡片组件
提供恢复默认配置的UI交互
"""
from qfluentwidgets import PushSettingCard, FluentIcon, MessageBox, InfoBar, InfoBarPosition
from PySide6.QtCore import Qt
from src.gui.i18n import t
from src.common.service_bus import service_bus
# TODO: 通过 app 实例访问 Service


class RestoreConfigCard(PushSettingCard):
    """恢复所有默认配置卡片"""

    def __init__(self, parent=None):
        super().__init__(
            "恢复",
            FluentIcon.SYNC,
            "恢复所有默认配置",
            "将分类、模板和UI配置恢复为官方默认值（不影响链接数据）",
            parent
        )

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        """点击恢复按钮"""
        # 显示警告对话框
        title = "警告"
        content = (
            "此操作将：\n"
            "• 恢复默认UI配置\n"
            "• 恢复默认分类定义\n"
            "• 恢复默认模板定义\n\n"
            "您的自定义配置将被覆盖！\n"
            "（用户链接数据不受影响）\n\n"
            "是否继续？"
        )

        dialog = MessageBox(title, content, self.window())
        dialog.yesButton.setText("确认恢复")
        dialog.cancelButton.setText("取消")

        if dialog.exec():
            # 用户确认，执行恢复
            self._execute_restore()

    def _execute_restore(self):
        """执行恢复操作"""
        # 调用服务
        success, msg = service_bus.config_restore_service.restore_all_defaults()

        if success:
            # 成功提示 - 使用顶部居中通知
            InfoBar.success(
                title="恢复成功",
                content="默认配置已恢复，应用将重新加载配置",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.window()
            )
            # 重新加载配置
            self._reload_configs()
        else:
            # 失败提示 - 使用顶部居中通知
            InfoBar.error(
                title="恢复失败",
                content=msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.window()
            )

    def _reload_configs(self):
        """重新加载配置"""
        from qfluentwidgets import qconfig
        from src.common.config import USER_CONFIG_FILE
        from src.common.signals import signal_bus

        # 重载 QFluentWidgets 配置
        qconfig.load(str(USER_CONFIG_FILE))

        # 重载分类和模板
        service_bus.category_manager.load_categories()
        service_bus.template_manager.load_templates()

        # 通知 UI 刷新
        signal_bus.data_refreshed.emit()


class RestoreCategoriesCard(PushSettingCard):
    """恢复默认分类卡片"""

    def __init__(self, parent=None):
        super().__init__(
            "恢复",
            FluentIcon.TAG,
            "恢复默认分类",
            "恢复官方分类定义（已创建的链接不受影响）",
            parent
        )

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        """点击恢复按钮"""
        title = "确认恢复默认分类"
        content = (
            "此操作将覆盖您的自定义分类！\n"
            "（已创建的链接不受影响）\n\n"
            "是否继续？"
        )

        dialog = MessageBox(title, content, self.window())
        dialog.yesButton.setText("确认")
        dialog.cancelButton.setText("取消")

        if dialog.exec():
            self._execute_restore()

    def _execute_restore(self):
        """执行恢复操作"""
        success, msg = service_bus.config_restore_service.restore_categories()

        if success:
            InfoBar.success(
                title="恢复成功",
                content="默认分类已恢复",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.window()
            )
            # 重新加载分类
            service_bus.category_manager.load_categories()
            from src.common.signals import signal_bus
            signal_bus.data_refreshed.emit()
        else:
            InfoBar.error(
                title="恢复失败",
                content=msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.window()
            )


class RestoreTemplatesCard(PushSettingCard):
    """恢复默认模板卡片"""

    def __init__(self, parent=None):
        super().__init__(
            "恢复",
            FluentIcon.DOCUMENT,
            "恢复默认模板",
            "恢复官方模板定义",
            parent
        )

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        """点击恢复按钮"""
        title = "确认恢复默认模板"
        content = (
            "此操作将覆盖您的自定义模板！\n\n"
            "是否继续？"
        )

        dialog = MessageBox(title, content, self.window())
        dialog.yesButton.setText("确认")
        dialog.cancelButton.setText("取消")

        if dialog.exec():
            self._execute_restore()

    def _execute_restore(self):
        """执行恢复操作"""
        success, msg = service_bus.config_restore_service.restore_templates()

        if success:
            InfoBar.success(
                title="恢复成功",
                content="默认模板已恢复",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.window()
            )
            # 重新加载模板
            service_bus.template_manager.load_templates()
            from src.common.signals import signal_bus
            signal_bus.data_refreshed.emit()
        else:
            InfoBar.error(
                title="恢复失败",
                content=msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.window()
            )
