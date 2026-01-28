"""
模版库页面文案
"""

LIBRARY_TEXTS = {
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
    
    # 分类管理对话框
    "category_manager_title": "分类管理",
    "category_manager_sort_mode": "分类管理 - 排序模式",
    
    # 工具栏按钮
    "btn_new": "新建",
    "btn_rename": "重命名",
    "btn_delete": "删除",
    "btn_sort": "排序",
    "btn_confirm_sort": "确认排序",
    "btn_cancel_sort": "取消排序",
    "btn_help": "帮助",
    "btn_done": "完成",
    "btn_cancel": "取消",
    
    # 对话框标题
    "dialog_new_category": "新建分类",
    "dialog_rename_category": "重命名分类",
    "dialog_confirm_delete": "确认删除",
    "dialog_help": "帮助",
    "dialog_failed": "失败",
    "dialog_hint": "提示",
    
    # 输入提示
    "input_category_name": "请输入分类名称：",
    "input_new_name": "请输入新名称：",
    
    # 成功消息
    "msg_sort_saved": "排序已保存",
    "msg_sort_cancelled": "已取消排序，未保存任何变更",
    
    # 右键菜单
    "menu_rename": "重命名 (F2)",
    "menu_add_child": "在此新建",
    "menu_delete": "删除此项",
    
    # 删除确认
    "confirm_delete_single": "确定要删除分类 '{name}' 吗？\n\n如果该分类下有子分类或模板，也会一并删除。",
    "confirm_delete_batch": "确定要删除以下 {count} 个分类吗？\n{names}\n\n这些分类下没有模板。",
    "confirm_delete_with_templates": "确定要删除以下 {count} 个分类吗？\n{names}\n\n⚠️ 警告：这些分类下共有 {template_count} 个模板：\n{template_info}\n\n删除分类后，这些模板也会一并删除！",
    
    # 结果消息
    "msg_delete_success": "已成功删除 {count} 个分类",
    "msg_delete_partial": "成功删除 {success} 个分类，失败 {failed} 个",
    "error_system_category_delete": "系统分类无法删除",
    "error_system_category_rename": "系统分类无法重命名",
    "error_empty_name": "分类名称不能为空",
    "error_duplicate_name": "同一层级下已存在名为 '{name}' 的分类",
    "error_empty_delete_selection": "请勾选要删除的分类",
    
    # 帮助内容
    "help_title": "📖 分类管理操作指南",
    "help_browse_mode": "【浏览模式】",
    "help_browse_1": "• 单击选中分类",
    "help_browse_2": "• 复选框用于批量删除",
    "help_browse_3": "• 按 F2 或点击重命名按钮编辑分类名称",
    "help_browse_4": "• 右键分类可快速访问常用操作",
    "help_sort_mode": "【排序模式】",
    "help_sort_1": "• 点击'排序'按钮进入排序模式",
    "help_sort_2": "• 拖拽分类调整顺序（功能开发中）",
    "help_sort_3": "• 点击'退出排序'保存并返回",
    "help_sort_4": "• 排序模式下无法进行其他操作",
    "help_shortcuts": "【快捷键】",
    "help_shortcuts_1": "• F2: 重命名选中的分类",
    "help_notes": "【注意事项】",
    "help_notes_1": "• 所有操作立即保存，无需点击'完成'按钮",
    "help_notes_2": "• 系统分类（如'未分类'）无法删除或重命名",
    "help_notes_3": "• 分类层级最多支持 3 层",
}
