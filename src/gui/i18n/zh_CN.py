"""
国际化文案配置
集中管理所有界面文案,方便后期多语言支持
"""
from typing import Dict, Any


class I18nManager:
    """国际化管理器"""
    
    _instance = None
    _current_language = "zh_CN"  # 当前语言
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化国际化管理器"""
        pass
    
    def get(self, key: str, **kwargs) -> str:
        """
        获取文案
        
        Args:
            key: 文案键,支持点号分隔的路径,如 "common.confirm"
            **kwargs: 动态参数,用于替换文案中的占位符
        
        Returns:
            文案字符串
        """
        keys = key.split(".")
        value = TEXTS
        
        try:
            for k in keys:
                value = value[k]
            
            # 如果有参数,进行替换
            if kwargs:
                return value.format(**kwargs)
            return value
        except (KeyError, TypeError):
            return f"[Missing: {key}]"
    
    def set_language(self, language: str):
        """设置当前语言"""
        self._current_language = language


# ========== 文案字典 ==========

TEXTS = {
    # ========== 通用文案 ==========
    "common": {
        "confirm": "确定",
        "cancel": "取消",
        "save": "保存",
        "delete": "删除",
        "edit": "编辑",
        "add": "添加",
        "remove": "移除",
        "close": "关闭",
        "refresh": "刷新",
        "search": "搜索",
        "filter": "筛选",
        "all": "全部",
        "yes": "是",
        "no": "否",
        "ok": "好的",
        "loading": "加载中...",
        "success": "成功",
        "failed": "失败",
        "error": "错误",
        "warning": "警告",
        "info": "提示",
    },
    
    # ========== 状态文案 ==========
    "status": {
        "disconnected": "未连接",
        "connected": "已连接",
        "ready": "就绪",
        "invalid": "失效",
        "running": "运行中",
        "stopped": "已停止",
    },
    
    # ========== 主控制台 ==========
    "console": {
        "title": "我的连接",
        "add_link": "新增连接",
        "scan_apps": "扫描本机应用",
        "refresh_size": "刷新统计",
        "batch_establish": "批量建立连接",
        "batch_disconnect": "批量断开连接",
        "clear_selection": "清除选择",
        "selected_count": "已选择 {count} 项",
        
        # 操作按钮
        "establish": "建立连接",
        "disconnect": "断开连接",
        "reconnect": "重新连接",
        
        # 表格列
        "col_name": "名称",
        "col_category": "分类",
        "col_source": "源路径",
        "col_target": "目标路径",
        "col_size": "占用空间",
        "col_status": "状态",
        "col_actions": "操作",
        
        # 空状态
        "empty_title": "暂无连接",
        "empty_desc": "点击「新增连接」或「扫描本机应用」开始管理",
        "empty_action": "开始使用",
        
        # 消息提示
        "msg_establish_success": "已成功建立连接:{name}",
        "msg_establish_failed": "建立连接失败:{name}",
        "msg_disconnect_success": "已成功断开连接:{name}",
        "msg_disconnect_failed": "断开连接失败:{name}",
        "msg_delete_confirm": "确定要删除连接 {name} 吗?\n这不会删除实际文件。",
        "msg_batch_establish_confirm": "将为 {count} 个软件建立连接,是否继续?",
        "msg_batch_disconnect_confirm": "将断开 {count} 个软件的连接,是否继续?",
        "msg_batch_complete": "成功: {success}/{total}",
        "msg_no_establish_items": "没有可建立连接的项目",
        "msg_no_disconnect_items": "没有可断开连接的项目",
        
        # 进程占用
        "process_warning_title": "文件占用警告",
        "process_warning_msg": "检测到以下进程正在占用文件:\n\n{processes}\n\n是否结束这些进程并继续?",
        "process_target_warning_msg": "检测到以下进程正在占用目标文件:\n\n{processes}\n\n是否结束这些进程并继续?",
        
        # 空间统计
        "refresh_size_confirm": "将计算 {count} 个连接的空间占用,可能需要一些时间。\n是否继续?",
        "refresh_size_progress": "正在计算",
        "refresh_size_complete": "计算完成 ✓",
        "refresh_size_result": "已更新 {count} 个连接的空间统计",
        "refresh_size_empty": "没有需要统计的连接",
    },
    
    # ========== 智能向导 ==========
    "wizard": {
        "title": "智能向导",
        "start_scan": "开始扫描",
        "stop_scan": "停止扫描",
        "import_selected": "一键导入",
        "scan_progress": "正在扫描...",
        "scan_complete": "扫描完成",
        "found_apps": "发现 {count} 个可管理的软件",
        "no_apps_found": "未发现可管理的软件",
        "import_success": "成功导入 {count} 个软件",
        "ignore_forever": "永久忽略",
        "ignored": "已忽略",
    },
    
    # ========== 模版库 ==========
    "library": {
        "title": "模版库",
        "official": "官方模版",
        "custom": "自定义模版",
        "search_placeholder": "搜索模版...",
        "filter_all": "全部",
        "filter_official": "官方",
        "filter_custom": "自定义",
        "template_count": "{count} 个模版",
        "add_custom": "添加自定义模版",
        "delete_template": "删除模版",
        "use_template": "使用模版",
        "empty_title": "暂无模版",
        "empty_desc": "添加自定义模版或从官方库导入",
    },
    
    # ========== 帮助页面 ==========
    "help": {
        "title": "帮助",
        "quick_start": "快速开始",
        "user_guide": "使用指南",
        "faq": "常见问题",
        "about": "关于",
    },
    
    # ========== 设置页面 ==========
    "settings": {
        "title": "设置",
        
        # 路径配置
        "group_path": "路径配置",
        "default_target_root": "默认仓库根路径",
        "select_path": "选择路径",
        "log_folder": "调试日志目录",
        "view_log": "查看日志",
        
        # 外观设置
        "group_appearance": "外观设置",
        "theme": "应用主题",
        "theme_desc": "选择应用的主题模式",
        "theme_system": "跟随系统",
        "theme_light": "亮色",
        "theme_dark": "暗色",
        "theme_changed": "主题已更新",
        "theme_changed_msg": "已切换到 {theme} 主题",
        
        # 启动设置
        "group_startup": "启动设置",
        "startup_page": "启动页面",
        "startup_page_desc": "设置程序启动时显示的页面",
        "startup_wizard": "智能向导",
        "startup_console": "我的连接",
        "startup_library": "模版库",
        "startup_changed": "设置已更新",
        "startup_changed_msg": "首启动页面已设置为 {page}",
    },
    
    # ========== 对话框 ==========
    "dialog": {
        "add_link_title": "新增连接",
        "edit_link_title": "编辑连接",
        "category_manager_title": "分类管理",
        "scan_wizard_title": "智能扫描向导",
        "confirm_delete": "确认删除",
        "batch_operation": "批量操作",
    },
    
    # ========== 分类 ==========
    "category": {
        "all": "全部",
        "uncategorized": "未分类",
        "game": "游戏",
        "browser": "浏览器",
        "social": "社交",
        "development": "开发工具",
        "media": "影音娱乐",
        "office": "办公软件",
        "other": "其他",
    },
    
    # ========== 错误消息 ==========
    "error": {
        "permission_denied": "权限不足",
        "file_not_found": "文件不存在",
        "path_invalid": "路径无效",
        "operation_failed": "操作失败",
        "network_error": "网络错误",
        "unknown_error": "未知错误",
    },
    
    # ========== 应用信息 ==========
    "app": {
        "name": "Ghost-Dir",
        "version": "7.4.0",
        "description": "Windows 跨磁盘目录迁移与连接管理工具",
        "author": "Ghost-Dir Team",
        "license": "MIT License",
    },
}


# ========== 快捷访问函数 ==========

# 创建全局实例
_i18n = I18nManager()


def t(key: str, **kwargs) -> str:
    """
    获取文案的快捷函数
    
    Args:
        key: 文案键
        **kwargs: 动态参数
    
    Returns:
        文案字符串
    
    Example:
        >>> t("common.confirm")
        "确定"
        >>> t("console.msg_establish_success", name="Chrome")
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
    获取分类文案
    
    Args:
        category: 分类值
    
    Returns:
        分类文案
    """
    # 先尝试从分类字典获取
    category_key = category.lower().replace(" ", "_")
    text = _i18n.get(f"category.{category_key}")
    
    # 如果没有找到,返回原值
    if text.startswith("[Missing:"):
        return category
    return text
