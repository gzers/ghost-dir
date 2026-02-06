# coding: utf-8
"""DAO 层初始化文件"""
from .template_dao import TemplateDAO
from .link_dao import LinkDAO
from .category_dao import CategoryDAO

__all__ = ['TemplateDAO', 'LinkDAO', 'CategoryDAO']
