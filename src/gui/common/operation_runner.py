"""
异步操作辅助工具 (Operation Runner)
统一封装单体与批量异步任务的 UI 反馈与线程管理
"""
import typing
from PySide6.QtWidgets import QWidget
from qfluentwidgets import StateToolTip, InfoBar, InfoBarPosition
from src.gui.common.task_runner import SimpleTaskWorker, BatchTaskWorker
from src.gui.components.progress_dialog import ProgressDialog
from src.gui.i18n import t

# 全局运行器池，防止 Worker 被 GC 回收
_runners: typing.Dict[str, typing.Any] = {}

def run_task_async(
    func: typing.Callable,
    *args,
    title: str = "正在处理...",
    parent: QWidget = None,
    on_finished: typing.Callable[[bool, str, typing.Any], None] = None,
    **kwargs
):
    """
    运行单体异步任务并提供反馈
    
    Args:
        func: 要执行的函数
        *args: 函数参数
        title: 初始提示标题
        parent: 父窗口（用于定位 ToolTip）
        on_finished: 完成后的回调 (success, msg, data)
    """
    tooltip = StateToolTip(title, "请稍候...", parent)
    tooltip.show()
    
    worker = SimpleTaskWorker(func, *args, **kwargs)
    
    def _on_done(success: bool, msg: str, data: typing.Any):
        tooltip.setContent(msg + (" ✓" if success else " ✗"))
        tooltip.setState(success)
        
        if on_finished:
            on_finished(success, msg, data)
            
        # 延迟清理引用
        task_id = f"task_{id(worker)}"
        _runners.pop(task_id, None)

    worker.signals.finished.connect(_on_done)
    
    # 保持强引用
    task_id = f"task_{id(worker)}"
    _runners[task_id] = worker
    worker.start()

def run_batch_task_async(
    items: list,
    func: typing.Callable,
    title: str,
    item_title_func: typing.Callable = None,
    parent: QWidget = None,
    on_finished: typing.Callable[[bool, str, typing.Any], None] = None
):
    """
    运行批量异步任务并提供进度条反馈
    
    Args:
        items: 项目列表
        func: 针对每个项目执行的函数
        title: 对话框标题
        item_title_func: 获取单个项目标题的函数
        parent: 父窗口
        on_finished: 全体完成后的回调
    """
    dlg = ProgressDialog(title, "正在准备...", parent.window() if parent else None)
    dlg.show()
    
    worker = BatchTaskWorker(items, func, item_title_func)
    
    def on_progress(p, text):
        dlg.setProgress(p)
        dlg.setDescription(text)
        
    def _on_done(success: bool, msg: str, data: typing.Any):
        dlg.close()
        if on_finished:
            on_finished(success, msg, data)
        else:
            # 默认反馈
            target = parent if parent else None
            InfoBar.success(t("common.success"), msg, parent=target)
            
        # 清理引用
        task_id = f"batch_{id(worker)}"
        _runners.pop(task_id, None)

    worker.signals.progress.connect(on_progress)
    worker.signals.finished.connect(_on_done)
    
    # 手动取消绑定
    dlg.cancelButton.clicked.connect(worker.cancel)
    
    # 保持强引用
    task_id = f"batch_{id(worker)}"
    _runners[task_id] = worker
    worker.start()
