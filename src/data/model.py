"""
数据模型定义
定义应用程序的核心数据结构
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime


class LinkStatus(Enum):
    """连接状态枚举"""
    DISCONNECTED = "disconnected"  # 🔴 未连接（实体在 C 盘）
    CONNECTED = "connected"        # 🟢 已连接（实体在 D 盘，C 盘有连接点）
    READY = "ready"                # 🟡 就绪（C 盘无文件，D 盘有文件）
    INVALID = "invalid"            # ⚪ 失效（连接断开或路径不存在）


@dataclass
class Template:
    """软件模版"""
    id: str                    # 唯一标识
    name: str                  # 软件名称
    default_src: str           # 默认源路径（支持环境变量）
    category: str              # 分类
    icon: Optional[str] = None # 图标路径
    is_custom: bool = False    # 是否为用户自定义模版
    description: Optional[str] = None  # 描述


@dataclass
class UserLink:
    """用户连接数据类"""
    id: str                        # 唯一标识符
    name: str                      # 显示名称
    source_path: str               # 源路径（C 盘）
    target_path: str               # 目标路径（D 盘）
    category: str                  # 分类
    template_id: Optional[str] = None  # 关联的模版 ID
    icon: Optional[str] = None     # 图标文件名
    last_known_size: int = 0       # 上次计算的空间大小（字节）
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def status(self) -> LinkStatus:
        """动态计算连接状态"""
        import os
        from ..core.link_opt import is_junction
        
        src_exists = os.path.exists(self.source_path)
        dst_exists = os.path.exists(self.target_path)
        src_is_junction = is_junction(self.source_path) if src_exists else False
        
        if src_is_junction and dst_exists:
            return LinkStatus.CONNECTED
        elif not src_exists and dst_exists:
            return LinkStatus.READY
        elif src_exists and not src_is_junction and not dst_exists:
            return LinkStatus.DISCONNECTED
        else:
            return LinkStatus.INVALID


@dataclass
class TransactionRecord:
    """事务记录（锁文件内容）"""
    operation: str                 # 操作类型：move, restore
    source_path: str               # 源路径
    target_path: str               # 目标路径
    link_id: str                   # 关联的连接 ID
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "operation": self.operation,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "link_id": self.link_id,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TransactionRecord':
        """从字典创建"""
        return cls(
            operation=data["operation"],
            source_path=data["source_path"],
            target_path=data["target_path"],
            link_id=data["link_id"],
            timestamp=data.get("timestamp", datetime.now().isoformat())
        )


@dataclass
class Category:
    """分类数据类"""
    id: str                        # 唯一标识符
    name: str                      # 显示名称
    icon: Optional[str] = None     # 图标
    color: Optional[str] = None    # 颜色标识
