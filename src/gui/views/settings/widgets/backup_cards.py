# coding:utf-8
"""
配置备份卡片
提供导出和导入配置备份的功能
"""
from pathlib import Path
from PySide6.QtWidgets import QFileDialog
from qfluentwidgets import PushSettingCard, FluentIcon, InfoBar, InfoBarPosition, MessageBox
# TODO: 迁移到新架构 ConfigBackupManager
from src.common.config import DATA_DIR


class ExportBackupCard(PushSettingCard):
    """导出配置备份卡片"""
    
    def __init__(self, parent=None):
        super().__init__(
            "导出备份",
            FluentIcon.SAVE,
            "导出配置备份",
            "将所有配置导出为 ZIP 文件",
            parent
        )
        
        # 连接信号
        self.clicked.connect(self._on_export_clicked)
    
    def _on_export_clicked(self):
        """导出按钮被点击"""
        # 选择保存位置
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择备份保存位置",
            str(Path.home() / "Desktop"),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if not folder:
            return
        
        try:
            # 导出备份
            manager = ConfigBackupManager()
            success, result = manager.export_all_configs(Path(folder))
            
            if success:
                InfoBar.success(
                    title="导出成功",
                    content=f"配置已导出到: {result}",
                    orient=InfoBarPosition.TOP,
                    isClosable=True,
                    duration=3000,
                    parent=self.window()
                )
            else:
                InfoBar.error(
                    title="导出失败",
                    content=result,
                    orient=InfoBarPosition.TOP,
                    isClosable=True,
                    duration=3000,
                    parent=self.window()
                )
        except Exception as e:
            InfoBar.error(
                title="导出失败",
                content=f"发生错误: {str(e)}",
                orient=InfoBarPosition.TOP,
                isClosable=True,
                duration=3000,
                parent=self.window()
            )


class ImportBackupCard(PushSettingCard):
    """导入配置备份卡片"""
    
    def __init__(self, parent=None):
        super().__init__(
            "导入备份",
            FluentIcon.DOWNLOAD,
            "导入配置备份",
            "从 ZIP 文件还原所有配置",
            parent
        )
        
        # 连接信号
        self.clicked.connect(self._on_import_clicked)
    
    def _on_import_clicked(self):
        """导入按钮被点击"""
        # 选择备份文件
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择备份文件",
            str(Path.home() / "Desktop"),
            "ZIP Files (*.zip)"
        )
        
        if not file_path:
            return
        
        # 确认对话框
        if not self._confirm_import():
            return
        
        try:
            # 还原备份
            manager = ConfigBackupManager()
            success, msg = manager.restore_from_backup(Path(file_path))
            
            if success:
                # 提示重启
                self._show_restart_dialog()
            else:
                InfoBar.error(
                    title="导入失败",
                    content=msg,
                    orient=InfoBarPosition.TOP,
                    isClosable=True,
                    duration=3000,
                    parent=self.window()
                )
        except Exception as e:
            InfoBar.error(
                title="导入失败",
                content=f"发生错误: {str(e)}",
                orient=InfoBarPosition.TOP,
                isClosable=True,
                duration=3000,
                parent=self.window()
            )
    
    def _confirm_import(self) -> bool:
        """显示确认对话框"""
        w = MessageBox(
            "确认导入",
            "导入备份将覆盖当前所有配置，当前配置会自动备份。\n\n确定要继续吗？",
            self.window()
        )
        w.yesButton.setText("确定")
        w.cancelButton.setText("取消")
        
        return w.exec()
    
    def _show_restart_dialog(self):
        """显示重启提示对话框"""
        w = MessageBox(
            "导入成功",
            "配置已成功导入！\n\n请重启应用以使配置生效。",
            self.window()
        )
        w.yesButton.setText("确定")
        w.cancelButton.hide()
        w.exec()
