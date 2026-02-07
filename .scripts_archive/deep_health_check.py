import sys
import os
import json
import traceback

# 强制进入项目根目录上下文
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def deep_inspect():
    print("=== [深度自检系统启动] ===")
    errors = []
    
    # 1. 检测 DAO 路径是否正确指向 config/ (开发环境)
    try:
        from src.dao import TemplateDAO, CategoryDAO, LinkDAO
        td = TemplateDAO()
        cd = CategoryDAO()
        ld = LinkDAO()
        
        print(f"[DAO] Template Config: {td.config_file}")
        if 'config\\default_templates.json' not in td.config_file and 'config/default_templates.json' not in td.config_file:
            errors.append(f"TemplateDAO 路径未指向开发态配置: {td.config_file}")
            
        # 2. 检测数据解析是否成功 (非空校验)
        templates = td.get_all()
        categories = cd.get_all()
        links = ld.get_all()
        
        print(f"[DATA] Loaded {len(templates)} templates")
        print(f"[DATA] Loaded {len(categories)} categories")
        
        if len(templates) == 0:
            errors.append("Template 解析为空，请检查 JSON 结构或路径！")
        if len(categories) == 0:
            errors.append("Category 解析为空，请检查 JSON 结构或路径！")
            
        # 3. 模拟 GUI 中的 is_leaf 压力测试
        from src.common.service_bus import service_bus
        cm = service_bus.category_manager
        
        print(f"[STRESS] 模拟分类树遍历自检...")
        for cat in categories:
            try:
                # 触发之前导致报错的逻辑
                _ = cm.is_leaf(cat.id)
            except Exception as e:
                errors.append(f"CategoryManager.is_leaf 失败 (ID: {cat.id}): {str(e)}")
        
        # 4. 检测 CategoryNode 属性完整性
        for cat in categories:
            if not hasattr(cat, 'id') or not hasattr(cat, 'name'):
                errors.append(f"CategoryNode 数据模型不完整 (ID: {getattr(cat, 'id', 'Unknown')})")

    except Exception as e:
        errors.append(f"系统启动级崩坏: {str(e)}\n{traceback.format_exc()}")

    # 结果审计
    if errors:
        print("\n❌ 检测到 [ {count} ] 项关键性错误:".format(count=len(errors)))
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n✅ 全量自检通过！系统架构稳健。")
        return True

if __name__ == "__main__":
    success = deep_inspect()
    sys.exit(0 if success else 1)
