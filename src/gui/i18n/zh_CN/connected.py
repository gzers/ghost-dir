"""
已连接页面文案
"""

CONNECTED_TEXTS = {
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
}
