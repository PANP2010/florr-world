#!/usr/bin/env python3
"""
测试运行器 - 一键运行所有测试
"""
import subprocess
import sys
import os

def run_tests():
    os.chdir("/home/kuli/florr-world")
    
    print("=" * 60)
    print("Florr World 测试套件")
    print("=" * 60)
    
    # 1. 单元测试
    print("\n[1/3] 运行单元测试...")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True, text=True
    )
    print(result.stdout[-2000:] if result.stdout else "")
    print(result.stderr[-500:] if result.stderr else "")
    
    # 2. 浏览器截图测试
    print("\n[2/3] 运行浏览器截图测试...")
    result2 = subprocess.run(
        ["python3", "browser_test_env/browser_tester.py"],
        capture_output=True, text=True
    )
    print(result2.stdout[-1000:] if result2.stdout else "")
    
    # 3. 截图对比测试
    print("\n[3/3] 运行截图对比测试...")
    result3 = subprocess.run(
        ["python3", "browser_test_env/module_screenshot_tester.py"],
        capture_output=True, text=True
    )
    print(result3.stdout[-500:] if result3.stdout else "")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_tests()
