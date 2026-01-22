"""
设置视图
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices, QPixmap
from qfluentwidgets import TitleLabel, StrongBodyLabel, BodyLabel, CardWidget, HyperlinkButton, PushButton
from ...common.config import APP_NAME, APP_VERSION
from ...common.resource_loader import get_resource_path


class SettingView(QWidget):
    """设置视图"""
    
    def __init__(self, parent=None):
        """初始化设置视图"""
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 标题
        title = TitleLabel("设置")
        layout.addWidget(title)
        
        # 关于卡片
        about_card = CardWidget()
        about_layout = QVBoxLayout(about_card)
        about_layout.setContentsMargins(20, 20, 20, 20)
        about_layout.setSpacing(12)
        
        # 应用图标和名称
        header_layout = QHBoxLayout()
        
        # 图标
        try:
            icon_label = QLabel()
            icon_path = get_resource_path("assets/icon.png")
            pixmap = QPixmap(str(icon_path))
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            header_layout.addWidget(icon_label)
        except:
            pass
        
        # 应用信息
        info_layout = QVBoxLayout()
        
        # 导入版本信息
        try:
            from ... import __version__, __author__, __github_url__
        except:
            __version__ = APP_VERSION
            __author__ = "EZIO T"
            __github_url__ = "https://github.com/gzers/ghost-dir"
        
        app_title = StrongBodyLabel(f"{APP_NAME}")
        version_label = BodyLabel(f"版本 {__version__}")
        version_label.setTextColor(Qt.GlobalColor.gray, Qt.GlobalColor.gray)
        
        info_layout.addWidget(app_title)
        info_layout.addWidget(version_label)
        info_layout.addStretch()
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        about_layout.addLayout(header_layout)
        
        # 描述
        desc_label = BodyLabel("目录连接管理器 - 安全迁移 C 盘文件\n\n"
                               "Ghost-Dir 是一款专为 Windows 设计的目录连接管理工具，"
                               "帮助您轻松将 C 盘的大型软件数据迁移到其他磁盘，"
                               "同时保持软件正常运行。采用事务安全机制，确保数据零丢失。")
        desc_label.setWordWrap(True)
        about_layout.addWidget(desc_label)
        
        # 作者信息
        author_label = BodyLabel(f"作者：{__author__}")
        about_layout.addWidget(author_label)
        
        # 链接按钮
        button_layout = QHBoxLayout()
        
        github_btn = HyperlinkButton(
            __github_url__,
            "GitHub 仓库",
            about_card
        )
        button_layout.addWidget(github_btn)
        
        button_layout.addStretch()
        
        about_layout.addLayout(button_layout)
        
        layout.addWidget(about_card)
        layout.addStretch()
