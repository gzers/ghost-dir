"""
智能扫描向导对话框
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QThread
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, BodyLabel, 
    PushButton, ProgressBar, CheckBox, ScrollArea
)
from ...core.scanner import SmartScanner
from ...data.template_manager import TemplateManager
from ...data.user_manager import UserManager


class ScanWorker(QThread):
    """扫描工作线程"""
    progress = Signal(int, int)  # current, total
    finished = Signal(list)  # discovered templates
    
    def __init__(self, scanner: SmartScanner):
        super().__init__()
        self.scanner = scanner
    
    def run(self):
        """执行扫描"""
        discovered = self.scanner.scan()
        self.finished.emit(discovered)


class ScanWizardDialog(MessageBoxBase):
    """智能扫描向导对话框"""
    
    scan_completed = Signal(int)  # imported count
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.template_manager = TemplateManager()
        self.user_manager = UserManager()
        self.scanner = SmartScanner(self.template_manager, self.user_manager)
        
        self.discovered = []
        self.checkboxes = {}
        
        self.setWindowTitle("智能扫描向导")
        self._init_ui()
        
        # 自动开始扫描
        self.start_scan()
    
    def _init_ui(self):
        """初始化 UI"""
        # 标题
        self.titleLabel = SubtitleLabel("正在扫描本机应用...")
        
        # 进度条
        self.progressBar = ProgressBar()
        self.progressBar.setRange(0, 0)  # 不确定进度
        
        # 状态标签
        self.statusLabel = BodyLabel("正在扫描 C 盘，查找可管理的软件...")
        
        # 结果区域（初始隐藏）
        self.resultWidget = QWidget()
        self.resultLayout = QVBoxLayout(self.resultWidget)
        self.resultLayout.setContentsMargins(0, 0, 0, 0)
        
        self.resultTitle = SubtitleLabel("发现以下软件：")
        self.resultLayout.addWidget(self.resultTitle)
        
        # 滚动区域
        self.scrollArea = ScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumHeight(300)
        
        self.checkboxContainer = QWidget()
        self.checkboxLayout = QVBoxLayout(self.checkboxContainer)
        self.checkboxLayout.setContentsMargins(10, 10, 10, 10)
        self.checkboxLayout.setSpacing(8)
        
        self.scrollArea.setWidget(self.checkboxContainer)
        self.resultLayout.addWidget(self.scrollArea)
        
        self.resultWidget.hide()
        
        # 添加到视图
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progressBar)
        self.viewLayout.addWidget(self.statusLabel)
        self.viewLayout.addWidget(self.resultWidget)
        
        # 按钮
        self.yesButton.setText("导入选中项")
        self.yesButton.setEnabled(False)
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(500)
    
    def start_scan(self):
        """开始扫描"""
        self.worker = ScanWorker(self.scanner)
        self.worker.finished.connect(self._on_scan_finished)
        self.worker.start()
    
    def _on_scan_finished(self, discovered):
        """扫描完成"""
        self.discovered = discovered
        
        # 更新 UI
        self.titleLabel.setText(f"扫描完成！发现 {len(discovered)} 个软件")
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(100)
        self.statusLabel.setText(f"共发现 {len(discovered)} 个可管理的软件")
        
        if discovered:
            # 显示结果
            self.resultWidget.show()
            
            # 创建复选框
            for template in discovered:
                checkbox = CheckBox(f"{template.name} ({template.category})")
                checkbox.setChecked(True)
                self.checkboxes[template.id] = checkbox
                self.checkboxLayout.addWidget(checkbox)
            
            self.yesButton.setEnabled(True)
        else:
            self.statusLabel.setText("未发现可管理的软件")
    
    def validate(self):
        """验证并导入"""
        # 获取选中的模版
        selected = []
        for template in self.discovered:
            if self.checkboxes[template.id].isChecked():
                selected.append(template)
        
        if not selected:
            return False
        
        # 导入
        count = self.scanner.import_templates(selected)
        self.scan_completed.emit(count)
        
        return True
