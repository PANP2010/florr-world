"""
Core - 核心玩法模块
包含游戏世界管理和核心玩法循环
"""
from .world import GameWorld, Region
from .loop import (
    GameLoop,
    ObservationSystem,
    HypothesisSystem,
    ExperimentSystem,
    FeedbackSystem,
    LoopPhase,
)

__all__ = [
    "GameWorld",
    "Region",
    "GameLoop",
    "ObservationSystem",
    "HypothesisSystem",
    "ExperimentSystem",
    "FeedbackSystem",
    "LoopPhase",
]
