"""
tests/test_core.py - 核心玩法模块测试
"""
import pytest
from src.core.world import GameWorld, Region
from src.core.loop import (
    GameLoop,
    ObservationSystem,
    HypothesisSystem,
    ExperimentSystem,
    FeedbackSystem,
    LoopPhase,
)


class TestRegion:
    """Region 数据类测试"""

    def test_region_creation(self):
        region = Region(name="TestRegion", bounds=(0, 0, 100, 100))
        assert region.name == "TestRegion"
        assert region.bounds == (0, 0, 100, 100)
        assert region.gravity_scale == 1.0
        assert region.time_scale == 1.0
        assert region.phase_active is False

    def test_region_with_custom_values(self):
        region = Region(
            name="GravityZone",
            bounds=(0, 0, 50, 50),
            gravity_scale=2.0,
            time_scale=0.5,
            phase_active=True,
        )
        assert region.gravity_scale == 2.0
        assert region.time_scale == 0.5
        assert region.phase_active is True


class TestGameWorld:
    """GameWorld 测试"""

    def test_world_creation(self):
        world = GameWorld(width=1920, height=1080)
        assert world.width == 1920
        assert world.height == 1080
        assert world.player is None
        assert world.regions == []

    def test_add_region(self):
        world = GameWorld(1000, 1000)
        region = Region(name="Zone1", bounds=(0, 0, 100, 100))
        world.add_region(region)
        assert len(world.regions) == 1
        assert world.regions[0].name == "Zone1"

    def test_get_region_at_inside(self):
        world = GameWorld(1000, 1000)
        region = Region(name="Zone1", bounds=(0, 0, 100, 100))
        world.add_region(region)
        found = world.get_region_at(50, 50)
        assert found is not None
        assert found.name == "Zone1"

    def test_get_region_at_outside(self):
        world = GameWorld(1000, 1000)
        region = Region(name="Zone1", bounds=(0, 0, 100, 100))
        world.add_region(region)
        found = world.get_region_at(500, 500)
        assert found is None

    def test_get_region_at_boundary(self):
        world = GameWorld(1000, 1000)
        region = Region(name="Zone1", bounds=(0, 0, 100, 100))
        world.add_region(region)
        found = world.get_region_at(0, 0)
        assert found is not None
        found = world.get_region_at(100, 100)
        assert found is not None

    def test_update_calls_physics(self):
        world = GameWorld(1000, 1000)
        world.physics.add_entity = lambda e: None
        world.physics.update = lambda dt: None
        world.update(0.016)
        # No exception means success


class TestObservationSystem:
    """观察系统测试"""

    def test_record(self):
        obs_sys = ObservationSystem()
        obs_id = obs_sys.record("gravity anomaly", (10, 20), {"intensity": 0.5})
        assert obs_id == 0
        assert len(obs_sys.observations) == 1

    def test_record_multiple(self):
        obs_sys = ObservationSystem()
        obs_sys.record("phenomenon 1", (0, 0), {})
        obs_sys.record("phenomenon 2", (10, 10), {})
        assert len(obs_sys.observations) == 2

    def test_get_observation(self):
        obs_sys = ObservationSystem()
        obs_sys.record("test", (5, 5), {"key": "value"})
        obs = obs_sys.get_observation(0)
        assert obs is not None
        assert obs.phenomenon == "test"
        assert obs.location == (5, 5)

    def test_get_observation_invalid_id(self):
        obs_sys = ObservationSystem()
        obs = obs_sys.get_observation(99)
        assert obs is None


class TestHypothesisSystem:
    """假设系统测试"""

    def test_propose(self):
        hypo_sys = HypothesisSystem()
        hypo_id = hypo_sys.propose(0, "gravity is stronger here")
        assert hypo_id == 0
        assert len(hypo_sys.hypotheses) == 1

    def test_get_hypothesis(self):
        hypo_sys = HypothesisSystem()
        hypo_sys.propose(0, "hypothesis content")
        hypo = hypo_sys.get_hypothesis(0)
        assert hypo is not None
        assert hypo["hypothesis"] == "hypothesis content"

    def test_get_hypothesis_invalid(self):
        hypo_sys = HypothesisSystem()
        hypo = hypo_sys.get_hypothesis(99)
        assert hypo is None


class TestExperimentSystem:
    """实验系统测试"""

    def test_design(self):
        exp_sys = ExperimentSystem()
        exp_id = exp_sys.design(hypothesis_id=5)
        assert exp_id == 0
        assert len(exp_sys.experiments) == 1

    def test_set_steps(self):
        exp_sys = ExperimentSystem()
        exp_id = exp_sys.design(hypothesis_id=0)
        exp_sys.set_steps(exp_id, ["step1", "step2"])
        exp = exp_sys.experiments[0]
        assert exp["steps"] == ["step1", "step2"]

    def test_record_results(self):
        exp_sys = ExperimentSystem()
        exp_id = exp_sys.design(hypothesis_id=0)
        exp_sys.record_results(exp_id, {"verified": True, "reason": "ok"})
        exp = exp_sys.experiments[0]
        assert exp["results"]["verified"] is True


class TestFeedbackSystem:
    """反馈系统测试"""

    def test_evaluate_verified(self):
        fb_sys = FeedbackSystem()
        result = fb_sys.evaluate({"verified": True, "reason": "matched", "confidence": 0.9})
        assert result["verified"] is True
        assert result["confidence"] == 0.9

    def test_evaluate_not_verified(self):
        fb_sys = FeedbackSystem()
        result = fb_sys.evaluate({"verified": False, "reason": "no match"})
        assert result["verified"] is False

    def test_evaluate_defaults(self):
        fb_sys = FeedbackSystem()
        result = fb_sys.evaluate({})
        assert result["verified"] is False
        assert result["confidence"] == 0.0


class TestGameLoop:
    """游戏循环测试"""

    def test_loop_creation(self):
        world = GameWorld(800, 600)
        loop = GameLoop(world)
        assert loop.world is world
        assert loop.phase == LoopPhase.OBSERVE
        assert isinstance(loop.observation, ObservationSystem)
        assert isinstance(loop.hypothesis, HypothesisSystem)

    def test_advance_phase(self):
        world = GameWorld(800, 600)
        loop = GameLoop(world)
        assert loop.phase == LoopPhase.OBSERVE
        loop.advance_phase()
        assert loop.phase == LoopPhase.HYPOTHESIZE
        loop.advance_phase()
        assert loop.phase == LoopPhase.EXPERIMENT
        loop.advance_phase()
        assert loop.phase == LoopPhase.FEEDBACK
        loop.advance_phase()
        assert loop.phase == LoopPhase.OBSERVE  # cycles back

    def test_set_phase(self):
        world = GameWorld(800, 600)
        loop = GameLoop(world)
        loop.set_phase(LoopPhase.EXPERIMENT)
        assert loop.phase == LoopPhase.EXPERIMENT

    def test_reset(self):
        world = GameWorld(800, 600)
        loop = GameLoop(world)
        loop.observation.record("test", (0, 0), {})
        loop.advance_phase()
        loop.reset()
        assert loop.phase == LoopPhase.OBSERVE
        assert len(loop.observation.observations) == 0
