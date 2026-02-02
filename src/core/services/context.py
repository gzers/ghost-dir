"""
服务上下文 (Service Context)
负责所有业务服务的初始化与生命周期管理
"""
from src.data.category_manager import CategoryManager
from src.data.template_manager import TemplateManager
from src.data.user_manager import UserManager
from src.core.services.category_service import CategoryService
from src.core.services.template_service import TemplateService
from src.core.services.config_service import ConfigService
from src.core.services.connection_service import ConnectionService


class ServiceContext:
    """全局服务容器"""
    _instance = None

    def __init__(self):
        # 1. 初始化底层 Manager
        self.user_manager = UserManager()
        self.category_manager = CategoryManager()
        self.template_manager = TemplateManager(self.category_manager)
        
        # 处理循环引用注入
        self.category_manager.set_template_manager(self.template_manager)

        # 2. 初始化高层 Service
        self.category_service = CategoryService(self.category_manager, self.template_manager)
        self.template_service = TemplateService(self.template_manager, self.category_manager, self.user_manager)
        self.config_service = ConfigService(self.user_manager)
        self.connection_service = ConnectionService(self.user_manager)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ServiceContext()
        return cls._instance


# 导出全局实例（单例模式）
service_bus = ServiceContext.instance()
