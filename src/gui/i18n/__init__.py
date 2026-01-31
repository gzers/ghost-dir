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
from .manager import I18nManager
from .zh_CN import TEXTS

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
    获取分类文案 (标准化公共实现)
    优先级: 实时配置名称 > i18n 翻译 > 智能全路径匹配 > 智能拆分降级 > 原值
    
    Args:
        category: 分类 ID 或名称
    
    Returns:
        最终显示的文案
    """
    if not category:
        return t("category.uncategorized")
        
    # 1. 优先从 CategoryManager 获取实时配置的名称 (解决拓展性)
    try:
        from src.data.user_manager import UserManager
        cm = UserManager().category_manager
        cat_node = cm.get_category_by_id(category)
        if cat_node and cat_node.name:
            return cat_node.name
    except:
        pass # 兜底逻辑
        
    # 2. 内部映射表：处理早期硬编码代号或常见变体
    INTERNAL_MAP = {
        "all": "all",
        "全部": "all",
        "uncategorized": "uncategorized",
        "未分类": "uncategorized",
    }
    
    clean_cat = category.lower().strip()
    key_suffix = INTERNAL_MAP.get(clean_cat, clean_cat.replace(" ", "_"))
    
    # 3. 尝试全路径/标准翻译
    text = t(f"category.{key_suffix}")
    
    # 4. 智能拆分匹配：支持处理 "dev_tools.editors" 这种复合扫描 ID
    if (text.startswith("[Missing:") or text == f"category.{key_suffix}") and "." in key_suffix:
        segments = key_suffix.split(".")
        first_segment = segments[0]
        parent_text = t(f"category.{first_segment}")
        
        if not (parent_text.startswith("[Missing:") or parent_text == f"category.{first_segment}"):
            # 如果父类有翻译，尝试组合子类
            sub_segment = segments[-1]
            sub_text = t(f"category.{sub_segment}")
            if not (sub_text.startswith("[Missing:") or sub_text == f"category.{sub_segment}"):
                return f"{parent_text} ({sub_text})"
            return parent_text

    # 5. 最终兜底：返回原值
    if text.startswith("[Missing:") or text == f"category.{key_suffix}":
        return category
        
    return text


__all__ = ['t', 'get_status_text', 'get_category_text']
