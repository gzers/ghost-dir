"""
扫描工作线程
在后台执行扫描任务，避免阻塞 UI
"""
from PySide6.QtCore import Signal, QThread


class ScanWorker(QThread):
    """
    扫描工作线程

    在后台线程中执行扫描操作，通过信号通知主线程扫描进度和结果。
    """

    # 信号定义
    progress = Signal(int, int)  # current, total - 扫描进度
    finished = Signal(list)      # discovered templates - 扫描完成
    error = Signal(str)          # error message - 扫描错误

    def __init__(self, scanner):
        """
        初始化扫描工作线程

        Args:
            scanner: 扫描器实例，用于执行实际的扫描操作
        """
        super().__init__()
        self.scanner = scanner

    def run(self):
        """
        执行扫描任务

        在后台线程中运行，扫描完成后通过 finished 信号发送结果，
        如果发生错误则通过 error 信号发送错误信息。
        """
        try:
            discovered = self.scanner.scan()
            self.finished.emit(discovered)
        except Exception as e:
            self.error.emit(str(e))
