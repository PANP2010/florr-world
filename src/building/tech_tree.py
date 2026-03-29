"""
TechTree - 四纪元科技树
第一纪元：基础工具
第二纪元：机械装置
第三纪元：能量科技
第四纪元：量子科技
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


class Era(Enum):
    FIRST = 1   # 基础工具
    SECOND = 2  # 机械装置
    THIRD = 3   # 能量科技
    FOURTH = 4  # 量子科技


@dataclass
class TechNode:
    name: str
    era: Era
    cost: int
    requires: List[str]  # 前置科技
    unlocked: bool = False
    description: str = ""


class TechTree:
    """科技树"""

    def __init__(self) -> None:
        self.techs: Dict[str, TechNode] = {}
        self.unlocked: Set[str] = set()
        self._init_techs()

    def _init_techs(self) -> None:
        # 第一纪元
        self.add_tech("basic_tools", "基础工具", Era.FIRST, 0, [])
        self.add_tech("wheel", "轮子", Era.FIRST, 10, ["basic_tools"])

        # 第二纪元
        self.add_tech("gear", "齿轮", Era.SECOND, 50, ["wheel"])
        self.add_tech("spring", "弹簧", Era.SECOND, 30, ["basic_tools"])

        # 第三纪元
        self.add_tech("battery", "电池", Era.THIRD, 100, ["gear"])
        self.add_tech("electric_motor", "电动机", Era.THIRD, 200, ["battery", "gear"])

        # 第四纪元
        self.add_tech("quantum_core", "量子核心", Era.FOURTH, 500, ["electric_motor"])
        self.add_tech("phase_generator", "相位发生器", Era.FOURTH, 1000, ["quantum_core"])

    def add_tech(
        self,
        tech_id: str,
        name: str,
        era: Era,
        cost: int,
        requires: List[str],
        description: str = "",
    ) -> None:
        self.techs[tech_id] = TechNode(
            name=name,
            era=era,
            cost=cost,
            requires=requires,
            unlocked=False,
            description=description,
        )

    def can_unlock(self, tech_id: str) -> bool:
        """检查是否可以解锁某科技（前置科技已全部解锁）"""
        if tech_id not in self.techs:
            return False
        node = self.techs[tech_id]
        if node.unlocked:
            return False
        return all(req in self.unlocked for req in node.requires)

    def unlock(self, tech_id: str) -> bool:
        """解锁科技，成功返回 True"""
        if not self.can_unlock(tech_id):
            return False
        node = self.techs[tech_id]
        node.unlocked = True
        self.unlocked.add(tech_id)
        return True

    def is_unlocked(self, tech_id: str) -> bool:
        """检查科技是否已解锁"""
        return tech_id in self.unlocked

    def get_era_techs(self, era: Era) -> List[TechNode]:
        """获取某纪元的所有科技"""
        return [t for t in self.techs.values() if t.era == era]

    def reset(self) -> None:
        """重置科技树（重新开始）"""
        self.unlocked.clear()
        for node in self.techs.values():
            node.unlocked = False
