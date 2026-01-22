"""
页面视图基类
提供统一的页面布局、标题栏和主题处理
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import TitleLabel, ScrollArea, ExpandLayout
from ..styles import (
    apply_page_layout, apply_container_style, apply_page_style,
    get_spacing, get_text_disabled, apply_font_style
)
from ...common.signals import signal_bus


class BasePageView(QFrame):
    """
    页面视图基类

    特性:
    - 统一的页面布局规范
    - 标题栏（标题 + 可选右侧工具栏）
    - 可选的工具栏区域
    - 可选的滚动内容区域
    - 支持在滚动区域外添加固定内容
    - 支持 ExpandLayout（用于设置页面）
    - 自动主题样式处理
    """

    # 主题变更信号
    theme_changed = Signal(str)

    def __init__(
        self,
        parent=None,
        title: str = "",
        show_toolbar: bool = False,
        enable_scroll: bool = True,
        use_expand_layout: bool = False,
        content_padding: bool = True
    ):
        """
        初始化页面视图基类

        Args:
            parent: 父组件
            title: 页面标题
            show_toolbar: 是否显示工具栏区域
            enable_scroll: 是否启用滚动区域
            use_expand_layout: 是否使用 ExpandLayout（用于设置页面）
            content_padding: 是否启用默认的内容区域内边距
        """
        super().__init__(parent)
        # 确保 QFrame 不绘制默认边框，但绘制背景
        self.setFrameShape(QFrame.NoFrame)

        self._title_text = title
        self._show_toolbar = show_toolbar
        self._enable_scroll = enable_scroll
        self._use_expand_layout = use_expand_layout
        self._content_padding = content_padding

        # 标题栏引用
        self._title_label = None
        self._title_layout = None
        self._right_toolbar = None

        # 工具栏引用
        self._toolbar_widget = None
        self._toolbar_layout = None

        # 主布局引用（用于在滚动区域外添加固定内容）
        self._main_layout = None

        # 滚动区域引用
        self._scroll_area = None
        self._content_container = None
        self._content_layout = None

        # 初始化 UI
        self._init_ui()

        # 连接主题信号
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._main_layout = layout

        # 标题栏
        if not self._use_expand_layout:
            self._init_title_bar(layout)

        # 工具栏（可选）
        if self._show_toolbar:
            self._init_toolbar(layout)

        # 内容区域
        self._init_content_area(layout)

        # 在主布局底部添加弹簧，确保所有内容靠顶对齐
        layout.addStretch(1)

        # 应用页面背景样式
        apply_page_style(self)

    def _init_title_bar(self, parent_layout: QVBoxLayout):
        """
        初始化标题栏

        Args:
            parent_layout: 父布局
        """
        # 创建标题容器以更好地控制布局
        title_container = QWidget()
        from PySide6.QtWidgets import QSizePolicy
        title_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        title_container.setStyleSheet("background: transparent;")
        
        self._title_layout = QHBoxLayout(title_container)
        # 使用统一布局规范 (与 ExpandLayout 统一)
        self._title_layout.setContentsMargins(36, 36, 36, 12)
        self._title_layout.setSpacing(get_spacing("lg"))

        # 标题
        if self._title_text:
            self._title_label = TitleLabel(self._title_text)
            self._title_layout.addWidget(self._title_label, 0, Qt.AlignmentFlag.AlignTop)

        # 右侧工具栏占位
        self._title_layout.addStretch()
        self._right_toolbar = QWidget()
        self._right_toolbar.setObjectName("right_toolbar")
        right_toolbar_layout = QHBoxLayout(self._right_toolbar)
        right_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        right_toolbar_layout.setSpacing(get_spacing("sm"))
        self._title_layout.addWidget(self._right_toolbar, 0, Qt.AlignmentFlag.AlignTop)
        self._right_toolbar.hide()  # 默认隐藏

        parent_layout.addWidget(title_container)

    def _init_toolbar(self, parent_layout: QVBoxLayout):
        """
        初始化工具栏区域

        Args:
            parent_layout: 父布局
        """
        self._toolbar_widget = QWidget()
        self._toolbar_widget.setStyleSheet("background: transparent;")
        self._toolbar_layout = QHBoxLayout(self._toolbar_widget)
        self._toolbar_layout.setContentsMargins(36, 12, 36, 12)
        self._toolbar_layout.setSpacing(get_spacing("md"))

        parent_layout.addWidget(self._toolbar_widget)

    def _init_content_area(self, parent_layout: QVBoxLayout):
        """
        初始化内容区域

        Args:
            parent_layout: 父布局
        """
        if self._enable_scroll:
            # 滚动区域
            self._scroll_area = ScrollArea()
            self._scroll_area.setWidgetResizable(True)
            self._scroll_area.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )

            # 设置滚动区域背景透明
            self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)
            self._scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

            # 容器 - 使用 QFrame 确保样式渲染
            self._content_container = QFrame()
            self._content_container.setFrameShape(QFrame.NoFrame)

            # 根据布局类型选择
            if self._use_expand_layout:
                self._content_layout = ExpandLayout(self._content_container)
                # 显式应用统一边距，防止 ExpandLayout 使用默认的小边距
                if self._content_padding:
                    self._content_layout.setContentsMargins(36, 12, 36, 36)
            else:
                self._content_layout = QVBoxLayout(self._content_container)
                
                # 设置间距
                from ..styles.utils import spacing_utils
                spacing_val = spacing_utils.get_list_spacing().get("group", 20)
                self._content_layout.setSpacing(spacing_val)
                
                # 应用内边距 (统一为 36, 12, 36, 36)
                if self._content_padding:
                    self._content_layout.setContentsMargins(36, 12, 36, 36)
                else:
                    self._content_layout.setContentsMargins(0, 0, 0, 0)
                    
                self._content_layout.addStretch()

            self._scroll_area.setWidget(self._content_container)
            parent_layout.addWidget(self._scroll_area, 10)

            # 应用容器背景样式
            self._update_container_style()
        else:
            # 非滚动区域
            if self._use_expand_layout:
                self._content_layout = ExpandLayout(self)
                # 显式应用统一边距
                if self._content_padding:
                    self._content_layout.setContentsMargins(36, 12, 36, 36)
            else:
                self._content_layout = QVBoxLayout()
                
                # 应用内边距 (统一为 36, 12, 36, 36)
                if self._content_padding:
                    self._content_layout.setContentsMargins(36, 12, 36, 36)
                else:
                    self._content_layout.setContentsMargins(0, 0, 0, 0)
                    
                self._content_layout.addStretch()
                parent_layout.addLayout(self._content_layout)

    def _update_container_style(self):
        """更新容器背景样式"""
        if self._content_container:
            # 统一使用容器样式（透明），背景色由 BasePageView 自身统一管理
            apply_container_style(self._content_container)

    def _on_theme_changed(self, theme: str):
        """
        主题变更处理

        Args:
            theme: 主题名称
        """
        apply_page_style(self)
        self._update_container_style()
        self.theme_changed.emit(theme)

    # ========== 公共 API ==========

    def get_title_label(self) -> TitleLabel:
        """
        获取标题标签

        Returns:
            标题标签组件
        """
        return self._title_label

    def set_title(self, title: str):
        """
        设置页面标题

        Args:
            title: 新标题
        """
        self._title_text = title
        if self._title_label:
            self._title_label.setText(title)

    def get_right_toolbar_layout(self) -> QHBoxLayout:
        """
        获取右侧工具栏布局

        用于在标题栏右侧添加控件

        Returns:
            右侧工具栏布局
        """
        self._right_toolbar.show()
        return self._right_toolbar.layout()

    def get_toolbar_layout(self) -> QHBoxLayout:
        """
        获取工具栏布局

        用于在工具栏区域添加控件

        Returns:
            工具栏布局，如果未启用则返回 None
        """
        if self._show_toolbar:
            return self._toolbar_layout
        return None

    def get_content_layout(self):
        """
        获取内容区域布局

        Returns:
            内容区域布局 (QVBoxLayout 或 ExpandLayout)
        """
        return self._content_layout

    def get_scroll_area(self) -> ScrollArea:
        """
        获取滚动区域

        Returns:
            滚动区域组件，如果未启用则返回 None
        """
        return self._scroll_area

    def get_content_container(self) -> QWidget:
        """
        获取内容容器

        Returns:
            内容容器组件
        """
        return self._content_container

    def add_to_content(self, widget: QWidget, before_stretch: bool = True):
        """
        添加控件到内容区域

        Args:
            widget: 要添加的控件
            before_stretch: 是否在 stretch 之前添加（仅 QVBoxLayout 有效）
        """
        if self._content_layout:
            if self._use_expand_layout:
                # ExpandLayout 直接添加
                self._content_layout.addWidget(widget)
            elif before_stretch:
                # 插入到 stretch 之前（对滚动和非滚动区域都生效）
                self._content_layout.insertWidget(
                    self._content_layout.count() - 1,
                    widget
                )
            else:
                self._content_layout.addWidget(widget)

    def add_fixed_content(self, widget: QWidget, before_scroll: bool = True, use_padding: bool = False, 
                          top_margin: int = 0, bottom_margin: int = 0, align_left: bool = False):
        """
        添加固定内容（在滚动区域外）

        适用于始终可见的控件，如扫描进度卡片、工具栏等

        Args:
            widget: 要添加的控件
            before_scroll: 是否在滚动区域之前添加（默认 True）
            use_padding: 是否应用页面标准水平内边距（默认 False）
            top_margin: 顶部边距（默认 0）
            bottom_margin: 底部边距（默认 0）
            align_left: 是否左对齐（默认 False，居中）
        """
        if not self._main_layout or not self._scroll_area:
            return

        target_widget = widget
        
        # 如果需要内边距或对齐，包裹一层容器
        if use_padding or align_left or top_margin > 0 or bottom_margin > 0:
            container = QWidget()
            from PySide6.QtWidgets import QSizePolicy
            container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
            
            # 使用垂直布局包裹，这样可以精确控制卡片的水平位置和外边距
            layout = QVBoxLayout(container)
            left_p = 36 if use_padding else 0
            right_p = 36 if use_padding else 0
            layout.setContentsMargins(left_p, top_margin, right_p, bottom_margin)
            layout.setSpacing(0)
            
            if align_left:
                layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            else:
                layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignTop)
                
            target_widget = container

        if before_scroll:
            # 插入到滚动区域之前
            index = self._main_layout.indexOf(self._scroll_area)
            if index == -1: # fallback
                index = self._main_layout.count() - 1 
            self._main_layout.insertWidget(index, target_widget)
        else:
            # 添加到滚动区域之后
            self._main_layout.addWidget(target_widget)

    def clear_content(self):
        """清空内容区域"""
        if self._content_layout:
            while self._content_layout.count() > 0:
                item = self._content_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    # 清理嵌套布局
                    while item.layout().count() > 0:
                        sub_item = item.layout().takeAt(0)
                        if sub_item.widget():
                            sub_item.widget().deleteLater()

    def show_empty_state(self, message: str = "暂无内容"):
        """
        显示空状态

        Args:
            message: 空状态提示文本
        """
        from qfluentwidgets import BodyLabel

        self.clear_content()

        empty_label = BodyLabel(message)
        apply_font_style(
            empty_label,
            size="md",
            color="disabled"
        )
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_to_content(empty_label, before_stretch=False)
