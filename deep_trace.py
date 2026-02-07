import sys
import os
import traceback

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def deep_inspect():
    print("--- 深度属性追踪启动 ---")
    try:
        from src.common.service_bus import service_bus
        ts = service_bus.template_service
        
        print(f"[Instance] Type: {type(ts)}")
        print(f"[Instance] Module: {ts.__class__.__module__}")
        print(f"[Instance] Attributes: {[m for m in dir(ts) if not m.startswith('__')]}")
        
        # 探测是否存在 get_all_templates
        if hasattr(ts, 'get_all_templates'):
            print("✅ 属性 get_all_templates 存在")
        else:
            print("❌ 属性 get_all_templates 缺失")
            # 记录此时的 traceback，看是谁在何时何地访问了它
            try:
                val = ts.get_all_templates
            except AttributeError:
                traceback.print_exc()

        # 启动应用
        from src.gui.app import run_app
        run_app()
        
    except Exception:
        print("\n❌ 捕获到错误:")
        traceback.print_exc()

if __name__ == "__main__":
    deep_inspect()
