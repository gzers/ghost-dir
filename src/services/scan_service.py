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
        1. 遍历常见的安装/数据目录
        2. 匹配模板中的默认路径
        """
        discovered = []
        
        # 定义搜索根目录
        search_roots = [
            os.environ.get('APPDATA'),
            os.environ.get('LOCALAPPDATA'),
            os.environ.get('ProgramFiles'),
            os.environ.get('ProgramFiles(x86)'),
            "D:\\", "E:\\" # 常用数据盘
        ]
        search_roots = [r for r in search_roots if r and os.path.exists(r)]

        # 扫描逻辑简化版：仅检查模板路径是否存在
        for template in self.templates:
            # 解析路径中的环境变量
            raw_path = template.default_src
            expanded_path = os.path.expandvars(raw_path)
            
            if self.progress_callback:
                self.progress_callback(f"正在检查: {expanded_path}")
                
            if os.path.exists(expanded_path):
                # 标记该模板已被发现
                discovered.append(template)
                
        return discovered

    def import_templates(self, templates: List[Template]) -> int:
        """导入选中的模板（此处仅模拟返回导入数量）"""
        return len(templates)
