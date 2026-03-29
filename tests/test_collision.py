"""
碰撞系统测试
测试 AABB vs AABB、Circle vs Circle、Circle vs AABB
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from physics.collision import AABB, Circle, CollisionSystem, CollisionManifold


class TestAABBvsAABB:
    """测试 AABB 与 AABB 碰撞"""
    
    def test_no_collision_separate_boxes(self):
        """测试：两个分离的AABB不应该碰撞"""
        system = CollisionSystem()
        system.add_box(0, 0, 10, 10, tag="box1")
        system.add_box(20, 0, 10, 10, tag="box2")
        
        results = system.check_all()
        assert len(results) == 0
    
    def test_collision_overlapping_boxes(self):
        """测试：两个重叠的AABB应该碰撞"""
        system = CollisionSystem()
        system.add_box(0, 0, 10, 10, tag="box1")
        system.add_box(5, 5, 10, 10, tag="box2")
        
        results = system.check_all()
        assert len(results) == 1
        assert results[0].depth > 0
    
    def test_collision_exact_touching(self):
        """测试：两个刚好接触的AABB应该碰撞"""
        system = CollisionSystem()
        system.add_box(0, 0, 10, 10, tag="box1")
        system.add_box(10, 0, 10, 10, tag="box2")
        
        results = system.check_all()
        assert len(results) == 1
    
    def test_collision_normal_direction(self):
        """测试：碰撞法线方向正确"""
        system = CollisionSystem()
        system.add_box(0, 0, 10, 10, tag="box1")
        system.add_box(5, 5, 10, 10, tag="box2")
        
        results = system.check_all()
        assert len(results) == 1
        # 法线应该是单位向量
        normal = results[0].normal
        assert abs(normal[0]) == 1.0 or abs(normal[1]) == 1.0
    
    def test_aabb_intersects_method(self):
        """测试：AABB.intersects 方法"""
        box1 = AABB(0, 0, 10, 10)
        box2 = AABB(5, 5, 10, 10)
        box3 = AABB(20, 20, 10, 10)
        
        assert box1.intersects(box2) == True
        assert box1.intersects(box3) == False


class TestCirclevsCircle:
    """测试 Circle 与 Circle 碰撞"""
    
    def test_no_collision_separate_circles(self):
        """测试：两个分离的圆不应该碰撞"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle1")
        system.add_circle(20, 0, 5, tag="circle2")
        
        results = system.check_all()
        assert len(results) == 0
    
    def test_collision_overlapping_circles(self):
        """测试：两个重叠的圆应该碰撞"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle1")
        system.add_circle(5, 0, 5, tag="circle2")
        
        results = system.check_all()
        assert len(results) == 1
        assert results[0].depth > 0
    
    def test_collision_concentric_circles(self):
        """测试：同心圆（圆心重合）"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle1")
        system.add_circle(0, 0, 3, tag="circle2")
        
        results = system.check_all()
        assert len(results) == 1
        # 法线默认(1,0)
        assert results[0].normal == (1.0, 0.0)
    
    def test_circle_intersects_method(self):
        """测试：Circle.intersects 方法"""
        c1 = Circle(0, 0, 5)
        c2 = Circle(8, 0, 5)
        c3 = Circle(20, 0, 5)
        
        assert c1.intersects(c2) == True
        assert c1.intersects(c3) == False
    
    def test_collision_depth(self):
        """测试：碰撞深度计算"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle1")
        system.add_circle(6, 0, 5, tag="circle2")
        
        results = system.check_all()
        assert len(results) == 1
        # 5 + 5 - 6 = 4
        assert results[0].depth == pytest.approx(4.0, rel=1e-5)


class TestCirclevsAABB:
    """测试 Circle 与 AABB 碰撞"""
    
    def test_no_collision_separated(self):
        """测试：分离的圆和AABB不应该碰撞"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle")
        system.add_box(20, 0, 10, 10, tag="box")
        
        results = system.check_all()
        assert len(results) == 0
    
    def test_collision_overlapping(self):
        """测试：重叠的圆和AABB应该碰撞"""
        system = CollisionSystem()
        system.add_circle(5, 5, 5, tag="circle")
        system.add_box(0, 0, 10, 10, tag="box")
        
        results = system.check_all()
        assert len(results) == 1
        assert results[0].depth > 0
    
    def test_circle_inside_aabb(self):
        """测试：圆完全在AABB内部"""
        system = CollisionSystem()
        system.add_circle(5, 5, 2, tag="circle")
        system.add_box(0, 0, 10, 10, tag="box")
        
        results = system.check_all()
        assert len(results) == 1
    
    def test_aabb_contains_circle_center(self):
        """测试：AABB包含圆心"""
        system = CollisionSystem()
        system.add_circle(5, 5, 10, tag="circle")  # 半径10
        system.add_box(0, 0, 10, 10, tag="box")    # 10x10
        
        results = system.check_all()
        assert len(results) == 1
    
    def test_circle_intersects_aabb_method(self):
        """测试：Circle.intersects_aabb 方法"""
        circle = Circle(5, 5, 5)
        box_inside = AABB(0, 0, 10, 10)
        box_outside = AABB(20, 20, 10, 10)
        
        assert circle.intersects_aabb(box_inside) == True
        assert circle.intersects_aabb(box_outside) == False
    
    def test_collision_point_on_aabb_edge(self):
        """测试：碰撞点应该在AABB边缘"""
        system = CollisionSystem()
        system.add_circle(5, 5, 5, tag="circle")
        system.add_box(10, 5, 10, 10, tag="box")
        
        results = system.check_all()
        assert len(results) == 1
        # 碰撞点x应该接近10（box的左边缘）
        point = results[0].point
        assert point[0] == pytest.approx(10.0, abs=0.001)


class TestCollisionSystem:
    """测试 CollisionSystem 整体功能"""
    
    def test_clear_colliders(self):
        """测试：清空碰撞体"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5)
        system.add_box(0, 0, 10, 10)
        
        assert len(system.colliders) == 2
        
        system.clear()
        assert len(system.colliders) == 0
    
    def test_multiple_collisions(self):
        """测试：多个碰撞体"""
        system = CollisionSystem()
        system.add_box(0, 0, 10, 10, tag="box1")
        system.add_box(5, 5, 10, 10, tag="box2")
        system.add_box(20, 20, 10, 10, tag="box3")
        system.add_circle(15, 15, 5, tag="circle")
        
        results = system.check_all()
        # box1 vs box2 应该碰撞
        # box2 vs circle 可能碰撞
        # box3 不与任何物体碰撞
        assert len(results) >= 1
    
    def test_collision_manifold_structure(self):
        """测试：CollisionManifold 数据结构"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle1")
        system.add_circle(6, 0, 5, tag="circle2")
        
        results = system.check_all()
        assert len(results) == 1
        
        manifold = results[0]
        assert isinstance(manifold, CollisionManifold)
        assert manifold.body_a["tag"] == "circle1"
        assert manifold.body_b["tag"] == "circle2"
        assert isinstance(manifold.normal, tuple)
        assert manifold.depth > 0
        assert isinstance(manifold.point, tuple)
    
    def test_normalized_normal(self):
        """测试：碰撞法线是单位向量"""
        system = CollisionSystem()
        system.add_circle(0, 0, 5, tag="circle1")
        system.add_circle(3, 4, 5, tag="circle2")  # dist = 5
        
        results = system.check_all()
        assert len(results) == 1
        
        normal = results[0].normal
        length = (normal[0]**2 + normal[1]**2) ** 0.5
        assert length == pytest.approx(1.0, abs=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
