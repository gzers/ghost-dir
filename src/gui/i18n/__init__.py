"""
国际化 (i18n) 模块
提供多语言支持和文案管理

使用示例:
    from src.gui.i18n import t
    
    # 获取文案
    text = t("common.confirm")  # "确定"
    
    # 带参数的文案
    text = t("connected.selected_count", count=5)  # "已选择 5 项"
"""
from src.gui.i18n.manager import I18nManager
from src.gui.i18n.zh_CN import TEXTS

# 创建全局实例并设置文案
_i18n = I18nManager()
_i18n.set_texts(TEXTS)


def t(key: str, **kwargs) -> str:
    """
    获取文案的快捷函数
    
    Args:
        key: 文案键,支持点号分隔的路径,如 "common.confirm"
        **kwargs: 动态参数,用于替换文案中的占位符
    
    Returns:
        文案字符串
    
    Example:
        >>> t("common.confirm")
        "确定"
        >>> t("connected.msg_establish_success", name="Chrome")
        "已成功建立连接:Chrome"
    """
    return _i18n.get(key, **kwargs)


def get_status_text(status: str) -> str:
    """
    获取状态文案
    
    Args:
        status: 状态值 (disconnected, connected, ready, invalid)
    
    Returns:
        状态文案
    """
    return t(f"status.{status}")


def get_category_text(category: str) -> str:
    """
    获取分类名称
    严格优先从 CategoryManager 获取 config/categories.json 中定义的名称
    
    Args:
        category: 分类 ID
    
    Returns:
        配置文件中定义的名称，若不存在则返回原 ID
    """
    if not category:
        return t("category.uncategorized")
        
    try:
        from src.data.user_manager import UserManager
        cat_mgr = UserManager().category_manager
        cat_node = cat_mgr.get_category_by_id(category)
        if cat_node and cat_node.name:
            return cat_node.name
    except:
        pass
        
    return category


__all__ = ['t', 'get_status_text', 'get_category_text']
