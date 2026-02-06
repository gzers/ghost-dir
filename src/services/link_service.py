# coding: utf-8
"""链接服务层"""
from typing import List, Optional
from src.models.link import UserLink
from src.dao.link_dao import LinkDAO


class LinkService:
    def __init__(self, dao: LinkDAO):
        self.dao = dao
    
    def get_all_links(self) -> List[UserLink]:
        return self.dao.get_all()
    
    def get_link_by_id(self, link_id: str) -> Optional[UserLink]:
        return self.dao.get_by_id(link_id)
    
    def get_links_by_category(self, category_id: str) -> List[UserLink]:
        all_links = self.dao.get_all()
        return [link for link in all_links if link.category == category_id]
    
    def add_link(self, link: UserLink) -> bool:
        return self.dao.add(link)
    
    def update_link(self, link: UserLink) -> bool:
        return self.dao.update(link)
    
    def delete_link(self, link_id: str) -> bool:
        return self.dao.delete(link_id)
