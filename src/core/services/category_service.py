"""
分类服务 (Category Service)
负责分类的业务逻辑编排、数据校验及 ViewModel 转换
"""
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from src.data.category_manager import CategoryManager
from src.data.template_manager import TemplateManager
from src.data.model import CategoryNode


@dataclass
class CategoryViewModel:
    """分类展示模型"""
    id: str
    name: str
    parent_id: Optional[str]
    order: int
    is_builtin: bool
    depth: int
    full_path_name: str
    item_count: int = 0  # 该分类下的直接模板数量
    has_children: bool = False
    is_leaf: bool = True


class CategoryService:
    """分类业务服务"""

    def __init__(self, category_manager: CategoryManager, template_manager: TemplateManager):
        self.manager = category_manager
        self.template_manager = template_manager

    def get_category_tree_view(self) -> List[CategoryViewModel]:
        """获取用于树形展示的扁平化 ViewModel 列表"""
        all_nodes = self.manager.get_all_categories()
        # 按层级和顺序排序以便 UI 直接使用
        sorted_nodes = self._sort_nodes_recursive(None, all_nodes)
        
        view_models = []
        for node in sorted_nodes:
            is_leaf = self.manager.is_leaf(node.id)
            templates = self.template_manager.get_templates_by_category(node.id)
            
            vm = CategoryViewModel(
                id=node.id,
                name=node.name,
                parent_id=node.parent_id,
                order=node.order,
                is_builtin=node.is_builtin,
                depth=node.get_depth(self.manager.categories),
                full_path_name=getattr(node, 'full_path_name', node.name),
                item_count=len(templates),
                has_children=not is_leaf,
                is_leaf=is_leaf
            )
            view_models.append(vm)
        return view_models

    def _sort_nodes_recursive(self, parent_id: Optional[str], all_nodes: List[CategoryNode]) -> List[CategoryNode]:
        """递归排序节点"""
        children = [n for n in all_nodes if n.parent_id == parent_id]
        children.sort(key=lambda x: x.order)
        
        result = []
        for child in children:
            result.append(child)
            result.extend(self._sort_nodes_recursive(child.id, all_nodes))
        return result

    def validate_delete(self, category_id: str) -> Tuple[str, Optional[Dict]]:
        """
        校验删除操作并返回状态
        
        Returns:
            (status, context)
            status: 'SUCCESS', 'REQUIRED_CONFIRM', 'ERROR'
        """
        category = self.manager.get_category_by_id(category_id)
        if not category:
            return "ERROR", {"message": "分类不存在"}
        
        if category.is_builtin:
            return "ERROR", {"message": "系统内置分类无法删除"}

        # 检查依赖
        templates = self.template_manager.get_templates_by_category_recursive(category_id)
        if templates:
            return "REQUIRED_CONFIRM", {
                "message": f"分类 '{category.name}' 及其子分类下共有 {len(templates)} 个模板，删除后这些模板将变为'未分类'。是否继续？",
                "template_count": len(templates)
            }
        
        return "SUCCESS", None

    def execute_delete(self, category_id: str, force: bool = False) -> Tuple[bool, str]:
        """执行删除逻辑（原子事务）"""
        # 注意：此处未来可接入 TransactionEngine

        status, context = self.validate_delete(category_id)
        if status == "ERROR":
            return False, context["message"]
        
        if status == "REQUIRED_CONFIRM" and not force:
            return False, "需要确认依赖处理"

        # 如果有模板，先迁移到未分类
        templates = self.template_manager.get_templates_by_category_recursive(category_id)
        for tpl in templates:
            tpl.category_id = "uncategorized"
        
        # 实际调用 manager 删除（manager 内部会递归删除子分类）
        success, msg = self.manager.delete_category(category_id)
        return success, msg

    def add_category(self, name: str, parent_id: Optional[str] = None) -> Tuple[bool, str]:
        """业务封装：添加分类"""
        name = name.strip()
        if not name:
            return False, "分类名称不能为空"
        
        # 检查同级重名
        siblings = self.manager.get_children(parent_id)
        if any(s.name == name for s in siblings):
            return False, "同级目录下已存在相同名称的分类"

        # 验证父级是否允许添加（例如：父级不能已有模板）
        if parent_id:
            can_add, msg = self.manager.can_add_child_category(parent_id)
            if not can_add:
                return False, msg

        # 构造 ID
        import time
        category_id = f"cat_{int(time.time())}"
        
        new_node = CategoryNode(
            id=category_id,
            name=name,
            parent_id=parent_id,
            order=len(siblings) + 1
        )
        
        return self.manager.add_category(new_node)

    def update_category(self, category_node: CategoryNode) -> Tuple[bool, str]:
        """业务封装：更新分类"""
        # 实质上是透传给 manager，但此处可以增加业务层校验
        return self.manager.update_category(category_node)
