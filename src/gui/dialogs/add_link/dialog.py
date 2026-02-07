"""
新增连接对话框
"""
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import MessageBoxBase, InfoBar
# TODO: 通过 app 实例访问 Service,而不是 service_bus
from src.common.service_bus import service_bus
from src.gui.dialogs.add_link.widgets import TemplateTabWidget, CustomTabWidget

class AddLinkDialog(MessageBoxBase):
    """新增连接对话框"""

    link_added = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.connection_service = service_bus.connection_service
        self.template_service = service_bus.template_service
        self.selected_template = None

        self.setWindowTitle("新增连接")
        self._init_ui()

    def _init_ui(self):
        """初始化 UI"""
        from PySide6.QtWidgets import QVBoxLayout, QStackedWidget
        from qfluentwidgets import SegmentedWidget

        # 创建主布局容器
        container = QVBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        container.setSpacing(12)

        # 创建分段导航栏（官方组件）
        self.pivot = SegmentedWidget()

        # 创建堆栈视图
        self.stackedWidget = QStackedWidget()

        # Tab 1: 从模版库选择
        self.templateTab = TemplateTabWidget(service_bus.template_manager, service_bus.user_manager)
        self.templateTab.template_selected_signal.connect(self._on_template_selected)
        self.templateTab.manage_categories_requested.connect(self._on_manage_categories)

        # Tab 2: 自定义
        self.customTab = CustomTabWidget(service_bus.user_manager)
        self.customTab.manage_categories_requested.connect(self._on_manage_categories)

        # 添加到堆栈和导航栏
        self.stackedWidget.addWidget(self.templateTab)
        self.stackedWidget.addWidget(self.customTab)
        self.pivot.addItem(routeKey='template', text='从模版库选择')
        self.pivot.addItem(routeKey='custom', text='自定义')

        # 连接导航切换信号
        self.pivot.currentItemChanged.connect(self._on_pivot_changed)
        self.pivot.setCurrentItem('template')

        # 添加到容器
        container.addWidget(self.pivot)
        container.addWidget(self.stackedWidget)

        # 创建包装器 widget
        from PySide6.QtWidgets import QWidget
        wrapper = QWidget()
        wrapper.setLayout(container)

        # 添加到视图
        self.viewLayout.addWidget(wrapper)

        # 按钮
        self.yesButton.setText("添加")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(600)
        self.widget.setMinimumHeight(500)

    def _on_pivot_changed(self, key):
        """导航切换回调"""
        index = 0 if key == 'template' else 1
        self.stackedWidget.setCurrentIndex(index)

    def _on_template_selected(self, template):
        """模版选中回调"""
        self.selected_template = template

    def _on_manage_categories(self):
        """打开分类管理对话框"""
        from src.gui.dialogs.category_manager import CategoryManagerDialog
        dialog = CategoryManagerDialog(self)
        dialog.categories_changed.connect(self._refresh_categories)
        dialog.exec()

    def _refresh_categories(self):
        """刷新分类列表"""
        self.templateTab.refresh_categories()
        self.customTab.refresh_categories()

    def validate(self):
        """验证并添加"""
        # 1. 提取数据
        if self.stackedWidget.currentIndex() == 0:  # 从模版添加
            data = {
                "name": self.templateTab.nameEdit.text(),
                "source": self.templateTab.sourceEdit.text(),
                "target": self.templateTab.targetEdit.text(),
                "category_id": self.templateTab.categorySelector.get_value()
            }
        else:  # 自定义添加
            data = {
                "name": self.customTab.customNameEdit.text(),
                "source": self.customTab.customSourceEdit.text(),
                "target": self.customTab.customTargetEdit.text(),
                "category_id": self.customTab.customCategorySelector.get_value()
            }

        # 2. 调用业务服务进行校验与添加
        success, msg = self.connection_service.validate_and_add_link(data, self.selected_template)

        if success:
            # 3. 处理后续业务：保存为模版
            if self.stackedWidget.currentIndex() == 1 and self.customTab.saveAsTemplateBtn.isChecked():
                self.template_service.add_template_from_data({
                    "name": data["name"],
                    "default_src": data["source"],
                    "category_id": data["category_id"]
                })

            self.link_added.emit()
            return True
        else:
            # 弹出业务错误提示
            InfoBar.warning(
                title="验证失败",
                content=msg,
                orient=Qt.Orientation.Horizontal,
                position='TopCenter',
                duration=3000,
                parent=self
            )

        return False
