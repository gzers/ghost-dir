"""
智能扫描器
自动发现可管理的软件
"""
from typing import List
from ..data.model import Template, UserLink
from ..data.template_manager import TemplateManager
from ..data.user_manager import UserManager
import uuid


class SmartScanner:
    """智能扫描器"""
    
    def __init__(self, template_manager: TemplateManager, user_manager: UserManager):
        """
        初始化智能扫描器
        
        Args:
            template_manager: 模版管理器
            user_manager: 用户数据管理器
        """
        self.template_manager = template_manager
        self.user_manager = user_manager
    
    def scan(self) -> List[Template]:
        """
        扫描本机，发现可管理的软件
        
        Returns:
            发现的模版列表
        """
        discovered = []
        existing_paths = {link.source_path for link in self.user_manager.get_all_links()}
        
        for template in self.template_manager.get_all_templates():
            # 展开环境变量
            expanded_path = self.template_manager.expand_path(template.default_src)
            
            # 检查路径是否存在且未被管理
            if (self.template_manager.validate_template_path(template) and 
                expanded_path not in existing_paths):
                discovered.append(template)
        
        print(f"扫描完成，发现 {len(discovered)} 个可管理的软件")
        return discovered
    
    def import_templates(self, templates: List[Template], target_drive: str = "D:\\") -> int:
        """
        批量导入模版为用户连接
        
        Args:
            templates: 要导入的模版列表
            target_drive: 目标驱动器
            
        Returns:
            成功导入的数量
        """
        success_count = 0
        
        for template in templates:
            try:
                # 创建用户连接
                source_path = self.template_manager.expand_path(template.default_src)
                target_path = target_drive + source_path[3:]  # C:\xxx -> D:\xxx
                
                link = UserLink(
                    id=str(uuid.uuid4()),
                    name=template.name,
                    source_path=source_path,
                    target_path=target_path,
                    category=template.category,
                    template_id=template.id,
                    icon=template.icon
                )
                
                if self.user_manager.add_link(link):
                    success_count += 1
                    
            except Exception as e:
                print(f"导入模版失败 {template.name}: {e}")
        
        print(f"成功导入 {success_count}/{len(templates)} 个连接")
        return success_count
