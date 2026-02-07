import os
from pathlib import Path

def super_fix(file_path):
    try:
        # 读取时自动处理 BOM (utf-8-sig)
        with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read()
        
        # 1. 将 Tab 替换为 4 个空格
        content = content.replace('\t', '    ')
        
        # 2. 移除行尾多余空格
        lines = [line.rstrip() for line in content.splitlines()]
        new_content = '\n'.join(lines) + '\n'
        
        # 3. 写回纯 UTF-8 (无 BOM)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True
    except Exception as e:
        print(f"处理失败 {file_path}: {e}")
        return False

src_dir = Path(r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir\src")
all_py = list(src_dir.rglob("*.py"))

print(f"--- 启动超级修复 (共 {len(all_py)} 个文件) ---")
fixed_count = 0
for py in all_py:
    if super_fix(py):
        fixed_count += 1

print(f"✅ 超级修复完成！已规范化 {fixed_count} 个文件。")
