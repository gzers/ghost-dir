"""
批量操作工具栏组件
"""
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Signal
from qfluentwidgets import BodyLabel, PushButton, ToolButton, FluentIcon
from ....components import Card


class BatchToolbar(Card):
    """批量操作工具栏"""
    
    # 信号
    batch_establish_clicked = Signal()
    batch_disconnect_clicked = Signal()
    clear_selection_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        
        self.selected_label = BodyLabel("已选中 0 项")
        layout.addWidget(self.selected_label)
        layout.addStretch()
        
        self.batch_establish_btn = PushButton(FluentIcon.LINK, "批量建立连接")
        self.batch_establish_btn.clicked.connect(self.batch_establish_clicked.emit)
        
        self.batch_disconnect_btn = PushButton(FluentIcon.CANCEL, "批量断开连接")
        self.batch_disconnect_btn.clicked.connect(self.batch_disconnect_clicked.emit)
        
        self.clear_selection_btn = ToolButton(FluentIcon.CLOSE)
        self.clear_selection_btn.clicked.connect(self.clear_selection_clicked.emit)
        
        layout.addWidget(self.batch_establish_btn)
        layout.addWidget(self.batch_disconnect_btn)
        layout.addWidget(self.clear_selection_btn)
    
    def update_count(self, count: int):
        """更新选中数量"""
        self.selected_label.setText(f"已选中 {count} 项")
