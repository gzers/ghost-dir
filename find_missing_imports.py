import os
import re
from pathlib import Path

src_dir = Path(r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir\src")
all_py = list(src_dir.rglob("*.py"))

missing_import_files = []

for py in all_py:
    try:
        content = py.read_text(encoding='utf-8')
        # 如果使用了 service_bus 但没有导入语句
        if re.search(r'\bservice_bus\.', content) and 'import service_bus' not in content:
            missing_import_files.append(py)
    except Exception:
        pass

if not missing_import_files:
    print("SUCCESS: NO_MISSING_IMPORTS")
else:
    print(f"FAILED: {len(missing_import_files)} FILES MISSING IMPORT")
    for f in missing_import_files:
        print(f"FILE: {f.relative_to(src_dir.parent)}")
