"""
PhysicsEngine - 物理引擎核心
提供基础物理模拟能力
"""
from typing import List, Dict, Any, Optional


class PhysicsEngine:
    """物理引擎主类"""

    def __init__(self):
        self.gravity: float = 9.8
        self.time_scale: float = 1.0
        self.entities: List[Any] = []

    def add_entity(self, entity: Any) -> None:
        """添加物理实体"""
        self.entities.append(entity)

    def remove_entity(self, entity: Any) -> None:
        """移除物理实体"""
        if entity in self.entities:
            self.entities.remove(entity)

    def update(self, dt: float) -> None:
        """更新物理状态"""
        for entity in self.entities:
            if hasattr(entity, "update_physics"):
                entity.update_physics(dt, self)

    def get_gravity_at(self, x: float, y: float) -> float:
        """获取指定位置的引力强度"""
        return self.gravity

    def set_gravity_scale(self, scale: float) -> None:
        """设置全局重力缩放"""
        self.gravity = 9.8 * scale
