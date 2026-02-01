# coding:utf-8
import re
from typing import Tuple, Any
from .base import BaseValidator


class NameValidator(BaseValidator):
    """ 名称校验器 (用于模板、分类名称等) """

    def __init__(self, min_len: int = 1, max_len: int = 100, allow_special: bool = False):
        self.min_len = min_len
        self.max_len = max_len
        self.allow_special = allow_special

    def validate(self, value: str) -> Tuple[bool, str]:
        """ 验证名称 """
        if not value or not value.strip():
            return False, "名称不能为空"
            
        text = self.normalize(value)
        
        if len(text) < self.min_len:
            return False, f"名称长度不能少于 {self.min_len} 个字符"
            
        if len(text) > self.max_len:
            return False, f"名称长度不能超过 {self.max_len} 个字符"
            
        if not self.allow_special:
            # 只允许字母、数字、中文、下划线、空格和短横线
            if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_\s\-]+$', text):
                return False, "名称包含非法字符 (仅限中文, 字母, 数字, _, -, 空格)"
                
        return True, ""

    def normalize(self, value: str) -> str:
        """ 标准化名称 """
        if not value:
            return ""
        # 移除多余空格
        return " ".join(value.split())
