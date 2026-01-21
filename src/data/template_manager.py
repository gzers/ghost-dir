"""
模版管理器
管理只读模版库
"""
import json
import os
from typing import List, Optional
from pathlib import Path
from ..data.model import Template
from ..common.resource_loader import get_data_file_path


class TemplateManager:
    """模版管理器"""
    
    def __init__(self):
        """初始化模版管理器"""
        self.templates: List[Template] = []
        self.load_templates()
    
    def load_templates(self):
        """从 JSON 文件加载模版"""
        try:
            template_file = get_data_file_path("templates.json")
            
            if not template_file.exists():
                print(f"模版文件不存在: {template_file}")
                return
            
            with open(template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.templates = [Template(**item) for item in data]
            # Store templates in a dictionary keyed by ID
            self.templates = {item['id']: Template(**item) for item in data}
            print(f"已加载 {len(self.templates)} 个模版")
            
        except Exception as e:
            print(f"加载模版时出错: {e}")
    
    def get_all_templates(self) -> List[Template]:
        """
        获取所有模版（官方 + 自定义）
        v7.4: 合并用户自定义模版
        """
        # 官方模版
        official_templates = list(self.templates.values())
        
        # 自定义模版（从 UserManager 获取）
        try:
            from .user_manager import UserManager
            user_manager = UserManager()
            custom_templates = user_manager.get_custom_templates()
            
            # 合并并返回
            return official_templates + custom_templates
        except Exception as e:
            print(f"获取自定义模版时出错: {e}")
            return official_templates
    
    def get_official_templates(self) -> List[Template]:
        """仅获取官方模版"""
        return list(self.templates.values())
    
    def get_template_by_id(self, template_id: str) -> Optional[Template]:
        """
        根据 ID 获取模版（官方或自定义）
        v7.4: 支持查找自定义模版
        """
        # 先查找官方模版
        if template_id in self.templates:
            return self.templates[template_id]
        
        # 再查找自定义模版
        try:
            from .user_manager import UserManager
            user_manager = UserManager()
            for template in user_manager.get_custom_templates():
                if template.id == template_id:
                    return template
        except Exception as e:
            print(f"查找自定义模版时出错: {e}")
        
        return None
    
    def search_templates(self, keyword: str) -> List[Template]:
        """搜索模版"""
        keyword = keyword.lower()
        results = []
        
        for template in self.templates:
            if (keyword in template.name.lower() or 
                keyword in template.id.lower() or
                keyword in template.category.lower()):
                results.append(template)
        
        return results
    
    def get_templates_by_category(self, category: str) -> List[Template]:
        """根据分类获取模版"""
        return [t for t in self.templates if t.category == category]
    
    def expand_path(self, path: str) -> str:
        """
        展开路径中的环境变量
        
        Args:
            path: 包含环境变量的路径
            
        Returns:
            展开后的路径
        """
        return os.path.expandvars(path)
    
    def validate_template_path(self, template: Template) -> bool:
        """
        验证模版路径是否存在
        
        Args:
            template: 模版对象
            
        Returns:
            True 如果路径存在，否则 False
        """
        expanded_path = self.expand_path(template.default_src)
        return os.path.exists(expanded_path)
    
    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set()
        for template in self.templates:
            categories.add(template.category)
        return sorted(list(categories))
