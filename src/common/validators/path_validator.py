# coding:utf-8
import re
import os
from typing import Tuple
from .base import BaseValidator


class PathValidator(BaseValidator):
    """ Windows 路径校验器 """

    def validate(self, value: str) -> Tuple[bool, str]:
        """ 验证路径格式 """
        if not value or not value.strip():
            return False, "路径不能为空"

        # 标准化后再验证
        normalized_path = self.normalize(value)

        # 简单的 Windows 路径格式校验 (驱动器盘符或 UNC 路径)
        # 驱动器盘符格式: D:\... 或 D:/...
        drive_pattern = r'^[a-zA-Z]:\\'
        # UNC 路径格式: \\server\share
        unc_pattern = r'^\\{2}[^\\]+\\'

        if not re.match(drive_pattern, normalized_path) and not re.match(unc_pattern, normalized_path):
            return False, "无效的 Windows 路径格式"

        return True, ""

    def normalize(self, value: str) -> str:
        r"""
        标准化路径:
        1. 移除 \\?\ 前缀 (长路径支持)
        2. 移除 \\?\UNC\ 前缀并保留 \\
        3. 统一分隔符为 \
        4. 去除首尾空格
        """
        if not value:
            return ""

        path = value.strip()

        # 1. 处理 UNC 前缀
        # 使用组合方式避免 r"" 结尾转义和 \U 转义问题
        unc_long_prefix = r"\\?\UNC" + "\\"

        if path.startswith(unc_long_prefix):
            # \\?\UNC\server\share -> \\server\share
            path = r"\\" + path[len(unc_long_prefix):]
        elif path.startswith(r"\\?\ "):
             path = path[4:].strip()
        elif path.startswith(r"\\?" + "\\"):
            # \\?\D:\folder -> D:\folder
            path = path[4:]

        # 2. 统一分隔符
        path = path.replace("/", "\\")

        # 3. 移除多余的连续反斜杠 (除了 UNC 的开头两个)
        if path.startswith(r"\\"):
            path = r"\\" + re.sub(r"\\+", r"\\", path[2:])
        else:
            path = re.sub(r"\\+", r"\\", path)

        # 4. 移除末尾的反斜杠 (除非是 C:\ 这种根目录)
        if len(path) > 3 and path.endswith("\\"):
            path = path.rstrip("\\")

        return path
