"""
状态徽章组件
显示连接状态的可视化指示器
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel
from src.models.link import LinkStatus  # 新架构: 使用 models 层
from src.gui.styles import (
    get_spacing, apply_badge_style, apply_icon_style,
    get_status_icon, get_status_colors, apply_font_style, apply_transparent_background_only
)
from src.gui.i18n import get_status_text


class StatusBadge(QWidget):
    """状态徽章组件"""

    def __init__(self, status, parent=None):
        """
        初始化状态徽章

        Args:
            status: 连接状态 (LinkStatus 枚举或其字符串值)
            parent: 父组件
        """
        super().__init__(parent)
        self.status = status
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        status_val = self.status.value if hasattr(self.status, 'value') else self.status
        
        # 0. 预加载样式配置
        status_colors = get_status_colors()
        icon_data = get_status_icon(status_val)
        status_text = get_status_text(status_val)
        
        # 应用标准徽章样式 (主要是容器级的 Padding 和边框)
        apply_badge_style(self, status=status_val)

        # 1. 布局构建
        if not self.layout():
            layout = QHBoxLayout(self)
            layout.setContentsMargins(6, 2, 8, 2) # 精调边距
            layout.setSpacing(6)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        else:
            layout = self.layout()
            # 清理旧组件 (如果存在)
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        # 2. 状态色球 (Icon)
        from qfluentwidgets import IconWidget, FluentIcon
        if isinstance(icon_data, str):
             self.icon_label = QLabel(icon_data, self)
             self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
             # 色球不需要 md 那么大，在中规中矩的 sm 级别最协调
             apply_icon_style(self.icon_label, size="sm")
             layout.addWidget(self.icon_label)
        else:
             # 兼容 QFluentWidgets 枚举图标
             self.icon_widget = IconWidget(icon_data, self)
             self.icon_widget.setFixedSize(14, 14)
             layout.addWidget(self.icon_widget)

        # 3. 状态文本
        self.text_label = BodyLabel(status_text, self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 固定使用 13px (标准 BodyLabel 略大，这里微调使之紧凑)
        self.text_label.setStyleSheet(f"font-size: 13px; color: {status_colors.get(status_val, '#808080')};")
        apply_transparent_background_only(self.text_label)
        layout.addWidget(self.text_label)

    def set_loading(self, is_loading: bool):
        """通用加载状态切换 (兼容旧接口并提升鲁棒性)"""
        # 徽章本身通常不负责转圈，转圈由父容器（如 LinkTable）叠加
        # 这里预留接口以防未来需要动态隐藏显示
        self.setVisible(not is_loading)

    def update_status(self, status: LinkStatus):
        """标准更新方法"""
        self.status = status
        self._init_ui()
        self.show()
