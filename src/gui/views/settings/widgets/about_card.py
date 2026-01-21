"""
关于信息卡片组件
"""
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from qfluentwidgets import CardWidget, TitleLabel, BodyLabel, HyperlinkButton
from .....common.config import APP_NAME, APP_VERSION
from .....common.resource_loader import get_resource_path


class AboutCard(CardWidget):
    """关于信息卡片"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # 应用图标和名称
        header_layout = QHBoxLayout()
        
        # 图标
        try:
            icon_label = QLabel()
            icon_path = get_resource_path("assets/icon.png")
            pixmap = QPixmap(str(icon_path))
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(
                    64, 64, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                ))
            header_layout.addWidget(icon_label)
        except:
            pass
        
        # 应用信息
        info_layout = QVBoxLayout()
        
        # 导入版本信息
        try:
            from ..... import __version__, __author__, __github_url__
        except:
            __version__ = APP_VERSION
            __author__ = "EZIO T"
            __github_url__ = "https://github.com/gzers/ghost-dir"
        
        app_title = TitleLabel(APP_NAME)
        version_label = BodyLabel(f"版本 {__version__}")
        version_label.setTextColor(Qt.GlobalColor.gray, Qt.GlobalColor.gray)
        
        info_layout.addWidget(app_title)
        info_layout.addWidget(version_label)
        info_layout.addStretch()
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # 描述
        desc_label = BodyLabel(
            "目录连接管理器 - 安全迁移 C 盘文件\n\n"
            "Ghost-Dir 是一款专为 Windows 设计的目录连接管理工具，"
            "帮助您轻松将 C 盘的大型软件数据迁移到其他磁盘，"
            "同时保持软件正常运行。采用事务安全机制，确保数据零丢失。"
        )
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 作者信息
        author_label = BodyLabel(f"作者：{__author__}")
        layout.addWidget(author_label)
        
        # 链接按钮
        button_layout = QHBoxLayout()
        
        github_btn = HyperlinkButton(
            __github_url__,
            "GitHub 仓库",
            self
        )
        button_layout.addWidget(github_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
