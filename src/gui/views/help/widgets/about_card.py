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
    apply_font_style, get_spacing, apply_badge_style, get_radius,
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
        # 初始化应用一次所有子组件样式
        self.update_style()
    
    def update_style(self, theme=None):
        """更新卡片及其子组件样式"""
        # 1. 更新卡片本体样式 (亚克力背景、跨度等)
        super().update_style(theme)
        
        # 2. 如果 UI 已创建，更新各个子板块的样式
        if hasattr(self, 'main_layout'):
            self._update_all_labels()

    def _init_ui(self):
        """初始化 UI"""
        # 选取预设的内容容器宽度级别
        self.setFixedWidth(get_content_width("narrow")) # 560px
        
        # 主布局 - 纵向排列
        self.main_layout = QVBoxLayout(self)
        # 选取预设的卡片布局边距规范
        apply_layout_margins(self.main_layout, preset="card")
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # ========== Header 区（顶部信息）==========
        self._init_header(self.main_layout)
        
        # Header 与 Body 间距
        self.main_layout.addSpacing(get_spacing("xl"))
        
        # ========== Body 区（正文说明）==========
        self._init_body(self.main_layout)
        
        # Body 与 Footer 间距
        self.main_layout.addSpacing(get_spacing("xl"))
        
        # ========== Footer 区（底部信息与链接）==========
        self._init_footer(self.main_layout)

    def _update_all_labels(self):
        """更新所有内部标签的样式（用于适配主题）"""
        # 由于子组件较多，在各自的创建方法中其实已经引用了实时颜色
        # 只要在主题变更时重新触发这些控件的 apply_font_style 即可
        # 实际上可以通过递归重绘或在 update_style 中重新调用初始化里的样式逻辑
        # 为了高效，我们在这里手动更新关键部分
        self._refresh_header_styles()
        self._refresh_body_styles()
        self._refresh_footer_styles()
    
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
        self.title_label = StrongBodyLabel(t("app.name"))
        info_layout.addWidget(self.title_label)
        
        # 版本号和副标题的水平布局
        version_subtitle_layout = QHBoxLayout()
        version_subtitle_layout.setSpacing(get_spacing("md"))
        
        # 版本号徽章
        self.version_badge = VersionBadge(t("app.version"))
        version_subtitle_layout.addWidget(self.version_badge, 0, Qt.AlignmentFlag.AlignVCenter)
        
        # 副标题
        self.subtitle_label = CaptionLabel(t("app.subtitle"))
        version_subtitle_layout.addWidget(self.subtitle_label, 0, Qt.AlignmentFlag.AlignVCenter)
        version_subtitle_layout.addStretch()
        
        info_layout.addLayout(version_subtitle_layout)
        
        header_layout.addLayout(info_layout, 1)
        parent_layout.addLayout(header_layout)

    def _refresh_header_styles(self):
        """刷新头部样式"""
        if hasattr(self, 'title_label'):
            apply_font_style(self.title_label, size="xl", weight="semibold")
        if hasattr(self, 'subtitle_label'):
            apply_font_style(self.subtitle_label, size="sm", color="secondary")
        # 版本号徽章内部也有 QWidget，它也是通过 QSS 设置的，也会在 StyleManager 驱动下更新
    
    def _init_body(self, parent_layout: QVBoxLayout):
        """初始化 Body 区"""
        body_layout = QVBoxLayout()
        body_layout.setSpacing(get_spacing("md"))
        
        # 描述段落
        self.desc_labels = [
            BodyLabel(t("app.description_line1")),
            BodyLabel(t("app.description_line2")),
            BodyLabel(t("app.description_line3"))
        ]
        
        for label in self.desc_labels:
            label.setWordWrap(True)
            body_layout.addWidget(label)
        
        parent_layout.addLayout(body_layout)

    def _refresh_body_styles(self):
        """刷新正文样式"""
        if hasattr(self, 'desc_labels'):
            for label in self.desc_labels:
                apply_font_style(label, size="md")
    
    def _init_footer(self, parent_layout: QVBoxLayout):
        """初始化 Footer 区"""
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(get_spacing("lg"))
        
        # 作者信息
        self.author_label = CaptionLabel(f"作者：{t('app.author')}")
        footer_layout.addWidget(self.author_label)
        
        # GitHub 链接按钮
        github_layout = QHBoxLayout()
        self.github_btn = HyperlinkButton(
            t("app.github_url"),
            t("app.github"),
            self
        )
        github_layout.addWidget(self.github_btn)
        github_layout.addStretch()
        
        footer_layout.addLayout(github_layout)
        parent_layout.addLayout(footer_layout)

    def _refresh_footer_styles(self):
        """刷新底部样式"""
        if hasattr(self, 'author_label'):
            apply_font_style(self.author_label, size="sm", color="disabled")
        if hasattr(self, 'github_btn'):
            apply_font_style(self.github_btn, size="md")
    
    def _create_app_icon(self) -> QLabel:
        """创建应用图标"""
        try:
            icon_label = QLabel()
            icon_path = get_resource_path("assets/icon.png")
            pixmap = QPixmap(str(icon_path))
            
            if not pixmap.isNull():
                # 使用系统规范的尺寸与圆角
                size = 56 # 保持原设计尺寸，但可以考虑后续纳入 ICON_SIZES
                radius = get_radius("md")
                
                scaled_pixmap = pixmap.scaled(
                    size, size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setFixedSize(size, size)
                
                # 设置对象名称以便样式定位
                if not icon_label.objectName():
                    icon_label.setObjectName("app_icon")

                return icon_label
        except Exception as e:
            print(f"加载应用图标失败: {e}")
        
        return None
