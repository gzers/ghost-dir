"""
主窗口
使用 FluentWindow 实现 Mica/Acrylic 效果
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon
from ..views.console import ConsoleView
from ..views.wizard import WizardView
from ..views.library import LibraryView
from ..views.help import HelpView
from ..views.settings import SettingView
from ...common.resource_loader import get_resource_path
from ...common.config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from ...utils.win_utils import is_transparency_enabled
from qfluentwidgets import isDarkTheme


class MainWindow(FluentWindow):
    """主窗口"""

    def __init__(self, user_manager=None):
        """初始化主窗口"""
        super().__init__()

        # 保存用户管理器引用
        self.user_manager = user_manager

        # 创建视图
        self.console_view = ConsoleView(self)
        self.wizard_view = WizardView(self)
        self.library_view = LibraryView(self)
        self.help_view = HelpView(self)
        self.setting_view = SettingView(self)

        self._init_window()
        self._init_navigation()

        # 监听主题变更，以更新优雅降级的背景色
        from ...common.signals import signal_bus
        signal_bus.theme_changed.connect(lambda _: self._init_window_effect())
    
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
        
        # 统一背景，使导航栏、侧栏面板、内容区透明
        # 注意：不设置 titleBar 的透明样式，避免覆盖按钮的主题颜色
        self.navigationInterface.setStyleSheet("background: transparent; border: none;")
        self.navigationInterface.panel.setStyleSheet("background: transparent; border: none;")
        self.stackedWidget.setStyleSheet("background: transparent;")
    
    def _init_navigation(self):
        """初始化导航栏"""
        # 设置 objectName
        self.console_view.setObjectName("consoleView")
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
        
        # 2. 我的连接
        self.addSubInterface(
            self.console_view,
            FluentIcon.HOME,
            "我的连接",
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
        startup_page = self.user_manager.get_startup_page() if self.user_manager else "wizard"
        page_map = {
            "wizard": self.wizard_view,
            "console": self.console_view,
            "library": self.library_view
        }
        self.switchTo(page_map.get(startup_page, self.wizard_view))

    def _init_window_effect(self):
        """初始化窗口特效（云母/亚克力/优雅降级）"""
        try:
            # 检查系统是否开启了透明效果（是个性化设置中的开关）
            if is_transparency_enabled():
                # 开启云母/亚克力效果
                self.setMicaEffectEnabled(True)
                # 只有开启了系统级透明，主窗体才设为透明以展示底色特显
                self.setStyleSheet("MainWindow { background: transparent; }")
            else:
                # 优雅降级：如果系统关闭了透明效果，禁用特效并使用主题实色背景
                # 否则会导致窗口呈现纯黑色（hall of mirrors 的另一种表现形式）
                self.setMicaEffectEnabled(False)
                
                # 根据当前主题选择背景色
                bg_color = "#202020" if isDarkTheme() else "#F3F3F3"
                self.setStyleSheet(f"MainWindow {{ background: {bg_color}; }}")
                
                # 针对台式机等可能关闭透明度的情况，确保窗口不使用 WA_TranslucentBackground
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        except Exception as e:
            print(f"窗口特效初始化失败: {e}")
