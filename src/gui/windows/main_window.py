"""
主窗口
使用 FluentWindow 实现 Mica/Acrylic 效果
"""
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, FluentIcon,
    setCustomStyleSheet, isDarkTheme, Theme
)
from src.common.resource_loader import get_resource_path
from src.common.config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from src.drivers.windows import is_transparency_enabled
from src.gui.styles import window_style_sheet
from src.common.service_bus import service_bus


class LazyViewContainer(QFrame):
    """延迟加载视图容器 (代理模式)"""

    def __init__(self, key: str, parent_window, parent=None):
        super().__init__(parent)
        self.key = key
        self.parent_window = parent_window
        self.view = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setObjectName(f"container_{key}")

    def load_view(self):
        """执行真实的视图加载"""
        if self.view:
            return self.view
            
        # 调用主窗口的工厂方法创建真视图
        self.view = self.parent_window._get_view_instance(self.key)
        self.layout.addWidget(self.view)
        return self.view


class MainWindow(FluentWindow):
    """主窗口"""

    def __init__(self, app=None):
        """初始化主窗口"""
        super().__init__()
        self.app = app
        service_bus.main_window = self

        # 已加载的真实视图实例缓存
        self._view_instances = {}
        # 容器映射，用于后台补全
        self._containers = {}

        # 1. 初始化窗口基础属性 (轻量)
        self._init_window()
        
        # 2. 初始化导航栏 (核心 V5：虚实分离)
        self._init_navigation()

        # 3. 信号绑定：当切换到某个容器时，确保其内容已加载
        self.stackedWidget.currentChanged.connect(self._on_stack_current_changed)

        # 4. 监听主题变更
        from src.common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _get_view_instance(self, name: str):
        """内部工厂方法：真正实例化业务视图"""
        if name in self._view_instances:
            return self._view_instances[name]
            
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
        self._view_instances[name] = view
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
        """初始化导航栏 (V5：同步注册所有容器，保证菜单完整；异步填充内容，保证动画顺滑)"""
        # 1. 确定首页
        startup_page_key = service_bus.config_service.get_startup_page() or "wizard"
        
        # 定义所有导航项配置
        nav_configs = {
            "wizard": (FluentIcon.ROBOT, "智能向导", NavigationItemPosition.TOP),
            "links": (FluentIcon.IOT, "我的链接", NavigationItemPosition.TOP),
            "library": (FluentIcon.BOOK_SHELF, "模版库", NavigationItemPosition.TOP),
            "help": (FluentIcon.INFO, "帮助", NavigationItemPosition.BOTTOM),
            "settings": (FluentIcon.SETTING, "设置", NavigationItemPosition.BOTTOM)
        }
        
        # 按照用户习惯的视觉顺序注册
        priority = ["wizard", "links", "library", "help", "settings"]
        
        for key in priority:
            icon, title, pos = nav_configs[key]
            # 创建轻量容器，不再一次性创建重型业务 View
            container = LazyViewContainer(key, self)
            self._containers[key] = container
            
            # 同步添加导航项，保证侧边栏在一瞬间就是全的
            self.addSubInterface(container, icon, title, position=pos)
            
            # 每添加一个容器都刷新一下，虽然容器很轻，但积少成多也要保证 UI 丝滑
            if self.app:
                self.app.processEvents()

        # 3. 首页容器立即加载
        home_container = self._containers[startup_page_key]
        home_container.load_view()
        self.switchTo(home_container)
        
        # 4. 启动静默后台补全
        QTimer.singleShot(600, self._background_load_views)

    def _on_stack_current_changed(self, index: int):
        """当堆栈窗口切换时，如果当前是占位容器，则触发加载"""
        widget = self.stackedWidget.widget(index)
        if isinstance(widget, LazyViewContainer):
            widget.load_view()

    def _on_nav_item_clicked(self, route_key):
        """点击菜单时的兜底加载"""
        # 寻找对应的容器，确保在用户切换到该页面时内容已加载
        for key, container in self._containers.items():
            if container.objectName() == route_key:
                container.load_view()
                break

    def _background_load_views(self):
        """主界面显示后，在后台悄悄把剩下的容器填满"""
        priority = ["wizard", "links", "library", "help", "settings"]
        startup_page_key = service_bus.config_service.get_startup_page() or "wizard"
        
        for key in priority:
            if key == startup_page_key:
                continue
                
            container = self._containers.get(key)
            if container and not container.view:
                # 补全内容
                container.load_view()
                # 每屏加完都给主程序喘息机会
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
