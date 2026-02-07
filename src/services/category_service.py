# coding: utf-8
"""分类服务层"""
from typing import List, Optional
from src.models.category import CategoryNode
from src.dao.category_dao import CategoryDAO


class CategoryService:
    def __init__(self, dao: CategoryDAO):
        self.dao = dao

    def get_all_categories(self) -> List[CategoryNode]:
        return self.dao.get_all()

    def get_category_by_id(self, category_id: str) -> Optional[CategoryNode]:
        return self.dao.get_by_id(category_id)

    def get_category_tree(self) -> List[CategoryNode]:
        all_cats = self.dao.get_all()
        roots = [c for c in all_cats if c.parent_id is None]
        return roots

    def get_children(self, parent_id: Optional[str]) -> List[CategoryNode]:
        all_cats = self.dao.get_all()
        return [c for c in all_cats if c.parent_id == parent_id]

    def is_leaf(self, category_id: str) -> bool:
        children = self.get_children(category_id)
        return len(children) == 0

    def add_category(self, category: CategoryNode) -> bool:
        return self.dao.add(category)

    def update_category(self, category: CategoryNode) -> bool:
        return self.dao.update(category)

    def delete_category(self, category_id: str) -> bool:
        return self.dao.delete(category_id)
