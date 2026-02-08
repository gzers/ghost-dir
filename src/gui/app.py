from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# 核心信息导入（轻量）
from src.common.config import APP_NAME, APP_VERSION

class GhostDirApp(QApplication):
    """Ghost-Dir 主应用程序"""

    def __init__(self, argv):
        """初始化应用程序"""
        super().__init__(argv)

        # 1. 立即执行 Service 初始化 (采用按需导入)
        self._init_services()

        # 2. 设置 AppUserModelID
        try:
            import ctypes
            myappid = 'ghost-dir.app.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        # 3. 设置应用程序信息
        self.setApplicationName(APP_NAME)
        self.setApplicationVersion(APP_VERSION)
        self.setOrganizationName("Ghost-Dir Team")

        # 4. 样式与图标（延迟导入）
        from qfluentwidgets import setFontFamilies
        setFontFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])

        from PySide6.QtGui import QIcon
        from src.common.resource_loader import get_resource_path
        try:
            icon_path = get_resource_path("assets/icon.png")
            self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"设置应用图标失败: {e}")

        # 启用高 DPI 缩放
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        # 5. 主题系统（延迟导入）
        self._init_theme_system()

    def _init_theme_system(self):
        """初始化主题系统，避免顶部导入阻塞"""
        from src.common.signals import signal_bus
        from qfluentwidgets import SystemThemeListener

        # 连接主题变更信号
        signal_bus.theme_changed.connect(self._apply_theme)
        signal_bus.theme_color_changed.connect(self._apply_theme_color)

        # 系统主题监听器
        self.system_theme_listener = SystemThemeListener(self)
        self.system_theme_listener.systemThemeChanged.connect(self._on_system_theme_changed)

    def _init_services(self):
        """初始化 Service 层 (按需导入，彻底阻断级联加载)"""
        from src.dao import TemplateDAO, LinkDAO, CategoryDAO
        from src.services import TemplateService, LinkService, CategoryService

        # 1. 初始化 DAO 层
        self.template_dao = TemplateDAO()
        self.link_dao = LinkDAO()
        self.category_dao = CategoryDAO()

        # 2. 初始化 Service 层 (依赖注入)
        self.template_service = TemplateService(self.template_dao)
        self.link_service = LinkService(self.link_dao)
        self.category_service = CategoryService(self.category_dao)

        print("[OK] Service 层初始化完成")

    def _apply_theme(self, theme: str):
        """应用主题设置"""
        from qfluentwidgets import setTheme, Theme
        try:
            theme_map = {
                "system": Theme.AUTO,
                "light": Theme.LIGHT,
                "dark": Theme.DARK
            }
            setTheme(theme_map.get(theme, Theme.AUTO))
            self._onThemeChangedFinished()
        except Exception as e:
            print(f"应用主题失败: {e}")

    def _on_system_theme_changed(self, theme):
        """系统主题变化回调"""
        from src.common.signals import signal_bus
        signal_bus.theme_changed.emit("system")

    def _onThemeChangedFinished(self):
        """主题切换完成后的处理"""
        from PySide6.QtCore import QTimer
        QTimer.singleShot(200, self._refresh_mica_effect)

    def _refresh_mica_effect(self):
        """刷新窗口云母特效"""
        window = self.topLevelWidgets()[0] if self.topLevelWidgets() else None
        if window and hasattr(window, '_init_window_effect'):
            window._init_window_effect()

    def _apply_theme_color(self, color: str):
        """应用主题色"""
        from qfluentwidgets import setThemeColor
        target_color = color
        if color == "system":
            try:
                from qframelesswindow.utils import getSystemAccentColor
                target_color = getSystemAccentColor()
            except Exception:
                target_color = "#009FAA"
        setThemeColor(target_color)

    def _startup_checks(self, splash=None):
        """启动时的安全检查"""
        from src.drivers.transaction import check_crash_recovery, recover_from_crash
        from qfluentwidgets import MessageBox
        from src.gui.i18n import t

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
    """运行应用程序 (三段式隔离启动)"""
    import sys
    
    # --- PHASE 1: 毫秒级首屏 (不加载任何业务逻辑) ---
    app = GhostDirApp(sys.argv)
    
    # 局部导入启动组件
    from src.gui.components.splash_screen import AppSplashScreen
    splash = AppSplashScreen()
    splash.show()
    
    # 释放 CPU 确保启动页第一时间绘制，循环 5 次以确保动画圆环开始旋转
    for _ in range(5):
        app.processEvents()

    # --- PHASE 2: 核心配置载入 (启动页背景下执行) ---
    # PHASE 2: 核心配置载入
    splash.set_message("正在连接服务总线...")
    from src.common.service_bus import service_bus
    from src.gui.i18n import t
    config_service = service_bus.config_service
    app.processEvents()

    splash.set_message("正在校验用户偏好设置...")
    app._apply_theme(config_service.get_theme())
    app._apply_theme_color(config_service.get_config("theme_color", "system"))
    
    splash.set_message("正在同步视觉主题...")
    splash.update_theme()
    for _ in range(5):
        app.processEvents()

    # PHASE 3: 业务层初始化与主窗口载入
    splash.set_message("正在进行环境安全检查...")
    app._startup_checks(splash)
    for _ in range(5):
        app.processEvents()

    splash.set_message("正在预热图形渲染引擎...")
    import time
    for _ in range(10):
        app.processEvents()
        time.sleep(0.005)

    splash.set_message("正在同步全量业务视图...")
    from src.gui.windows.main_window import MainWindow
    window = MainWindow(app)
    
    splash.set_message("正在唤醒系统核心组件...")
    # 在显示前确保窗口尺寸和位置正确
    window.resize(1200, 800)
    window._center_on_screen()
    
    # 直接显示主窗口，不使用置顶标志避免窗口重建
    window.show()
    window.raise_()
    window.activateWindow()
    app.processEvents()
    
    splash.set_message("系统已就绪")
    for _ in range(10):
        app.processEvents()
        time.sleep(0.01)
    
    # 先关闭启动页
    splash.finish()
    
    # 确保主窗口获得焦点
    window.raise_()
    window.activateWindow()

    # 最终渲染刷新，确保主窗口首页组件加载完成
    for _ in range(10):
        app.processEvents()

    sys.exit(app.exec())
