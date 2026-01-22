"""
模版管理器
管理只读模版库，支持多数据源加载
"""
import json
import os
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime
from ..data.model import Template
from ..common.config import DEFAULT_TEMPLATES_CONFIG, TEMPLATE_CACHE_FILE


class TemplateManager:
    """模版管理器"""
    
    def __init__(self):
        """初始化模版管理器"""
        self.templates: Dict[str, Template] = {}
        self.cache_metadata: Dict = {}  # 缓存元数据（版本、更新时间等）
        self.load_templates()
    
    def load_templates(self):
        """
        从多数据源加载模版
        优先级：API 缓存 > 默认配置 > 空列表
        """
        try:
            # 1. 尝试从 API 缓存加载（如果存在且有效）
            if self._load_from_cache():
                print(f"已从缓存加载 {len(self.templates)} 个模版")
                return
            
            # 2. 回退到默认配置文件
            if self._load_from_default_config():
                print(f"已加载 {len(self.templates)} 个模版")
                return
            
            # 3. 如果都失败，使用空列表
            print("警告: 未能加载任何模版")
            self.templates = {}
            
        except Exception as e:
            print(f"加载模版时出错: {e}")
            self.templates = {}
    
    def _load_from_cache(self) -> bool:
        """
        从 API 缓存文件加载模版
        
        Returns:
            True 如果成功加载，否则 False
        """
        try:
            if not TEMPLATE_CACHE_FILE.exists():
                return False
            
            with open(TEMPLATE_CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证缓存有效性（可选：检查时间戳、版本等）
            if not self._is_cache_valid(data):
                return False
            
            # 加载模版数据
            templates_data = data.get('templates', [])
            self.templates = {item['id']: Template(**item) for item in templates_data}
            self.cache_metadata = {
                'version': data.get('version', 'unknown'),
                'last_updated': data.get('last_updated', ''),
                'source': 'api_cache'
            }
            
            return len(self.templates) > 0
            
        except Exception as e:
            print(f"从缓存加载模版失败: {e}")
            return False
    
    def _load_from_default_config(self) -> bool:
        """
        从默认配置文件加载模版
        
        Returns:
            True 如果成功加载，否则 False
        """
        try:
            if not DEFAULT_TEMPLATES_CONFIG.exists():
                print(f"默认模版配置文件不存在: {DEFAULT_TEMPLATES_CONFIG}")
                return False
            
            with open(DEFAULT_TEMPLATES_CONFIG, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载模版数据
            templates_data = data.get('templates', [])
            self.templates = {item['id']: Template(**item) for item in templates_data}
            self.cache_metadata = {
                'version': data.get('version', '1.0.0'),
                'last_updated': data.get('last_updated', ''),
                'source': 'default_config'
            }
            
            return len(self.templates) > 0
            
        except Exception as e:
            print(f"从默认配置加载模版失败: {e}")
            return False
    
    def _is_cache_valid(self, cache_data: Dict) -> bool:
        """
        验证缓存是否有效
        
        Args:
            cache_data: 缓存数据
            
        Returns:
            True 如果缓存有效，否则 False
        """
        # 当前简单实现：只要有 templates 字段就认为有效
        # 未来可以添加时间戳验证、版本检查等
        return 'templates' in cache_data and len(cache_data['templates']) > 0
    
    def update_template_cache(self, templates: List[Template], metadata: Dict = None):
        """
        更新模版缓存文件（预留给 API 集成使用）
        
        Args:
            templates: 模版列表
            metadata: 元数据（版本、更新时间等）
        """
        try:
            cache_data = {
                'version': metadata.get('version', '1.0.0') if metadata else '1.0.0',
                'last_updated': datetime.now().isoformat(),
                'source': 'api',
                'templates': [
                    {
                        'id': t.id,
                        'name': t.name,
                        'default_src': t.default_src,
                        'category': t.category,
                        'icon': t.icon,
                        'description': t.description
                    }
                    for t in templates
                ]
            }
            
            # 确保目录存在
            TEMPLATE_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(TEMPLATE_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"已更新模版缓存: {len(templates)} 个模版")
            
        except Exception as e:
            print(f"更新模版缓存失败: {e}")
    
    def clear_cache(self):
        """清除缓存文件，强制重新加载"""
        try:
            if TEMPLATE_CACHE_FILE.exists():
                TEMPLATE_CACHE_FILE.unlink()
                print("已清除模版缓存")
        except Exception as e:
            print(f"清除缓存失败: {e}")
    
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
        
        for template in self.templates.values():
            if (keyword in template.name.lower() or 
                keyword in template.id.lower() or
                keyword in template.category.lower()):
                results.append(template)
        
        return results
    
    def get_templates_by_category(self, category: str) -> List[Template]:
        """根据分类获取模版"""
        return [t for t in self.templates.values() if t.category == category]
    
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
        for template in self.templates.values():
            categories.add(template.category)
        return sorted(list(categories))
    
    # ========== API 集成预留方法 ==========
    
    def fetch_templates_from_api(self, api_url: str = "") -> bool:
        """
        从远程 API 获取模版（预留接口）
        
        Args:
            api_url: API 地址
            
        Returns:
            True 如果成功获取并更新缓存，否则 False
        """
        # TODO: 实现 API 调用逻辑
        raise NotImplementedError("API integration not yet implemented")
    
    def is_api_available(self) -> bool:
        """检查 API 是否可用（预留）"""
        # TODO: 实现 API 可用性检查
        return False
