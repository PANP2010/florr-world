import pytest
from src.physics.collision import AABB, Circle, CollisionSystem

def test_aabb_intersects():
    a = AABB(0, 0, 10, 10)
    b = AABB(5, 5, 10, 10)
    assert a.intersects(b) == True
    
def test_aabb_no_intersect():
    a = AABB(0, 0, 10, 10)
    b = AABB(20, 20, 10, 10)
    assert a.intersects(b) == False
    
def test_circle_intersects():
    a = Circle(0, 0, 5)
    b = Circle(8, 0, 5)
    assert a.intersects(b) == True
    
def test_circle_no_intersect():
    a = Circle(0, 0, 5)
    b = Circle(20, 0, 5)
    assert a.intersects(b) == False
    
def test_collision_system():
    system = CollisionSystem()
    aabb = AABB(0, 0, 10, 10)
    circle = Circle(5, 5, 3)
    # AABB 和 Circle 的碰撞检测
    result = system.check_collision(aabb, circle)
    assert result == True
