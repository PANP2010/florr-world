#!/usr/bin/env python3
"""
Playwright 截图测试器
用于测试 florr 游戏界面
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

SCREENSHOTS_DIR = Path("screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)

class BrowserTester:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        
    def launch(self, headless: bool = True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page(viewport={"width": 1280, "height": 720})
        
    def screenshot(self, name: str, url: str = "about:blank"):
        """截取页面截图"""
        if url != "about:blank":
            self.page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(1)
        path = SCREENSHOTS_DIR / f"{name}.png"
        self.page.screenshot(path=path, full_page=False)
        print(f"✓ 截图: {path}")
        return path
        
    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

def test_local_game():
    """测试本地游戏窗口"""
    tester = BrowserTester()
    tester.launch(headless=True)
    
    # 如果有本地游戏运行在 localhost，可以测试
    tester.screenshot("game_startup", "http://localhost:8000")
    tester.screenshot("game_menu", "http://localhost:8000/menu")
    
    tester.close()

def test_florrio():
    """测试 florr.io 游戏网站"""
    tester = BrowserTester()
    tester.launch(headless=True)
    
    print("测试 florr.io...")
    tester.screenshot("florr_homepage", "https://florr.io")
    
    # 尝试进入游戏
    try:
        tester.page.goto("https://florr.io", timeout=10000)
        tester.page.wait_for_timeout(3000)
        tester.screenshot("florr_game", "current")
    except Exception as e:
        print(f"游戏加载失败: {e}")
    
    tester.close()

def run_all_tests():
    """运行所有截图测试"""
    print("=" * 50)
    print("Playwright 截图测试")
    print("=" * 50)
    
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    # 测试 florr.io
    print("\n[1/2] 测试 florr.io...")
    try:
        test_florrio()
    except Exception as e:
        print(f"florr.io 测试失败: {e}")
    
    print("\n[2/2] 截图已保存到 screenshots/")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()
