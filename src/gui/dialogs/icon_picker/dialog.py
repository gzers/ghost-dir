"""
图标选择器对话框
基于 MessageBoxBase 的自定义对话框，用于选择 FluentIcon
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QLabel
from PySide6.QtGui import QIcon
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, SearchLineEdit,
    PushButton, FluentIcon, TransparentToolButton
)


# FluentIcon 图标列表（常用图标）
FLUENT_ICONS = [
    "ADD", "FOLDER", "DOCUMENT", "EDIT", "DELETE", "SAVE", "CANCEL",
    "ACCEPT", "CLOSE", "SEARCH", "SETTING", "HOME", "DOWNLOAD", "UPLOAD",
    "SHARE", "COPY", "CUT", "PASTE", "UNDO", "REDO",
    "ZOOM_IN", "ZOOM_OUT", "REFRESH", "SYNC", "CLOUD",
    "CODE", "DEVELOPER", "GLOBE", "CHAT", "MESSAGE", "MAIL",
    "CALENDAR", "CLOCK", "ALARM", "TAG", "FLAG", "STAR",
    "HEART", "EMOJI", "PHOTO", "VIDEO", "MUSIC", "MICROPHONE",
    "GAME", "LIBRARY", "BOOK", "EDUCATION", "CERTIFICATE",
    "SHOPPING_CART", "MARKET", "CAFE", "FOOD", "DRINK",
    "BUS", "CAR", "AIRPLANE", "TRAIN", "BIKE",
    "PEOPLE", "CONTACT", "ROBOT", "IOT", "VPN",
    "WIFI", "BLUETOOTH", "USB", "POWER", "BATTERY",
    "BRIGHTNESS", "VOLUME", "MUTE", "PLAY", "PAUSE",
    "STOP", "PREVIOUS", "NEXT", "SHUFFLE", "REPEAT",
    "PIN", "UNPIN", "LOCK", "UNLOCK", "HIDE", "VIEW",
    "UP", "DOWN", "LEFT", "RIGHT", "BACK", "FORWARD",
    "CHEVRON_UP", "CHEVRON_DOWN", "CHEVRON_LEFT", "CHEVRON_RIGHT",
    "MORE", "MENU", "GRID", "LIST", "TILES"
]


class IconPickerDialog(MessageBoxBase):
    """图标选择器对话框"""

    icon_selected = Signal(str)  # 图标被选中时发出信号

    def __init__(self, current_icon: str = "Folder", parent=None):
        """
        初始化图标选择器

        Args:
            current_icon: 当前选中的图标名称
            parent: 父窗口
        """
        super().__init__(parent)
        self.selected_icon = current_icon
        self.icon_buttons = {}  # 存储所有图标容器

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel('选择图标', self)

        # 搜索框
        self.searchEdit = SearchLineEdit(self)
        self.searchEdit.setPlaceholderText('搜索图标...')
        self.searchEdit.setFixedWidth(400)

        # 图标网格容器
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setFixedHeight(450)  # 适中的高度，确保按钮可见

        self.iconContainer = QWidget()
        self.iconGrid = QGridLayout(self.iconContainer)
        self.iconGrid.setSpacing(8)
        self.iconGrid.setContentsMargins(10, 10, 10, 10)

        self._init_icon_grid()

        self.scrollArea.setWidget(self.iconContainer)

        # 添加到布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.searchEdit)
        self.viewLayout.addWidget(self.scrollArea)

        # 按钮文本
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        # 设置对话框大小
        self.widget.setMinimumWidth(600)

    def _init_icon_grid(self):
        """初始化图标网格"""
        row, col = 0, 0
        columns = 6  # 每行6个图标

        for icon_name in FLUENT_ICONS:
            try:
                # 获取 FluentIcon
                icon = getattr(FluentIcon, icon_name, None)
                if not icon:
                    continue

                # 创建图标容器
                container = self._create_icon_widget(icon_name, icon)
                self.icon_buttons[icon_name] = container

                # 添加到网格
                self.iconGrid.addWidget(container, row, col)

                col += 1
                if col >= columns:
                    col = 0
                    row += 1

            except Exception as e:
                print(f"加载图标 {icon_name} 失败: {e}")
                continue

    def _create_icon_widget(self, icon_name: str, icon) -> QWidget:
        """
        创建图标容器（包含按钮和标签）

        Args:
            icon_name: 图标名称
            icon: FluentIcon 对象

        Returns:
            包含按钮和标签的容器widget
        """
        # 创建容器
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # 创建按钮
        btn = TransparentToolButton(icon, container)
        btn.setFixedSize(56, 56)
        btn.setIconSize(QSize(28, 28))
        btn.setToolTip(icon_name)

        # 创建标签
        label = QLabel(icon_name, container)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 9px; color: gray;")
        label.setWordWrap(True)
        label.setFixedWidth(70)

        # 添加到布局
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # 存储按钮引用
        container.button = btn
        container.label = label
        container.icon_name = icon_name

        # 如果是当前选中的图标，高亮显示
        if icon_name == self.selected_icon:
            btn.setStyleSheet("""
                TransparentToolButton {
                    background-color: rgba(0, 120, 212, 0.1);
                    border: 2px solid rgb(0, 120, 212);
                    border-radius: 4px;
                }
            """)

        # 绑定点击事件
        btn.clicked.connect(lambda: self._on_icon_clicked(icon_name))

        return container

    def _on_icon_clicked(self, icon_name: str):
        """
        图标被点击

        Args:
            icon_name: 图标名称
        """
        # 清除之前选中的高亮
        if self.selected_icon in self.icon_buttons:
            old_container = self.icon_buttons[self.selected_icon]
            old_container.button.setStyleSheet("")

        # 设置新选中的高亮
        self.selected_icon = icon_name
        if icon_name in self.icon_buttons:
            container = self.icon_buttons[icon_name]
            container.button.setStyleSheet("""
                TransparentToolButton {
                    background-color: rgba(0, 120, 212, 0.1);
                    border: 2px solid rgb(0, 120, 212);
                    border-radius: 4px;
                }
            """)

        # 发出信号
        self.icon_selected.emit(icon_name)

    def _on_search_changed(self, text: str):
        """
        搜索文本改变

        Args:
            text: 搜索文本
        """
        text = text.lower()

        for icon_name, container in self.icon_buttons.items():
            # 如果搜索文本为空或图标名称包含搜索文本，显示容器
            if not text or text in icon_name.lower():
                container.setVisible(True)
            else:
                container.setVisible(False)

    def _connect_signals(self):
        """连接信号"""
        self.searchEdit.textChanged.connect(self._on_search_changed)

    def get_selected_icon(self) -> str:
        """
        获取选中的图标名称

        Returns:
            图标名称
        """
        return self.selected_icon
