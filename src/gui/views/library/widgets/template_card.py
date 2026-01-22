"""
模版卡片组件
显示单个模版的详细信息
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    CardWidget, BodyLabel, ToolTipFilter,
    ToolTipPosition, ImageLabel
)


class TemplateCard(CardWidget):
    """模版卡片组件"""

    # 信号定义
    clicked = Signal(str)  # template_id

    def __init__(self, template, is_custom=False, parent=None):
        super().__init__(parent)
        self.template = template
        self.is_custom = is_custom
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 头部：图标和名称
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        # 图标
        self.icon = BodyLabel()
        if self.template.icon:
            try:
                # 尝试加载图标
                from PySide6.QtGui import QPixmap
                pixmap = QPixmap(self.template.icon)
                if not pixmap.isNull():
                    icon_label = ImageLabel()
                    icon_label.setFixedSize(48, 48)
                    icon_label.setImage(self.template.icon)
                    header_layout.addWidget(icon_label)
                    header_layout.addSpacing(8)
            except:
                pass

        # 使用 emoji 作为默认图标
        if self.icon.text() == "":
            emoji = "📦" if not self.is_custom else "🎨"
            icon = BodyLabel()
            icon.setText(emoji)
            from ....styles import StyleManager
            icon.setStyleSheet(StyleManager.get_icon_style("lg"))
            icon.setFixedSize(48, 48)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(icon)
            header_layout.addSpacing(8)

        # 名称和类型
        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)

        from ....styles import apply_font_style
        self.name_label = BodyLabel(self.template.name)
        apply_font_style(self.name_label, size="md", weight="semibold")
        self.name_label.setWordWrap(True)
        name_layout.addWidget(self.name_label)

        # 类型标签 - 使用统一样式
        type_label = BodyLabel()
        from ....styles import StyleManager, get_font_style, get_radius, get_spacing
        if self.is_custom:
            type_label.setText("🎨 自定义")
            bg = "#FFF1F0"
            color = "#FF4D4F"
        else:
            type_label.setText("⭐ 官方")
            bg = "#E6F7FF"
            color = "#1890FF"

        type_label.setStyleSheet(
            f"background-color: {bg}; "
            f"color: {color}; "
            f"padding: 2px 8px; "
            f"border-radius: {get_radius('sm')}px; "
            f"{get_font_style(size='xs')}"
        )
        name_layout.addWidget(type_label)

        header_layout.addLayout(name_layout, stretch=1)

        layout.addLayout(header_layout)

        # 分类
        self.category_label = BodyLabel(f"分类: {self.template.category}")
        from ....styles import apply_muted_text_style
        apply_muted_text_style(self.category_label, size=14)
        layout.addWidget(self.category_label)

        # 路径 - 使用统一样式
        from ....styles import StyleManager, apply_font_style
        self.path_label = BodyLabel(self.template.default_src)
        apply_font_style(self.path_label, size="xs", color=StyleManager.get_text_disabled())
        self.path_label.setWordWrap(True)
        layout.addWidget(self.path_label)

        layout.addStretch()

        # 鼠标悬停效果
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super().mousePressEvent(event)
        self.clicked.emit(self.template.id)

    def get_template(self):
        """获取关联的模版"""
        return self.template
