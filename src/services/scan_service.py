# coding: utf-8
"""智能扫描服务"""
import os
import re
from typing import List, Callable, Optional
from src.models.template import Template

class SmartScanner:
    """智能扫描引擎"""
    
    def __init__(self, templates: List[Template]):
        self.templates = templates
        self.progress_callback: Optional[Callable[[str], None]] = None

    def set_progress_callback(self, callback: Callable[[str], None]):
        """设置扫描进度回调"""
        self.progress_callback = callback

    def scan(self) -> List[Template]:
        """
        全量扫描本机应用
        1. 检查模板中的默认路径
        2. 如果默认路径不存在，尝试在常用安装目录下进行关键词匹配
        """
        discovered = []
        print(f"DEBUG: SmartScanner started with {len(self.templates)} templates.")
        
        # 定义搜索根目录
        search_roots = [
            os.environ.get('ProgramFiles'),
            os.environ.get('ProgramFiles(x86)'),
            os.environ.get('LOCALAPPDATA'),
            os.environ.get('APPDATA'),
            "D:\\", "E:\\", "F:\\" # 常用数据盘
        ]
        search_roots = [r for r in search_roots if r and os.path.exists(r)]
        print(f"DEBUG: Search roots for fallback: {search_roots}")

        for template in self.templates:
            # 1. 尝试原始路径
            raw_path = template.default_src
            expanded_path = os.path.expandvars(raw_path)
            
            if self.progress_callback:
                self.progress_callback(f"正在扫描: {template.name}")
                
            if os.path.exists(expanded_path):
                print(f"DEBUG: Found {template.name} via default path: {expanded_path}")
                discovered.append(template)
                continue

            # 2. 备选方案：由于用户可能安装在非 C 盘，提取模板路径中的特征名进行搜索
            # 例如 "C:\Program Files (x86)\Steam\steamapps" -> 搜索 "Steam\steamapps"
            path_parts = expanded_path.replace("\\", "/").split("/")
            # 取最后两级作为特征
            if len(path_parts) >= 2:
                feature_path = os.path.join(path_parts[-2], path_parts[-1])
                for root in search_roots:
                    # 避免对 C 盘根目录做深层次 walk (性能考虑)
                    # 只在常用软件目录下查找
                    test_path = os.path.join(root, feature_path)
                    if os.path.exists(test_path):
                        print(f"DEBUG: Found {template.name} via fallback search at {test_path}")
                        # 更新模板的临时检测路径
                        template.default_src = test_path
                        discovered.append(template)
                        break

        print(f"DEBUG: Scan finished. Discovered: {len(discovered)}")
        return discovered

    def import_templates(self, templates: List[Template]) -> int:
        """导入选中的模板（此处仅模拟返回导入数量）"""
        return len(templates)
