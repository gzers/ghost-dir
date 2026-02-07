# coding: utf-8
"""
服务总线 - 全局 Service 访问点
"""
from src.dao import TemplateDAO, LinkDAO, CategoryDAO
from src.services import TemplateService, LinkService, CategoryService, ConfigService
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

        # 1. 初始化 DAO 层
        self._template_dao = TemplateDAO()
        self._link_dao = LinkDAO()
        self._category_dao = CategoryDAO()

        # 2. 初始化 Service 层
        self.template_service = TemplateService(self._template_dao)
        self.link_service = LinkService(self._link_dao)
        self.category_service = CategoryService(self._category_dao)
        self.config_service = ConfigService()

        # 3. 初始化 Manager 层 (显式持有)
        self.template_manager = TemplateManager()
        self.category_manager = CategoryManager()
        self.user_manager = UserManager()

        self.connection_service = self.link_service
        self.main_window = None  # 增加主窗口全局引用

        self._initialized = True

# 全局单例
service_bus = ServiceBus()
