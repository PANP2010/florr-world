"""
CollisionSystem - 碰撞检测与响应
支持：AABB、圆形碰撞检测与碰撞响应
"""
import math
from typing import Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class AABB:
    """轴对齐边界框"""
    x: float
    y: float
    width: float
    height: float
    
    @property
    def center_x(self) -> float:
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        return self.y + self.height / 2
    
    @property
    def left(self) -> float:
        return self.x
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def top(self) -> float:
        return self.y
    
    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    def intersects(self, other: 'AABB') -> bool:
        """检测两个AABB是否相交"""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)


@dataclass  
class Circle:
    """圆形碰撞体"""
    x: float
    y: float
    radius: float
    
    @property
    def center_x(self) -> float:
        return self.x
    
    @property
    def center_y(self) -> float:
        return self.y
    
    def intersects(self, other: 'Circle') -> bool:
        """检测两个圆形是否相交"""
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.sqrt(dx*dx + dy*dy)
        return dist < self.radius + other.radius
        
    def intersects_aabb(self, aabb: AABB) -> bool:
        """检测圆与AABB是否相交"""
        nearest_x = max(aabb.x, min(self.x, aabb.x + aabb.width))
        nearest_y = max(aabb.y, min(self.y, aabb.y + aabb.height))
        dx = self.x - nearest_x
        dy = self.y - nearest_y
        return dx*dx + dy*dy < self.radius * self.radius


@dataclass
class CollisionManifold:
    """碰撞流形，包含碰撞详细信息"""
    body_a: object
    body_b: object
    normal: Tuple[float, float]
    depth: float
    point: Tuple[float, float]


class CollisionSystem:
    """碰撞检测系统"""
    
    def __init__(self):
        self.colliders = []
        
    def add_box(self, x: float, y: float, w: float, h: float, tag: str = ""):
        """添加矩形碰撞体"""
        self.colliders.append({
            "type": "aabb", 
            "shape": AABB(x, y, w, h), 
            "tag": tag
        })
        
    def add_circle(self, x: float, y: float, r: float, tag: str = ""):
        """添加圆形碰撞体"""
        self.colliders.append({
            "type": "circle", 
            "shape": Circle(x, y, r), 
            "tag": tag
        })
    
    def clear(self):
        """清空所有碰撞体"""
        self.colliders.clear()
        
    def check_all(self) -> List[CollisionManifold]:
        """检测所有碰撞体之间的碰撞"""
        results = []
        for i in range(len(self.colliders)):
            for j in range(i+1, len(self.colliders)):
                col = self._check_pair(self.colliders[i], self.colliders[j])
                if col:
                    results.append(col)
        return results
    
    def _check_pair(self, a: dict, b: dict) -> Optional[CollisionManifold]:
        """检测一对碰撞体之间的碰撞"""
        type_a, type_b = a["type"], b["type"]
        shape_a, shape_b = a["shape"], b["shape"]
        
        # Circle vs Circle
        if type_a == "circle" and type_b == "circle":
            return self._circle_vs_circle(shape_a, shape_b, a, b)
        
        # Circle vs AABB
        if type_a == "circle" and type_b == "aabb":
            return self._circle_vs_aabb(shape_a, shape_b, a, b)
        
        # AABB vs Circle
        if type_a == "aabb" and type_b == "circle":
            return self._circle_vs_aabb(shape_b, shape_a, b, a)
        
        # AABB vs AABB
        if type_a == "aabb" and type_b == "aabb":
            return self._aabb_vs_aabb(shape_a, shape_b, a, b)
        
        return None
    
    def _circle_vs_circle(self, a: Circle, b: Circle, 
                          body_a: dict, body_b: dict) -> Optional[CollisionManifold]:
        """圆形 vs 圆形碰撞检测"""
        dx = b.x - a.x
        dy = b.y - a.y
        dist = math.sqrt(dx*dx + dy*dy)
        min_dist = a.radius + b.radius
        
        if dist < min_dist:
            # 计算碰撞法线
            if dist == 0:
                normal = (1.0, 0.0)
            else:
                normal = (dx / dist, dy / dist)
            
            # 碰撞深度
            depth = min_dist - dist
            
            # 碰撞点（取圆心连线上的点）
            point = (
                a.x + normal[0] * a.radius,
                a.y + normal[1] * a.radius
            )
            
            return CollisionManifold(body_a, body_b, normal, depth, point)
        
        return None
    
    def _circle_vs_aabb(self, circle: Circle, aabb: AABB,
                        body_circle: dict, body_aabb: dict) -> Optional[CollisionManifold]:
        """圆形 vs AABB碰撞检测"""
        if not circle.intersects_aabb(aabb):
            return None
        
        # 找到圆心上距离AABB最近的点
        nearest_x = max(aabb.x, min(circle.x, aabb.x + aabb.width))
        nearest_y = max(aabb.y, min(circle.y, aabb.y + aabb.height))
        
        dx = circle.x - nearest_x
        dy = circle.y - nearest_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # 计算法线
        if dist == 0:
            # 圆心在AABB内部，找最近边
            dx = circle.x - aabb.center_x
            dy = circle.y - aabb.center_y
            
            # 判断在AABB的哪一侧
            half_w = aabb.width / 2
            half_h = aabb.height / 2
            
            overlap_x = half_w - abs(dx)
            overlap_y = half_h - abs(dy)
            
            if overlap_x < overlap_y:
                normal = (1.0 if dx > 0 else -1.0, 0.0)
                depth = overlap_x
            else:
                normal = (0.0, 1.0 if dy > 0 else -1.0)
                depth = overlap_y
                
            point = (nearest_x, nearest_y)
        else:
            normal = (dx / dist, dy / dist)
            depth = circle.radius - dist
            point = (nearest_x, nearest_y)
        
        return CollisionManifold(body_circle, body_aabb, normal, depth, point)
    
    def _aabb_vs_aabb(self, a: AABB, b: AABB,
                      body_a: dict, body_b: dict) -> Optional[CollisionManifold]:
        """AABB vs AABB碰撞检测"""
        if not a.intersects(b):
            return None
        
        # 计算重叠量
        overlap_left = (a.x + a.width) - b.x
        overlap_right = (b.x + b.width) - a.x
        overlap_top = (a.y + a.height) - b.y
        overlap_bottom = (b.y + b.height) - a.y
        
        # 找最小重叠方向
        min_overlap_x = min(overlap_left, overlap_right)
        min_overlap_y = min(overlap_top, overlap_bottom)
        
        if min_overlap_x < min_overlap_y:
            depth = min_overlap_x
            if overlap_left < overlap_right:
                normal = (-1.0, 0.0)
            else:
                normal = (1.0, 0.0)
        else:
            depth = min_overlap_y
            if overlap_top < overlap_bottom:
                normal = (0.0, -1.0)
            else:
                normal = (0.0, 1.0)
        
        # 碰撞点取AABB中心
        point = ((a.x + a.width/2 + b.x + b.width/2) / 2,
                 (a.y + a.height/2 + b.y + b.height/2) / 2)
        
        return CollisionManifold(body_a, body_b, normal, depth, point)
