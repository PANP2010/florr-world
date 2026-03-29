# 🌌 Florr World

> 2D 开放世界游戏引擎 — 奇异物理 × 建造系统 × 玩家质点

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)](https://pygame.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎮 什么是 Florr World？

一款 2D 开放世界游戏，核心特色是**奇异物理**——在经典力学基础上引入量子隧穿、惯性奇点、时间常数偏移等物理现象，玩家通过探索、实验来理解这个世界的规律。

## ✨ 核心特色

### 奇异物理引擎
- 🌀 **惯性奇点** — 极端加速下惯性归零，实现瞬间位移
- 👻 **相位穿透** — 物体可进入相位态穿越障碍
- 🌍 **重力异常层** — 不同区域重力方向/强度动态变化
- ⚛️ **量子纠缠** — 粒子跨距离即时关联
- ⏱️ **时间常数偏移** — 局部时间流速可调

### 玩家质点系统
- 🎯 5种属性：质量、电荷、自旋、动能、连接端口
- 🔗 5种连接类型：弹簧、铰链、融合、相位链接、引力连接

### 四纪元科技树
- 第一纪元 → 第二纪元 → 第三纪元 → 第四纪元
- 从基础工具到量子科技的完整升级路径

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/PANP2010/florr-world.git
cd florr-world

# 安装依赖
pip install pygame

# 运行游戏
python main.py
```

## 📁 项目结构

```
florr_world/
├── src/
│   ├── physics/     # 物理引擎 + 奇异物理
│   ├── player/      # 玩家质点系统
│   ├── building/    # 建造与工具
│   └── core/       # 核心玩法循环
├── tests/          # 测试套件
├── docs/           # 文档
└── main.py         # 入口
```

## 🛠️ 开发

```bash
# 运行测试
python -m pytest tests/

# 代码规范检查
ruff check src/
```

## 📜 许可证

MIT License
