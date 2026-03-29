"""
Test suite for exotic physics systems
"""
import pytest
import math


class MockVector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class MockRigidBody:
    def __init__(self):
        self.mass = 1.0
        self.velocity = MockVector2(0, 0)
        self.acceleration = MockVector2(0, 0)
        self._forces = []
        
    def apply_force(self, force):
        self._forces.append(force)


class TestInertialSingularity:
    def test_below_threshold_no_effect(self):
        from src.physics.exotic import InertialSingularity
        body = MockRigidBody()
        body.acceleration = MockVector2(100, 0)
        singularity = InertialSingularity(threshold=5000.0)
        result = singularity.apply(body)
        assert result is False
        assert len(body._forces) == 0

    def test_above_threshold_applies_force(self):
        from src.physics.exotic import InertialSingularity
        body = MockRigidBody()
        body.acceleration = MockVector2(6000, 0)
        body.mass = 2.0
        singularity = InertialSingularity(threshold=5000.0)
        result = singularity.apply(body)
        assert result is True
        assert len(body._forces) == 1


class TestPhaseShift:
    def test_activate_when_ready(self):
        from src.physics.exotic import PhaseShift
        body = MockRigidBody()
        phase = PhaseShift(body)
        result = phase.activate()
        assert result is True
        assert phase.is_phase_active is True

    def test_activate_on_cooldown(self):
        from src.physics.exotic import PhaseShift
        body = MockRigidBody()
        phase = PhaseShift(body)
        phase.current_cooldown = 3.0
        result = phase.activate()
        assert result is False

    def test_update_costs_cooldown(self):
        from src.physics.exotic import PhaseShift
        body = MockRigidBody()
        phase = PhaseShift(body)
        phase.current_cooldown = 2.0
        phase.update(1.0)
        assert phase.current_cooldown == 1.0


class TestGravityAnomaly:
    def test_inside_region(self):
        from src.physics.exotic import GravityAnomaly
        anomaly = GravityAnomaly((0, 0, 100, 100), MockVector2(0, 980))
        assert anomaly.is_inside(50, 50) is True

    def test_outside_region(self):
        from src.physics.exotic import GravityAnomaly
        anomaly = GravityAnomaly((0, 0, 100, 100), MockVector2(0, 980))
        assert anomaly.is_inside(150, 50) is False

    def test_custom_gravity(self):
        from src.physics.exotic import GravityAnomaly
        custom_grav = MockVector2(0, -500)
        anomaly = GravityAnomaly((0, 0, 100, 100), custom_grav)
        g = anomaly.get_gravity()
        assert g.y == -500


class TestQuantumEntanglement:
    def test_propagate_velocity(self):
        from src.physics.exotic import QuantumEntanglePair
        a = MockRigidBody()
        b = MockRigidBody()
        a.velocity.x = 100
        a.velocity.y = 200
        pair = QuantumEntanglePair(a, b)
        pair.propagate_state()
        assert b.velocity.x == a.velocity.x
        assert b.velocity.y == a.velocity.y


class TestTimeDilationField:
    def test_inside_field_slows_time(self):
        from src.physics.exotic import TimeDilationField
        field = TimeDilationField((0, 0, 100, 100), 0.5)
        dt = field.get_effective_dt(0.016, 50, 50)
        assert dt == pytest.approx(0.008)

    def test_outside_field_normal_time(self):
        from src.physics.exotic import TimeDilationField
        field = TimeDilationField((0, 0, 100, 100), 0.5)
        dt = field.get_effective_dt(0.016, 200, 50)
        assert dt == pytest.approx(0.016)

    def test_time_acceleration(self):
        from src.physics.exotic import TimeDilationField
        field = TimeDilationField((0, 0, 100, 100), 2.0)
        dt = field.get_effective_dt(0.016, 50, 50)
        assert dt == pytest.approx(0.032)
