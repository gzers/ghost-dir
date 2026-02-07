# coding: utf-8
import sys
import os

# 确保项目根目录在路径中
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.services.link_service import LinkService
    import inspect
    
    print(f"DEBUG: LinkService file source: {inspect.getfile(LinkService)}")
    print(f"DEBUG: LinkService members: {[m for m in dir(LinkService) if not m.startswith('__')]}")
    
    if hasattr(LinkService, 'calculate_sizes_async'):
        print("SUCCESS: calculate_sizes_async found in LinkService class.")
    else:
        print("FAILURE: calculate_sizes_async NOT found in LinkService class.")

except Exception as e:
    print(f"DEBUG: Error during probe: {e}")
