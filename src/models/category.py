# coding: utf-8
"""分类数据模型"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class CategoryNode:
    id: str
    name: str
    parent_id: Optional[str] = None
    order: int = 0
    children: List['CategoryNode'] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: dict):
        node = cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            parent_id=data.get('parent_id'),
            order=data.get('order', 0)
        )
        children_data = data.get('children', [])
        node.children = [cls.from_dict(child) for child in children_data]
        return node
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'order': self.order,
            'children': [child.to_dict() for child in self.children]
        }
