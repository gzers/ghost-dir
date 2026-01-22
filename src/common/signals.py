"""
全局信号总线
用于模块间的松耦合通信
"""
from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """全局信号总线"""
    
    # 连接状态变更信号
    link_status_changed = Signal(str)  # link_id
    
    # 扫描完成信号
    scan_completed = Signal(list)  # discovered_links
    
    # 操作进度信号
    operation_progress = Signal(str, int, int)  # operation_name, current, total
    
    # 操作完成信号
    operation_completed = Signal(str, bool, str)  # operation_name, success, message
    
    # 批量操作完成信号
    batch_operation_completed = Signal(int, int)  # success_count, total_count
    
    # 数据刷新信号
    data_refreshed = Signal()
    
    # 分类变更信号
    categories_changed = Signal()

    # 主题变更信号
    theme_changed = Signal(str)  # theme_name (light/dark/system)


# 全局单例
signal_bus = SignalBus()
