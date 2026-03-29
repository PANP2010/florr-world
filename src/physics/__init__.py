"""
物理引擎模块

提供 2D 物理模拟功能：
- 刚体动力学
- 碰撞检测（AABB、圆形）
- 碰撞响应（弹性、非弹性）
"""
from .engine import Vector2, RigidBody, PhysicsEngine
from .collision import (
    AABB,
    Circle,
    CollisionManifold,
    CollisionDetector,
    CollisionResponse
)

__all__ = [
    # 核心
    'Vector2',
    'RigidBody',
    'PhysicsEngine',
    # 碰撞
    'AABB',
    'Circle',
    'CollisionManifold',
    'CollisionDetector',
    'CollisionResponse',
]

__version__ = '0.1.0'
