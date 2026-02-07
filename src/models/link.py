# coding: utf-8
"""链接数据模型"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LinkStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    READY = "ready"      # 就绪状态（但未连接）
    INVALID = "invalid"  # 失效状态
    ERROR = "error"  # 通用错误或未知冲突


@dataclass
class UserLink:
    id: str
    name: str
    source_path: str
    target_path: str
    category: Optional[str] = None
    status: LinkStatus = LinkStatus.DISCONNECTED
    last_known_size: int = 0  # 上次计算的占用空间大小（字节）
    resolve_path: Optional[str] = None  # 实际探测到的物理指向路径（用于 REDIRECTED 状态显示）

    @classmethod
    def from_dict(cls, data: dict):
        status_str = data.get('status', 'disconnected')
        try:
            status = LinkStatus(status_str) if isinstance(status_str, str) else status_str
        except ValueError:
            # 兼容已废弃的 redirected 等旧状态，统一回退到 disconnected 触发重新探测
            status = LinkStatus.DISCONNECTED

        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            source_path=data.get('source_path', ''),
            target_path=data.get('target_path', ''),
            category=data.get('category'),
            status=status,
            last_known_size=data.get('last_known_size', 0)
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'source_path': self.source_path,
            'target_path': self.target_path,
            'category': self.category,
            'status': self.status.value if isinstance(self.status, LinkStatus) else self.status,
            'last_known_size': self.last_known_size,
            'resolve_path': self.resolve_path
        }
