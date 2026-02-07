"""
通用任务运行器 (Generic Task Runner)
提供标准化的异步执行接口与信号反馈
"""
import traceback
from typing import Callable, Any, List
from PySide6.QtCore import QThread, Signal, QObject


class TaskSignal(QObject):
    """任务信号定义"""
    started = Signal()
    progress = Signal(int, str)  # (百分比, 状态文本)
    finished = Signal(bool, str, object)  # (是否成功, 消息, 返回值)


class SimpleTaskWorker(QThread):
    """简单任务工作线程"""

    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignal()

    def run(self):
        """执行后台逻辑"""
        self.signals.started.emit()
        try:
            # 执行物理逻辑
            res = self.func(*self.args, **self.kwargs)

            # 协议约定：返回 Tuple[bool, str] 或单纯的 bool
            if isinstance(res, tuple):
                success, msg = res[0], res[1]
                data = res[2] if len(res) > 2 else None
            else:
                success, msg, data = res, "操作完成", None

            self.signals.finished.emit(success, msg, data)
        except Exception as e:
            msg = f"操作异常: {str(e)}"
            traceback.print_exc()
            self.signals.finished.emit(False, msg, None)


class BatchTaskWorker(QThread):
    """批量任务工作线程"""

    def __init__(self, items: List[Any], func: Callable, title_func: Callable = None):
        super().__init__()
        self.items = items
        self.func = func # 处理单项的方法
        self.title_func = title_func # 生成单项标题的方法
        self.signals = TaskSignal()
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        self.signals.started.emit()
        success_count = 0
        fail_count = 0
        total = len(self.items)

        for i, item in enumerate(self.items):
            if self._is_cancelled:
                break

            title = self.title_func(item) if self.title_func else f"正在处理第 {i+1} 项"
            progress_pct = int((i / total) * 100)
            self.signals.progress.emit(progress_pct, title)

            try:
                res = self.func(item)
                if isinstance(res, tuple):
                    if res[0]: success_count += 1
                    else: fail_count += 1
                elif res:
                    success_count += 1
                else:
                    fail_count += 1
            except:
                fail_count += 1

        final_msg = f"任务结束。成功: {success_count}, 失败: {fail_count}"
        self.signals.finished.emit(True, final_msg, (success_count, fail_count))
