# coding: utf-8
"""链接数据模型"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LinkStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class UserLink:
    id: str
    name: str
    source_path: str
    target_path: str
    category: Optional[str] = None
    status: LinkStatus = LinkStatus.DISCONNECTED

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
            status=status
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'source_path': self.source_path,
            'target_path': self.target_path,
            'category': self.category,
            'status': self.status.value if isinstance(self.status, LinkStatus) else self.status
        }
