# coding:utf-8
"""
配置文件校验器
独立的校验逻辑，与 UI 完全解耦
"""
import json
from pathlib import Path
from typing import Tuple


class ConfigValidator:
    """配置文件校验器"""
    
    @staticmethod
    def validate_json_syntax(file_path: Path) -> Tuple[bool, str]:
        """
        校验 JSON 文件语法
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, ""
        except json.JSONDecodeError as e:
            error_msg = f"JSON 格式错误\n错误行: {e.lineno}\n详细信息: {e.msg}"
            return False, error_msg
        except FileNotFoundError:
            return False, f"文件不存在: {file_path}"
        except Exception as e:
            return False, f"文件读取失败: {str(e)}"
    
    @staticmethod
    def validate_config_structure(file_path: Path) -> Tuple[bool, str]:
        """
        校验 config.json 结构 (适配 v7.4+ 扁平化结构)
        
        必需字段：
        - theme (str)
        - theme_color (str)
        - startup_page (str)
        
        Args:
            file_path: config.json 文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 校验必需的扁平化字段
            required_fields = {
                "theme": str,
                "theme_color": str,
                "startup_page": str
            }
            
            for field, expected_type in required_fields.items():
                if field not in data:
                    # 如果不存在，可能是旧版本，尝试兼容 QFluentWidgets 节 (可选)
                    if "QFluentWidgets" in data:
                        continue
                    return False, f"缺少必需字段: {field}"
                
                if not isinstance(data[field], expected_type):
                    return False, f"字段类型错误: {field} 应为 {expected_type.__name__}"
            
            # 校验 theme 的值
            valid_themes = ["system", "light", "dark"]
            current_theme = data.get("theme")
            if current_theme and current_theme not in valid_themes:
                return False, f"theme 值无效，应为: {', '.join(valid_themes)}"
            
            return True, ""
        except Exception as e:
            return False, f"结构校验失败: {str(e)}"
    
    @staticmethod
    def validate_categories_structure(file_path: Path) -> Tuple[bool, str]:
        """
        校验 categories.json 结构
        
        必需字段：
        - categories (list)
        每个分类必须包含：
        - id (str)
        - name (str)
        - parent_id (str | null)
        - order (int)
        - is_builtin (bool)
        
        Args:
            file_path: categories.json 文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查根节点
            if "categories" not in data:
                return False, "缺少 categories 数组"
            
            if not isinstance(data["categories"], list):
                return False, "categories 必须是数组类型"
            
            # 检查每个分类的字段
            required_fields = {
                "id": str,
                "name": str,
                "order": int,
                "is_builtin": bool
            }
            
            for idx, category in enumerate(data["categories"]):
                for field, expected_type in required_fields.items():
                    if field not in category:
                        return False, f"分类 {idx} 缺少必需字段: {field}"
                    
                    if not isinstance(category[field], expected_type):
                        return False, f"分类 {idx} 字段类型错误: {field} 应为 {expected_type.__name__}"
                
                # parent_id 可以是 str 或 null
                if "parent_id" not in category:
                    return False, f"分类 {idx} 缺少必需字段: parent_id"
                
                if category["parent_id"] is not None and not isinstance(category["parent_id"], str):
                    return False, f"分类 {idx} 字段类型错误: parent_id 应为 str 或 null"
            
            return True, ""
        except Exception as e:
            return False, f"结构校验失败: {str(e)}"
    
    @staticmethod
    def validate_templates_structure(file_path: Path) -> Tuple[bool, str]:
        """
        校验 default_templates.json 结构
        
        必需字段：
        - templates (list)
        每个模板必须包含：
        - id (str)
        - name (str)
        - default_src (str)
        - category_id (str)
        - default_target (str)
        - is_custom (bool)
        
        Args:
            file_path: default_templates.json 文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查根节点
            if "templates" not in data:
                return False, "缺少 templates 数组"
            
            if not isinstance(data["templates"], list):
                return False, "templates 必须是数组类型"
            
            # 检查每个模板的字段
            required_fields = {
                "id": str,
                "name": str,
                "default_src": str,
                "category_id": str,
                "default_target": str,
                "is_custom": bool
            }
            
            for idx, template in enumerate(data["templates"]):
                for field, expected_type in required_fields.items():
                    if field not in template:
                        return False, f"模板 {idx} 缺少必需字段: {field}"
                    
                    if not isinstance(template[field], expected_type):
                        return False, f"模板 {idx} 字段类型错误: {field} 应为 {expected_type.__name__}"
            
            return True, ""
        except Exception as e:
            return False, f"结构校验失败: {str(e)}"
