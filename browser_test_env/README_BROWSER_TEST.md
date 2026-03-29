# Playwright 浏览器截图测试环境

本目录提供 Playwright 自动化浏览器截图测试能力，用于验证 florr 游戏界面。

## 环境准备

```bash
# 安装 Playwright
pip3 install playwright --break-system-packages

# 安装 Chromium 浏览器
playwright install chromium

# 如果安装失败，尝试带依赖安装
playwright install --with-deps chromium
```

## 目录结构

```
browser_test_env/
├── browser_tester.py          # Playwright 截图测试器
├── module_screenshot_tester.py # 模块截图对比测试
├── test_runner.py             # 测试运行器（一键运行所有测试）
└── README_BROWSER_TEST.md     # 本文档
```

## 使用方法

### 1. 快速截图测试

```bash
cd /home/kuli/florr-world
python3 browser_test_env/browser_tester.py
```

截图将保存到 `screenshots/` 目录。

### 2. 模块截图对比测试

```bash
python3 browser_test_env/module_screenshot_tester.py
```

- `screenshots/baseline/` - 基线截图（参考基准）
- `screenshots/current/` - 当前截图（待对比）

### 3. 一键运行所有测试

```bash
python3 browser_test_env/test_runner.py
```

运行顺序：
1. 单元测试（pytest）
2. 浏览器截图测试
3. 截图对比测试

## 截图目录

```
screenshots/
├── baseline/           # 基线截图
│   └── *.png
├── current/           # 当前截图
│   └── *.png
├── florr_homepage.png # florr.io 主页截图
└── florr_game.png     # florr.io 游戏截图
```

## 自定义截图

```python
from browser_test_env.browser_tester import BrowserTester

tester = BrowserTester()
tester.launch(headless=True)
tester.screenshot("my_test", "https://example.com")
tester.close()
```

## 注意事项

- 如果 `playwright install chromium` 失败，使用 `playwright install --with-deps chromium`
- 截图保存在 `screenshots/` 目录
- baseline 截图作为参考基准，首次需要手动保存基线
- 对比测试需要先有 baseline 才能正常工作
