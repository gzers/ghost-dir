"""
主窗口
使用 FluentWindow 实现云母/亚克力效果
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon
from ..views.console import ConsoleView
from ..views.settings import SettingView
from ...common.resource_loader import get_resource_path
from ...common.config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT


class MainWindow(FluentWindow):
    """主窗口"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("Ghost-Dir - 目录连接管理器")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(1200, 800)
        
        # 设置窗口图标
        icon_path = get_resource_path("assets/icon.ico")
        self.setWindowIcon(QIcon(str(icon_path)))
        
        # 初始化界面
        self._init_navigation()
        self._init_window_effect()
    
    def _init_navigation(self):
        """初始化导航栏"""
        # 创建视图
        self.console_view = ConsoleView(self)
        self.console_view.setObjectName("consoleView")
        
        self.setting_view = SettingView(self)
        self.setting_view.setObjectName("settingView")
        
        # 添加子界面到导航栏
        self.addSubInterface(
            self.console_view,
            FluentIcon.HOME,
            "主控制台",
            NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.setting_view,
            FluentIcon.SETTING,
            "设置",
            NavigationItemPosition.BOTTOM
        )
        
        # 设置默认界面
        self.stackedWidget.setCurrentWidget(self.console_view)
    
    def _init_window_effect(self):
        """初始化窗口特效（云母/亚克力）"""
        try:
            # FluentWindow 会自动根据系统版本启用 Mica 或 Acrylic
            # Windows 11: Mica
            # Windows 10: Acrylic
            # 其他: 纯色背景
            pass
        except Exception as e:
            print(f"窗口特效初始化失败: {e}")
