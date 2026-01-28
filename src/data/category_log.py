"""
分类操作日志数据模型
用于记录分类的增删改和排序操作历史
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from enum import Enum


class CategoryOperation(Enum):
    """分类操作类型"""
    CREATE = "create"     # 新建
    RENAME = "rename"     # 重命名
    DELETE = "delete"     # 删除
    UPDATE = "update"     # 更新 (除了重命名以外的属性)
    UPDATE_STRUCTURE = "update_structure"  # 结构变更（层级或排序）


@dataclass
class CategoryLogEntry:
    """分类操作日志条目"""
    timestamp: str          # 操作时间 (ISO格式)
    operation: str          # 操作类型 (CategoryOperation.value)
    category_id: str        # 相关分类ID (如果是批量操作，可能为主ID或system)
    category_name: str      # 分类名称
    details: Optional[Dict] = None  # 额外信息，如旧名称、目标父ID、受影响数量等
    
    def to_dict(self) -> Dict:
        """转换为字典以便序列化"""
        return {
            "timestamp": self.timestamp,
            "operation": self.operation,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CategoryLogEntry':
        """从字典创建条目"""
        return cls(
            timestamp=data["timestamp"],
            operation=data["operation"],
            category_id=data["category_id"],
            category_name=data["category_name"],
            details=data.get("details")
        )
