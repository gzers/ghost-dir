import sys
import os
import traceback
import inspect
import importlib

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def diagnostic_run():
    print("--- 启动【内存清道夫】诊断 V3 ---")
    try:
        # 1. 强制重载模块，彻底驱除幽灵缓存
        import src.services.template_service
        importlib.reload(src.services.template_service)
        from src.services.template_service import TemplateService
        
        print(f"[Clear] Class Path: {inspect.getfile(TemplateService)}")
        print(f"[Clear] Real Methods: {[m for m in dir(TemplateService) if not m.startswith('_')]}")

        # 2. 强行初始化或重新初始化 ServiceBus
        from src.common.service_bus import ServiceBus, service_bus
        # 由于 service_bus 是全局单例，我们需要检查它是否已经持有旧实例
        # 强制更新实例中的 Service
        from src.dao import TemplateDAO
        service_bus.template_service = TemplateService(TemplateDAO())
        
        print(f"[Bus] Final ts attributes: {[m for m in dir(service_bus.template_service) if not m.startswith('_')]}")
        
        # 3. 启动应用
        from src.gui.app import run_app
        run_app()
        
    except Exception:
        print("\n❌ 捕获到运行时错误:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    diagnostic_run()
