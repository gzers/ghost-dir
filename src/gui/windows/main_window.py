"""
主窗口
使用 FluentWindow 实现 Mica/Acrylic 效果
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, FluentIcon,
    setCustomStyleSheet, isDarkTheme, Theme
)
from PySide6.QtCore import Qt, QSize, QTimer
# TODO: 通过 app 实例访问 Service
from src.gui.views.links import LinksView
from src.gui.views.wizard import WizardView
from src.gui.views.library import LibraryView
from src.gui.views.help import HelpView
from src.gui.views.settings import SettingView
from src.common.resource_loader import get_resource_path
from src.common.config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from src.drivers.windows import is_transparency_enabled
from src.gui.styles import window_style_sheet
from src.common.service_bus import service_bus


class MainWindow(FluentWindow):
    """主窗口"""

    def __init__(self, app=None):
        """初始化主窗口"""
        super().__init__()
        self.app = app
        service_bus.main_window = self

        # 视图缓存，用于实现延迟加载
        self._views = {}

        # 1. 初始化窗口基础属性 (轻量)
        self._init_window()
        
        # 2. 初始化导航栏并加载首屏 (按需创建)
        self._init_navigation()

        # 3. 监听主题变更
        from src.common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _get_view(self, name: str):
        """延迟创建视图实例"""
        if name in self._views:
            return self._views[name]
        
        # 这种模式可以极大地减少启动时的组件堆叠压力
        view_class_map = {
            "links": ("src.gui.views.links", "LinksView"),
            "wizard": ("src.gui.views.wizard", "WizardView"),
            "library": ("src.gui.views.library", "LibraryView"),
            "help": ("src.gui.views.help", "HelpView"),
            "settings": ("src.gui.views.settings", "SettingView")
        }
        
        if name not in view_class_map:
            return None
            
        module_path, class_name = view_class_map[name]
        import importlib
        module = importlib.import_module(module_path)
        view_class = getattr(module, class_name)
        
        view = view_class(self)
        view.setObjectName(f"{name}View")
        self._views[name] = view
        
        # 关键点：每创建一个重型视图，都给 UI 线程一个喘息机会
        if self.app:
            self.app.processEvents()
            
        return view

    def _init_window(self):
        """初始化窗口基础信息"""
        self.setWindowTitle("Ghost-Dir")
        self.resize(1200, 800)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        try:
            icon_path = get_resource_path("assets/icon.png")
            self.setWindowIcon(QIcon(str(icon_path)))
        except Exception:
            pass

        self._init_window_effect()
        self._center_on_screen()

    def _center_on_screen(self):
        """将窗口移动到屏幕中央 (解决启动显示偏移)"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.x() + (screen.width() - size.width()) // 2)
        y = (screen.y() + (screen.height() - size.height()) // 2)
        self.move(x, y)

    def _init_navigation(self):
        """初始化导航栏 (实现首页抢先展示，其余业务页面后台异步挂载)"""
        # 1. 确定首页
        startup_page_key = service_bus.config_service.get_startup_page() or "wizard"
        
        # 定义所有导航项配置 (Icon, Title, Position)
        self._nav_configs = {
            "wizard": (FluentIcon.ROBOT, "智能向导", NavigationItemPosition.TOP),
            "links": (FluentIcon.IOT, "我的链接", NavigationItemPosition.TOP),
            "library": (FluentIcon.BOOK_SHELF, "模版库", NavigationItemPosition.TOP),
            "help": (FluentIcon.INFO, "帮助", NavigationItemPosition.BOTTOM),
            "settings": (FluentIcon.SETTING, "设置", NavigationItemPosition.BOTTOM)
        }
        
        # 2. 抢先加载首页视图并挂载
        home_view = self._get_view(startup_page_key)
        icon, title, pos = self._nav_configs[startup_page_key]
        self.addSubInterface(home_view, icon, title, position=pos)

        # 初始切换
        self.switchTo(home_view)
        
        # 3. 关键：在主窗口显示后的第一秒开始静默挂载剩余页面
        QTimer.singleShot(800, self._lazy_load_remaining_views)

    def _lazy_load_remaining_views(self):
        """利用官方接口顺序加载剩余视图，避开索引操作坑"""
        # 按照用户习惯的视觉顺序加载剩余项
        priority = ["wizard", "links", "library", "help", "settings"]
        startup_page_key = service_bus.config_service.get_startup_page() or "wizard"
        
        for key in priority:
            # 跳过已经加载的首页
            if key == startup_page_key:
                continue
                
            if key not in self._views:
                view = self._get_view(key)
                icon, title, pos = self._nav_configs[key]
                # 走官方 addSubInterface 接口，它是线程安全且会自动同步内部动画状态的
                self.addSubInterface(view, icon, title, position=pos)
                
                if self.app:
                    self.app.processEvents()

    def _init_window_effect(self):
        """初始化窗口特效（云母/亚克力/优雅降级）"""
        try:
            if is_transparency_enabled():
                # 开启云母/亚克力效果
                self.setMicaEffectEnabled(True)
            else:
                self.setMicaEffectEnabled(False)
                window_style_sheet.apply(self)
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        except Exception as e:
            print(f"窗口特效初始化失败: {e}")

    def _on_theme_changed(self, theme):
        """处理主题变更"""
        # 重新初始化背景效果
        self._init_window_effect()

        # 官方修正：如果开启了云母特效，主题切换后需要通过定时器重新触发系统特效更新
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))
