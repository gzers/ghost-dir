# coding: utf-8
"""
Temporary Manager Wrappers
Decouples UI from the new Service layer during transition.
"""
from src.dao import TemplateDAO, LinkDAO, CategoryDAO
from src.services import TemplateService, LinkService, CategoryService

class TemplateManager:
    def __init__(self):
        self._dao = TemplateDAO()
        self._service = TemplateService(self._dao)
        self.templates = {}
        self.load_templates()

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

    def load_templates(self):
        """Standard interface for refreshing data"""
        all_tpls = self._service.get_all_templates()
        self.templates = {t.id: t for t in all_tpls}

    def validate_all_templates(self):
        return []

class CategoryManager:
    def __init__(self):
        self._dao = CategoryDAO()
        self._service = CategoryService(self._dao)
        self.categories = {}
        self.load_categories()

    def load_categories(self):
        """Standard interface for refreshing data"""
        all_cats = self._service.get_all_categories()
        self.categories = {c.id: c for c in all_cats}

    def get_all_categories(self):
        """Forward to service"""
        return self._service.get_all_categories()

    def get_category_tree(self):
        return self._service.get_category_tree()

    def get_category_by_id(self, category_id: str):
        return self._service.get_category_by_id(category_id)

    def get_children(self, parent_id: str):
        return self._service.get_children(parent_id)

    def is_leaf(self, category_id: str):
        return self._service.is_leaf(category_id)

    def add_category(self, category):
        res = self._service.add_category(category)
        self.load_categories()
        return res

    def update_category(self, category):
        res = self._service.update_category(category)
        self.load_categories()
        return res

    def delete_category(self, category_id: str):
        res = self._service.delete_category(category_id)
        self.load_categories()
        return res

class UserManager:
    def __init__(self):
        self._dao = LinkDAO()
        self._service = LinkService(self._dao)

    def get_all_links(self, category_id: str = "all"):
        return self._service.get_all_links(category_id)

    def get_link_by_id(self, link_id: str):
        return self._service.get_link_by_id(link_id)

    def get_links_by_category(self, category_id: str):
        return self._service.get_links_by_category(category_id)

    def add_link(self, link):
        return self._service.add_link(link)

    def update_link(self, link):
        return self._service.update_link(link)

    def remove_link(self, link_id: str):
        return self._service.delete_link(link_id)
