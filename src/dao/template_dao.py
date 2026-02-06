# coding: utf-8
"""模板数据访问对象"""
from typing import List, Optional
from src.models.template import Template
from src.common.config import get_config_path
import json
import os


class TemplateDAO:
    def __init__(self):
        self.config_file = get_config_path('templates.json')
        self._ensure_exists()
    
    def _ensure_exists(self):
        if not os.path.exists(self.config_file):
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_all(self) -> List[Template]:
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Template.from_dict(item) for item in data]
        except:
            return []
    
    def get_by_id(self, tid: str) -> Optional[Template]:
        for t in self.get_all():
            if t.id == tid:
                return t
        return None
    
    def add(self, template: Template) -> bool:
        data = [t.to_dict() for t in self.get_all()]
        data.append(template.to_dict())
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    def update(self, template: Template) -> bool:
        data = [t.to_dict() for t in self.get_all()]
        for i, item in enumerate(data):
            if item.get('id') == template.id:
                data[i] = template.to_dict()
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        return False
    
    def delete(self, tid: str) -> bool:
        data = [t.to_dict() for t in self.get_all()]
        new_data = [item for item in data if item.get('id') != tid]
        if len(new_data) < len(data):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            return True
        return False
