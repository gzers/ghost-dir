"""
公共文案
包含通用操作、状态、分类、错误消息、对话框等
"""

COMMON_TEXTS = {
    # 通用操作文案
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
    "partial_success": "部分成功",
    "error": "错误",
    "warning": "警告",
    "info": "提示",
}

STATUS_TEXTS = {
    # 状态文案
    "disconnected": "未连接",
    "connected": "已连接",
    "ready": "就绪",
    "invalid": "失效",
    "running": "运行中",
    "stopped": "已停止",
}

CATEGORY_TEXTS = {
    # 分类文案
    "all": "全部",
    "uncategorized": "未分类",
    "game": "游戏",
    "browser": "浏览器",
    "social": "社交",
    "development": "开发工具",
    "media": "影音娱乐",
    "office": "办公软件",
    "other": "其他",
    
    # 细分与扫描向导常用词条
    "dev_tools": "开发工具",
    "cloud_storage": "云空间",
    "games": "游戏",
    "platforms": "游戏平台",
    "editors": "编辑器",
    "tools": "工具",
}

ERROR_TEXTS = {
    # 错误消息
    "permission_denied": "权限不足",
    "file_not_found": "文件不存在",
    "path_invalid": "路径无效",
    "operation_failed": "操作失败",
    "network_error": "网络错误",
    "unknown_error": "未知错误",
}

DIALOG_TEXTS = {
    # 对话框标题
    "add_link_title": "新增连接",
    "edit_link_title": "编辑连接",
    "category_manager_title": "分类管理",
    "scan_wizard_title": "智能扫描向导",
    "confirm_delete": "确认删除",
    "batch_operation": "批量操作",
}
