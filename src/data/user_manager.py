"""
用户数据管理器
管理用户连接数据
"""
import json
import uuid
from typing import List, Optional
from datetime import datetime
from dataclasses import asdict
from ..data.model import UserLink, Category, Template
from ..common.config import (
    USER_DATA_FILE, DEFAULT_CATEGORY,
    DEFAULT_TARGET_ROOT, DEFAULT_THEME, DEFAULT_THEME_COLOR, DEFAULT_STARTUP_PAGE
)


class UserManager:
    """用户数据管理器"""
    
    def __init__(self):
        """初始化用户数据管理器"""
        self.data_file = USER_DATA_FILE
        self.links: List[UserLink] = []
        self.categories: List[Category] = []

        # v7.4 新增字段
        self.custom_templates: List[Template] = []      # 用户自定义模版
        self.ignored_ids: List[str] = []                # 扫描忽略名单
        self.default_target_root: str = DEFAULT_TARGET_ROOT  # 默认仓库路径
        self.theme: str = DEFAULT_THEME                      # 主题：light/dark/system
        self.theme_color: str = DEFAULT_THEME_COLOR          # 主题色
        self.startup_page: str = DEFAULT_STARTUP_PAGE        # 首次打开：wizard/console/library
        
        self._ensure_data_dir()
        self._load_data()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        from ..common.config import CONFIG_FILE
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    def _load_data(self):
        """加载用户数据"""
        from ..common.config import CONFIG_FILE
        if not CONFIG_FILE.exists():
            self._init_default_data()
            return

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # v7.4 数据迁移
            data = self._migrate_data(data)

            # 加载连接
            self.links = [
                UserLink(**link_data)
                for link_data in data.get('links', [])
            ]

            # 加载分类
            self.categories = [
                Category(**cat_data)
                for cat_data in data.get('categories', [])
            ]

            # v7.4 新增字段
            self.custom_templates = [
                Template(**tpl_data)
                for tpl_data in data.get('custom_templates', [])
            ]
            self.ignored_ids = data.get('ignored_ids', [])
            self.default_target_root = data.get('default_target_root', DEFAULT_TARGET_ROOT)
            self.theme = data.get('theme', DEFAULT_THEME)      # 主题
            self.theme_color = data.get('theme_color', DEFAULT_THEME_COLOR)  # 主题色
            self.startup_page = data.get('startup_page', DEFAULT_STARTUP_PAGE)  # 首次打开
            
            # 确保有默认分类
            if not any(c.name == DEFAULT_CATEGORY for c in self.categories):
                self.categories.append(Category(
                    id=str(uuid.uuid4()),
                    name=DEFAULT_CATEGORY
                ))
            
            print(f"已加载 {len(self.links)} 个连接，{len(self.categories)} 个分类")
            print(f"已加载 {len(self.custom_templates)} 个自定义模版")
            
        except Exception as e:
            print(f"加载用户数据时出错: {e}")
            self._init_default_data()
    
    def _migrate_data(self, data: dict) -> dict:
        """数据迁移：v1.0 → v7.4"""
        # 添加新字段（如果不存在）
        if 'custom_templates' not in data:
            data['custom_templates'] = []
        if 'ignored_ids' not in data:
            data['ignored_ids'] = []
        if 'default_target_root' not in data:
            data['default_target_root'] = DEFAULT_TARGET_ROOT
        if 'theme' not in data:
            data['theme'] = DEFAULT_THEME
        if 'theme_color' not in data:
            data['theme_color'] = DEFAULT_THEME_COLOR
        if 'startup_page' not in data:
            data['startup_page'] = DEFAULT_STARTUP_PAGE

        return data
    
    def _init_default_data(self):
        """创建默认数据"""
        self.links = []
        self.categories = [
            Category(id=str(uuid.uuid4()), name="游戏"),
            Category(id=str(uuid.uuid4()), name="浏览器"),
            Category(id=str(uuid.uuid4()), name="社交"),
            Category(id=str(uuid.uuid4()), name=DEFAULT_CATEGORY),
        ]
        self._save_data()
    
    def _save_data(self):
        """保存用户数据"""
        from ..common.config import CONFIG_FILE
        try:
            data = {
                'links': [asdict(link) for link in self.links],
                'categories': [asdict(cat) for cat in self.categories],
                # v7.4 新增字段
                'custom_templates': [asdict(tpl) for tpl in self.custom_templates],
                'ignored_ids': self.ignored_ids,
                'default_target_root': self.default_target_root,
                'theme': self.theme,
                'theme_color': self.theme_color,
                'startup_page': self.startup_page
            }

            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存用户数据失败: {e}")
    
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
    
    # ========== v7.4 新增：自定义模版管理 ==========
    
    def add_custom_template(self, template: Template) -> bool:
        """添加自定义模版"""
        try:
            template.is_custom = True  # 标记为自定义
            self.custom_templates.append(template)
            self._save_data()
            return True
        except Exception as e:
            print(f"添加自定义模版时出错: {e}")
            return False
    
    def get_custom_templates(self) -> List[Template]:
        """获取所有自定义模版"""
        return self.custom_templates
    
    def remove_custom_template(self, template_id: str) -> bool:
        """删除自定义模版"""
        try:
            self.custom_templates = [t for t in self.custom_templates if t.id != template_id]
            self._save_data()
            return True
        except Exception as e:
            print(f"删除自定义模版时出错: {e}")
            return False
    
    # ========== v7.4 新增：忽略名单管理 ==========
    
    def add_to_ignore_list(self, template_id: str) -> bool:
        """添加到忽略名单"""
        try:
            if template_id not in self.ignored_ids:
                self.ignored_ids.append(template_id)
                self._save_data()
            return True
        except Exception as e:
            print(f"添加到忽略名单时出错: {e}")
            return False
    
    def remove_from_ignore_list(self, template_id: str) -> bool:
        """从忽略名单移除"""
        try:
            if template_id in self.ignored_ids:
                self.ignored_ids.remove(template_id)
                self._save_data()
            return True
        except Exception as e:
            print(f"从忽略名单移除时出错: {e}")
            return False
    
    def is_ignored(self, template_id: str) -> bool:
        """检查是否在忽略名单中"""
        return template_id in self.ignored_ids
    
    # ========== v7.4 新增：默认仓库路径管理 ==========
    
    def set_default_target_root(self, path: str) -> bool:
        """设置默认仓库路径"""
        try:
            self.default_target_root = path
            self._save_data()
            return True
        except Exception as e:
            print(f"设置默认仓库路径时出错: {e}")
            return False
    
    def get_default_target_root(self) -> str:
        """获取默认仓库路径"""
        return self.default_target_root
    
    # ========== v7.4 新增：辅助方法 ==========

    def has_link_for_template(self, template_id: str) -> bool:
        """检查是否已有该模版的连接"""
        return any(link.template_id == template_id for link in self.links)

    # ========== v7.4 新增：主题和首页管理 ==========

    def set_theme(self, theme: str) -> bool:
        """设置主题：light/dark/system"""
        if theme not in ['light', 'dark', 'system']:
            return False
        try:
            self.theme = theme
            self._save_data()
            return True
        except Exception as e:
            print(f"设置主题时出错: {e}")
            return False

    def get_theme(self) -> str:
        """获取当前主题"""
        return self.theme

    def set_startup_page(self, page: str) -> bool:
        """设置首启动页面：wizard/console/library"""
        if page not in ['wizard', 'console', 'library']:
            return False
        try:
            self.startup_page = page
            self._save_data()
            return True
        except Exception as e:
            print(f"设置首启动页面时出错: {e}")
            return False

    def get_startup_page(self) -> str:
        """获取首启动页面"""
        return self.startup_page

    def set_theme_color(self, color: str) -> bool:
        """设置主题色"""
        try:
            self.theme_color = color
            self._save_data()
            return True
        except Exception as e:
            print(f"设置主题色时出错: {e}")
            return False

    def get_theme_color(self) -> str:
        """获取主题色"""
        return self.theme_color
