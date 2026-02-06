# coding: utf-8
"""
临时 Manager 包装器
目的: 让旧的 GUI 代码可以继续使用 Manager 接口,内部调用新的 Service
这是一个过渡方案,后续可以逐步移除
"""
from src.dao import TemplateDAO, LinkDAO, CategoryDAO
from src.services import TemplateService, LinkService, CategoryService


class TemplateManager:
    """模板管理器 - Service 包装器"""
    
    def __init__(self):
        self._dao = TemplateDAO()
        self._service = TemplateService(self._dao)
    
    def get_all_templates(self):
        return self._service.get_all_templates()
    
    def get_template_by_id(self, template_id: str):
        return self._service.get_template_by_id(template_id)
    
    def get_templates_by_category(self, category_id: str):
        return self._service.get_templates_by_category(category_id)
    
    def add_template(self, template):
        return self._service.add_template(template)
    
    def update_template(self, template):
        return self._service.update_template(template)
    
    def delete_template(self, template_id: str):
        return self._service.delete_template(template_id)


class CategoryManager:
    """分类管理器 - Service 包装器"""
    
    def __init__(self):
        self._dao = CategoryDAO()
        self._service = CategoryService(self._dao)
        self.categories = {}
        self._load_categories()
    
    def _load_categories(self):
        all_cats = self._service.get_all_categories()
        self.categories = {cat.id: cat for cat in all_cats}
    
    def get_category_tree(self):
        return self._service.get_category_tree()
    
    def get_category_by_id(self, category_id: str):
        return self._service.get_category_by_id(category_id)
    
    def get_children(self, parent_id: str):
        return self._service.get_children(parent_id)
    
    def is_leaf(self, category_id: str):
        return self._service.is_leaf(category_id)
    
    def add_category(self, category):
        result = self._service.add_category(category)
        self._load_categories()
        return result
    
    def update_category(self, category):
        result = self._service.update_category(category)
        self._load_categories()
        return result
    
    def delete_category(self, category_id: str):
        result = self._service.delete_category(category_id)
        self._load_categories()
        return result


class UserManager:
    """用户链接管理器 - Service 包装器"""
    
    def __init__(self):
        self._dao = LinkDAO()
        self._service = LinkService(self._dao)
    
    def get_all_links(self):
        return self._service.get_all_links()
    
    def get_link_by_id(self, link_id: str):
        return self._service.get_link_by_id(link_id)
    
    def get_links_by_category(self, category_id: str):
        return self._service.get_links_by_category(category_id)
    
    def add_link(self, link):
        return self._service.add_link(link)
    
    def update_link(self, link):
        return self._service.update_link(link)
    
    def delete_link(self, link_id: str):
        return self._service.delete_link(link_id)
