"""
模版管理器
管理只读模版库，支持多数据源加载
"""
import json
import os
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from datetime import datetime
from ..data.model import Template
from ..common.config import (
    DEFAULT_TEMPLATES_CONFIG, TEMPLATE_CACHE_FILE,
    LEGACY_CATEGORY_MAP, APP_VERSION
)


class TemplateManager:
    """模版管理器"""
    
    def __init__(self, category_manager=None):
        """初始化模版管理器"""
        self.templates: Dict[str, Template] = {}
        self.cache_metadata: Dict = {}  # 缓存元数据（版本、更新时间等）
        self.category_manager = category_manager  # 分类管理器引用
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
            
            # 自动补全路径信息
            self._enrich_template_paths()
            
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
            self.templates = {item['id']: Template.from_dict(item) for item in templates_data}
            self.cache_metadata = {
                'version': data.get('version', '1.0.0'),
                'last_updated': data.get('last_updated', ''),
                'source': 'default_config'
            }
            # 自动补全路径信息
            self._enrich_template_paths()
            
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
        """搜索模版（支持名称、ID、以及所属分类名称）"""
        keyword = keyword.lower()
        results = []
        
        # 预先获取分类 ID 到名称的映射，以便支持按分类名搜索
        cat_map = {}
        if self.category_manager:
            cat_map = {c.id: c.name.lower() for c in self.category_manager.get_all_categories()}
        
        for template in self.get_all_templates():
            # 基础字段匹配
            match = (keyword in template.name.lower() or 
                    keyword in template.id.lower())
            
            # 分类名匹配
            if not match and self.category_manager:
                cat_name = cat_map.get(template.category_id, "")
                if keyword in cat_name:
                    match = True
                    
            if match:
                results.append(template)
        
        return results
    
    def get_templates_by_category(self, category_id: str) -> List[Template]:
        """根据分类 ID 获取模版"""
        return [t for t in self.get_all_templates() if t.category_id == category_id]
    
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
        """获取所有使用过的分类 ID"""
        categories = set()
        for template in self.get_all_templates():
            categories.add(template.category_id)
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

    def _enrich_template_paths(self):
        """为所有模板填充分类全路径信息"""
        if not self.category_manager:
            return
            
        for template in self.templates.values():
            category = self.category_manager.get_category_by_id(template.category_id)
            if category:
                # 确保分类已经有了全路径信息（如果还没保存过可能为空）
                if not category.full_path_code:
                    self.category_manager._update_all_full_paths()
                template.category_path_code = category.full_path_code
                template.category_path_name = category.full_path_name
    
    # ========== 分类系统集成方法 ==========
    
    def set_category_manager(self, category_manager):
        """设置分类管理器引用"""
        self.category_manager = category_manager
    
    def get_templates_by_category(self, category_id: str) -> List[Template]:
        """
        获取指定分类下的所有模板
        
        Args:
            category_id: 分类ID
            
        Returns:
            模板列表
        """
        return [
            template for template in self.templates.values()
            if template.category_id == category_id
        ]
    
    def get_templates_by_category_recursive(self, category_id: str) -> List[Template]:
        """
        递归获取指定分类及其所有子分类下的模板
        
        Args:
            category_id: 分类ID
            
        Returns:
            模板列表
        """
        if not self.category_manager:
            return self.get_templates_by_category(category_id)
        
        # 获取所有子孙分类
        category_ids = {category_id}
        descendants = self.category_manager._get_all_descendants(category_id)
        category_ids.update(c.id for c in descendants)
        
        # 获取所有相关模板
        templates = []
        for template in self.templates.values():
            if template.category_id in category_ids:
                templates.append(template)
        
        return templates
    
    def validate_all_templates(self) -> List[Template]:
        """
        验证所有模板的分类是否有效，返回孤儿模板列表
        
        Returns:
            孤儿模板列表
        """
        if not self.category_manager:
            return []
        
        orphaned = []
        
        for template in self.templates.values():
            # 获取模板的分类ID（兼容旧版）
            category_id = getattr(template, 'category_id', None)
            if not category_id:
                # 尝试从旧版 category 字段映射
                old_category = getattr(template, 'category', None)
                if old_category:
                    category_id = LEGACY_CATEGORY_MAP.get(old_category, 'uncategorized')
                    template.category_id = category_id
                else:
                    category_id = 'uncategorized'
                    template.category_id = category_id
            
            # 检查分类是否存在
            if not self.category_manager.get_category_by_id(category_id):
                orphaned.append(template)
                # 自动修复：归入"未分类"
                template.category_id = 'uncategorized'
        
        return orphaned
    
    # ========== 导出/导入功能 ==========
    
    def export_to_file(
        self,
        file_path: str,
        include_categories: bool = True,
        include_templates: bool = True,
        category_filter: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """
        导出模板库到文件
        
        Args:
            file_path: 导出文件路径
            include_categories: 是否包含分类
            include_templates: 是否包含模板
            category_filter: 要导出的分类ID列表（None表示全部）
            
        Returns:
            (是否成功, 消息)
        """
        try:
            export_data = {
                "export_version": "1.0.0",
                "export_date": datetime.now().isoformat(),
                "export_by": f"Ghost-Dir v{APP_VERSION}",
                "categories": [],
                "templates": []
            }
            
            if include_categories and self.category_manager:
                categories = self.category_manager.get_all_categories()
                if category_filter:
                    categories = [c for c in categories if c.id in category_filter]
                export_data["categories"] = [
                    {
                        "id": c.id,
                        "name": c.name,
                        "parent_id": c.parent_id,
                        "icon": c.icon,
                        "order": c.order
                    }
                    for c in categories
                ]
            
            if include_templates:
                templates = list(self.templates.values())
                if category_filter:
                    templates = [
                        t for t in templates
                        if getattr(t, 'category_id', getattr(t, 'category', 'uncategorized')) in category_filter
                    ]
                export_data["templates"] = [
                    {
                        "id": t.id,
                        "name": t.name,
                        "default_src": t.default_src,
                        "category_id": getattr(t, 'category_id', getattr(t, 'category', 'uncategorized')),
                        "default_target": getattr(t, 'default_target', None),
                        "icon": t.icon,
                        "description": t.description
                    }
                    for t in templates
                ]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True, f"成功导出 {len(export_data['categories'])} 个分类和 {len(export_data['templates'])} 个模板"
        
        except Exception as e:
            return False, f"导出失败: {str(e)}"
    
    def import_from_file(
        self,
        file_path: str,
        conflict_strategy: str = "skip"
    ) -> Tuple[bool, str]:
        """
        从文件导入模板库
        
        Args:
            file_path: 导入文件路径
            conflict_strategy: 冲突处理策略 (skip, overwrite, rename)
            
        Returns:
            (是否成功, 消息)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # 验证文件格式
            if "export_version" not in import_data:
                return False, "无效的导出文件格式"
            
            # ID 映射表：旧ID -> 新ID
            category_id_map = {}
            
            # 1. 导入分类，记录ID映射
            imported_categories = 0
            if self.category_manager:
                for cat_data in import_data.get("categories", []):
                    from ..data.model import CategoryNode
                    original_id = cat_data["id"]
                    category = CategoryNode(**cat_data)
                    
                    new_id, renamed = self.category_manager.add_category_with_conflict(
                        category, conflict_strategy
                    )
                    
                    if renamed and new_id:
                        category_id_map[original_id] = new_id
                    
                    if new_id:
                        imported_categories += 1
            
            # 2. 导入模板，使用映射表修正 category_id
            imported_templates = 0
            orphaned_templates = []
            
            for tpl_data in import_data.get("templates", []):
                template = Template(**tpl_data)
                
                # 修正 category_id
                if template.category_id in category_id_map:
                    template.category_id = category_id_map[template.category_id]
                
                # 检查分类是否存在
                if self.category_manager and not self.category_manager.get_category_by_id(template.category_id):
                    orphaned_templates.append(template)
                    template.category_id = "uncategorized"
                
                # 处理冲突
                if template.id in self.templates:
                    if conflict_strategy == "skip":
                        continue
                    elif conflict_strategy == "overwrite":
                        self.templates[template.id] = template
                    elif conflict_strategy == "rename":
                        counter = 1
                        new_id = f"{template.id}_{counter}"
                        while new_id in self.templates:
                            counter += 1
                            new_id = f"{template.id}_{counter}"
                        template.id = new_id
                        self.templates[new_id] = template
                else:
                    self.templates[template.id] = template
                
                imported_templates += 1
            
            # 提示
            message = f"成功导入 {imported_categories} 个分类和 {imported_templates} 个模板"
            if orphaned_templates:
                message += f"\n有 {len(orphaned_templates)} 个模板的分类不存在，已归入'未分类'"
            
            return True, message
        
        except Exception as e:
            return False, f"导入失败: {str(e)}"
