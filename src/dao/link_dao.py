# coding: utf-8
"""链接数据访问对象"""
from typing import List, Optional
from src.models.link import UserLink
from src.common.config import get_config_path
import json
import os


class LinkDAO:
    def __init__(self):
        self.config_file = get_config_path('links.json')
        self._ensure_exists()
    
    def _ensure_exists(self):
        if not os.path.exists(self.config_file):
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_all(self) -> List[UserLink]:
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [UserLink.from_dict(item) for item in data]
        except:
            return []
    
    def get_by_id(self, lid: str) -> Optional[UserLink]:
        for link in self.get_all():
            if link.id == lid:
                return link
        return None
    
    def add(self, link: UserLink) -> bool:
        data = [l.to_dict() for l in self.get_all()]
        data.append(link.to_dict())
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    def update(self, link: UserLink) -> bool:
        data = [l.to_dict() for l in self.get_all()]
        for i, item in enumerate(data):
            if item.get('id') == link.id:
                data[i] = link.to_dict()
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        return False
    
    def delete(self, lid: str) -> bool:
        data = [l.to_dict() for l in self.get_all()]
        new_data = [item for item in data if item.get('id') != lid]
        if len(new_data) < len(data):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            return True
        return False
