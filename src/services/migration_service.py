# coding: utf-8
"""
数据迁移服务 - 负责跨目录的数据移动/复制
支持异步执行、进度反馈、取消操作以及基本的回滚能力
"""
import os
import shutil
import time
import logging
from typing import Callable, Optional
from PySide6.QtCore import QObject, Signal, QThread

# 设置日志
logger = logging.getLogger(__name__)

class MigrationWorker(QObject):
    """迁移工作执行器 - 运行在子线程中"""
    # 进度信号: (已迁移字节, 总字节, 当前文件名)
    progress_updated = Signal(int, int, str)
    # 完成信号: (是否成功, 错误信息)
    finished = Signal(bool, str)
    
    def __init__(self, source: str, target: str, mode: str = "copy"):
        super().__init__()
        self.source = source
        self.target = target
        self.mode = mode  # "copy" 或 "move"
        self.cleanup_source = False # 成功后是否清理原始 source 目录
        self.is_aborted = False
        self.total_size = 0
        self.processed_size = 0
        self.copied_paths = [] # 用于简单回滚

    def abort(self):
        """中止迁移"""
        self.is_aborted = True

    def calculate_total_size(self, path: str) -> int:
        """递归计算文件/文件夹大小"""
        if os.path.isfile(path):
            return os.path.getsize(path)
        
        total = 0
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if self.is_aborted: break
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += self.calculate_total_size(entry.path)
        except Exception as e:
            logger.error(f"计算大小出错: {path}, {e}")
        return total

    def run(self):
        """执行迁移主逻辑"""
        try:
            # 1. 前置检查
            if not os.path.exists(self.source):
                self.finished.emit(False, f"源路径不存在: {self.source}")
                return

            # 2. 计算总大小
            self.total_size = self.calculate_total_size(self.source)
            if self.is_aborted:
                self.finished.emit(False, "操作已取消")
                return

            # 3. 开始执行
            success = False
            if os.path.isfile(self.source):
                success = self._migrate_file(self.source, self.target)
            else:
                success = self._migrate_folder(self.source, self.target)

            if self.is_aborted:
                self._rollback()
                self.finished.emit(False, "操作已取消")
            elif success:
                # 核心修正：如果模式是 move，或者显式要求清理
                if self.mode == "move" or self.cleanup_source:
                    try:
                        logger.info(f"迁移成功，正在清理原始路径: {self.source}")
                        if os.path.isfile(self.source):
                            os.remove(self.source)
                        else:
                            shutil.rmtree(self.source)
                    except Exception as e:
                        # 清理失败不代表迁移失败，记录警告
                        logger.warning(f"迁移成功但清理原始路径失败（可能被锁定）: {e}")
                
                self.finished.emit(True, "")
            else:
                self._rollback()
                self.finished.emit(False, "迁移过程中发生未知错误")

        except Exception as e:
            logger.exception("迁移执行异常")
            self._rollback()
            self.finished.emit(False, str(e))

    def _migrate_file(self, src: str, dst: str) -> bool:
        """迁移单个文件"""
        if self.is_aborted: return False
        
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            # 使用 shutil.copy2 保留元数据
            # 为了实现进度，如果文件很大，我们本可以分块读写，
            # 但为了简单稳定，暂时直接调用 copy2，对单文件不显示分块进度
            # 之后如果需要超大文件进度，可以重写此部分
            filename = os.path.basename(src)
            self.progress_updated.emit(self.processed_size, self.total_size, filename)
            
            shutil.copy2(src, dst)
            self.processed_size += os.path.getsize(src)
            self.copied_paths.append(dst)
            
            self.progress_updated.emit(self.processed_size, self.total_size, filename)
            return True
        except Exception as e:
            logger.error(f"复制文件失败 {src} -> {dst}: {e}")
            return False

    def _migrate_folder(self, src: str, dst: str) -> bool:
        """递归迁移文件夹"""
        if self.is_aborted: return False

        try:
            os.makedirs(dst, exist_ok=True)
            self.copied_paths.append(dst)

            with os.scandir(src) as it:
                for entry in it:
                    if self.is_aborted: return False
                    
                    target_path = os.path.join(dst, entry.name)
                    if entry.is_file(follow_symlinks=False):
                        if not self._migrate_file(entry.path, target_path):
                            return False
                    elif entry.is_dir(follow_symlinks=False):
                        if not self._migrate_folder(entry.path, target_path):
                            return False
            return True
        except Exception as e:
            logger.error(f"复制文件夹失败 {src} -> {dst}: {e}")
            return False

    def _rollback(self):
        """简单回滚：删除已创建的目标路径"""
        logger.info("正在回滚：删除已迁移的部分数据...")
        for path in reversed(self.copied_paths):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    if not os.listdir(path): # 只删除空目录，或者根据需要 rmtree
                        os.rmdir(path)
                    else:
                        shutil.rmtree(path)
            except Exception as e:
                logger.warning(f"回滚清理失败: {path}, {e}")

class MigrationService:
    """数据迁移服务"""
    
    def __init__(self):
        self._thread: Optional[QThread] = None
        self._worker: Optional[MigrationWorker] = None

    def migrate_async(
        self, 
        source: str, 
        target: str, 
        mode: str = "copy",
        on_progress: Callable = None,
        on_finished: Callable = None
    ):
        """
        开始异步迁移任务
        
        Args:
            source: 源路径
            target: 目标路径
            mode: "copy" (默认) 或 "move"
            on_progress: 进度回调函数 (current, total, filename)
            on_finished: 完成回调函数 (success, error_msg)
        """
        # 如果已有任务在运行，先停止（原则上 UI 应保证同一时间只有一个迁移）
        self.cancel_migration()

        self._thread = QThread()
        self._worker = MigrationWorker(source, target, mode)
        self._worker.moveToThread(self._thread)

        # 信号连接
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._worker.deleteLater
        
        if on_progress:
            self._worker.progress_updated.connect(on_progress)
        
        # 内部包装完成回调以清理引用
        self._on_finished_cb = on_finished
        
        self._thread.start()

    def _on_worker_finished(self, success: bool, msg: str):
        """Worker 完成时的清理工作"""
        if self._on_finished_cb:
            self._on_finished_cb(success, msg)
        self._worker = None
        self._thread = None

    def cancel_migration(self):
        """取消正在进行的迁移"""
        if self._worker:
            self._worker.abort()
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()
            self._worker = None
            self._thread = None
