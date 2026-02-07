"""
链接页面文案
"""

LINKS_TEXTS = {
    "title": "我的链接",
    "add_link": "新增链接",
    "scan_apps": "扫描本机应用",
    "refresh_size": "刷新统计",
    "batch_establish": "批量建立链接",
    "batch_disconnect": "批量断开链接",
    "batch_remove": "批量移除",
    "refresh_status": "刷新链接状态",
    "clear_selection": "清除选择",
    "selected_count": "已选择 {count} 项",

    # 视图切换
    "view_list": "列表视图",
    "view_category": "分类视图",
    "search_placeholder": "搜索软件名称...",

    # 状态文案
    "status_connected": "正常",
    "status_invalid": "失效",
    "status_ready": "就绪",
    "status_disconnected": "未链接",

    # 状态说明 (帮助弹窗)
    "status_help_title": "状态定义说明",
    "status_connected_desc": "文件物理位置已在目标驱动器，源位置为符号链接点。完全不占源驱动器空间。",
    "status_disconnected_desc": "文件物理位置仍在源位置，尚未迁移。会持续占用源驱动器空间。",
    "status_ready_desc": "文件已在目标驱动器，但源位置对应的链接点丢失或未建立。可通过「建立链接」恢复。",
    "status_invalid_desc": "由于路径不存在或原始配置损坏，链接已失效。请检查文件是否存在。",

    # 操作按钮
    "establish": "建立链接",
    "disconnect": "断开链接",
    "reconnect": "重新链接",

    # 表格列
    "col_name": "名称",
    "col_category": "分类",
    "col_source": "源路径",
    "col_target": "目标路径",
    "col_size": "占用空间",
    "col_status": "状态",
    "col_actions": "操作",

    # 空状态
    "empty_title": "暂无链接",
    "empty_desc": "点击「新增链接」或「扫描本机应用」开始管理",
    "empty_action": "开始使用",

    # 消息提示
    "msg_establish_success": "已成功建立链接:{name}",
    "msg_establish_failed": "建立链接失败:{name}",
    "msg_disconnect_success": "已成功断开链接:{name}",
    "msg_disconnect_failed": "断开链接失败:{name}",
    "msg_delete_confirm": "确定要删除链接 {name} 吗?\n这不会删除实际文件。",
    "msg_batch_establish_confirm": "将为 {count} 个软件建立链接,是否继续?",
    "msg_batch_disconnect_confirm": "将断开 {count} 个软件的链接,是否继续?",
    "msg_batch_complete": "成功: {success}/{total}",
    "msg_no_establish_items": "没有可建立链接的项目",
    "msg_no_disconnect_items": "没有可断开链接的项目",

    # 进程占用
    "process_warning_title": "文件占用警告",
    "process_warning_msg": "检测到以下进程正在占用文件:\n\n{processes}\n\n是否结束这些进程并继续?",
    "process_target_warning_msg": "检测到以下进程正在占用目标文件:\n\n{processes}\n\n是否结束这些进程并继续?",

    # 空间统计
    "refresh_size_confirm": "将计算 {count} 个链接的空间占用,可能需要一些时间。\n是否继续?",
    "refresh_size_progress": "正在计算",
    "refresh_size_complete": "计算完成 ✓",
    "refresh_size_result": "已更新 {count} 个链接的空间统计",
    "refresh_size_empty": "没有需要统计的链接",

    # 编辑链接
    "edit_link": "编辑链接",
    "link_name": "软件名称",
    "link_name_placeholder": "请输入软件名称",
    "category": "所属分类",
    "source_path": "源路径",
    "target_path": "目标路径",
    "confirm_remove_title": "确认移除",
    "confirm_remove_msg": "确定要移除选中的 {count} 个链接吗？\n这不会删除实际文件。",
    "edit_path_locked_tip": "当前链接已建立，如需修改路径请先断开链接。",
    "edit_rule_title": "路径编辑规则",
    "edit_rule_desc": "为了确保链接的完整性，仅在<b>非正常（未链接、就绪、失效）</b>状态下允许修改路径。若链接已建立，请先执行「断开链接」后再进行路径调整。",
}
