# coding: utf-8
"""分类数据访问对象"""
from typing import List, Optional
from src.models.category import CategoryNode
from src.common.config import get_config_path
import json
import os


class CategoryDAO:
    def __init__(self):
        self.config_file = get_config_path('categories.json')
        self._ensure_exists()
    
    def _ensure_exists(self):
        if not os.path.exists(self.config_file):
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_all(self) -> List[CategoryNode]:
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [CategoryNode.from_dict(item) for item in data]
        except:
            return []
    
    def get_by_id(self, cid: str) -> Optional[CategoryNode]:
        for cat in self.get_all():
            if cat.id == cid:
                return cat
        return None
    
    def add(self, category: CategoryNode) -> bool:
        data = [c.to_dict() for c in self.get_all()]
        data.append(category.to_dict())
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    def update(self, category: CategoryNode) -> bool:
        data = [c.to_dict() for c in self.get_all()]
        for i, item in enumerate(data):
            if item.get('id') == category.id:
                data[i] = category.to_dict()
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        return False
    
    def delete(self, cid: str) -> bool:
        data = [c.to_dict() for c in self.get_all()]
        new_data = [item for item in data if item.get('id') != cid]
        if len(new_data) < len(data):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            return True
        return False
