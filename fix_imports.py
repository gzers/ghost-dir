"""
批量添加 service_bus 导入的脚本
"""
import re
from pathlib import Path

# 需要添加导入的文件列表
files_to_fix = [
    "src/gui/views/wizard/wizard_view.py",
    "src/gui/views/settings/widgets/restore_config_cards.py",
    "src/gui/views/settings/setting_view.py",
    "src/gui/views/links/links_view.py",
    "src/gui/views/library/library_view.py",
    "src/gui/dialogs/template_edit/dialog.py",
    "src/gui/dialogs/edit_link/dialog.py",
    "src/gui/dialogs/category_manager/dialog.py",
    "src/gui/dialogs/add_link/dialog.py",
]

import_statement = "from src.common.service_bus import service_bus\n"

base_dir = Path(r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir")

for file_path in files_to_fix:
    full_path = base_dir / file_path
    if not full_path.exists():
        print(f"文件不存在: {full_path}")
        continue
    
    content = full_path.read_text(encoding='utf-8')
    
    # 检查是否已经有导入
    if "from src.common.service_bus import service_bus" in content:
        print(f"已存在导入: {file_path}")
        continue
    
    # 找到最后一个 import 语句的位置
    lines = content.split('\n')
    last_import_index = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')) and not line.strip().startswith('#'):
            last_import_index = i
    
    if last_import_index >= 0:
        # 在最后一个 import 后面添加
        lines.insert(last_import_index + 1, import_statement.rstrip())
        new_content = '\n'.join(lines)
        full_path.write_text(new_content, encoding='utf-8')
        print(f"已修复: {file_path}")
    else:
        print(f"未找到导入语句: {file_path}")

print("\n修复完成！")
