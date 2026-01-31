"""
智能扫描器
自动发现可管理的软件
"""
import os
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
        支持：1. 存在于模板库中的原始目录 2. C 盘已经建立的 Junction 连接点
        
        Returns:
            发现的模版列表
        """
        discovered = []
        existing_paths = {link.source_path for link in self.user_manager.get_all_links()}
        from .link_opt import is_junction
        
        for template in self.template_manager.get_all_templates():
            # 🆕 v7.4: 过滤已忽略的模版
            if self.user_manager.is_ignored(template.id):
                continue
                
            # 🆕 v7.4: 过滤已经在库中的模版（基于 template_id）
            if self.user_manager.has_link_for_template(template.id):
                continue

            # 展开环境变量
            expanded_path = self.template_manager.expand_path(template.default_src)
            
            # 校验逻辑：
            # 1. 如果路径是 Junction，说明可能已经手动建立过连接，属于“已建立链接”的自动导入
            # 2. 如果路径是普通目录且存在，属于“待迁移”的软件扫描
            if (os.path.exists(expanded_path) and expanded_path not in existing_paths):
                # 标记该模板发现时是否已经是连接状态，方便后续 import 处理
                setattr(template, '_auto_detected_junction', is_junction(expanded_path))
                discovered.append(template)
        
        print(f"扫描完成，发现 {len(discovered)} 个个通过或待管理的软件")
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
        from .link_opt import get_junction_target
        
        for template in templates:
            try:
                # 创建用户连接
                source_path = self.template_manager.expand_path(template.default_src)
                
                # 语义优化：如果探测到已经是 Junction，说明已经建立过链接，自动读取其目标路径
                is_manual_junction = getattr(template, '_auto_detected_junction', False)
                if is_manual_junction:
                    target_path = get_junction_target(source_path) or (target_drive + source_path[3:])
                else:
                    # 普通扫描导入，默认生成映射路径
                    target_path = target_drive + source_path[3:]  # C:\xxx -> D:\xxx
                
                # 获取分类（同步到分类树）
                # 兼容性修复：优先取 category_id，回滚到 category，最后才是 uncategorized
                cat_id = getattr(template, 'category_id', getattr(template, 'category', 'uncategorized'))
                
                link = UserLink(
                    id=str(uuid.uuid4()),
                    name=template.name,
                    source_path=source_path,
                    target_path=target_path,
                    category=cat_id,
                    template_id=template.id,
                    icon=template.icon
                )
                
                if self.user_manager.add_link(link):
                    success_count += 1
                    
            except Exception as e:
                print(f"导入模版失败 {template.name}: {e}")
        
        print(f"成功导入 {success_count}/{len(templates)} 个连接")
        return success_count
