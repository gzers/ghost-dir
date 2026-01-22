"""
关于信息卡片组件
采用专业的布局和统一的样式系统
"""
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from qfluentwidgets import (
    StrongBodyLabel, BodyLabel, CaptionLabel,
    HyperlinkButton
)
from ....i18n import t
from ....components import Card
from ....styles import (
    apply_font_style, get_spacing, apply_badge_style, 
    get_text_secondary, get_text_disabled,
    get_content_width, apply_layout_margins
)
from .....common.resource_loader import get_resource_path


class VersionBadge(QWidget):
    """版本号徽章组件"""
    
    def __init__(self, version: str, parent=None):
        super().__init__(parent)
        self._init_ui(version)
    
    def _init_ui(self, version: str):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        # 选取预设的徽章边距规范
        apply_layout_margins(layout, preset="badge")
        layout.setSpacing(0)
        
        # 版本号标签
        version_label = CaptionLabel(f"v{version}")
        apply_font_style(
            version_label,
            size="sm",
            color="secondary"
        )
        layout.addWidget(version_label)
        
        # 应用标准徽章样式
        apply_badge_style(self, status="invalid") 


class AboutCard(Card):
    """关于信息卡片"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        # 选取预设的内容容器宽度级别
        self.setFixedWidth(get_content_width("narrow")) # 560px
        
        # 主布局 - 纵向排列
        main_layout = QVBoxLayout(self)
        # 选取预设的卡片布局边距规范
        apply_layout_margins(main_layout, preset="card")
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # ========== Header 区（顶部信息）==========
        self._init_header(main_layout)
        
        # Header 与 Body 间距
        main_layout.addSpacing(get_spacing("xl"))
        
        # ========== Body 区（正文说明）==========
        self._init_body(main_layout)
        
        # Body 与 Footer 间距
        main_layout.addSpacing(get_spacing("xl"))
        
        # ========== Footer 区（底部信息与链接）==========
        self._init_footer(main_layout)
    
    def _init_header(self, parent_layout: QVBoxLayout):
        """初始化 Header 区"""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(get_spacing("lg"))
        
        # 左侧：应用图标
        icon_label = self._create_app_icon()
        if icon_label:
            header_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)
        
        # 右侧：标题与版本信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(get_spacing("xs"))
        
        # 应用标题
        title_label = StrongBodyLabel(t("app.name"))
        apply_font_style(
            title_label,
            size="xl",
            weight="semibold"
        )
        info_layout.addWidget(title_label)
        
        # 版本号和副标题的水平布局
        version_subtitle_layout = QHBoxLayout()
        version_subtitle_layout.setSpacing(get_spacing("md"))
        
        # 版本号徽章
        version_badge = VersionBadge(t("app.version"))
        version_subtitle_layout.addWidget(version_badge, 0, Qt.AlignmentFlag.AlignVCenter)
        
        # 副标题
        subtitle_label = CaptionLabel(t("app.subtitle"))
        apply_font_style(
            subtitle_label,
            size="sm",
            color="secondary"
        )
        version_subtitle_layout.addWidget(subtitle_label, 0, Qt.AlignmentFlag.AlignVCenter)
        version_subtitle_layout.addStretch()
        
        info_layout.addLayout(version_subtitle_layout)
        
        header_layout.addLayout(info_layout, 1)
        parent_layout.addLayout(header_layout)
    
    def _init_body(self, parent_layout: QVBoxLayout):
        """初始化 Body 区"""
        body_layout = QVBoxLayout()
        body_layout.setSpacing(get_spacing("md"))
        
        # 描述段落 1
        desc1 = BodyLabel(t("app.description_line1"))
        desc1.setWordWrap(True)
        apply_font_style(desc1, size="md")
        body_layout.addWidget(desc1)
        
        # 描述段落 2
        desc2 = BodyLabel(t("app.description_line2"))
        desc2.setWordWrap(True)
        apply_font_style(desc2, size="md")
        body_layout.addWidget(desc2)
        
        # 描述段落 3
        desc3 = BodyLabel(t("app.description_line3"))
        desc3.setWordWrap(True)
        apply_font_style(desc3, size="md")
        body_layout.addWidget(desc3)
        
        parent_layout.addLayout(body_layout)
    
    def _init_footer(self, parent_layout: QVBoxLayout):
        """初始化 Footer 区"""
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(get_spacing("lg"))
        
        # 作者信息
        author_label = CaptionLabel(f"作者：{t('app.author')}")
        apply_font_style(
            author_label,
            size="sm",
            color="disabled"
        )
        footer_layout.addWidget(author_label)
        
        # GitHub 链接按钮（不使用图标，避免颜色突兀）
        github_layout = QHBoxLayout()
        github_btn = HyperlinkButton(
            t("app.github_url"),
            t("app.github"),
            self
        )
        apply_font_style(github_btn, size="md")
        github_layout.addWidget(github_btn)
        github_layout.addStretch()
        
        footer_layout.addLayout(github_layout)
        parent_layout.addLayout(footer_layout)
    
    def _create_app_icon(self) -> QLabel:
        """创建应用图标"""
        try:
            icon_label = QLabel()
            icon_path = get_resource_path("assets/icon.png")
            pixmap = QPixmap(str(icon_path))
            
            if not pixmap.isNull():
                # 图标大小 56x56，圆角处理
                scaled_pixmap = pixmap.scaled(
                    56, 56,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setFixedSize(56, 56)
                
                # 添加圆角样式
                icon_label.setStyleSheet("""
                    QLabel {
                        border-radius: 8px;
                    }
                """)
                
                return icon_label
        except Exception as e:
            print(f"加载应用图标失败: {e}")
        
        return None
