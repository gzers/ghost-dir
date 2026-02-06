"""
用户数据管理器
管理用户连接数据
"""
import json
import uuid
from typing import List, Optional
from datetime import datetime
from dataclasses import asdict
from src.data.model import UserLink, Category, Template
from src.common.config import USER_LINKS_FILE, DEFAULT_CATEGORY


class UserManager:
    """用户数据管理器 (单例)"""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化用户数据管理器"""
        if UserManager._initialized:
            return
        
        self.data_file = USER_LINKS_FILE
        self.links: List[UserLink] = []
        self.ignored_ids: List[str] = []  # 扫描忽略名单
        
        # 集成分类管理器
        from src.data.category_manager import CategoryManager
        self.category_manager = CategoryManager()
        
        self._ensure_data_dir()
        self._load_data()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        from src.common.config import USER_LINKS_FILE
        USER_LINKS_FILE.parent.mkdir(parents=True, exist_ok=True)

    def reload(self):
        """重新从磁盘加载最新数据，用于多实例同步"""
        self._load_data()

    def _load_data(self):
        """加载用户链接数据"""
        from src.common.config import USER_LINKS_FILE
        if not USER_LINKS_FILE.exists():
            self._init_default_data()
            return

        try:
            with open(USER_LINKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 数据迁移
            data = self._migrate_data(data)

            # 加载连接
            self.links = [
                UserLink(**link_data)
                for link_data in data.get('links', [])
            ]

            # 加载忽略列表
            self.ignored_ids = data.get('ignored_ids', [])
            
            print(f"已加载 {len(self.links)} 个连接")
            
            UserManager._initialized = True
            
        except Exception as e:
            print(f"加载用户数据时出错: {e}")
            self._init_default_data()
    
    def _migrate_data(self, data: dict) -> dict:
        """数据迁移"""
        # 确保有 ignored_ids 字段
        if 'ignored_ids' not in data:
            data['ignored_ids'] = []

        # 补全链接的全路径字段
        for link in data.get('links', []):
            if 'category_path_code' not in link or not link['category_path_code']:
                cat = self.category_manager.get_category_by_id(link.get('category'))
                if cat:
                    link['category_path_code'] = getattr(cat, 'full_path_code', "")
                    link['category_path_name'] = getattr(cat, 'full_path_name', "")

        return data
    
    def _init_default_data(self):
        """创建默认数据"""
        self.links = []
        self.ignored_ids = []
        self._save_data()
    
    def _save_data(self):
        """保存用户链接数据"""
        from src.common.config import USER_LINKS_FILE
        try:
            data = {
                'links': [asdict(link) for link in self.links],
                'ignored_ids': self.ignored_ids
            }

            with open(USER_LINKS_FILE, 'w', encoding='utf-8') as f:
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
            
            self._enrich_link_path(link)
            self.links.append(link)
            self._save_data()
            # 发射全局通知
            from src.common.signals import signal_bus
            signal_bus.data_refreshed.emit()
            return True
            
        except Exception as e:
            print(f"添加连接时出错: {e}")
            return False
    
    def remove_link(self, link_id: str) -> bool:
        """删除连接"""
        try:
            self.links = [l for l in self.links if l.id != link_id]
            self._save_data()
            # 发射全局通知
            from src.common.signals import signal_bus
            signal_bus.data_refreshed.emit()
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
                    self._enrich_link_path(link)
                    self.links[i] = link
                    self._save_data()
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
    
    def get_links_by_category(self, category_id: str) -> List[UserLink]:
        """根据分类 ID 获取连接"""
        return [l for l in self.links if l.category == category_id]
    
    def update_link_size(self, link_id: str, size: int) -> bool:
        """更新连接的空间大小缓存"""
        link = self.get_link_by_id(link_id)
        if link:
            link.last_known_size = size
            return self.update_link(link)
        return False
    
    # ========== 忽略名单管理 ==========
    
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
    
    # ========== 辅助方法 ==========

    def has_link_for_template(self, template_id: str) -> bool:
        """检查是否已有该模版的连接"""
        return any(link.template_id == template_id for link in self.links)

    def _enrich_link_path(self, link: UserLink):
        """为单个链接填充分类全路径信息"""
        if not self.category_manager:
            return
            
        cat = self.category_manager.get_category_by_id(link.category)
        if cat:
            link.category_path_code = cat.full_path_code
            link.category_path_name = cat.full_path_name
