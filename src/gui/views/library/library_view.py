"""
模版库视图
浏览所有官方和自定义模版
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
from PySide6.QtCore import Qt
from qfluentwidgets import (
    SubtitleLabel, SearchLineEdit, ComboBox, PushButton,
    ScrollArea, FluentIcon, InfoBar, InfoBarPosition
)
from ...i18n import t
from ....data.user_manager import UserManager
from ....data.template_manager import TemplateManager
from ....data.model import Template
from .widgets import TemplateCard


class LibraryView(QWidget):
    """模版库视图"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 初始化数据管理器
        self.template_manager = TemplateManager()
        self.user_manager = UserManager()

        # 模版数据
        self.all_templates = []
        self.filtered_templates = []
        self.template_cards = {}

        # 筛选状态
        self.current_category = "全部"

        # 初始化 UI
        self._init_ui()

        # 加载数据
        self._load_templates()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 设置页面背景为透明
        from ...styles import apply_page_style
        apply_page_style(self)

        # 标题
        title_layout = QHBoxLayout()
        from ...styles import apply_page_layout
        apply_page_layout(title_layout, spacing="section")
        title_layout.setContentsMargins(24, 24, 24, 8)  # 顶部 24px, 底部 8px 以贴合内容
        from qfluentwidgets import SubtitleLabel
        self.title_label = SubtitleLabel(t("library.title"))
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        # 统计信息
        self.count_label = PushButton()
        self.count_label.setEnabled(False)
        self.count_label.setStyleSheet("border: none; padding: 4px 12px;")
        title_layout.addWidget(self.count_label)

        layout.addLayout(title_layout)

        # 搜索和筛选栏
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(24, 10, 24, 10)
        filter_layout.setSpacing(12)

        # 搜索框
        self.search_edit = SearchLineEdit()
        self.search_edit.setPlaceholderText(t("library.search_placeholder"))
        self.search_edit.setFixedWidth(300)
        self.search_edit.textChanged.connect(self._on_search_changed)
        filter_layout.addWidget(self.search_edit)

        filter_layout.addStretch()

        # 分类筛选
        filter_layout.addWidget(PushButton("分类:"))
        self.category_combo = ComboBox()
        self.category_combo.addItems(["全部"])
        self.category_combo.setFixedWidth(150)
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        filter_layout.addWidget(self.category_combo)

        # 类型筛选
        filter_layout.addWidget(PushButton("类型:"))
        self.type_combo = ComboBox()
        self.type_combo.addItems(["全部", "官方", "自定义"])
        self.type_combo.setFixedWidth(120)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        filter_layout.addWidget(self.type_combo)

        layout.addLayout(filter_layout)

        # 模版网格区域
        self.scroll_area = ScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        apply_page_layout(self.grid_layout, spacing="section")  # 网格项间距 16px
        self.grid_layout.setContentsMargins(24, 12, 24, 24)  # 侧边 24px

        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        # 设置背景色（亮色主题下需要）
        self._update_theme_style()
        from ....common.signals import signal_bus
        signal_bus.theme_changed.connect(self._on_theme_changed)

    def _update_theme_style(self):
        """更新主题样式"""
        from ...styles import apply_container_style
        apply_container_style(self.scroll_widget)

    def _on_theme_changed(self, theme):
        """主题变更"""
        self._update_theme_style()

    def _load_templates(self):
        """加载所有模版"""
        # 获取所有模版（官方 + 自定义）
        all_templates = self.template_manager.get_all_templates()

        # 获取自定义模版 ID 集合
        custom_ids = set(t.id for t in self.user_manager.get_custom_templates())

        # 标记自定义模版
        self.all_templates = [
            (template, template.id in custom_ids)
            for template in all_templates
        ]

        # 更新分类列表
        categories = set(t.category for t, _ in self.all_templates)
        current_index = self.category_combo.currentIndex()
        self.category_combo.clear()
        self.category_combo.addItem("全部")
        for category in sorted(categories):
            self.category_combo.addItem(category)
        if 0 <= current_index < self.category_combo.count():
            self.category_combo.setCurrentIndex(current_index)

        # 应用筛选
        self._apply_filter()

    def _apply_filter(self):
        """应用搜索和筛选"""
        category_filter = self.category_combo.currentText()
        type_filter = self.type_combo.currentText()
        search_text = self.search_edit.text().lower()

        self.filtered_templates = [
            (template, is_custom)
            for template, is_custom in self.all_templates
            if (
                (category_filter == "全部" or template.category == category_filter)
                and (type_filter == "全部"
                     or (is_custom and type_filter == "自定义")
                     or (not is_custom and type_filter == "官方"))
                and search_text in template.name.lower()
            )
        ]

        # 更新显示
        self._update_template_display()

    def _update_template_display(self):
        """更新模版显示"""
        # 清空现有卡片
        for card in self.template_cards.values():
            card.deleteLater()
        self.template_cards.clear()

        # 创建新卡片
        if not self.filtered_templates:
            self._show_empty_state()
            self.count_label.setText("共 0 个模版")
            return

        row = 0
        col = 0
        columns = 3  # 每行 3 列

        for template, is_custom in self.filtered_templates:
            card = TemplateCard(template, is_custom)
            card.clicked.connect(self._on_card_clicked)

            self.grid_layout.addWidget(card, row, col)
            self.template_cards[template.id] = card

            col += 1
            if col >= columns:
                col = 0
                row += 1

        # 添加弹簧填充剩余空间
        if col > 0 or row > 0:
            self.grid_layout.setRowStretch(row, 1)

        # 更新统计
        self.count_label.setText(f"共 {len(self.filtered_templates)} 个模版")

    def _show_empty_state(self):
        """显示空状态"""
        from qfluentwidgets import BodyLabel

        empty_label = BodyLabel("没有找到匹配的模版")
        empty_label.setStyleSheet("color: #999; font-size: 14px;")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(empty_label, 0, 0)

    def _on_search_changed(self, text):
        """搜索文本改变"""
        self._apply_filter()

    def _on_category_changed(self, index):
        """分类改变"""
        self._apply_filter()

    def _on_type_changed(self, index):
        """类型改变"""
        self._apply_filter()

    def _on_card_clicked(self, template_id):
        """模版卡片点击"""
        card = self.template_cards[template_id]
        template = card.get_template()
        is_custom = card.is_custom

        # 显示模版详情（暂时用消息框）
        from qfluentwidgets import MessageBox

        info_text = f"""
        模版名称: {template.name}
        分类: {template.category}
        类型: {'自定义' if is_custom else '官方'}
        源路径: {template.default_src}
        """

        box = MessageBox("模版详情", info_text, self)
        box.yesButton.setText("确定")
        box.cancelButton.hide()
        box.exec()

    def refresh(self):
        """刷新模版列表"""
        self._load_templates()

        InfoBar.success(
            title="刷新成功",
            content="模版库已更新",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=2000
        )
