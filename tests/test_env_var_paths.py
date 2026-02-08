# coding: utf-8
"""测试路径验证器对环境变量的支持"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common.validators import PathValidator

def test_env_var_paths():
    validator = PathValidator()
    
    # 测试用例
    test_cases = [
        ("%USERPROFILE%\\Desktop", "环境变量路径"),
        ("%APPDATA%\\MyApp", "APPDATA 环境变量"),
        ("%USERPROFILE%\\A.trae", "用户提供的路径"),
        ("D:\\test", "普通路径"),
        ("C:\\Users\\Test", "普通路径"),
    ]
    
    print("=" * 60)
    print("测试环境变量路径验证")
    print("=" * 60)
    
    for path, desc in test_cases:
        is_valid, msg = validator.validate(path)
        normalized = validator.normalize(path)
        
        status = "✅ 通过" if is_valid else "❌ 失败"
        print(f"\n{status} [{desc}]")
        print(f"  原始路径: {path}")
        print(f"  标准化后: {normalized}")
        if not is_valid:
            print(f"  错误信息: {msg}")

if __name__ == "__main__":
    test_env_var_paths()
