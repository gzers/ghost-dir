"""
空状态组件
用于列表为空时的友好提示
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import PushButton, BodyLabel, TitleLabel, FluentIcon
from src.gui.styles import StyleManager, get_spacing


class EmptyState(QWidget):
    """空状态组件"""
    
    action_clicked = Signal()  # 操作按钮点击信号
    
    def __init__(
        self,
        icon: FluentIcon = FluentIcon.FOLDER,
        title: str = "暂无数据",
        description: str = "",
        action_text: str = "",
        parent=None
    ):
        """
        初始化空状态组件
        
        Args:
            icon: 显示的图标
            title: 标题文本
            description: 描述文本
            action_text: 操作按钮文本(为空则不显示按钮)
            parent: 父组件
        """
        super().__init__(parent)
        self.icon = icon
        self.title_text = title
        self.desc_text = description
        self.action_text = action_text
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(get_spacing("lg"))
        
        # 图标
        icon_label = QLabel()
        icon_label.setPixmap(self.icon.icon().pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # 标题
        title_label = TitleLabel(self.title_text)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 描述
        if self.desc_text:
            desc_label = BodyLabel(self.desc_text)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet(f"color: {StyleManager.get_text_secondary()};")
            layout.addWidget(desc_label)
        
        # 操作按钮
        if self.action_text:
            action_btn = PushButton(self.action_text)
            action_btn.clicked.connect(self.action_clicked.emit)
            layout.addWidget(action_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 设置背景透明
        self.setStyleSheet("background: transparent;")
    
    def update_content(self, title: str = None, description: str = None, action_text: str = None):
        """
        更新内容
        
        Args:
            title: 新标题
            description: 新描述
            action_text: 新操作按钮文本
        """
        if title:
            self.title_text = title
        if description:
            self.desc_text = description
        if action_text:
            self.action_text = action_text
        
        # 清除旧布局
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 重新初始化
        self._init_ui()
