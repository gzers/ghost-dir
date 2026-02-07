import os
import py_compile
from pathlib import Path

src_dir = Path(r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir\src")
all_py = list(src_dir.rglob("*.py"))

error_files = []

for py in all_py:
    try:
        py_compile.compile(str(py), doraise=True)
    except Exception as e:
        error_files.append((py, str(e)))

if not error_files:
    print("SUCCESS: ALL_PASS")
else:
    print(f"FAILED: {len(error_files)} FILES")
    for f, e in error_files:
        print(f"FILE: {f}")
        # 仅取异常信息的最后两行关键定位
        error_msg = "\n".join(e.splitlines()[-2:])
        print(f"ERROR: {error_msg}\n")
