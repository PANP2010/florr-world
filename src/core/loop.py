"""
GameLoop - 核心玩法循环
观察 → 假设 → 实验 → 反馈
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class LoopPhase(Enum):
    """玩法循环阶段"""

    OBSERVE = "observe"
    HYPOTHESIZE = "hypothesize"
    EXPERIMENT = "experiment"
    FEEDBACK = "feedback"


@dataclass
class Observation:
    """观察记录"""

    phenomenon: str
    location: tuple
    data: dict
    timestamp: float = 0.0


class ObservationSystem:
    """观察系统 - 记录玩家观察到的现象"""

    def __init__(self):
        self.observations: List[Observation] = []

    def record(self, phenomenon: str, location: tuple, data: dict) -> int:
        """
        记录一次观察

        Args:
            phenomenon: 观察到的现象名称
            location: 观察位置 (x, y)
            data: 观察数据

        Returns:
            观察记录的ID
        """
        obs = Observation(phenomenon=phenomenon, location=location, data=data)
        self.observations.append(obs)
        return len(self.observations) - 1

    def get_observation(self, observation_id: int) -> Optional[Observation]:
        """获取指定ID的观察记录"""
        if 0 <= observation_id < len(self.observations):
            return self.observations[observation_id]
        return None

    def list_observations(self) -> List[Observation]:
        """列出所有观察记录"""
        return list(self.observations)


class HypothesisSystem:
    """假设系统 - 玩家提出假设"""

    def __init__(self):
        self.hypotheses: List[Dict[str, Any]] = []

    def propose(self, observation_id: int, hypothesis: str) -> int:
        """
        提出假设

        Args:
            observation_id: 基于的观察记录ID
            hypothesis: 假设内容

        Returns:
            假设的ID
        """
        hypo = {
            "id": len(self.hypotheses),
            "observation_id": observation_id,
            "hypothesis": hypothesis,
            "verified": False,
        }
        self.hypotheses.append(hypo)
        return hypo["id"]

    def get_hypothesis(self, hypothesis_id: int) -> Optional[Dict[str, Any]]:
        """获取指定ID的假设"""
        for h in self.hypotheses:
            if h["id"] == hypothesis_id:
                return h
        return None


class ExperimentSystem:
    """实验系统 - 设计实验验证"""

    def __init__(self):
        self.experiments: List[Dict[str, Any]] = []

    def design(self, hypothesis_id: int) -> int:
        """
        设计实验

        Args:
            hypothesis_id: 要验证的假设ID

        Returns:
            实验的ID
        """
        exp = {
            "id": len(self.experiments),
            "hypothesis_id": hypothesis_id,
            "steps": [],
            "results": None,
        }
        self.experiments.append(exp)
        return exp["id"]

    def set_steps(self, experiment_id: int, steps: List[str]) -> None:
        """设置实验步骤"""
        for exp in self.experiments:
            if exp["id"] == experiment_id:
                exp["steps"] = steps
                return

    def record_results(self, experiment_id: int, results: dict) -> None:
        """记录实验结果"""
        for exp in self.experiments:
            if exp["id"] == experiment_id:
                exp["results"] = results
                return


class FeedbackSystem:
    """反馈系统 - 验证结果"""

    def evaluate(self, experiment_results: dict) -> dict:
        """
        评估实验结果

        Args:
            experiment_results: 实验结果数据

        Returns:
            评估结果，包含verified布尔值和reason说明
        """
        verified = experiment_results.get("verified", False)
        reason = experiment_results.get("reason", "未提供原因")
        return {
            "verified": verified,
            "reason": reason,
            "confidence": experiment_results.get("confidence", 0.0),
        }


class GameLoop:
    """核心玩法循环"""

    def __init__(self, world: Any):
        """
        初始化游戏循环

        Args:
            world: 游戏世界对象
        """
        self.world = world
        self.observation = ObservationSystem()
        self.hypothesis = HypothesisSystem()
        self.experiment = ExperimentSystem()
        self.feedback = FeedbackSystem()
        self.phase: LoopPhase = LoopPhase.OBSERVE

    def advance_phase(self) -> None:
        """推进到下一个阶段"""
        phases = list(LoopPhase)
        current_idx = phases.index(self.phase)
        self.phase = phases[(current_idx + 1) % len(phases)]

    def set_phase(self, phase: LoopPhase) -> None:
        """设置当前阶段"""
        self.phase = phase

    def reset(self) -> None:
        """重置游戏循环"""
        self.observation = ObservationSystem()
        self.hypothesis = HypothesisSystem()
        self.experiment = ExperimentSystem()
        self.feedback = FeedbackSystem()
        self.phase = LoopPhase.OBSERVE
