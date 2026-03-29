"""
碰撞系统测试
测试 AABB vs AABB、Circle vs Circle、Circle vs AABB
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from physics.collision import AABB, Circle, CollisionDetector, CollisionManifold
from physics.engine import Vector2


class TestAABBvsAABB:
    """测试 AABB 与 AABB 碰撞"""
    
    def test_no_collision_separate_boxes(self):
        """测试：两个分离的AABB不应该碰撞"""
        a = AABB(Vector2(0, 0), Vector2(10, 10))
        b = AABB(Vector2(20, 0), Vector2(30, 10))
        
        result = CollisionDetector.aabb_vs_aabb(a, b)
        assert result is None
    
    def test_collision_overlapping_boxes(self):
        """测试：两个重叠的AABB应该碰撞"""
        a = AABB(Vector2(0, 0), Vector2(10, 10))
        b = AABB(Vector2(5, 5), Vector2(15, 15))
        
        result = CollisionDetector.aabb_vs_aabb(a, b)
        assert result is not None
        assert result.penetration > 0
    
    def test_collision_exact_touching(self):
        """测试：两个刚好接触的AABB应该碰撞"""
        a = AABB(Vector2(0, 0), Vector2(10, 10))
        b = AABB(Vector2(10, 0), Vector2(20, 10))
        
        result = CollisionDetector.aabb_vs_aabb(a, b)
        assert result is not None
    
    def test_collision_normal_direction(self):
        """测试：碰撞法线方向正确"""
        a = AABB(Vector2(0, 0), Vector2(10, 10))
        b = AABB(Vector2(5, 5), Vector2(15, 15))
        
        result = CollisionDetector.aabb_vs_aabb(a, b)
        assert result is not None
        # 法线应该是单位向量
        normal = result.normal
        assert abs(normal.x) == 1.0 or abs(normal.y) == 1.0
    
    def test_aabb_intersects_method(self):
        """测试：AABB.intersects 方法"""
        box1 = AABB(Vector2(0, 0), Vector2(10, 10))
        box2 = AABB(Vector2(5, 5), Vector2(15, 15))
        box3 = AABB(Vector2(20, 20), Vector2(30, 30))
        
        assert box1.intersects(box2) == True
        assert box1.intersects(box3) == False


class TestCirclevsCircle:
    """测试 Circle 与 Circle 碰撞"""
    
    def test_no_collision_separate_circles(self):
        """测试：两个分离的圆不应该碰撞"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(20, 0), 5)
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is None
    
    def test_collision_overlapping_circles(self):
        """测试：两个重叠的圆应该碰撞"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(6, 0), 5)
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is not None
        assert result.penetration > 0
    
    def test_collision_concentric_circles(self):
        """测试：同心圆（圆心重合）"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(0, 0), 3)
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is not None
        # 法线默认应该是 (1, 0)
        assert result.normal.x == 1.0
        assert result.normal.y == 0.0
    
    def test_circle_intersects_method(self):
        """测试：Circle.intersects 方法"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(8, 0), 5)
        c3 = Circle(Vector2(20, 0), 5)
        
        assert c1.intersects(c2) == True
        assert c1.intersects(c3) == False
    
    def test_collision_penetration_depth(self):
        """测试：碰撞穿透深度计算"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(6, 0), 5)
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is not None
        # 5 + 5 - 6 = 4
        assert result.penetration == pytest.approx(4.0, rel=1e-5)
    
    def test_contact_point_calculation(self):
        """测试：接触点计算"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(6, 0), 5)
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is not None
        assert len(result.contact_points) > 0


class TestCirclevsAABB:
    """测试 Circle 与 AABB 碰撞"""
    
    def test_no_collision_separated(self):
        """测试：分离的圆和AABB不应该碰撞"""
        c = Circle(Vector2(0, 0), 5)
        a = AABB(Vector2(20, 0), Vector2(30, 10))
        
        result = CollisionDetector.circle_vs_aabb(c, a)
        assert result is None
    
    def test_collision_overlapping(self):
        """测试：重叠的圆和AABB应该碰撞"""
        c = Circle(Vector2(5, 5), 5)
        a = AABB(Vector2(0, 0), Vector2(10, 10))
        
        result = CollisionDetector.circle_vs_aabb(c, a)
        assert result is not None
        assert result.penetration > 0
    
    def test_circle_inside_aabb(self):
        """测试：圆完全在AABB内部"""
        c = Circle(Vector2(5, 5), 2)
        a = AABB(Vector2(0, 0), Vector2(10, 10))
        
        result = CollisionDetector.circle_vs_aabb(c, a)
        assert result is not None
    
    def test_aabb_contains_circle_center(self):
        """测试：AABB包含圆心"""
        c = Circle(Vector2(5, 5), 10)  # 半径10
        a = AABB(Vector2(0, 0), Vector2(10, 10))  # 10x10
        
        result = CollisionDetector.circle_vs_aabb(c, a)
        assert result is not None
    
    def test_circle_intersects_aabb_method(self):
        """测试：Circle.intersects_aabb 方法"""
        c = Circle(Vector2(5, 5), 5)
        box_inside = AABB(Vector2(0, 0), Vector2(10, 10))
        box_outside = AABB(Vector2(20, 20), Vector2(30, 30))
        
        assert c.intersects_aabb(box_inside) == True
        assert c.intersects_aabb(box_outside) == False
    
    def test_collision_point_on_aabb_edge(self):
        """测试：碰撞点应该在AABB边缘"""
        c = Circle(Vector2(5, 5), 5)
        a = AABB(Vector2(10, 5), Vector2(20, 15))
        
        result = CollisionDetector.circle_vs_aabb(c, a)
        assert result is not None
        # 碰撞点x应该接近10（box的左边缘）
        point = result.contact_points[0]
        assert point.x == pytest.approx(10.0, abs=0.001)


class TestCollisionManifold:
    """测试 CollisionManifold 数据结构"""
    
    def test_manifold_has_required_fields(self):
        """测试：CollisionManifold 包含必要字段"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(6, 0), 5)
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is not None
        
        assert hasattr(result, 'normal')
        assert hasattr(result, 'penetration')
        assert hasattr(result, 'contact_points')
    
    def test_normal_is_unit_vector(self):
        """测试：碰撞法线是单位向量"""
        c1 = Circle(Vector2(0, 0), 5)
        c2 = Circle(Vector2(3, 4), 5)  # dist = 5
        
        result = CollisionDetector.circle_vs_circle(c1, c2)
        assert result is not None
        
        normal = result.normal
        length = (normal.x**2 + normal.y**2) ** 0.5
        assert length == pytest.approx(1.0, abs=1e-6)


class TestAABBStructure:
    """测试 AABB 数据结构"""
    
    def test_aabb_properties(self):
        """测试：AABB 属性"""
        a = AABB(Vector2(5, 10), Vector2(15, 20))
        
        assert a.width == 10.0
        assert a.height == 10.0
        assert a.center.x == 10.0
        assert a.center.y == 15.0


class TestCircleStructure:
    """测试 Circle 数据结构"""
    
    def test_circle_center(self):
        """测试：Circle 圆心"""
        c = Circle(Vector2(10, 20), 5)
        
        assert c.center.x == 10.0
        assert c.center.y == 20.0
        assert c.radius == 5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
