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
        
        使用 CategoryNode.validate() 进行数据校验
        
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
            
            # 使用模型校验每个分类
            from src.data.model import CategoryNode
            
            for idx, cat_data in enumerate(data["categories"]):
                try:
                    category = CategoryNode.from_dict(cat_data)
                    valid, msg = category.validate()
                    if not valid:
                        return False, f"分类 {idx} 校验失败: {msg}"
                except KeyError as e:
                    return False, f"分类 {idx} 缺少必需字段: {str(e)}"
                except Exception as e:
                    return False, f"分类 {idx} 数据错误: {str(e)}"
            
            return True, ""
        except Exception as e:
            return False, f"结构校验失败: {str(e)}"

    
    @staticmethod
    def validate_templates_structure(file_path: Path) -> Tuple[bool, str]:
        """
        校验 default_templates.json 结构
        
        使用 Template.validate() 进行数据校验
        
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
            
            # 使用模型校验每个模板
            from src.data.model import Template
            
            for idx, tpl_data in enumerate(data["templates"]):
                try:
                    template = Template.from_dict(tpl_data)
                    valid, msg = template.validate()
                    if not valid:
                        return False, f"模板 {idx} 校验失败: {msg}"
                except KeyError as e:
                    return False, f"模板 {idx} 缺少必需字段: {str(e)}"
                except Exception as e:
                    return False, f"模板 {idx} 数据错误: {str(e)}"
            
            return True, ""
        except Exception as e:
            return False, f"结构校验失败: {str(e)}"
