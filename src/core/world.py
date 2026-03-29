"""
World - 游戏世界
管理所有实体、区域、物理状态
"""
from dataclasses import dataclass
from typing import List, Optional, Any
from ..physics.engine import PhysicsEngine
from ..player.particle import PlayerParticle


@dataclass
class Region:
    """区域 - 可以有特殊物理属性"""

    name: str
    bounds: tuple  # (x1, y1, x2, y2)
    gravity_scale: float = 1.0
    time_scale: float = 1.0
    phase_active: bool = False


class GameWorld:
    """游戏世界"""

    def __init__(self, width: int, height: int):
        """
        初始化游戏世界

        Args:
            width: 世界宽度
            height: 世界高度
        """
        self.width = width
        self.height = height
        self.physics = PhysicsEngine()
        self.player: Optional[PlayerParticle] = None
        self.regions: List[Region] = []

    def add_region(self, region: Region) -> None:
        """
        添加区域到世界

        Args:
            region: 区域对象
        """
        self.regions.append(region)

    def get_region_at(self, x: float, y: float) -> Optional[Region]:
        """
        获取指定坐标所在的区域

        Args:
            x: X坐标
            y: Y坐标

        Returns:
            区域对象，如果坐标不在任何区域内则返回None
        """
        for region in self.regions:
            x1, y1, x2, y2 = region.bounds
            if x1 <= x <= x2 and y1 <= y <= y2:
                return region
        return None

    def update(self, dt: float) -> None:
        """
        更新世界状态

        Args:
            dt: 时间步长
        """
        self.physics.update(dt)
        if self.player:
            self.player.update_position(dt)
