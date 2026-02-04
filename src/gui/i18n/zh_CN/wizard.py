"""
智能向导页面文案
"""

WIZARD_TEXTS = {
    "title": "智能向导",
    
    # 扫描进度卡片
    "scan_card_title": "智能扫描",
    "scan_card_subtitle": "自动发现本机可管理的软件",
    "scan_card_icon": "🔍",
    
    # 按钮文案
    "start_scan": "开始扫描",
    "stop_scan": "停止扫描",
    "import_selected": "一键导入",
    "rescan": "重新扫描",
    "cancel": "取消",
    
    # 状态文案
    "scan_idle": "准备就绪",
    "scan_progress": "正在扫描...",
    "scan_progress_detail": "正在扫描本机，请稍候...",
    "scan_progress_count": "正在扫描: {current}/{total}",
    "scan_complete": "扫描完成",
    "scan_complete_detail": "扫描完成！发现 {count} 个可管理的软件",
    "scan_error": "扫描失败: {error}",
    
    # 结果统计
    "found_apps": "发现 {count} 个可管理的软件",
    "no_apps_found": "未发现可管理的软件",
    "selected_count": "已选中 {count} 项",
    "import_success": "成功导入 {count} 个软件",
    
    # 其他
    "ignore_forever": "永久忽略",
    "ignored": "已忽略",
    
    # 配置编辑器
    "config_editor": {
        "title": "高级配置",
        "description": "直接编辑底层配置文件，自定义软件的行为逻辑。",
        "config_json": "全局设置",
        "config_json_desc": "管理扫描深度、忽略列表及系统参数。",
        "categories_json": "分类树定义",
        "categories_json_desc": "自定义左侧导航栏的目录结构与层级。",
        "templates_json": "模板规则",
        "templates_json_desc": "定义不同后缀名文件的自动分类策略。",
        "edit": "编辑",
        "status_ok": "格式正确",
        "status_error": "格式错误",
        "opened": "已在外部编辑器中打开",
        "save_to_reload": "保存后将自动重载配置。",
        "open_failed": "无法打开文件，请检查文件路径。",
        "reloaded": "配置已更新且格式正确。",
        "validation_failed": "配置文件格式校验失败",
        "json_error": "JSON 格式错误",
        "line": "错误行",
        "detail": "详细信息",
        "export": "导出备份",
        "restore": "还原备份",
        "export_title": "导出配置备份",
        "export_success": "导出成功: {path}",
        "restore_title": "选择配置备份",
        "restore_confirm_title": "确认还原",
        "restore_confirm_message": "此操作将覆盖当前配置，是否继续？",
        "restore_success": "还原成功，配置已重新加载。",
    }
}
