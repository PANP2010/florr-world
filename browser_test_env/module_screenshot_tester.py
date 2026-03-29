#!/usr/bin/env python3
"""
模块截图对比测试
通过游戏界面截图验证各模块功能
"""
import os
import cv2
import numpy as np
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

class ModuleScreenshotTester:
    """测试游戏各模块的截图"""
    
    def __init__(self):
        self.baseline_dir = Path("screenshots/baseline")
        self.current_dir = Path("screenshots/current")
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.current_dir.mkdir(parents=True, exist_ok=True)
        
    def capture_game_state(self, state_name: str):
        """捕获游戏状态截图"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            
            # 假设游戏在 localhost:8000
            try:
                page.goto("http://localhost:8000", timeout=5000)
                page.wait_for_timeout(2000)
                page.screenshot(path=str(self.current_dir / f"{state_name}.png"))
            except:
                pass
                
            browser.close()
    
    def compare_with_baseline(self, state_name: str, threshold: float = 0.95) -> bool:
        """对比基线截图，返回是否通过"""
        baseline = self.baseline_dir / f"{state_name}.png"
        current = self.current_dir / f"{state_name}.png"
        
        if not baseline.exists():
            print(f"⚠ 基线不存在: {baseline}")
            return False
        
        if not current.exists():
            print(f"✗ 当前截图不存在: {current}")
            return False
        
        # 读取图片
        b = cv2.imread(str(baseline))
        c = cv2.imread(str(current))
        
        if b is None or c is None:
            return False
        
        # 计算相似度
        diff = cv2.absdiff(b, c)
        similarity = 1.0 - (np.sum(diff) / (diff.shape[0] * diff.shape[1] * 255))
        
        print(f"[{state_name}] 相似度: {similarity:.2%}")
        return similarity >= threshold
