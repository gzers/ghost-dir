# coding:utf-8
from abc import ABC, abstractmethod
from typing import Tuple, Any


class BaseValidator(ABC):
    """ 校验器基类 """

    @abstractmethod
    def validate(self, value: str) -> Tuple[bool, str]:
        """
        验证输入值

        Args:
            value: 输入字符串

        Returns:
            (is_valid, error_message): 验证结果和错误信息
        """
        pass

    @abstractmethod
    def normalize(self, value: str) -> str:
        """
        标准化输入值 (例如: 移除多余空格, 处理路径前缀等)

        Args:
            value: 输入字符串

        Returns:
            标准化后的字符串
        """
        return value.strip()
