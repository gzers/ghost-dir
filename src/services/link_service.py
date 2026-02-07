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
            path = link.source_path
            
            # 使用 os.scandir 替代 os.walk 以获得更高的性能，并在大型扫描中分批反馈
            try:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        total_size = os.path.getsize(path)
                    else:
                        # 深度统计文件夹大小
                        for root, dirs, files in os.walk(path):
                            for f in files:
                                try:
                                    fp = os.path.join(root, f)
                                    # 注意：如果是链接，我们通常统计链接本身还是目标？
                                    # 这里遵循用户直觉：统计源路径下所有物理文件的大小
                                    total_size += os.path.getsize(fp)
                                except (OSError, PermissionError):
                                    continue
            except Exception:
                total_size = 0
            
            # 记录并更新数据库
            link.last_known_size = total_size
            dao.update(link)
            
            results[lid] = total_size
            # 关键：确保信号被发出，让 UI 停止加载动画
            self.item_finished.emit(lid, total_size)
        
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
        
        # 0. 辅助函数：获取 Windows 下的真实标准化物理路径
        def get_real_path(path):
            if not os.path.exists(path): return None
            # 使用 Python 原生的 realpath (3.8+ 在 Windows 上支持解析链接)
            # 配合 normpath 消除所有样式差异，统一转小写进行不区分大小写比对
            try:
                resolved = os.path.realpath(path)
                return os.path.normpath(resolved).lower()
            except:
                return os.path.normcase(os.path.abspath(path)).lower()

        # 1. 获取物理标准化路径
        # 注意：在这里 real_src 获取的是“实测最终指向”
        # 我们需要先知道 src (入口) 本身的属性
        def get_attrs(p):
            if os.name != 'nt': return 0
            try:
                import ctypes
                return ctypes.windll.kernel32.GetFileAttributesW(p)
            except: return -1

        src_attrs = get_attrs(src)
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        
        # 2. 判断逻辑
        # 情况 A: 源路径根本不存在 (Invalid)
        if not os.path.exists(src):
            link.resolve_path = None
            return LinkStatus.INVALID
            
        # 情况 B: 源路径是一个已建立的链接 (Symlink/Junction) - 这是最核心的“已连接”判定
        if src_attrs != -1 and (src_attrs & FILE_ATTRIBUTE_REPARSE_POINT):
            real_target = get_real_path(src) # 获取链接指向的终点
            link.resolve_path = real_target
            
            # [核心改变] 遵循用户直觉：只要链接存在且指向的位置在物理上是存在的，就视为正常已连接
            if real_target and os.path.exists(real_target):
                # 如果实测指向与预期备份路径确实不一致，我们只在后台记录 resolve_path，UI 依然给绿灯
                return LinkStatus.CONNECTED
            else:
                # 链接通了，但指向的是一个空地址（源头被删或移动）
                return LinkStatus.INVALID
                
        # 情况 C: 源路径存在但不是链接 (普通文件/目录)
        # 这时看目标路径
        if not os.path.exists(dst):
            # 目标不存在，说明可以迁移 (Ready)
            link.resolve_path = None
            return LinkStatus.READY
        else:
            # 源和目标都作为普通物理路径存在，这是真正的“路径冲突”
            link.resolve_path = None
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

    def refresh_link_status(self, link_id: str) -> LinkStatus:
        """同步刷新单个链接状态"""
        link = self.get_link_by_id(link_id)
        if not link: return LinkStatus.INVALID
        
        worker = ServiceWorker()
        new_status = worker._check_single_link(link)
        
        # 即使状态没变，resolve_path 可能变了，所以也需要更新
        link.status = new_status
        self.dao.update(link)
        return new_status

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
