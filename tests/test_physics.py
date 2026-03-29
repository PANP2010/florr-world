"""
物理引擎单元测试
"""
import pytest
import math
from src.physics import (
    Vector2,
    RigidBody,
    PhysicsEngine,
    AABB,
    Circle,
    CollisionDetector,
    CollisionResponse,
    CollisionManifold
)


class TestVector2:
    """Vector2 向量类测试"""
    
    def test_creation(self):
        """测试向量创建"""
        v = Vector2(3, 4)
        assert v.x == 3
        assert v.y == 4
    
    def test_addition(self):
        """测试向量加法"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        result = v1 + v2
        assert result.x == 4
        assert result.y == 6
    
    def test_subtraction(self):
        """测试向量减法"""
        v1 = Vector2(5, 7)
        v2 = Vector2(2, 3)
        result = v1 - v2
        assert result.x == 3
        assert result.y == 4
    
    def test_multiplication(self):
        """测试标量乘法"""
        v = Vector2(3, 4)
        result = v * 2
        assert result.x == 6
        assert result.y == 8
        
        # 右乘
        result = 3 * v
        assert result.x == 9
        assert result.y == 12
    
    def test_division(self):
        """测试标量除法"""
        v = Vector2(6, 8)
        result = v / 2
        assert result.x == 3
        assert result.y == 4
    
    def test_magnitude(self):
        """测试向量长度"""
        v = Vector2(3, 4)
        assert v.magnitude() == pytest.approx(5)
        
        # 零向量
        v0 = Vector2(0, 0)
        assert v0.magnitude() == 0
    
    def test_normalized(self):
        """测试单位向量"""
        v = Vector2(3, 4)
        n = v.normalized()
        assert n.x == pytest.approx(0.6)
        assert n.y == pytest.approx(0.8)
        
        # 零向量应该返回零向量
        v0 = Vector2(0, 0)
        n0 = v0.normalized()
        assert n0.x == 0
        assert n0.y == 0
    
    def test_dot(self):
        """测试点积"""
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        assert v1.dot(v2) == 1 * 3 + 2 * 4  # 11
    
    def test_cross(self):
        """测试叉积"""
        v1 = Vector2(1, 0)
        v2 = Vector2(0, 1)
        assert v1.cross(v2) == 1  # 右手定则，z轴正方向
    
    def test_distance(self):
        """测试向量距离"""
        v1 = Vector2(0, 0)
        v2 = Vector2(3, 4)
        assert v1.distance_to(v2) == pytest.approx(5)
    
    def test_angle(self):
        """测试角度计算"""
        v = Vector2(1, 0)
        assert v.angle() == pytest.approx(0)
        
        v2 = Vector2(0, 1)
        assert v2.angle() == pytest.approx(math.pi / 2)
    
    def test_rotate(self):
        """测试向量旋转"""
        v = Vector2(1, 0)
        v_rot = v.rotated(math.pi / 2)  # 旋转90度
        assert v_rot.x == pytest.approx(0, abs=1e-10)
        assert v_rot.y == pytest.approx(1, abs=1e-10)
    
    def test_lerp(self):
        """测试线性插值"""
        v1 = Vector2(0, 0)
        v2 = Vector2(10, 10)
        
        result = v1.lerp(v2, 0.5)
        assert result.x == pytest.approx(5)
        assert result.y == pytest.approx(5)
        
        result = v1.lerp(v2, 0)
        assert result.x == 0
        assert result.y == 0
    
    def test_negate(self):
        """测试向量取负"""
        v = Vector2(3, 4)
        neg = -v
        assert neg.x == -3
        assert neg.y == -4


class TestRigidBody:
    """RigidBody 刚体类测试"""
    
    def test_creation(self):
        """测试刚体创建"""
        body = RigidBody(
            mass=10,
            position=Vector2(100, 200)
        )
        assert body.mass == 10
        assert body.position == Vector2(100, 200)
        assert body.velocity == Vector2(0, 0)
    
    def test_apply_force(self):
        """测试施加力"""
        body = RigidBody(mass=10, position=Vector2(0, 0))
        force = Vector2(10, 0)
        body.apply_force(force)
        
        assert len(body.forces) == 1
        assert body.forces[0] == force
    
    def test_update_motion(self):
        """测试刚体运动更新"""
        # 创建刚体，初始速度为0
        body = RigidBody(
            mass=1,
            position=Vector2(0, 0),
            velocity=Vector2(0, 0)
        )
        
        # 施加一个恒定的力 (1N)
        body.apply_force(Vector2(1, 0))
        
        # 时间步长 1 秒
        # a = F/m = 1/1 = 1 m/s²
        # v = v0 + a*dt = 0 + 1*1 = 1 m/s
        # p = p0 + v*dt = 0 + 1*1 = 1 m
        body.update(1)
        
        assert body.velocity.x == pytest.approx(1)
        assert body.position.x == pytest.approx(1)
    
    def test_static_body(self):
        """测试静态刚体（不受力影响）"""
        body = RigidBody(
            mass=float('inf'),
            position=Vector2(0, 0),
            is_static=True
        )
        
        body.apply_force(Vector2(1000, 0))
        body.update(1)
        
        # 静态物体位置不变
        assert body.position.x == 0
    
    def test_gravity_effect(self):
        """测试重力效果"""
        body = RigidBody(
            mass=1,
            position=Vector2(0, 0),
            velocity=Vector2(0, 0)
        )
        
        # 模拟重力 (向下)
        gravity = Vector2(0, 10)
        body.apply_force(gravity * body.mass)
        
        body.update(1)
        
        assert body.velocity.y == pytest.approx(10)
        assert body.position.y == pytest.approx(10)


class TestPhysicsEngine:
    """PhysicsEngine 物理引擎测试"""
    
    def test_creation(self):
        """测试引擎创建"""
        engine = PhysicsEngine()
        assert engine.gravity == Vector2(0, 980)
        assert len(engine.bodies) == 0
    
    def test_custom_gravity(self):
        """测试自定义重力"""
        gravity = Vector2(0, -9.8)
        engine = PhysicsEngine(gravity=gravity)
        assert engine.gravity == gravity
    
    def test_add_body(self):
        """测试添加刚体"""
        engine = PhysicsEngine()
        body = RigidBody(mass=1, position=Vector2(0, 0))
        
        engine.add_body(body)
        
        assert len(engine.bodies) == 1
        assert engine.bodies[0] is body
    
    def test_remove_body(self):
        """测试移除刚体"""
        engine = PhysicsEngine()
        body = RigidBody(mass=1, position=Vector2(0, 0))
        engine.add_body(body)
        
        engine.remove_body(body)
        
        assert len(engine.bodies) == 0
    
    def test_update_with_gravity(self):
        """测试带重力的更新"""
        engine = PhysicsEngine(gravity=Vector2(0, 10))
        body = RigidBody(mass=1, position=Vector2(0, 0))
        engine.add_body(body)
        
        engine.update(1)
        
        # 应该受到重力影响
        assert body.velocity.y == pytest.approx(10)
        assert body.position.y == pytest.approx(10)
    
    def test_collision_detection(self):
        """测试碰撞检测"""
        engine = PhysicsEngine()
        
        # 创建两个圆形刚体（使用默认半径10）
        body_a = RigidBody(mass=1, position=Vector2(0, 0))
        body_b = RigidBody(mass=1, position=Vector2(5, 0))
        
        engine.add_body(body_a)
        engine.add_body(body_b)
        
        collisions = engine.check_collisions()
        
        # 距离5 < 半径20，应该检测到碰撞
        assert len(collisions) == 1


class TestAABB:
    """AABB 碰撞检测测试"""
    
    def test_creation(self):
        """测试 AABB 创建"""
        aabb = AABB(
            min=Vector2(0, 0),
            max=Vector2(100, 50)
        )
        assert aabb.width == 100
        assert aabb.height == 50
        assert aabb.center == Vector2(50, 25)
    
    def test_intersects(self):
        """测试 AABB 相交检测"""
        aabb1 = AABB(min=Vector2(0, 0), max=Vector2(100, 100))
        aabb2 = AABB(min=Vector2(50, 50), max=Vector2(150, 150))
        aabb3 = AABB(min=Vector2(200, 200), max=Vector2(300, 300))
        
        assert aabb1.intersects(aabb2) is True
        assert aabb1.intersects(aabb3) is False
    
    def test_contains_point(self):
        """测试点包含检测"""
        aabb = AABB(min=Vector2(0, 0), max=Vector2(100, 100))
        
        assert aabb.contains_point(Vector2(50, 50)) is True
        assert aabb.contains_point(Vector2(0, 0)) is True
        assert aabb.contains_point(Vector2(100, 100)) is True
        assert aabb.contains_point(Vector2(150, 50)) is False
    
    def test_union(self):
        """测试 AABB 合并"""
        aabb1 = AABB(min=Vector2(0, 0), max=Vector2(50, 50))
        aabb2 = AABB(min=Vector2(100, 100), max=Vector2(150, 150))
        
        union = aabb1.union(aabb2)
        
        assert union.min == Vector2(0, 0)
        assert union.max == Vector2(150, 150)


class TestCircle:
    """Circle 圆形碰撞测试"""
    
    def test_creation(self):
        """测试圆形创建"""
        circle = Circle(center=Vector2(100, 100), radius=50)
        
        assert circle.center == Vector2(100, 100)
        assert circle.radius == 50
    
    def test_circle_vs_circle(self):
        """测试圆与圆碰撞"""
        circle_a = Circle(center=Vector2(0, 0), radius=10)
        circle_b = Circle(center=Vector2(15, 0), radius=10)
        circle_c = Circle(center=Vector2(100, 100), radius=10)
        
        assert circle_a.intersects(circle_b) is True
        assert circle_a.intersects(circle_c) is False
    
    def test_circle_vs_aabb(self):
        """测试圆与 AABB 碰撞"""
        circle = Circle(center=Vector2(50, 50), radius=20)
        aabb = AABB(min=Vector2(40, 40), max=Vector2(60, 60))
        
        assert circle.intersects_aabb(aabb) is True


class TestCollisionDetector:
    """CollisionDetector 碰撞检测器测试"""
    
    def test_circle_vs_circle(self):
        """测试圆形碰撞检测"""
        circle_a = Circle(center=Vector2(0, 0), radius=10)
        circle_b = Circle(center=Vector2(15, 0), radius=10)
        
        manifold = CollisionDetector.circle_vs_circle(circle_a, circle_b)
        
        assert manifold is not None
        assert manifold.penetration == pytest.approx(5)  # 20 - 15 = 5
        assert manifold.normal == Vector2(1, 0)
    
    def test_circle_vs_circle_no_collision(self):
        """测试无碰撞情况"""
        circle_a = Circle(center=Vector2(0, 0), radius=10)
        circle_b = Circle(center=Vector2(100, 0), radius=10)
        
        manifold = CollisionDetector.circle_vs_circle(circle_a, circle_b)
        
        assert manifold is None
    
    def test_aabb_vs_aabb(self):
        """测试 AABB 碰撞检测"""
        aabb_a = AABB(min=Vector2(0, 0), max=Vector2(50, 50))
        aabb_b = AABB(min=Vector2(40, 40), max=Vector2(90, 90))
        
        manifold = CollisionDetector.aabb_vs_aabb(aabb_a, aabb_b)
        
        assert manifold is not None
        assert manifold.penetration == 10  # 50 - 40


class TestCollisionResponse:
    """CollisionResponse 碰撞响应测试"""
    
    def test_elastic_collision(self):
        """测试弹性碰撞响应"""
        # 创建两个质量相等的物体
        body_a = RigidBody(mass=1, position=Vector2(0, 0), velocity=Vector2(10, 0))
        body_b = RigidBody(mass=1, position=Vector2(20, 0), velocity=Vector2(0, 0))
        
        # 创建碰撞流形
        manifold = CollisionManifold(
            body_a=body_a,
            body_b=body_b,
            normal=Vector2(1, 0),
            penetration=0,
            contact_points=[Vector2(10, 0)]
        )
        
        CollisionResponse.resolve_collision(body_a, body_b, manifold)
        
        # 弹性碰撞：动量守恒
        # 初始动量 = 10 * 1 + 0 * 1 = 10
        total_momentum = body_a.velocity.x + body_b.velocity.x
        assert total_momentum == pytest.approx(10)
    
    def test_inelastic_collision(self):
        """测试非弹性碰撞"""
        body_a = RigidBody(mass=1, position=Vector2(0, 0), velocity=Vector2(10, 0))
        body_b = RigidBody(mass=1, position=Vector2(20, 0), velocity=Vector2(0, 0))
        
        manifold = CollisionManifold(
            body_a=body_a,
            body_b=body_b,
            normal=Vector2(1, 0),
            penetration=0,
            contact_points=[Vector2(10, 0)]
        )
        
        CollisionResponse.resolve_inelastic_collision(body_a, body_b, manifold)
        
        # 非弹性碰撞：合并后速度相同
        assert body_a.velocity.x == pytest.approx(body_b.velocity.x)


class TestPhysicsIntegration:
    """物理引擎集成测试"""
    
    def test_free_fall(self):
        """测试自由落体"""
        engine = PhysicsEngine(gravity=Vector2(0, 100))  # 100 px/s²
        
        # 从 y=0 自由落体
        body = RigidBody(mass=1, position=Vector2(100, 0))
        engine.add_body(body)
        
        # 模拟 1 秒
        engine.update(1)
        
        # v = g * t = 100 * 1 = 100
        assert body.velocity.y == pytest.approx(100)
        
        # s = 0.5 * g * t² = 0.5 * 100 * 1 = 50
        assert body.position.y == pytest.approx(50)
    
    def test_projectile_motion(self):
        """测试抛体运动"""
        engine = PhysicsEngine(gravity=Vector2(0, 100))
        
        # 水平抛出
        body = RigidBody(mass=1, position=Vector2(0, 0), velocity=Vector2(50, 0))
        engine.add_body(body)
        
        # 模拟 1 秒
        engine.update(1)
        
        # x = v0x * t = 50 * 1 = 50
        assert body.position.x == pytest.approx(50)
        assert body.velocity.x == pytest.approx(50)  # 水平不受力
        
        # y = 0.5 * g * t² = 50
        assert body.position.y == pytest.approx(50)
        assert body.velocity.y == pytest.approx(100)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
