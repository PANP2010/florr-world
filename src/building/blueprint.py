"""
Blueprint - 蓝图系统
玩家设计并保存结构
"""
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any


@dataclass
class BlueprintComponent:
    component_type: str
    position: Tuple[float, float]
    rotation: float
    params: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component_type": self.component_type,
            "position": self.position,
            "rotation": self.rotation,
            "params": self.params,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlueprintComponent":
        return cls(
            component_type=data["component_type"],
            position=tuple(data["position"]),
            rotation=data["rotation"],
            params=data["params"],
        )


@dataclass
class Blueprint:
    name: str
    author: str
    components: List[BlueprintComponent] = field(default_factory=list)
    total_cost: int = 0

    def add_component(self, comp: BlueprintComponent) -> None:
        self.components.append(comp)

    def remove_component(self, index: int) -> BlueprintComponent:
        """移除指定索引的组件"""
        return self.components.pop(index)

    def clear(self) -> None:
        """清空所有组件"""
        self.components.clear()
        self.total_cost = 0

    def calculate_cost(self, cost_table: Dict[str, int]) -> int:
        """根据成本表计算蓝图总成本"""
        total = 0
        for comp in self.components:
            total += cost_table.get(comp.component_type, 0)
        self.total_cost = total
        return total

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "author": self.author,
            "components": [c.to_dict() for c in self.components],
            "total_cost": self.total_cost,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Blueprint":
        bp = cls(
            name=data["name"],
            author=data["author"],
            components=[
                BlueprintComponent.from_dict(c) for c in data.get("components", [])
            ],
            total_cost=data.get("total_cost", 0),
        )
        return bp
