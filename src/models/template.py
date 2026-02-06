# coding: utf-8
"""模板数据模型"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Template:
    id: str
    name: str
    default_src: str
    default_target: Optional[str] = None
    category_id: Optional[str] = None
    description: Optional[str] = None
    order: int = 0
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            default_src=data.get('default_src', ''),
            default_target=data.get('default_target'),
            category_id=data.get('category_id'),
            description=data.get('description'),
            order=data.get('order', 0)
        )
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'default_src': self.default_src,
            'default_target': self.default_target,
            'category_id': self.category_id,
            'description': self.description,
            'order': self.order
        }
