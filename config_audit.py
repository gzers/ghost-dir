import json
import os
import sys

# 设置路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def audit_json_files():
    configs = {
        "Template": "config/default_templates.json",
        "Category": "config/default_categories.json"
    }
    
    for name, path in configs.items():
        print(f"\n--- 审计 {name} 配置 ({path}) ---")
        full_path = os.path.join(BASE_DIR, path)
        
        if not os.path.exists(full_path):
            print(f"❌ 物理文件丢失: {full_path}")
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"文件大小: {len(content)} 字节")
                
                # 特别检查：是否有 BOM
                if content.startswith('\ufeff'):
                    print("⚠️ 警告: 发现 UTF-8 BOM，解析可能受影响。")
                
                data = json.loads(content)
                
                # 结构校验
                if name == "Template":
                    if not isinstance(data, dict) or 'templates' not in data:
                        print(f"❌ Template 结构异常，缺少 'templates' 键。")
                    else:
                        items = data['templates']
                        print(f"✅ 发现 {len(items)} 个模板项")
                        # 抽样检查第一个项
                        if items:
                            first = items[0]
                            required = ['id', 'name', 'default_src']
                            missing = [r for r in required if r not in first]
                            if missing:
                                print(f"❌ 模板项缺少必填字段: {missing}")
                            else:
                                print(f"✅ 抽样字段校验通过: {first['name']}")
                
                if name == "Category":
                    if not isinstance(data, dict) or 'categories' not in data:
                        print(f"❌ Category 结构异常，缺少 'categories' 键。")
                    else:
                        items = data['categories']
                        print(f"✅ 发现 {len(items)} 个分类项")
                        # 抽样检查
                        if items:
                            first = items[0]
                            required = ['id', 'name']
                            missing = [r for r in required if r not in first]
                            if missing:
                                print(f"❌ 分类项缺少必填字段: {missing}")
                            else:
                                print(f"✅ 抽样字段校验通过: {first['name']}")
                                
        except json.JSONDecodeError as e:
            print(f"❌ JSON 语法错误: {str(e)}")
            # 尝试定位错误行
            lines = content[:e.pos].split('\n')
            print(f"错误大致发生位置: 行 {len(lines)}, 列 {len(lines[-1])}")
        except Exception as e:
            print(f"❌ 读取过程中发生未知错误: {str(e)}")

if __name__ == "__main__":
    audit_json_files()
