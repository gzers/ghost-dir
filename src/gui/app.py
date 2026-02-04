"""
主应用程序类
"""
import sys
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import (setTheme, Theme, setThemeColor, SystemThemeListener, setFontFamilies, 
                            MessageBox, isDarkTheme, TitleLabel, SubtitleLabel, 
                            CaptionLabel, IndeterminateProgressBar)
from src.common.signals import signal_bus
from src.utils.admin import ensure_admin
from src.core.engine.transaction_engine import check_crash_recovery, recover_from_crash
from src.common.config import APP_NAME, APP_VERSION
from src.gui.i18n import t


from src.common.resource_loader import get_resource_path
import src.gui.common.notification  # 注册自定义置顶居中通知管理器


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
        self.setApplicationName(APP_NAME)
        self.setApplicationVersion(APP_VERSION)
        self.setOrganizationName("Ghost-Dir Team")

        # 字体标准化（QFluentWidgets 标准）
        setFontFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])

        #设置应用图标
        try:
            icon_path = get_resource_path("assets/icon.png")
            self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"设置应用图标失败: {e}")

        # 启用高 DPI 缩放
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        # 连接主题变更信号
        signal_bus.theme_changed.connect(self._apply_theme)
        signal_bus.theme_color_changed.connect(self._apply_theme_color)

        # 系统主题监听器（用于跟随系统主题）
        self.system_theme_listener = SystemThemeListener(self)
        # 连接系统主题变更信号
        self.system_theme_listener.systemThemeChanged.connect(self._on_system_theme_changed)

    def _apply_theme(self, theme: str):
        """应用主题设置"""
        try:
            theme_map = {
                "system": Theme.AUTO,
                "light": Theme.LIGHT,
                "dark": Theme.DARK
            }
            setTheme(theme_map.get(theme, Theme.AUTO))

            # 主题切换完成后处理
            self._onThemeChangedFinished()
        except Exception as e:
            print(f"应用主题失败: {e}")

    def _on_system_theme_changed(self, theme: Theme):
        """系统主题变化回调"""
        # 触发自定义信号以通知其他组件
        signal_bus.theme_changed.emit("system")

    def _onThemeChangedFinished(self):
        """主题切换完成后的处理"""
        # 刷新窗口云母特效（如果有主窗口实例）
        from PySide6.QtCore import QTimer
        QTimer.singleShot(200, self._refresh_mica_effect)

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
    
    def _startup_checks(self, splash=None):
        """启动时的安全检查"""
        # 1. 强制检查管理员权限
        if splash:
            splash.set_message(t("app.splash_check_admin"))
            self.processEvents()
            
        from src.utils.admin import ensure_admin
        ensure_admin()
        
        # 2. 检查崩溃恢复
        if splash:
            splash.set_message(t("app.splash_check_data"))
            self.processEvents()

        crash_record = check_crash_recovery()
        if crash_record:
            # 如果有启动页，保持开启作为背景
            message = f"检测到上次操作异常中断：\n\n" \
                     f"操作类型: {crash_record.operation}\n" \
                     f"源路径: {crash_record.source_path}\n" \
                     f"目标路径: {crash_record.target_path}\n\n" \
                     f"是否自动恢复到操作前状态？"
            dialog = MessageBox("检测到异常中断", message, None)
            dialog.yesButton.setText("是")
            dialog.cancelButton.setText("否")

            if dialog.exec():
                if recover_from_crash(crash_record):
                    MessageBox("恢复成功", "已成功恢复到操作前状态，数据未丢失。", None).exec()
                else:
                    MessageBox("恢复失败", "自动恢复失败，请手动检查文件状态。", None).exec()


def run_app():
    """运行应用程序"""
    app = GhostDirApp(sys.argv)

    # 通过服务中枢加载全局配置
    from src.core.services.context import service_bus
    config_service = service_bus.config_service

    # 应用主题设置
    app._apply_theme(config_service.get_theme())
    app._apply_theme_color(config_service.get_config("theme_color", "system"))

    # ========== 创建高级启动界面 ==========
    from src.gui.components.splash_screen import AppSplashScreen
    
    splash = AppSplashScreen()
    splash.show()
    
    # 虽然显示了，但需要处理事件让它渲染出来
    app.processEvents()
    # ===================================

    # 执行启动检查（在启动页背景下执行）
    app._startup_checks(splash)

    # 导入并创建主窗口（耗时操作）
    from .windows.main_window import MainWindow
    window = MainWindow()
    
    # 主窗口创建完成，关闭启动界面
    splash.finish()
    
    window.show()

    sys.exit(app.exec())
