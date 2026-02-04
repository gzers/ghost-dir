"""
组件化启动界面
"""
from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from qfluentwidgets import (SplashScreen, TitleLabel, CaptionLabel, 
                            IndeterminateProgressRing, isDarkTheme)

from src.common.config import APP_VERSION, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from src.common.resource_loader import get_resource_path
from src.gui.i18n import t


class AppSplashScreen(SplashScreen):
    """Ghost-Dir 高级启动界面组件（支持主题跟随）"""

    def __init__(self, parent=None):
        # 不传图标给基类，彻底堵死基类的图标来源，解决图标重叠问题
        super().__init__(QIcon(), parent)
        
        # 1. 基础配置
        self.resize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # 2. 隐藏原生组件
        if hasattr(self, 'titleLabel'):
            self.titleLabel.hide()
        if hasattr(self, 'iconLabel'):
            self.iconLabel.hide()
            
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            
        # 3. 构建布局
        icon_path = get_resource_path("assets/icon.png")
        self.__init_layout(str(icon_path))

    def paintEvent(self, event):
        """自定义绘制事件，支持主题跟随的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 根据主题绘制背景色
        bg_color = QColor("#202020") if isDarkTheme() else QColor("#F3F3F3")
        painter.fillRect(self.rect(), bg_color)

    def drawContents(self, painter):
        """禁止渲染文字内容"""
        pass

    def __init_layout(self, icon_path):
        """初始化 UI 布局"""
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(0, 80, 0, 60)
        self.v_layout.setSpacing(20)
        self.v_layout.setAlignment(Qt.AlignCenter)

        # 应用图标
        self.icon_label = QLabel(self)
        pixmap = QPixmap(icon_path).scaled(192, 192, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(self.icon_label)

        # 软件大标题
        self.title_label = TitleLabel("Ghost-Dir", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(self.title_label)

        self.v_layout.addSpacing(10)

        # 加载动画 (圆环进度条)
        self.progress_ring = IndeterminateProgressRing(self)
        self.progress_ring.setFixedSize(48, 48)
        self.v_layout.addWidget(self.progress_ring, 0, Qt.AlignCenter)

        self.v_layout.addStretch(1)

        # 底部状态及版本 (使用国际化)
        self.status_label = CaptionLabel(t("app.splash_initializing"), self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(self.status_label)

        self.version_label = CaptionLabel(f"v{APP_VERSION}", self)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(self.version_label)

    def set_message(self, text: str):
        """
        更新进度消息
        
        Args:
            text: 提示文字
        """
        self.status_label.setText(text)
