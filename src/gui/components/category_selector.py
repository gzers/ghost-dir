"""
分类选择下拉框组件
支持层级展示和只选叶子分类
"""
from typing import Optional
from PySide6.QtCore import Qt
from qfluentwidgets import ComboBox
from src.data.category_manager import CategoryManager


class CategorySelector(ComboBox):
    """分类选择下拉框组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_manager = None
        self.setPlaceholderText('选择分类')
        # 核心：设置为可编辑模式，以便 setText 能生效，或者确保视图能同步显示
        # Note: QFluentWidgets 的 ComboBox 在非编辑模式下有时需要显式同步其内部 LineEdit
    
    def set_manager(self, category_manager: CategoryManager):
        """设置分类管理器并加载数据"""
        self.category_manager = category_manager
        self.refresh()
    
    def refresh(self):
        """重新加载分类项"""
        if not self.category_manager:
            return
            
        current_data = self.currentData()
        self.clear()
        
        # 只加载叶子分类
        for category in self.category_manager.get_all_categories():
            if self.category_manager.is_leaf(category.id):
                # 获取深度以计算缩进
                depth = category.get_depth(self.category_manager.categories)
                indent = "  " * (depth - 1)
                display_name = f"{indent}{category.name}"
                
                # 显式添加项并设置数据，确保 ID 能够被 findData 找到
                self.addItem(display_name)
                self.setItemData(self.count() - 1, category.id)
        
        # 尝试恢复之前选中的值
        if current_data:
            self.set_value(current_data)
            
    def set_value(self, category_id: str):
        """设置选中的分类 ID"""
        if not category_id:
            return
            
        idx = self.findData(category_id)
        if idx >= 0:
            self.setCurrentIndex(idx)
            # 同步显示文本 (针对 QFluentWidgets)
            self.setText(self.itemText(idx).strip())
        else:
            # 兼容性匹配
            for i in range(self.count()):
                if str(self.itemData(i)) == str(category_id):
                    self.setCurrentIndex(i)
                    self.setText(self.itemText(i).strip())
                    break

    def get_value(self) -> Optional[str]:
        """获取当前选中的分类 ID"""
        return self.currentData()
