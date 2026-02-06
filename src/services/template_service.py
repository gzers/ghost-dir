# coding: utf-8
"""模板服务层"""
from typing import List, Optional
from src.models.template import Template
from src.dao.template_dao import TemplateDAO


class TemplateService:
    def __init__(self, dao: TemplateDAO):
        self.dao = dao
    
    def get_all_templates(self) -> List[Template]:
        return self.dao.get_all()
    
    def get_template_by_id(self, template_id: str) -> Optional[Template]:
        return self.dao.get_by_id(template_id)
    
    def get_templates_by_category(self, category_id: str) -> List[Template]:
        all_templates = self.dao.get_all()
        return [t for t in all_templates if t.category_id == category_id]
    
    def add_template(self, template: Template) -> bool:
        return self.dao.add(template)
    
    def update_template(self, template: Template) -> bool:
        return self.dao.update(template)
    
    def delete_template(self, template_id: str) -> bool:
        return self.dao.delete(template_id)
