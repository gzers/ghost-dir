import sys
import os
import traceback
import inspect

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def diagnostic_run():
    print("--- 启动强力运行时诊断 V2 ---")
    try:
        # 1. 强制顶层导入类，确保不走偏
        from src.services.template_service import TemplateService
        print(f"[Check] Class Path: {inspect.getfile(TemplateService)}")
        
        # 2. 检查 ServiceBus 状态
        from src.common.service_bus import service_bus
        ts = service_bus.template_service
        
        print(f"[Check] Instance ID: {id(ts)}")
        print(f"[Check] Instance Methods: {[m for m in dir(ts) if not m.startswith('_')]}")
        
        if not hasattr(ts, 'get_all_templates'):
            print("❌ 警告：即使强力导入后属性依然缺失！尝试手动修复内存对象...")
            # 手动注入方法作为最后防线 (虽然不推荐，但可用于测试)
            # ts.get_all_templates = TemplateService.get_all_templates.__get__(ts, TemplateService)
        
        # 3. 启动应用
        from src.gui.app import run_app
        run_app()
        
    except Exception:
        print("\n❌ 捕获到运行时错误:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    diagnostic_run()
