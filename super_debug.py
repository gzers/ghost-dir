import sys
import os
import inspect

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def super_debug():
    print("=== 超级诊断启动 ===")
    
    # 1. 检查模块加载路径
    from src.services.template_service import TemplateService
    print(f"[Module] TemplateService defined in: {inspect.getfile(TemplateService)}")
    print(f"[Class] Attributes in class: {[m for m in dir(TemplateService) if not m.startswith('__')]}")
    
    # 2. 检查 ServiceBus 实例
    from src.common.service_bus import service_bus
    ts = service_bus.template_service
    print(f"\n[Instance] service_bus.template_service type: {type(ts)}")
    print(f"[Instance] Memory ID: {id(ts)}")
    print(f"[Instance] Attributes found: {[m for m in dir(ts) if not m.startswith('__')]}")
    
    # 3. 检查是否有重名类混淆
    try:
        import src.services
        print(f"\n[Package] src.services content: {dir(src.services)}")
    except Exception as e:
        print(f"Error checking package: {e}")

    # 4. 尝试动态调研属性
    if hasattr(ts, 'get_all_templates'):
        print("\n✅ instance.get_all_templates EXISTS!")
    else:
        print("\n❌ instance.get_all_templates MISSING!")
        
    # 5. 检查源码中是否有 setattr 等动态修改操作
    print("\n[Audit] Checking for dynamic attribute manipulation...")
    from src.common.service_bus import ServiceBus
    print(f"ServiceBus init source snippet:\n{inspect.getsource(ServiceBus.__init__)}")

if __name__ == "__main__":
    super_debug()
