"""
主窗口
使用 FluentWindow 实现 Mica/Acrylic 效果
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
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
from src.utils.win_utils import is_transparency_enabled
from src.gui.styles import window_style_sheet


class MainWindow(FluentWindow):
    """主窗口"""

    def __init__(self, app=None):
        """初始化主窗口
        
        Args:
            app: GhostDirApp 实例,提供 Service 层访问
        """
        super().__init__()
        
        # 保存 app 引用以访问新的 Service 层
        self.app = app

        # TODO: 暂时保留旧的 service_bus,逐步迁移
        self.user_manager = service_bus.user_manager

        # 创建视图 (构造函数已适配注入模式)
        self.links_view = LinksView(self)
        self.wizard_view = WizardView(self)
        self.library_view = LibraryView(self)
        self.help_view = HelpView(self)
        self.setting_view = SettingView(self)

        self._init_window()
        self._init_navigation()

        # 监听主题变更
        from src.common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)
    
    def _init_window(self):
        """初始化窗口"""
        self.setWindowTitle("Ghost-Dir")
        self.resize(1200, 800)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # 设置图标
        try:
            icon_path = get_resource_path("assets/icon.png")
            self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"加载图标失败: {e}")

        # 初始化窗口特效与降级处理
        self._init_window_effect()

    def _init_navigation(self):
        """初始化导航栏"""
        # 设置 objectName
        self.links_view.setObjectName("linksView")
        self.wizard_view.setObjectName("wizardView")
        self.library_view.setObjectName("libraryView")
        self.help_view.setObjectName("helpView")
        self.setting_view.setObjectName("settingView")
        
        # 顶部业务区
        # 1. 智能向导（第一位）
        self.addSubInterface(
            self.wizard_view,
            FluentIcon.ROBOT,
            "智能向导",
            position=NavigationItemPosition.TOP
        )
        
        # 2. 我的链接
        self.addSubInterface(
            self.links_view,
            FluentIcon.IOT,
            "我的链接",
            position=NavigationItemPosition.TOP
        )
        
        # 3. 模版库
        self.addSubInterface(
            self.library_view,
            FluentIcon.BOOK_SHELF,
            "模版库",
            position=NavigationItemPosition.TOP
        )
        
        # 底部功能区
        self.addSubInterface(
            self.help_view,
            FluentIcon.INFO,
            "帮助",
            position=NavigationItemPosition.BOTTOM
        )
        
        self.addSubInterface(
            self.setting_view,
            FluentIcon.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM
        )

        # 设置默认启动页面
        startup_page = service_bus.config_service.get_startup_page()
        page_map = {
            "wizard": self.wizard_view,
            "links": self.links_view,
            "library": self.library_view
        }
        self.switchTo(page_map.get(startup_page, self.wizard_view))

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
