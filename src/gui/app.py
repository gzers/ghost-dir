"""
主应用程序类
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from qfluentwidgets import setTheme, Theme
from ..utils.admin import ensure_admin
from ..core.transaction import check_crash_recovery, recover_from_crash
from ..common.resource_loader import get_resource_path


class GhostDirApp(QApplication):
    """Ghost-Dir 主应用程序"""

    def __init__(self, argv):
        """初始化应用程序"""
        super().__init__(argv)

        # 设置应用程序信息
        self.setApplicationName("Ghost-Dir")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Ghost-Dir Team")

        # 启用高 DPI 缩放
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        # 执行启动检查
        self._startup_checks()

    def _apply_theme(self, theme: str):
        """应用主题设置"""
        theme_map = {
            "system": Theme.AUTO,
            "light": Theme.LIGHT,
            "dark": Theme.DARK
        }
        setTheme(theme_map.get(theme, Theme.AUTO))
    
    def _startup_checks(self):
        """启动时的安全检查"""
        # 1. 检查管理员权限（暂时跳过，避免闪退）
        # ensure_admin()
        # 改为仅提示
        from ..utils.admin import is_admin
        if not is_admin():
            QMessageBox.warning(
                None,
                "权限提示",
                "建议以管理员身份运行本程序，以确保连接点创建功能正常工作。\n\n"
                "请右键点击程序，选择'以管理员身份运行'。"
            )
        
        # 2. 检查崩溃恢复
        crash_record = check_crash_recovery()
        if crash_record:
            reply = QMessageBox.question(
                None,
                "检测到异常中断",
                f"检测到上次操作异常中断：\n\n"
                f"操作类型: {crash_record.operation}\n"
                f"源路径: {crash_record.source_path}\n"
                f"目标路径: {crash_record.target_path}\n\n"
                f"是否自动恢复到操作前状态？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if recover_from_crash(crash_record):
                    QMessageBox.information(
                        None,
                        "恢复成功",
                        "已成功恢复到操作前状态，数据未丢失。"
                    )
                else:
                    QMessageBox.warning(
                        None,
                        "恢复失败",
                        "自动恢复失败，请手动检查文件状态。"
                    )


def run_app():
    """运行应用程序"""
    app = GhostDirApp(sys.argv)

    # 加载用户数据并应用设置
    from ..data.user_manager import UserManager
    user_manager = UserManager()

    # 应用主题设置
    app._apply_theme(user_manager.get_theme())

    # 导入并创建主窗口（传入用户管理器）
    from .windows.main_window import MainWindow
    window = MainWindow(user_manager)
    window.show()

    sys.exit(app.exec())
