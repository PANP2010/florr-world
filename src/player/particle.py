"""
PlayerParticle - 玩家质点
代表玩家的基本粒子实体
"""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class PlayerParticle:
    """玩家质点"""

    mass: float = 1.0
    charge: float = 0.0
    spin: float = 0.0
    kinetic_energy: float = 0.0
    position: Tuple[float, float] = (0.0, 0.0)
    velocity: Tuple[float, float] = (0.0, 0.0)
    connections: List[any] = field(default_factory=list)

    def apply_force(self, fx: float, fy: float) -> None:
        """施加力"""
        if self.mass > 0:
            ax = fx / self.mass
            ay = fy / self.mass
            vx, vy = self.velocity
            self.velocity = (vx + ax, vy + ay)

    def update_position(self, dt: float) -> None:
        """更新位置"""
        x, y = self.position
        vx, vy = self.velocity
        self.position = (x + vx * dt, y + vy * dt)

    def add_connection(self, connection: any) -> None:
        """添加连接"""
        self.connections.append(connection)

    def remove_connection(self, connection: any) -> None:
        """移除连接"""
        if connection in self.connections:
            self.connections.remove(connection)
