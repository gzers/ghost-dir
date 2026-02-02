"""
模板服务 (Template Service)
负责模板的过滤、搜索、CRUD 以及导入导出业务编排
"""
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass

from src.data.template_manager import TemplateManager
from src.data.category_manager import CategoryManager
from src.data.user_manager import UserManager
from src.data.model import Template


@dataclass
class TemplateViewModel:
    """模板展示模型"""
    id: str
    name: str
    category_id: str
    category_name: str
    category_full_path: str
    description: str
    icon: str
    default_src: str
    is_valid: bool = True
    is_custom: bool = False
    tags: List[str] = None


class TemplateService:
    """模板业务服务"""

    def __init__(self, template_manager: TemplateManager, category_manager: CategoryManager, user_manager: UserManager):
        self.manager = template_manager
        self.category_manager = category_manager
        self.user_manager = user_manager

    def get_filtered_templates(
        self, 
        category_id: str = "all", 
        search_text: str = ""
    ) -> List[TemplateViewModel]:
        """
        统一过滤逻辑（搜索词 + 分类范围）
        实现原 LibraryView._filter_templates 的核心逻辑
        """
        search_text = search_text.strip().lower()
        
        # 1. 确定基础模板池
        if category_id == "all":
            base_templates = self.manager.get_all_templates()
        else:
            base_templates = self.manager.get_templates_by_category_recursive(category_id)
            
        # 2. 搜索过滤
        filtered = []
        for tpl in base_templates:
            if not search_text:
                filtered.append(tpl)
                continue
            
            # 匹配逻辑：名称、描述、标签、分类全名
            tags_str = ' '.join(getattr(tpl, 'tags', [])).lower()
            cat_name = ""
            cat = self.category_manager.get_category_by_id(tpl.category_id)
            if cat:
                cat_name = getattr(cat, 'full_path_name', cat.name).lower()

            if (search_text in tpl.name.lower() or 
                (tpl.description and search_text in tpl.description.lower()) or
                (search_text in tags_str) or
                (search_text in cat_name)):
                filtered.append(tpl)
                
        # 3. 转换为 ViewModel
        return [self._to_view_model(t) for t in filtered]

    def _to_view_model(self, t: Template) -> TemplateViewModel:
        """模型转换"""
        cat = self.category_manager.get_category_by_id(t.category_id)
        cat_name = cat.name if cat else "未知"
        cat_full = getattr(cat, 'full_path_name', cat_name)
        
        return TemplateViewModel(
            id=t.id,
            name=t.name,
            category_id=t.category_id,
            category_name=cat_name,
            category_full_path=cat_full,
            description=t.description or "",
            icon=t.icon or "Folder",
            default_src=t.default_src,
            is_valid=self.manager.validate_template_path(t),
            is_custom=t.is_custom,
            tags=getattr(t, 'tags', [])
        )

    def add_template(self, template: Template) -> Tuple[bool, str]:
        """添加模板逻辑封装"""
        try:
            success = self.user_manager.add_custom_template(template)
            if success:
                self.manager.load_templates()
                return True, "模板添加成功"
            return False, "持久化失败"
        except Exception as e:
            return False, str(e)

    def update_template(self, template: Template) -> Tuple[bool, str]:
        """更新模板逻辑封装"""
        try:
            # 注意：此处逻辑需对齐 UserManager 接口
            if self.user_manager.has_custom_template(template.id):
                self.user_manager.remove_custom_template(template.id)
                self.user_manager.add_custom_template(template)
                self.manager.load_templates()
                return True, "模板更新成功"
            return False, "无法修改内置模板"
        except Exception as e:
            return False, str(e)

    def delete_template(self, template_id: str) -> Tuple[bool, str]:
        """删除模板核心逻辑"""
        try:
            if self.user_manager.remove_custom_template(template_id):
                self.manager.load_templates()
                return True, "成功移除自定义模板"
            return False, "无法删除内置模板或模板不存在"
        except Exception as e:
            return False, str(e)

    def batch_delete_templates(self, template_ids: List[str]) -> Tuple[bool, str]:
        """批量删除模板"""
        errors = []
        success_count = 0
        for tid in template_ids:
            success, msg = self.delete_template(tid)
            if success:
                success_count += 1
            else:
                errors.append(f"{tid}: {msg}")
        
        if not errors:
            return True, f"成功删除 {success_count} 个模板"
        return success_count > 0, f"删除了 {success_count} 个，失败 {len(errors)} 个"

    def export_to_file(self, file_path: str, options: Dict) -> Tuple[bool, str]:
        """导出业务落地"""
        return self.manager.export_to_file(file_path, **options)

    def import_from_file(self, file_path: str, options: Dict) -> Tuple[bool, str]:
        """导入业务落地"""
        success, msg = self.manager.import_from_file(file_path, **options)
        if success:
            self.manager.load_templates()
        return success, msg
