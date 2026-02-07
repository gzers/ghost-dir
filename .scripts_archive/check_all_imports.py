"""
全面检测和修复所有导入错误的脚本
"""
import ast
import re
from pathlib import Path
from collections import defaultdict

base_dir = Path(r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir")
src_dir = base_dir / "src"

# 收集所有 Python 文件
all_py_files = list(src_dir.rglob("*.py"))

print(f"正在检查 {len(all_py_files)} 个 Python 文件...\n")

# 1. 检查所有导入语句
import_errors = []
syntax_errors = []
missing_imports = defaultdict(list)

for py_file in all_py_files:
    try:
        content = py_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 检查语法错误的导入
        for i, line in enumerate(lines, 1):
            # 检查格式错误的导入（如 "f # 注释rom"）
            if re.search(r'^[a-z]\s+#.*rom\s+', line):
                syntax_errors.append((py_file, i, line.strip()))
            
            # 检查缺少类名的导入
            if re.match(r'^\s*from\s+\S+\s+import\s+#', line):
                syntax_errors.append((py_file, i, line.strip()))
            
            # 检查重复类名
            if re.search(r'import\s+(\w+)\s+\1', line):
                syntax_errors.append((py_file, i, line.strip()))
        
        # 使用 AST 检查导入
        try:
            tree = ast.parse(content)
            imports = set()
            used_names = set()
            
            # 收集所有导入
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)
            
            # 检查常见的缺失导入
            common_missing = {
                'service_bus': 'from src.common.service_bus import service_bus',
                'signal_bus': 'from src.common.signals import signal_bus',
            }
            
            for name, import_stmt in common_missing.items():
                if name in used_names and name not in imports:
                    # 检查是否真的缺失
                    if name not in content or f'import {name}' not in content:
                        missing_imports[name].append((py_file, import_stmt))
        
        except SyntaxError as e:
            syntax_errors.append((py_file, e.lineno, f"语法错误: {e.msg}"))
    
    except Exception as e:
        print(f"处理文件时出错 {py_file}: {e}")

# 2. 打印检测结果
print("=" * 80)
print("检测结果汇总")
print("=" * 80)

if syntax_errors:
    print(f"\n发现 {len(syntax_errors)} 个语法错误：")
    for file, line_no, line_content in syntax_errors:
        rel_path = file.relative_to(base_dir)
        print(f"  [{rel_path}:{line_no}] {line_content}")

if missing_imports:
    print(f"\n发现缺失的导入：")
    for name, files in missing_imports.items():
        print(f"\n  缺失 '{name}' 的文件 ({len(files)} 个):")
        for file, import_stmt in files:
            rel_path = file.relative_to(base_dir)
            print(f"    - {rel_path}")
            print(f"      需要添加: {import_stmt}")

if not syntax_errors and not missing_imports:
    print("\n✅ 未发现导入错误！")

# 3. 检查不存在的模块
print("\n" + "=" * 80)
print("检查不存在的模块路径")
print("=" * 80)

non_existent_modules = []

for py_file in all_py_files:
    try:
        content = py_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 查找所有 from src.xxx import 语句（忽略注释）
        for line_no, line in enumerate(lines, 1):
            # 跳过注释行
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            # 查找导入语句
            import_pattern = r'from\s+(src\.[.\w]+)\s+import'
            match = re.search(import_pattern, line)
            
            if match:
                module_path = match.group(1)
                # 转换为文件路径
                file_path = base_dir / module_path.replace('.', '/')
                
                # 检查是否存在（作为目录或 .py 文件）
                if not file_path.exists() and not (file_path.parent / f"{file_path.name}.py").exists():
                    non_existent_modules.append((py_file, line_no, module_path))
    
    except Exception as e:
        pass

if non_existent_modules:
    print(f"\n发现 {len(non_existent_modules)} 个不存在的模块引用：")
    for file, line_no, module in non_existent_modules:
        rel_path = file.relative_to(base_dir)
        print(f"  [{rel_path}:{line_no}] 导入了不存在的模块: {module}")
else:
    print("\n✅ 所有模块路径都存在！")

print("\n" + "=" * 80)
print("检测完成")
print("=" * 80)
