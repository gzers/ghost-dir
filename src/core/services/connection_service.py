"""
连接服务 (Connection Service)
负责链接操作执行、状态跟踪、空间计算调度及事务保障
"""
from typing import List, Optional, Dict, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from src.data.user_manager import UserManager
from src.data.model import UserLink, LinkStatus
from src.core.engine.transaction_engine import TransactionEngine




@dataclass
class LinkViewModel:
    """连接展示模型 - 字段对齐 UserLink 以兼容现有 UI 组件"""
    id: str
    name: str
    source_path: str      # 兼容 UserLink.source_path
    target_path: str      # 兼容 UserLink.target_path
    category: str         # 兼容 UserLink.category
    status: str           # 兼容 UserLink.status (使用 LinkStatus 常量)
    last_known_size: int  # 兼容 UserLink.last_known_size
    size_str: str         # 新增属性：已格式化的字符串显示
    category_path: str    # 新增属性：分类全路径名称
    created_at: str
    is_scanned: bool = False


class ConnectionService:
    """链接业务服务"""

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self._async_runners: Dict[str, Any] = {} # 存储异步任务引用
        self._size_calc_running = False # 🆕 运行标志位

    def get_all_links(self, category_id: str = "all") -> List[LinkViewModel]:
        """获取连接列表 ViewModel"""
        links = self.user_manager.get_all_links()
        if category_id != "all":
            links = [l for l in links if l.category == category_id]
            
        return [self._to_view_model(l) for l in links]

    def _to_view_model(self, l: UserLink) -> LinkViewModel:
        """模型转换：处理数据对齐与状态探测"""
        # TODO: 接入 i18n
        from src.common.config import format_size
        
        # 实时状态探测（可选，也可依赖 link.status）
        current_status = l.status
        
        # 计算格式化大小
        size_bytes = l.last_known_size
        size_str = format_size(size_bytes) if size_bytes > 0 else "未计算"
        
        return LinkViewModel(
            id=l.id,
            name=l.name,
            source_path=l.source_path,
            target_path=l.target_path,
            category=l.category,
            category_path=getattr(l, 'category_path_name', '未分类'),
            status=current_status,
            last_known_size=size_bytes,
            size_str=size_str,
            created_at=l.created_at
        )

    def _format_size(self, size_bytes: int) -> str:
        from src.common.config import format_size
        return format_size(size_bytes)

    def establish_connection(self, source: str, target: str, name: str, category: str) -> Tuple[bool, str]:
        """执行连接事务"""
        # 简化版实现，未来可集成 SafetyEngine

        tm = TransactionEngine(source, target, name)

        if tm.establish_link():
            return True, f"已成功建立 {name} 的连接"
        return False, "建立连接失败，请检查路径权限或磁盘占用"

    def disconnect_connection(self, link_id: str) -> Tuple[bool, str]:
        """关闭连接"""
        link = self.user_manager.get_link_by_id(link_id)
        if not link:
            return False, "链接不存在"
            
        tm = TransactionEngine(link.source_path, link.target_path, link.id)

        if tm.disconnect_link():
            return True, "连接已断开"
            
        return False, "断开操作中途失败，已尝试保护现场"

    def establish_connection_by_id(self, link_id: str) -> Tuple[bool, str]:
        """通过 ID 建立连接"""
        link = self.user_manager.get_link_by_id(link_id)
        if not link:
            return False, "连接配置不存在"
            
        return self.establish_connection(
            link.source_path, 
            link.target_path, 
            link.name, 
            link.category
        )

    def reconnect_connection(self, link_id: str) -> Tuple[bool, str]:
        """重新连接 (接口别名，确保 UI 兼容)"""
        return self.establish_connection_by_id(link_id)

    def calculate_sizes_async(self, link_ids: List[str], on_finished_callback):
        """异步触发大小计算"""
        links = []
        for lid in link_ids:
            link = self.user_manager.get_link_by_id(lid)
            if link: links.append(link)
            
        if not links or self._size_calc_running: 
            return
        
        self._size_calc_running = True

        from PySide6.QtCore import QThread, Signal
        import os
        class SizeWorker(QThread):
            finished = Signal(dict)
            def run(self):
                from src.utils.space_analyzer import calculate_directory_size
                results = {}
                for l in links:
                    # 获取有效路径
                    path = l.source_path if os.path.exists(l.source_path) else l.target_path
                    if os.path.exists(path):
                        size = calculate_directory_size(path)
                        results[l.id] = size
                self.finished.emit(results)
        
        worker = SizeWorker()
        worker.finished.connect(on_finished_callback)
        worker.finished.connect(self._on_size_batch_done)
        self._async_runners['size_calc'] = worker
        worker.finished.connect(self._reset_calc_flag)
        worker.start()

    def _reset_calc_flag(self):
        """重置运行状态"""
        self._size_calc_running = False

    def _on_size_batch_done(self, results: Dict[str, int]):
        """批量更新大小缓存并持久化"""
        for lid, size in results.items():
            self.user_manager.update_link_size(lid, size)
        
        # 🆕 显式广播数据已刷新信号，通知所有 UI 组件重新读取已持久化的数据
        from src.common.signals import signal_bus
        signal_bus.data_refreshed.emit()

    def batch_establish(self, link_ids: List[str]) -> Tuple[int, int]:
        """批量建立连接 (返回: 成功数, 失败数)"""
        success, fail = 0, 0
        for lid in link_ids:
            res, _ = self.establish_connection_by_id(lid)
            if res: success += 1
            else: fail += 1
        return success, fail

    def batch_disconnect(self, link_ids: List[str]) -> Tuple[int, int]:
        """批量断开连接 (返回: 成功数, 失败数)"""
        success, fail = 0, 0
        for lid in link_ids:
            res, _ = self.disconnect_connection(lid)
            if res: success += 1
            else: fail += 1
        return success, fail
