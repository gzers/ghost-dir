import os
import py_compile
from pathlib import Path

src_dir = Path(r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir\src")
all_py = list(src_dir.rglob("*.py"))

print(f"--- 启动全量编译器扫描 (共 {len(all_py)} 个文件) ---")
err_count = 0
for py in all_py:
    try:
        py_compile.compile(str(py), doraise=True)
    except py_compile.PyCompileError as e:
        print(f"❌ 语法错误: {py.relative_to(src_dir.parent)}")
        print(f"   {str(e).splitlines()[-1]}")
        err_count += 1
    except Exception as e:
        print(f"⚠️ 处理异常: {py}: {e}")

print(f"\n扫描完成，共发现 {err_count} 个文件存在严重语法错误。")
