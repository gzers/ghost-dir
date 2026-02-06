# coding: utf-8
"""
服务总线 - 全局 Service 访问点
这是一个临时方案,提供全局访问 Service 和 Manager 的接口
"""
from src.dao import TemplateDAO, LinkDAO, CategoryDAO
from src.services import TemplateService, LinkService, CategoryService
from src.common.managers import TemplateManager, CategoryManager, UserManager


class ServiceBus:
    """服务总线 - 单例模式"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # 初始化 DAO 层
        self._template_dao = TemplateDAO()
        self._link_dao = LinkDAO()
        self._category_dao = CategoryDAO()
        
        # 初始化 Service 层
        self.template_service = TemplateService(self._template_dao)
        self.link_service = LinkService(self._link_dao)
        self.category_service = CategoryService(self._category_dao)
        
        # 初始化 Manager 层 (临时包装器)
        self.template_manager = TemplateManager()
        self.category_manager = CategoryManager()
        self.user_manager = UserManager()
        
        # 兼容旧代码的别名
        self.connection_service = self.link_service
        
        self._initialized = True


# 全局单例实例
service_bus = ServiceBus()
