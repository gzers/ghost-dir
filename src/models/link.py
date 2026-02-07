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
    ERROR = "error"


@dataclass
class UserLink:
    id: str
    name: str
    source_path: str
    target_path: str
    category: Optional[str] = None
    status: LinkStatus = LinkStatus.DISCONNECTED
    last_known_size: int = 0  # 上次计算的占用空间大小（字节）

    @classmethod
    def from_dict(cls, data: dict):
        status_str = data.get('status', 'disconnected')
        if isinstance(status_str, str):
            status = LinkStatus(status_str)
        else:
            status = status_str

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
            'last_known_size': self.last_known_size
        }
