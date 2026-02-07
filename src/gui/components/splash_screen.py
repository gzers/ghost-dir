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
        
        # 4. 样式应用
        self.update_theme()
        
    def update_theme(self):
        """同步用户配置的主题，刷新背景和文字颜色"""
        from qfluentwidgets import isDarkTheme
        from PySide6.QtGui import QPalette, QColor
        
        is_dark = isDarkTheme()
        # 符合 Fluent 设计的底色 (不再使用 Alpha 以免导致渲染黑块)
        bg_color = QColor(32, 32, 32) if is_dark else QColor(243, 243, 243)
        text_color = "white" if is_dark else "black"
        
        # 1. 彻底解决背景问题：使用 QPalette + AutoFillBackground
        # 这是 Qt 中最稳健的背景色设置方式，不会干扰子控件绘制
        palette = self.palette()
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, QColor(text_color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # 2. 局部样式表：仅作用于根容器和 QLabel，保护 ProgressRing 不被干扰
        self.setStyleSheet(f"""
            AppSplashScreen {{
                background-color: {bg_color.name()};
                border: none;
            }}
            QLabel {{
                color: {text_color};
                background: transparent;
            }}
        """)
        
        # 3. 进度条颜色适配 (强制强调色，确保可见)
        if hasattr(self, 'progress_ring'):
            # 尝试获取主题主色，如果失败则使用显眼的蓝绿色
            from qfluentwidgets import themeColor
            self.progress_ring.setCustomBarColor(themeColor(), themeColor())
            self.progress_ring.raise_()
            self.progress_ring.show()

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

        self.v_layout.addSpacing(20)

        # 加载动画 (圆环进度条)
        self.progress_ring = IndeterminateProgressRing(self)
        self.progress_ring.setFixedSize(60, 60)
        self.progress_ring.setStrokeWidth(5) # 强化线条
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
