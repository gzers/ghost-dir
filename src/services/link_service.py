# coding: utf-8
"""
链接服务层 - 专题优化版
集成了并发扫描、信号节流、任务抢占及线程安全管理
"""
import os
import sys
import time
import subprocess
import concurrent.futures
from typing import List, Optional, Callable
from PySide6.QtCore import QThread, Signal, QObject
from src.models.link import UserLink, LinkStatus
from src.dao.link_dao import LinkDAO

class ServiceWorker(QObject):
    """通用服务 Worker - 增强型：支持中断与实时日志"""
    item_finished = Signal(str, object)
    all_finished = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_aborted = False # 取消标志位

    def calculate_sizes(self, link_ids: List[str], dao: LinkDAO):
        """[专题重组] 极速并发空间统计"""
        results = {}
        all_links = dao.get_all()
        link_map = {l.id: l for l in all_links}
        total_tasks = len(link_ids)
        state = {'completed': 0}
        
        print(f"\n>>>> [Space Audit] 启动, 共 {total_tasks} 任务 <<<<")
        sys.stdout.flush()

        def _get_folder_size(path):
            if self.is_aborted: return 0
            total = 0
            try:
                with os.scandir(path) as it:
                    for entry in it:
                        if self.is_aborted: break
                        try:
                            if entry.is_file(follow_symlinks=False):
                                total += entry.stat(follow_symlinks=False).st_size
                            elif entry.is_dir(follow_symlinks=False):
                                total += _get_folder_size(entry.path)
                        except: continue
            except: pass
            return total

        def _get_size(lid):
            if self.is_aborted: return lid, 0
            link = link_map.get(lid)
            if not link: return lid, 0
            
            total = 0
            try:
                path = link.source_path
                if os.path.exists(path):
                    if os.path.isfile(path):
                        total = os.path.getsize(path)
                    else:
                        total = _get_folder_size(path)
            except: pass
            return lid, total

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(link_ids), 8)) as executor:
            future_to_id = {executor.submit(_get_size, lid): lid for lid in link_ids}
            for future in concurrent.futures.as_completed(future_to_id):
                if self.is_aborted: break
                
                state['completed'] += 1
                try:
                    lid, size = future.result()
                    results[lid] = size
                    
                    if lid in link_map:
                        link = link_map[lid]
                        link.last_known_size = size
                        try: dao.update(link)
                        except: pass
                    
                    self.item_finished.emit(lid, size)
                    
                    from src.common.config import format_size
                    progress = (state['completed'] / total_tasks) * 100
                    name = link_map.get(lid).name if lid in link_map else "Unknown"
                    sys.stdout.write(f"\r[Audit] {progress:3.0f}% | 处理中: {name[:20]:<20} | {format_size(size):>10}")
                    sys.stdout.flush()
                except Exception as e:
                    print(f"\n[Error] 计算项目失败: {e}")

        status_msg = "已取消" if self.is_aborted else "已完成"
        print(f"\n>>>> [Space Audit] {status_msg} <<<<\n")
        sys.stdout.flush()
        self.all_finished.emit(results)

    def detect_status(self, link_ids: List[str], dao: LinkDAO):
        """[专题重组] 并发状态探测"""
        results = {}
        all_links = dao.get_all()
        link_map = {l.id: l for l in all_links}

        def _get_status(lid):
            if self.is_aborted: return lid, LinkStatus.DISCONNECTED
            link = link_map.get(lid)
            if not link: return lid, LinkStatus.INVALID
            return lid, self._check_single_link(link)

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(link_ids), 16)) as executor:
            future_to_id = {executor.submit(_get_status, lid): lid for lid in link_ids}
            for future in concurrent.futures.as_completed(future_to_id):
                if self.is_aborted: break
                lid, status = future.result()
                results[lid] = status
                
                link = link_map.get(lid)
                if link and status != link.status:
                    link.status = status
                    dao.update(link)
                self.item_finished.emit(lid, status)

        self.all_finished.emit(results)

    def _check_single_link(self, link: UserLink) -> LinkStatus:
        src = link.source_path
        def get_real_path(path):
            if not os.path.exists(path): return None
            try:
                resolved = os.path.realpath(path)
                return os.path.normpath(resolved).lower()
            except:
                return os.path.normcase(os.path.abspath(path)).lower()
        def get_attrs(p):
            if os.name != 'nt': return 0
            try:
                import ctypes
                return ctypes.windll.kernel32.GetFileAttributesW(p)
            except: return -1

        src_attrs = get_attrs(src)
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        if not os.path.exists(src):
            link.resolve_path = None
            return LinkStatus.INVALID
        if src_attrs != -1 and (src_attrs & FILE_ATTRIBUTE_REPARSE_POINT):
            real_target = get_real_path(src)
            link.resolve_path = real_target
            if real_target and os.path.exists(real_target):
                return LinkStatus.CONNECTED
            return LinkStatus.INVALID
        dst = link.target_path
        if not os.path.exists(dst):
            link.resolve_path = None
            return LinkStatus.READY
        link.resolve_path = None
        return LinkStatus.ERROR

class LinkService:
    def __init__(self, dao: LinkDAO):
        self.dao = dao
        self._current_worker = None
        self._active_threads = set()

    def get_all_links(self, category_id: str = "all") -> List[UserLink]:
        return self.dao.get_all() if category_id == "all" else self.get_links_by_category(category_id)

    def get_link_by_id(self, link_id: str) -> Optional[UserLink]:
        return self.dao.get_by_id(link_id)

    def get_links_by_category(self, category_id: str) -> List[UserLink]:
        return [l for l in self.dao.get_all() if l.category == category_id]

    def add_link(self, link: UserLink) -> bool: return self.dao.add(link)
    def update_link(self, link: UserLink) -> bool: return self.dao.update(link)
    def delete_link(self, link_id: str) -> bool: return self.dao.delete(link_id)

    def calculate_sizes_async(self, link_ids: List[str], item_cb: Callable, finished_cb: Callable):
        self._start_worker(lambda w: w.calculate_sizes(link_ids, self.dao), item_cb, finished_cb)

    def refresh_status_async(self, link_ids: List[str], item_cb: Callable, finished_cb: Callable):
        self._start_worker(lambda w: w.detect_status(link_ids, self.dao), item_cb, finished_cb)

    def refresh_link_status(self, link_id: str) -> LinkStatus:
        """同步刷新单个链接状态"""
        link = self.get_link_by_id(link_id)
        if not link: return LinkStatus.INVALID
        worker = ServiceWorker()
        new_status = worker._check_single_link(link)
        link.status = new_status
        self.dao.update(link)
        return new_status

    def _start_worker(self, task_fn: Callable, item_cb: Callable, finished_cb: Callable):
        # 抢占式中止旧任务
        if self._current_worker:
            self._current_worker.is_aborted = True
        
        thread = QThread()
        worker = ServiceWorker()
        self._current_worker = worker
        
        self._active_threads.add(thread)
        worker.moveToThread(thread)
        
        thread.started.connect(lambda: task_fn(worker))
        if item_cb: worker.item_finished.connect(item_cb)
        if finished_cb: worker.all_finished.connect(finished_cb)
        
        def _cleanup():
            thread.quit()
            if thread in self._active_threads:
                self._active_threads.remove(thread)
            thread.deleteLater()

        worker.all_finished.connect(_cleanup)
        thread.start()
