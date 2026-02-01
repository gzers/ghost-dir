# coding:utf-8
import sys
import os

# 将项目根目录添加到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.common.validators import PathValidator

def test_path_validator():
    validator = PathValidator()
    
    test_cases = [
        # (输入路径, 预期输出)
        (r"\\?\D:\Software\Devices\Razer", r"D:\Software\Devices\Razer"),
        (r"\\?\UNC\server\share\folder", r"\\server\share\folder"),
        (r"D:/Users/Test/Documents", r"D:\Users\Test\Documents"),
        (r"C:\Windows\\System32\/", r"C:\Windows\System32"),
        (r"\\?\ ", ""), # 测试异常输入
        (r"D:\Data\\ ", r"D:\Data"),
    ]
    
    all_passed = True
    for input_path, expected in test_cases:
        result = validator.normalize(input_path)
        if result == expected:
            print(f"✅ PASS: [{input_path}] -> [{result}]")
        else:
            print(f"❌ FAIL: [{input_path}] -> Expected [{expected}], got [{result}]")
            all_passed = False
            
    # 验证逻辑
    valid_cases = [
        r"C:\Test",
        r"D:\Soft\App",
        r"\\server\share\file",
    ]
    
    for path in valid_cases:
        is_valid, msg = validator.validate(path)
        if is_valid:
            print(f"✅ VALID: [{path}]")
        else:
            print(f"❌ INVALID: [{path}] - {msg}")
            all_passed = False

    return all_passed

if __name__ == "__main__":
    if test_path_validator():
        print("\n✨ All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed.")
        sys.exit(1)
