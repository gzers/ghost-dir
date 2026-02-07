import sys
import os
import importlib
import inspect

# Ensure base path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def ultra_probe():
    print("=== ULTRA PROBE START ===")
    
    # Force reload
    import src.services.template_service
    importlib.reload(src.services.template_service)
    from src.services.template_service import TemplateService
    
    # 1. Inspect class methods with REPR
    print("\n[V1] Class dir (repr):")
    methods = [m for m in dir(TemplateService) if not m.startswith("_")]
    for m in methods:
        print(f"  - {repr(m)} (Hex: {m.encode('utf-8').hex()})")
        
    # 2. Inspect instance
    from src.dao import TemplateDAO
    instance = TemplateService(TemplateDAO())
    print("\n[V2] Instance dir (repr):")
    i_methods = [m for m in dir(instance) if not m.startswith("_")]
    for m in i_methods:
        print(f"  - {repr(m)} (Hex: {m.encode('utf-8').hex()})")

    # 3. Test call
    try:
        instance.get_all_templates()
        print("\n✅ CALL SUCCESSFUL!")
    except AttributeError as e:
        print(f"\n❌ CALL FAILED: {repr(e)}")
        
if __name__ == "__main__":
    ultra_probe()
