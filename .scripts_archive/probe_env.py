import sys
import os
import inspect

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def probe_environment():
    print("=== 深度运行时探测启动 ===")
    
    # 1. 检查模块加载情况
    from src.services.template_service import TemplateService
    print(f"[Class] TemplateService source: {inspect.getfile(TemplateService)}")
    print(f"[Class] Methods found: {[m for m in dir(TemplateService) if not m.startswith('_')]}")

    # 2. 检查单例状态
    from src.common.service_bus import service_bus
    ts_instance = service_bus.template_service
    print(f"\n[Instance] Type: {type(ts_instance)}")
    print(f"[Instance] Memory ID: {id(ts_instance)}")
    print(f"[Instance] Methods list: {[m for m in dir(ts_instance) if not m.startswith('_')]}")

    # 3. 检查是否有属性污染 (检查实例 __dict__)
    print(f"\n[Instance] Dict: {ts_instance.__dict__.keys()}")
    
    # 4. 尝试动态调用
    try:
        ts_instance.get_all_templates()
        print("\n✅ 调用成功!")
    except AttributeError as e:
        print(f"\n❌ 调用失败: {e}")
        # 如果失败，强行搜索所有成员
        import difflib
        all_members = dir(ts_instance)
        closest = difflib.get_close_matches('get_all_templates', all_members)
        print(f"相似成员建议: {closest}")

if __name__ == "__main__":
    probe_environment()
