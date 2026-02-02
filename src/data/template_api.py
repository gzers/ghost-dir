"""
模板 API 客户端（预留）
未来用于从远程服务器获取模板数据
"""
from typing import List, Dict, Optional
from src.data.model import Template


class TemplateAPIClient:
    """模板 API 客户端（预留接口）"""
    
    def __init__(self, api_url: str = ""):
        """
        初始化 API 客户端
        
        Args:
            api_url: API 服务器地址
        """
        self.api_url = api_url
        self.timeout = 10  # 请求超时时间（秒）
    
    async def fetch_templates(self) -> List[Template]:
        """
        从 API 获取模板列表（待实现）
        
        Returns:
            模板列表
            
        Raises:
            NotImplementedError: 当前未实现
        """
        raise NotImplementedError("API integration not yet implemented")
    
    async def fetch_template_by_id(self, template_id: str) -> Optional[Template]:
        """
        从 API 获取指定模板（待实现）
        
        Args:
            template_id: 模板 ID
            
        Returns:
            模板对象，如果不存在则返回 None
            
        Raises:
            NotImplementedError: 当前未实现
        """
        raise NotImplementedError("API integration not yet implemented")
    
    def is_available(self) -> bool:
        """
        检查 API 是否可用
        
        Returns:
            当前始终返回 False（未实现）
        """
        return False
    
    async def check_updates(self) -> Dict:
        """
        检查模板更新（待实现）
        
        Returns:
            更新信息字典
            
        Raises:
            NotImplementedError: 当前未实现
        """
        raise NotImplementedError("API integration not yet implemented")
