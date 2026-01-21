"""
用户数据管理器
管理用户连接数据
"""
import json
import uuid
from typing import List, Optional
from datetime import datetime
from ..data.model import UserLink, Category
from ..common.config import USER_DATA_FILE, DEFAULT_CATEGORY


class UserManager:
    """用户数据管理器"""
    
    def __init__(self):
        """初始化用户数据管理器"""
        self.links: List[UserLink] = []
        self.categories: List[Category] = []
        self.load_data()
    
    def load_data(self):
        """从 JSON 文件加载用户数据"""
        try:
            if not USER_DATA_FILE.exists():
                # 创建默认数据
                self._create_default_data()
                return
            
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载连接
            self.links = [UserLink(**item) for item in data.get('links', [])]
            
            # 加载分类
            self.categories = [Category(**item) for item in data.get('categories', [])]
            
            # 确保有默认分类
            if not any(c.name == DEFAULT_CATEGORY for c in self.categories):
                self.categories.append(Category(
                    id=str(uuid.uuid4()),
                    name=DEFAULT_CATEGORY
                ))
            
            print(f"已加载 {len(self.links)} 个连接，{len(self.categories)} 个分类")
            
        except Exception as e:
            print(f"加载用户数据时出错: {e}")
            self._create_default_data()
    
    def _create_default_data(self):
        """创建默认数据"""
        self.links = []
        self.categories = [
            Category(id=str(uuid.uuid4()), name="游戏"),
            Category(id=str(uuid.uuid4()), name="浏览器"),
            Category(id=str(uuid.uuid4()), name="社交"),
            Category(id=str(uuid.uuid4()), name=DEFAULT_CATEGORY),
        ]
        self.save_data()
    
    def save_data(self):
        """保存用户数据到 JSON 文件"""
        try:
            data = {
                'links': [vars(link) for link in self.links],
                'categories': [vars(cat) for cat in self.categories]
            }
            
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"保存用户数据时出错: {e}")
    
    # ========== 连接管理 ==========
    
    def add_link(self, link: UserLink) -> bool:
        """添加连接"""
        try:
            # 检查是否已存在
            if any(l.id == link.id for l in self.links):
                print(f"连接已存在: {link.id}")
                return False
            
            self.links.append(link)
            self.save_data()
            return True
            
        except Exception as e:
            print(f"添加连接时出错: {e}")
            return False
    
    def remove_link(self, link_id: str) -> bool:
        """删除连接"""
        try:
            self.links = [l for l in self.links if l.id != link_id]
            self.save_data()
            return True
            
        except Exception as e:
            print(f"删除连接时出错: {e}")
            return False
    
    def update_link(self, link: UserLink) -> bool:
        """更新连接"""
        try:
            for i, l in enumerate(self.links):
                if l.id == link.id:
                    link.updated_at = datetime.now().isoformat()
                    self.links[i] = link
                    self.save_data()
                    return True
            
            print(f"连接不存在: {link.id}")
            return False
            
        except Exception as e:
            print(f"更新连接时出错: {e}")
            return False
    
    def get_link_by_id(self, link_id: str) -> Optional[UserLink]:
        """根据 ID 获取连接"""
        for link in self.links:
            if link.id == link_id:
                return link
        return None
    
    def get_all_links(self) -> List[UserLink]:
        """获取所有连接"""
        return self.links
    
    def get_links_by_category(self, category: str) -> List[UserLink]:
        """根据分类获取连接"""
        return [l for l in self.links if l.category == category]
    
    def update_link_size(self, link_id: str, size: int) -> bool:
        """更新连接的空间大小缓存"""
        link = self.get_link_by_id(link_id)
        if link:
            link.last_known_size = size
            return self.update_link(link)
        return False
    
    # ========== 分类管理 ==========
    
    def add_category(self, category: Category) -> bool:
        """添加分类"""
        try:
            # 检查是否已存在
            if any(c.name == category.name for c in self.categories):
                print(f"分类已存在: {category.name}")
                return False
            
            self.categories.append(category)
            self.save_data()
            return True
            
        except Exception as e:
            print(f"添加分类时出错: {e}")
            return False
    
    def remove_category(self, category_id: str) -> bool:
        """删除分类"""
        try:
            # 不允许删除默认分类
            category = self.get_category_by_id(category_id)
            if category and category.name == DEFAULT_CATEGORY:
                print("不能删除默认分类")
                return False
            
            # 将该分类下的连接移到默认分类
            for link in self.links:
                if link.category == category.name:
                    link.category = DEFAULT_CATEGORY
            
            self.categories = [c for c in self.categories if c.id != category_id]
            self.save_data()
            return True
            
        except Exception as e:
            print(f"删除分类时出错: {e}")
            return False
    
    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """根据 ID 获取分类"""
        for category in self.categories:
            if category.id == category_id:
                return category
        return None
    
    def get_all_categories(self) -> List[Category]:
        """获取所有分类"""
        return self.categories
