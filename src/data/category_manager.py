"""
分类管理器
管理分类树结构，支持多层级分类
"""
import json
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from ..data.model import CategoryNode
from ..data.category_log import CategoryLogEntry, CategoryOperation
from ..common.config import CATEGORIES_CONFIG, CATEGORY_LOG_FILE, MAX_CATEGORY_DEPTH, SYSTEM_CATEGORIES


class CategoryManager:
    """分类管理器"""
    
    def __init__(self):
        """初始化分类管理器"""
        self.categories: Dict[str, CategoryNode] = {}
        self.template_manager = None  # 延迟注入，避免循环依赖
        self.logs: List[CategoryLogEntry] = []
        self.load_categories()
        self._load_logs()
    
    def set_template_manager(self, template_manager):
        """设置模板管理器引用（用于验证）"""
        self.template_manager = template_manager
    
    def load_categories(self) -> None:
        """从配置文件加载分类"""
        try:
            if not CATEGORIES_CONFIG.exists():
                print(f"分类配置文件不存在: {CATEGORIES_CONFIG}")
                self._create_default_category()
                return
            
            with open(CATEGORIES_CONFIG, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            categories_data = data.get('categories', [])
            self.categories = {
                item['id']: CategoryNode.from_dict(item)
                for item in categories_data
            }
            
            print(f"已加载 {len(self.categories)} 个分类")
            
        except Exception as e:
            print(f"加载分类配置失败: {e}")
            self._create_default_category()

    # ========== 日志管理 ==========

    def _load_logs(self):
        """加载操作日志"""
        if not CATEGORY_LOG_FILE.exists():
            return
        
        try:
            with open(CATEGORY_LOG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logs = [CategoryLogEntry.from_dict(item) for item in data]
        except Exception as e:
            print(f"加载分类日志失败: {e}")

    def _save_logs(self):
        """保存操作日志"""
        try:
            # 仅保留最近 1000 条日志
            if len(self.logs) > 1000:
                self.logs = self.logs[-1000:]
                
            with open(CATEGORY_LOG_FILE, 'w', encoding='utf-8') as f:
                data = [log.to_dict() for log in self.logs]
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存分类日志失败: {e}")

    def _log_operation(self, operation: CategoryOperation, category_id: str, category_name: str, details: Optional[Dict] = None):
        """记录操作日志"""
        from datetime import datetime
        entry = CategoryLogEntry(
            timestamp=datetime.now().isoformat(),
            operation=operation.value,
            category_id=category_id,
            category_name=category_name,
            details=details
        )
        self.logs.append(entry)
        self._save_logs()

    def get_recent_logs(self, limit: int = 50) -> List[CategoryLogEntry]:
        """获取最近的操作日志"""
        return self.logs[-limit:]
    
    def _create_default_category(self):
        """创建默认的"未分类"分类"""
        uncategorized = CategoryNode(
            id="uncategorized",
            name="未分类",
            order=99,
            is_builtin=True
        )
        self.categories = {"uncategorized": uncategorized}
    
    def save_categories(self):
        """保存分类到配置文件"""
        try:
            # 确保配置目录存在
            CATEGORIES_CONFIG.parent.mkdir(parents=True, exist_ok=True)
            
            # 转换为字典列表，按 order 字段排序
            categories_list = sorted(self.categories.values(), key=lambda x: x.order)
            
            # 更新全路径字段
            self._update_all_full_paths()
            
            categories_data = [cat.to_dict() for cat in categories_list]
            
            # 保存到文件
            data = {'categories': categories_data}
            with open(CATEGORIES_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"已保存 {len(self.categories)} 个分类到配置文件")
            return True
        except Exception as e:
            print(f"保存分类配置失败: {e}")
            return False
    
    # ========== 基础查询方法 ==========
    
    def get_all_categories(self) -> List[CategoryNode]:
        """获取所有分类"""
        return list(self.categories.values())
    
    def get_category_by_id(self, category_id: str) -> Optional[CategoryNode]:
        """根据ID获取分类"""
        return self.categories.get(category_id)
    
    def get_children(self, parent_id: Optional[str] = None) -> List[CategoryNode]:
        """
        获取指定父分类的所有子分类
        
        Args:
            parent_id: 父分类ID，None表示获取根分类
            
        Returns:
            子分类列表，按order排序
        """
        children = [
            cat for cat in self.categories.values()
            if cat.parent_id == parent_id
        ]
        return sorted(children, key=lambda x: x.order)
    
    def get_category_tree(self) -> List[CategoryNode]:
        """获取分类树（只返回根节点）"""
        return self.get_children(None)
    
    def is_leaf(self, category_id: str) -> bool:
        """
        判断是否为叶子分类
        
        Args:
            category_id: 分类ID
            
        Returns:
            True 如果是叶子分类（没有子分类）
        """
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        
        return category.is_leaf(list(self.categories.values()))
    
    # ========== 编辑方法 ==========
    
    def add_category(self, category: CategoryNode) -> Tuple[bool, str]:
        """
        添加分类
        
        Args:
            category: 分类对象
            
        Returns:
            (是否成功, 消息)
        """
        # 1. 检查ID是否已存在
        if category.id in self.categories:
            return False, f"分类ID '{category.id}' 已存在"
        
        # 2. 验证深度
        depth = category.get_depth(self.categories)
        if depth > MAX_CATEGORY_DEPTH:
            return False, f"分类层级不能超过 {MAX_CATEGORY_DEPTH} 层"
        
        # 3. 验证父分类是否可以添加子分类
        if category.parent_id:
            can_add, msg = self.can_add_child_category(category.parent_id)
            if not can_add:
                return False, msg
        
        # 4. 添加分类
        self.categories[category.id] = category
        self._clear_depth_cache()
        
        # 5. 保存到配置文件
        self.save_categories()
        # 记录日志
        self._log_operation(CategoryOperation.CREATE, category.id, category.name, {
            "parent_id": category.parent_id,
            "order": category.order
        })
        return True, f"分类 '{category.name}' 添加成功"
    
    def update_category(self, category: CategoryNode) -> Tuple[bool, str]:
        """
        更新分类
        
        Args:
            category: 分类对象
            
        Returns:
            (是否成功, 消息)
        """
        # 1. 检查分类是否存在
        if category.id not in self.categories:
            return False, f"分类 '{category.id}' 不存在"
        
        old_category = self.categories[category.id]
        
        # 2. 禁止修改系统分类的关键属性
        if category.id in SYSTEM_CATEGORIES:
            if old_category.parent_id != category.parent_id:
                return False, "系统分类的父分类无法修改"
        
        # 3. 检测循环依赖
        if category.parent_id:
            if self._has_circular_dependency(category.id, category.parent_id):
                return False, "不能将分类移动到自己的子分类下，这会造成循环依赖"
        
        # 4. 验证深度
        depth = category.get_depth(self.categories)
        if depth > MAX_CATEGORY_DEPTH:
            return False, f"分类层级不能超过 {MAX_CATEGORY_DEPTH} 层"
        
        # 5. 更新分类
        self.categories[category.id] = category
        self._clear_depth_cache()
        
        # 6. 保存到配置文件
        self.save_categories()
        self._log_operation(CategoryOperation.UPDATE, category.id, category.name, {
            "old_name": old_category.name,
            "old_parent_id": old_category.parent_id,
            "new_parent_id": category.parent_id,
            "old_order": old_category.order,
            "new_order": category.order
        })
        
        return True, f"成功更新分类 '{category.name}'"
    
    def delete_category(self, category_id: str) -> Tuple[bool, str]:
        """
        删除分类
        
        Args:
            category_id: 分类ID
            
        Returns:
            (是否成功, 消息)
        """
        # 1. 检查分类是否存在
        if category_id not in self.categories:
            return False, "分类不存在"
        
        # 2. 禁止删除系统分类
        if category_id in SYSTEM_CATEGORIES:
            return False, "系统分类无法删除"
        
        # 3. 检查当前分类下是否有模板
        if self.template_manager:
            templates = self.template_manager.get_templates_by_category(category_id)
            if templates:
                category_name = self.get_category_by_id(category_id).name
                return False, f"分类 '{category_name}' 下有 {len(templates)} 个模板，无法删除"
        
        # 4. 递归检查所有子分类是否有模板
        all_children = self._get_all_descendants(category_id)
        if self.template_manager:
            for child in all_children:
                child_templates = self.template_manager.get_templates_by_category(child.id)
                if child_templates:
                    return False, f"子分类 '{child.name}' 下有 {len(child_templates)} 个模板，无法删除"
        
        # 5. 递归删除所有子分类（从叶子开始）
        children_ids = [child.id for child in all_children]
        for child_id in reversed(children_ids):
            if child_id in self.categories:
                del self.categories[child_id]
        
        # 6. 删除当前分类
        category_name = self.categories[category_id].name
        del self.categories[category_id]
        self._clear_depth_cache()
        
        # 7. 保存到配置文件
        self.save_categories()
        
        self._log_operation(CategoryOperation.DELETE, category_id, category_name, {
            "had_children": len(children_ids) > 0,
            "children_count": len(children_ids)
        })
        
        child_count = len(all_children)
        if child_count > 0:
            return True, f"已删除分类 '{category_name}' 及其 {child_count} 个子分类"
        else:
            return True, f"已删除分类 '{category_name}'"
    
    def rename_category(self, category_id: str, new_name: str) -> Tuple[bool, str]:
        """
        重命名分类
        
        Args:
            category_id: 分类ID
            new_name: 新名称
            
        Returns:
            (是否成功, 消息)
        """
        # 1. 检查分类是否存在
        if category_id not in self.categories:
            return False, "分类不存在"
        
        category = self.categories[category_id]
        
        # 2. 禁止修改系统分类的名称
        if category_id in SYSTEM_CATEGORIES:
            return False, "系统分类无法重命名"
        
        # 3. 验证新名称不为空
        new_name = new_name.strip()
        if not new_name:
            return False, "分类名称不能为空"
        
        # 4. 验证同一父分类下名称唯一性
        siblings = self.get_children(category.parent_id)
        for sibling in siblings:
            if sibling.id != category_id and sibling.name == new_name:
                return False, f"同一层级下已存在名为 '{new_name}' 的分类"
        
        # 5. 更新名称
        old_name = category.name
        category.name = new_name
        
        # 6. 保存到配置文件
        self.save_categories()
        self._log_operation(CategoryOperation.RENAME, category_id, new_name, {
            "old_name": old_name
        })
        
        return True, f"已将分类 '{old_name}' 重命名为 '{new_name}'"
    
    def update_category_structure(self, structure_data: List[Tuple[str, Optional[str], int]]) -> Tuple[bool, str]:
        """
        批量更新分类的层级结构和顺序
        
        Args:
            structure_data: [(category_id, parent_id, new_order), ...]
            
        Returns:
            (是否成功, 消息)
        """
        # 1. 验证所有分类ID都存在
        for category_id, _, _ in structure_data:
            if category_id not in self.categories:
                return False, f"分类 '{category_id}' 不存在"
        
        # 2. 批量更新 parent_id 和 order 字段
        updated_count = 0
        for category_id, new_parent_id, new_order in structure_data:
            category = self.categories[category_id]
            changed = False
            
            if category.parent_id != new_parent_id:
                category.parent_id = new_parent_id
                changed = True
            
            if category.order != new_order:
                category.order = new_order
                changed = True
                
            if changed:
                updated_count += 1
        
        # 3. 清除深度缓存并保存
        if updated_count > 0:
            self._clear_depth_cache()
            self.save_categories()
            self._log_operation(CategoryOperation.UPDATE_STRUCTURE, "batch", "批量结构更新", {
                "updated_count": updated_count,
                "changes": structure_data # 可以记录更详细的变更
            })
            return True, f"已成功保存结构变更（共 {updated_count} 处修改）"
        else:
            return True, "结构未发生变化"

    def reorder_categories(self, category_orders: List[Tuple[str, int]]) -> Tuple[bool, str]:
        """
        (保持向后兼容) 批量更新分类的 order 字段
        """
        data = []
        for cat_id, order in category_orders:
            cat = self.get_category_by_id(cat_id)
            if cat:
                data.append((cat_id, cat.parent_id, order))
        return self.update_category_structure(data)
    
    # ========== 验证方法 ==========
    
    def can_add_child_category(self, parent_id: str) -> Tuple[bool, str]:
        """
        验证是否可以给指定分类添加子分类
        
        Args:
            parent_id: 父分类ID
            
        Returns:
            (是否可以, 错误信息)
        """
        # 检查父分类是否存在
        parent = self.get_category_by_id(parent_id)
        if not parent:
            return False, "父分类不存在"
        
        # 检查父分类下是否有模板
        if self.template_manager:
            templates = self.template_manager.get_templates_by_category(parent_id)
            if templates:
                return False, f"分类 '{parent.name}' 下有 {len(templates)} 个模板，请先移动模板后再添加子分类"
        
        return True, ""
    
    def _has_circular_dependency(self, category_id: str, new_parent_id: str) -> bool:
        """
        检测是否会造成循环依赖
        
        Args:
            category_id: 要移动的分类ID
            new_parent_id: 新的父分类ID
            
        Returns:
            True 如果会造成循环依赖
        """
        current_id = new_parent_id
        visited = set()
        
        while current_id:
            if current_id in visited:
                return True  # 已经存在循环
            
            if current_id == category_id:
                return True  # 新父分类是当前分类的子孙
            
            visited.add(current_id)
            parent = self.get_category_by_id(current_id)
            if not parent:
                break
            current_id = parent.parent_id
        
        return False
    
    def _get_all_descendants(self, category_id: str) -> List[CategoryNode]:
        """
        获取所有子孙分类
        
        Args:
            category_id: 分类ID
            
        Returns:
            所有子孙分类列表
        """
        descendants = []
        children = self.get_children(category_id)
        
        for child in children:
            descendants.append(child)
            descendants.extend(self._get_all_descendants(child.id))
        
        return descendants
    
    def _update_all_full_paths(self):
        """递归更新所有分类的全路径编码和名称"""
        # 获取所有根节点
        roots = self.get_children(None)
        
        for root in roots:
            self._recursive_update_path(root, "", "")

    def _recursive_update_path(self, node: CategoryNode, parent_path_code: str, parent_path_name: str):
        """递归计算节点路径"""
        # 计算编码部分：如果子 ID 以 "父ID." 开头，则仅提取后缀以去除冗余
        node_part_code = node.id
        if node.parent_id and node.id.startswith(f"{node.parent_id}."):
            node_part_code = node.id[len(node.parent_id) + 1:]
            
        if parent_path_code:
            node.full_path_code = f"{parent_path_code}/{node_part_code}"
            node.full_path_name = f"{parent_path_name}/{node.name}"
        else:
            node.full_path_code = node.id
            node.full_path_name = node.name
            
        # 递归更新子节点
        children = self.get_children(node.id)
        for child in children:
            self._recursive_update_path(child, node.full_path_code, node.full_path_name)

    def _clear_depth_cache(self):
        """清除所有深度缓存"""
        for cat in self.categories.values():
            cat._depth = -1
    
    # ========== 导入/导出支持 ==========
    
    def add_category_with_conflict(
        self,
        category: CategoryNode,
        conflict_strategy: str = "skip"
    ) -> Tuple[Optional[str], bool]:
        """
        添加分类（支持冲突处理）
        
        Args:
            category: 分类对象
            conflict_strategy: 冲突处理策略 (skip, overwrite, rename)
            
        Returns:
            (新ID, 是否重命名)
        """
        if category.id in self.categories:
            if conflict_strategy == "skip":
                return None, False
            elif conflict_strategy == "overwrite":
                self.categories[category.id] = category
                return category.id, False
            elif conflict_strategy == "rename":
                # 生成新ID
                new_id = self._generate_unique_id(category.id)
                category.id = new_id
                self.categories[new_id] = category
                return new_id, True
        else:
            success, msg = self.add_category(category)
            if success:
                return category.id, False
            else:
                return None, False
    
    def _generate_unique_id(self, base_id: str) -> str:
        """生成唯一ID"""
        counter = 1
        while f"{base_id}_{counter}" in self.categories:
            counter += 1
        return f"{base_id}_{counter}"
