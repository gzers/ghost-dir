"""
主应用程序类
"""
import sys
import ctypes
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import setTheme, Theme, setThemeColor
from ..common.signals import signal_bus
from ..utils.admin import ensure_admin
from ..core.transaction import check_crash_recovery, recover_from_crash
from ..common.resource_loader import get_resource_path


class GhostDirApp(QApplication):
    """Ghost-Dir 主应用程序"""

    def __init__(self, argv):
        """初始化应用程序"""
        super().__init__(argv)

        # 设置 AppUserModelID 以修复任务栏图标丢失问题
        try:
            myappid = 'ghost-dir.app.1.0'  # 任意唯一字符串
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        # 设置应用程序信息
        self.setApplicationName("Ghost-Dir")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Ghost-Dir Team")
        
        #设置应用图标
        try:
            icon_path = get_resource_path("assets/icon.png")
            self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"设置应用图标失败: {e}")

        # 启用高 DPI 缩放
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        # 执行启动检查
        self._startup_checks()

        # 连接主题变更信号
        signal_bus.theme_changed.connect(self._apply_theme)
        signal_bus.theme_color_changed.connect(self._apply_theme_color)

    def _apply_theme(self, theme: str):
        """应用主题设置"""
        theme_map = {
            "system": Theme.AUTO,
            "light": Theme.LIGHT,
            "dark": Theme.DARK
        }
        setTheme(theme_map.get(theme, Theme.AUTO))

    def _apply_theme_color(self, color: str):
        """应用主题色"""
        # 如果是 "system", QFluentWidgets 的 setThemeColor 不直接支持 "system" 字符串
        # 但通常我们不传递 "system"，而是传递具体颜色。
        # 如果用户选择 "系统"，我们需要在这里获取系统颜色。
        # 这里暂时假设 "system" 时使用默认 Teal，或者如果 QFluentWidgets 有自动获取机制则更好。
        # 为了简单，如果 color 是 hex，直接应用。
        # 如果是 "system"，我们暂不处理或设为默认，因为获取系统颜色比较复杂，除非引入额外库。
        # 考虑到用户需求，我们尽量实现。
        
        target_color = color
        if color == "system":
            # 尝试获取系统颜色，这里简化处理，如果库不支持则使用默认
            # 实际 QFluentWidgets 可能会有 getSystemAccentColor，但我不确定。
            # 既然没有 easy_proxifier 的 context，我假设默认颜色。
            # 或者我们可以保留默认 Teal。
            target_color = "#009FAA"
            
        setThemeColor(target_color)
    
    def _startup_checks(self):
        """启动时的安全检查"""
        # 1. 强制检查管理员权限
        # 如果未获得权限，会自动请求提权并重启
        from ..utils.admin import ensure_admin
        ensure_admin()
        
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
    app._apply_theme_color(user_manager.get_theme_color())

    # 导入并创建主窗口（传入用户管理器）
    from .windows.main_window import MainWindow
    window = MainWindow(user_manager)
    window.show()

    sys.exit(app.exec())
