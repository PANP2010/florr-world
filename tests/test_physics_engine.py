import pytest
import math
from src.physics.engine import PhysicsEngine, RigidBody, Vector2

def test_vector2_add():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 4)
    v3 = v1 + v2
    assert abs(v3.x - 4) < 0.001
    assert abs(v3.y - 6) < 0.001
    
def test_vector2_mul():
    v1 = Vector2(3, 4)
    v2 = v1 * 2
    assert abs(v2.x - 6) < 0.001
    assert abs(v2.y - 8) < 0.001
    
def test_rigidbody_apply_force():
    body = RigidBody(mass=2.0, position=Vector2(0, 0))
    body.apply_force(Vector2(10, 0))
    body.update(1.0)
    # v = F/m * t = 10/2 * 1 = 5
    assert abs(body.velocity.x - 5) < 0.1

def test_physics_engine_gravity():
    engine = PhysicsEngine(gravity=Vector2(0, 10))
    body = RigidBody(mass=1.0, position=Vector2(0, 0))
    engine.add_body(body)
    engine.update(1.0)
    # a = F/m = 10/1 = 10
    assert abs(body.velocity.y - 10) < 0.1
