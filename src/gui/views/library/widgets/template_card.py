"""
模版卡片组件
显示单个模版的详细信息
"""
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import BodyLabel, ImageLabel
from src.gui.components import Card
from src.gui.styles import (
    apply_font_style, apply_muted_text_style, apply_badge_style,
    get_spacing, get_radius, get_icon_size, get_icon_background
)
from src.gui.i18n import get_category_text


class TemplateCard(Card):
    """模版卡片组件"""

    # 信号定义
    clicked = Signal(str)  # template_id

    def __init__(self, template, is_custom=False, parent=None):
        super().__init__(parent)
        self.template = template
        self.is_custom = is_custom
        self._init_ui()
        # 初次应用内部样式
        self._refresh_content_styles()

    def _init_ui(self):
        """初始化 UI"""
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)

        # 头部：图标和名称
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        # 图标处理
        self._setup_icon(header_layout)

        # 名称和类型布局
        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)

        # 名称标签
        self.name_label = BodyLabel(self.template.name)
        self.name_label.setWordWrap(True)
        name_layout.addWidget(self.name_label)

        # 类型徽章
        self.type_label = BodyLabel()
        self.type_label.setText("🎨 自定义" if self.is_custom else "⭐ 官方")
        name_layout.addWidget(self.type_label)

        header_layout.addLayout(name_layout, stretch=1)
        self.main_layout.addLayout(header_layout)

        # 分类
        cat_display = get_category_text(self.template.category_id)
        self.category_label = BodyLabel(cat_display)
        self.main_layout.addWidget(self.category_label)

        # 路径
        self.path_label = BodyLabel(self.template.default_src)
        self.path_label.setWordWrap(True)
        self.main_layout.addWidget(self.path_label)

        self.main_layout.addStretch()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_icon(self, layout):
        """设置图标区域"""
        icon_size = 48
        
        # 尝试加载图片图标
        if self.template.icon:
            try:
                from PySide6.QtGui import QPixmap
                pixmap = QPixmap(self.template.icon)
                if not pixmap.isNull():
                    img_label = ImageLabel()
                    img_label.setFixedSize(icon_size, icon_size)
                    img_label.setImage(self.template.icon)
                    layout.addWidget(img_label)
                    layout.addSpacing(8)
                    return
            except:
                pass

        # 降级使用 emoji 图标
        emoji = "🎨" if self.is_custom else "📦"
        icon_label = BodyLabel(emoji)
        icon_label.setFixedSize(icon_size, icon_size)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        layout.addSpacing(8)

    def _refresh_content_styles(self):
        """刷新内部组件的文字与徽章样式"""
        # 标题
        apply_font_style(self.name_label, size="md", weight="semibold")
        
        # 徽章样式
        status = "warning" if self.is_custom else "connected"
        apply_badge_style(self.type_label, status=status)
        
        # 分类与路径
        apply_muted_text_style(self.category_label, size="sm")
        apply_font_style(self.path_label, size="xs", color="disabled")

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super().mousePressEvent(event)
        self.clicked.emit(self.template.id)

    def get_template(self):
        """获取关联的模版"""
        return self.template

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super().mousePressEvent(event)
        self.clicked.emit(self.template.id)

    def get_template(self):
        """获取关联的模版"""
        return self.template
