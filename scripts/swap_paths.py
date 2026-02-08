# coding: utf-8
"""
数据库字段交换脚本
将所有链接的 source_path 和 target_path 互换
"""
import json
import os
from pathlib import Path

def swap_source_target_paths():
    """交换所有链接的 source_path 和 target_path"""
    # 获取数据库文件路径
    app_data_dir = Path(os.path.expandvars("%APPDATA%")) / ".ghost-dir"
    db_file = app_data_dir / "links.json"
    
    if not db_file.exists():
        print(f"数据库文件不存在: {db_file}")
        return False
    
    # 备份原文件
    backup_file = db_file.with_suffix('.json.backup')
    import shutil
    shutil.copy2(db_file, backup_file)
    print(f"已备份到: {backup_file}")
    
    # 读取数据
    with open(db_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 交换字段
    modified_count = 0
    for link in data.get('links', []):
        source = link.get('source_path')
        target = link.get('target_path')
        
        if source and target:
            # 交换
            link['source_path'] = target
            link['target_path'] = source
            modified_count += 1
            print(f"已交换: {link.get('name')}")
            print(f"  原 source: {source}")
            print(f"  原 target: {target}")
            print(f"  新 source: {link['source_path']}")
            print(f"  新 target: {link['target_path']}")
            print()
    
    # 保存
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"完成！共修改 {modified_count} 条链接")
    print(f"备份文件: {backup_file}")
    return True

if __name__ == "__main__":
    swap_source_target_paths()
