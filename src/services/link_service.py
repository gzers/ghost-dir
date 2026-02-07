# coding: utf-8
"""链接服务层"""
from typing import List, Optional, Callable
import os
import time
import subprocess
from PySide6.QtCore import QThread, Signal, QObject
from src.models.link import UserLink, LinkStatus
from src.dao.link_dao import LinkDAO

class ServiceWorker(QObject):
    """通用服务 Worker - 处理耗时任务（空间统计、状态探测）"""
    # 逐个完成的信号: (link_id, data)
    item_finished = Signal(str, object)
    # 全部完成的信号: (results_dict)
    all_finished = Signal(dict)

    def calculate_sizes(self, link_ids: List[str], dao: LinkDAO):
        """批量计算大小"""
        results = {}
        all_links = dao.get_all()
        link_map = {l.id: l for l in all_links}

        for lid in link_ids:
            if lid not in link_map: continue
            
            link = link_map[lid]
            total_size = 0
            if os.path.exists(link.source_path):
                if os.path.isfile(link.source_path):
                    total_size = os.path.getsize(link.source_path)
                else:
                    try:
                        for root, dirs, files in os.walk(link.source_path):
                            for f in files:
                                fp = os.path.join(root, f)
                                if os.path.exists(fp): total_size += os.path.getsize(fp)
                    except Exception: pass
            
            if total_size != link.last_known_size:
                link.last_known_size = total_size
                dao.update(link)
            
            results[lid] = total_size
            self.item_finished.emit(lid, total_size)
            time.sleep(0.01)
        
        self.all_finished.emit(results)

    def detect_status(self, link_ids: List[str], dao: LinkDAO):
        """批量探测探测状态"""
        results = {}
        all_links = dao.get_all()
        link_map = {l.id: l for l in all_links}

        for lid in link_ids:
            if lid not in link_map: continue
            link = link_map[lid]
            
            new_status = self._check_single_link(link)
            
            if new_status != link.status:
                link.status = new_status
                dao.update(link)
            
            results[lid] = new_status
            self.item_finished.emit(lid, new_status)
            time.sleep(0.01)
            
        self.all_finished.emit(results)

    def _check_single_link(self, link: UserLink) -> LinkStatus:
        """探测单个链接状态的核心逻辑"""
        src = link.source_path
        dst = link.target_path
        
        # 1. 源路径检查（物理文件是否存在）
        if not os.path.exists(src):
            return LinkStatus.INVALID
            
        # 2. 目标路径状态检查
        if not os.path.exists(dst):
            return LinkStatus.READY
            
        # 3. 链接有效性检查 (Windows 符号链接/目录联接)
        try:
            # os.path.islink 在 Windows 下有限（不识别 Junction）
            # 使用 fsutil 或底层属性检查
            if os.name == 'nt':
                import ctypes
                FILE_ATTRIBUTE_REPARSE_POINT = 0x400
                attrs = ctypes.windll.kernel32.GetFileAttributesW(dst)
                
                # 如果是重解析点（符号链接、联接点等）
                if attrs != -1 and (attrs & FILE_ATTRIBUTE_REPARSE_POINT):
                    return LinkStatus.CONNECTED
                
                # 备用方案：通过 dir 命令确认
                parent_dir = os.path.dirname(dst)
                base_name = os.path.basename(dst)
                # 使用 L 参数显示重解析点目标，D 参数仅目录
                output = subprocess.check_output(f'dir /L "{parent_dir}"', shell=True).decode('gbk', errors='ignore')
                
                # Windows 下 JUNCTION 会显示为 <JUNCTION> 或 [Name]
                # SYMLINKD 会显示为 <SYMLINKD>
                if f"<{base_name}>" in output or f"[{base_name}]" in output or f" {base_name} [" in output:
                    return LinkStatus.CONNECTED
            else:
                # Unix/MacOS
                if os.path.islink(dst):
                    return LinkStatus.CONNECTED
        except:
            pass
            
        # 4. 冲突检查：如果目标存在但不是链接，说明被真实文件占用了
        # 这通常发生在迁移不彻底或手动移动文件后
        return LinkStatus.ERROR

class LinkService:
    def __init__(self, dao: LinkDAO):
        self.dao = dao
        self._worker_thread = None
        self._worker = None

    def get_all_links(self, category_id: str = "all") -> List[UserLink]:
        return self.dao.get_all() if category_id == "all" else self.get_links_by_category(category_id)

    def get_link_by_id(self, link_id: str) -> Optional[UserLink]:
        return self.dao.get_by_id(link_id)

    def get_links_by_category(self, category_id: str) -> List[UserLink]:
        return [link for link in self.dao.get_all() if link.category == category_id]

    def add_link(self, link: UserLink) -> bool: return self.dao.add(link)
    def update_link(self, link: UserLink) -> bool: return self.dao.update(link)
    def delete_link(self, link_id: str) -> bool: return self.dao.delete(link_id)
    def delete_links(self, link_ids: List[str]) -> bool: return self.dao.delete_batch(link_ids)

    def calculate_sizes_async(self, link_ids: List[str], item_cb: Callable, finished_cb: Callable):
        """异步单线程统计大小"""
        self._start_worker(lambda w: w.calculate_sizes(link_ids, self.dao), item_cb, finished_cb)

    def refresh_status_async(self, link_ids: List[str], item_cb: Callable, finished_cb: Callable):
        """异步批量刷新链接状态"""
        self._start_worker(lambda w: w.detect_status(link_ids, self.dao), item_cb, finished_cb)

    def _start_worker(self, task_fn: Callable, item_cb: Callable, finished_cb: Callable):
        if self._worker_thread and self._worker_thread.isRunning(): return
        
        self._worker_thread = QThread()
        self._worker = ServiceWorker()
        self._worker.moveToThread(self._worker_thread)
        
        self._worker_thread.started.connect(lambda: task_fn(self._worker))
        if item_cb: self._worker.item_finished.connect(item_cb)
        if finished_cb: self._worker.all_finished.connect(finished_cb)
        
        self._worker.all_finished.connect(self._worker_thread.quit)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        self._worker_thread.start()
