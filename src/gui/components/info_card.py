"""
信息卡片组件
用于显示路径、分类、大小等信息
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from qfluentwidgets import BodyLabel, CaptionLabel, FluentIcon
from ..styles import StyleManager, get_spacing, get_radius


class InfoCard(QWidget):
    """信息卡片组件"""
    
    clicked = Signal()  # 点击信号
    
    def __init__(
        self,
        icon: FluentIcon,
        label: str,
        content: str,
        clickable: bool = False,
        parent=None
    ):
        """
        初始化信息卡片
        
        Args:
            icon: 图标
            label: 标签文本
            content: 内容文本
            clickable: 是否可点击
            parent: 父组件
        """
        super().__init__(parent)
        self.icon = icon
        self.label_text = label
        self.content_text = content
        self.clickable = clickable
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            get_spacing("md"),
            get_spacing("sm"),
            get_spacing("md"),
            get_spacing("sm")
        )
        layout.setSpacing(get_spacing("md"))
        
        # 图标
        icon_label = QLabel()
        icon_label.setPixmap(self.icon.icon().pixmap(20, 20))
        layout.addWidget(icon_label)
        
        # 文本区域
        text_layout = QVBoxLayout()
        text_layout.setSpacing(get_spacing("xs"))
        
        # 标签
        label = CaptionLabel(self.label_text)
        label.setStyleSheet(f"color: {StyleManager.get_text_secondary()};")
        text_layout.addWidget(label)
        
        # 内容
        content = BodyLabel(self.content_text)
        content.setWordWrap(True)
        text_layout.addWidget(content)
        
        layout.addLayout(text_layout, 1)
        
        # 样式
        self._apply_style()
        
        # 可点击
        if self.clickable:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    
    def _apply_style(self):
        """应用样式"""
        bg = StyleManager.get_card_background()
        border = StyleManager.get_border_color()
        radius = get_radius("md")
        
        style = f"""
            InfoCard {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: {radius}px;
            }}
            InfoCard:hover {{
                background-color: {StyleManager.get_hover_background()};
            }}
        """
        self.setStyleSheet(style)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if self.clickable:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def update_content(self, content: str):
        """
        更新内容
        
        Args:
            content: 新内容
        """
        self.content_text = content
        # 找到内容标签并更新
        text_layout = self.layout().itemAt(1)
        if text_layout:
            content_label = text_layout.itemAt(1).widget()
            if content_label:
                content_label.setText(content)
