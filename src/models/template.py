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
    is_custom: bool = False
    category_path_name: Optional[str] = None # 模板所属分类的全路径名称

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            default_src=data.get('default_src', ''),
            default_target=data.get('default_target'),
            category_id=data.get('category_id'),
            description=data.get('description'),
            order=data.get('order', 0),
            is_custom=data.get('is_custom', False),
            category_path_name=data.get('category_path_name')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'default_src': self.default_src,
            'default_target': self.default_target,
            'category_id': self.category_id,
            'description': self.description,
            'order': self.order,
            'is_custom': self.is_custom,
            'category_path_name': self.category_path_name
        }
