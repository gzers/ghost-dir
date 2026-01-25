"""
主应用程序类
"""
import sys
import ctypes
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import setTheme, Theme, setThemeColor, SystemThemeListener
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

        # 系统主题监听器（用于跟随系统主题）
        self.system_theme_listener = SystemThemeListener(self)
        # 连接系统主题变更信号
        self.system_theme_listener.systemThemeChanged.connect(self._on_system_theme_changed)

    def _apply_theme(self, theme: str):
        """应用主题设置"""
        theme_map = {
            "system": Theme.AUTO,
            "light": Theme.LIGHT,
            "dark": Theme.DARK
        }
        setTheme(theme_map.get(theme, Theme.AUTO))

        # 启动或停止系统主题监听器
        if theme == "system":
            if not self.system_theme_listener.isRunning():
                self.system_theme_listener.start()
        else:
            if self.system_theme_listener.isRunning():
                self.system_theme_listener.stop()

        # 主题切换完成后处理
        self._onThemeChangedFinished()

    def _on_system_theme_changed(self, theme: Theme):
        """系统主题变化回调"""
        # 触发自定义信号以通知其他组件
        signal_bus.theme_changed.emit("system")

    def _onThemeChangedFinished(self):
        """主题切换完成后的处理"""
        # 刷新窗口云母特效（如果有主窗口实例）
        # 注意：这里需要延迟刷新以确保主题已经完全切换
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self._refresh_mica_effect)

    def _refresh_mica_effect(self):
        """刷新窗口云母特效"""
        # 获取主窗口并刷新特效
        window = self.topLevelWidgets()[0] if self.topLevelWidgets() else None
        if window and hasattr(window, '_init_window_effect'):
            window._init_window_effect()

    def _apply_theme_color(self, color: str):
        """应用主题色"""
        target_color = color
        if color == "system":
            # 使用 qframelesswindow 的 getSystemAccentColor 获取系统强调色
            try:
                from qframelesswindow.utils import getSystemAccentColor
                target_color = getSystemAccentColor()
            except (ImportError, Exception) as e:
                # 如果获取失败，使用默认的 Teal 颜色
                target_color = "#009FAA"
                print(f"获取系统强调色失败，使用默认颜色: {e}")

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
