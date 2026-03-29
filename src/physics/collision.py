"""
碰撞检测模块

提供 AABB、圆形、碰撞响应等碰撞检测功能
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union
from .engine import Vector2, RigidBody
import math


@dataclass
class AABB:
    """
    轴对齐边界框（Axis-Aligned Bounding Box）
    
    用于快速碰撞检测的矩形区域
    
    Attributes:
        min: 左下角坐标
        max: 右上角坐标
    """
    min: Vector2
    max: Vector2
    
    @property
    def width(self) -> float:
        """宽度"""
        return self.max.x - self.min.x
    
    @property
    def height(self) -> float:
        """高度"""
        return self.max.y - self.min.y
    
    @property
    def center(self) -> Vector2:
        """中心点"""
        return Vector2(
            (self.min.x + self.max.x) / 2,
            (self.min.y + self.max.y) / 2
        )
    
    @property
    def left(self) -> float:
        """左边界 x"""
        return self.min.x
    
    @property
    def right(self) -> float:
        """右边界 x"""
        return self.max.x
    
    @property
    def top(self) -> float:
        """上边界 y"""
        return self.max.y
    
    @property
    def bottom(self) -> float:
        """下边界 y"""
        return self.min.y
    
    def intersects(self, other: 'AABB') -> bool:
        """
        检测两个 AABB 是否相交
        
        Args:
            other: 另一个 AABB
        
        Returns:
            是否相交
        """
        if self.max.x < other.min.x or self.min.x > other.max.x:
            return False
        if self.max.y < other.min.y or self.min.y > other.max.y:
            return False
        return True
    
    def contains_point(self, point: Vector2) -> bool:
        """
        检测点是否在 AABB 内部
        
        Args:
            point: 点坐标
        
        Returns:
            是否在内部
        """
        return (self.min.x <= point.x <= self.max.x and 
                self.min.y <= point.y <= self.max.y)
    
    def union(self, other: 'AABB') -> 'AABB':
        """
        合并两个 AABB，返回包含两者的最小 AABB
        
        Args:
            other: 另一个 AABB
        
        Returns:
            合并后的 AABB
        """
        return AABB(
            min=Vector2(min(self.min.x, other.min.x), min(self.min.y, other.min.y)),
            max=Vector2(max(self.max.x, other.max.x), max(self.max.y, other.max.y))
        )
    
    def expanded(self, margin: float) -> 'AABB':
        """
        扩展 AABB 边界
        
        Args:
            margin: 扩展量
        
        Returns:
            扩展后的 AABB
        """
        return AABB(
            min=Vector2(self.min.x - margin, self.min.y - margin),
            max=Vector2(self.max.x + margin, self.max.y + margin)
        )
    
    @classmethod
    def from_center_size(cls, center: Vector2, width: float, height: float) -> 'AABB':
        """
        从中心点和尺寸创建 AABB
        
        Args:
            center: 中心点
            width: 宽度
            height: 高度
        
        Returns:
            AABB 实例
        """
        half_w = width / 2
        half_h = height / 2
        return cls(
            min=Vector2(center.x - half_w, center.y - half_h),
            max=Vector2(center.x + half_w, center.y + half_h)
        )
    
    def __repr__(self) -> str:
        return f"AABB(min={self.min}, max={self.max})"


@dataclass
class Circle:
    """
    圆形碰撞形状
    
    Attributes:
        center: 圆心
        radius: 半径
    """
    center: Vector2
    radius: float
    
    def intersects(self, other: 'Circle') -> bool:
        """
        检测两个圆形是否相交
        
        Args:
            other: 另一个圆形
        
        Returns:
            是否相交
        """
        distance = self.center.distance_to(other.center)
        return distance < (self.radius + other.radius)
    
    def intersects_aabb(self, aabb: AABB) -> bool:
        """
        检测圆形与 AABB 是否相交
        
        Args:
            aabb: AABB
        
        Returns:
            是否相交
        """
        # 找到圆心到 AABB 最近的点
        closest_x = max(aabb.min.x, min(self.center.x, aabb.max.x))
        closest_y = max(aabb.min.y, min(self.center.y, aabb.max.y))
        
        # 计算距离
        distance = Vector2(closest_x, closest_y).distance_to(self.center)
        return distance < self.radius
    
    def contains_point(self, point: Vector2) -> bool:
        """
        检测点是否在圆形内部
        
        Args:
            point: 点坐标
        
        Returns:
            是否在内部
        """
        return self.center.distance_to(point) <= self.radius
    
    def to_aabb(self) -> AABB:
        """
        转换为 AABB（包含圆形的最小矩形）
        
        Returns:
            AABB
        """
        return AABB(
            min=Vector2(self.center.x - self.radius, self.center.y - self.radius),
            max=Vector2(self.center.x + self.radius, self.center.y + self.radius)
        )
    
    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius})"


@dataclass
class CollisionManifold:
    """
    碰撞流形，记录碰撞详细信息
    
    Attributes:
        body_a: 碰撞体 A
        body_b: 碰撞体 B
        normal: 碰撞法线（从 A 指向 B）
        penetration: 穿透深度
        contact_points: 接触点列表
    """
    body_a: RigidBody
    body_b: RigidBody
    normal: Vector2
    penetration: float
    contact_points: List[Vector2] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        """碰撞是否有效"""
        return self.penetration > 0


class CollisionDetector:
    """
    碰撞检测器
    
    提供各种碰撞形状之间的检测算法
    """
    
    @staticmethod
    def circle_vs_circle(circle_a: Circle, circle_b: Circle) -> Optional[CollisionManifold]:
        """
        圆形 vs 圆形碰撞检测
        
        Args:
            circle_a: 圆形 A
            circle_b: 圆形 B
        
        Returns:
            碰撞流形，无碰撞则返回 None
        """
        delta = circle_b.center - circle_a.center
        distance = delta.magnitude()
        sum_radius = circle_a.radius + circle_b.radius
        
        if distance >= sum_radius:
            return None
        
        # 计算碰撞信息
        normal = delta.normalized() if distance > 0 else Vector2(1, 0)
        penetration = sum_radius - distance
        
        # 接触点（取两个圆心的中点）
        contact = circle_a.center + normal * (circle_a.radius - penetration / 2)
        
        return CollisionManifold(
            body_a=None,  # 需要调用者填充
            body_b=None,
            normal=normal,
            penetration=penetration,
            contact_points=[contact]
        )
    
    @staticmethod
    def circle_vs_aabb(circle: Circle, aabb: AABB) -> Optional[CollisionManifold]:
        """
        圆形 vs AABB 碰撞检测
        
        Args:
            circle: 圆形
            aabb: AABB
        
        Returns:
            碰撞流形，无碰撞则返回 None
        """
        # 找到圆心到 AABB 最近的点
        closest_x = max(aabb.min.x, min(circle.center.x, aabb.max.x))
        closest_y = max(aabb.min.y, min(circle.center.y, aabb.max.y))
        closest = Vector2(closest_x, closest_y)
        
        # 计算距离
        delta = circle.center - closest
        distance_sq = delta.magnitude_squared()
        
        if distance_sq >= circle.radius ** 2:
            return None
        
        distance = math.sqrt(distance_sq)
        
        # 计算碰撞信息
        if distance > 0:
            normal = delta / distance
        else:
            # 圆心在 AABB 内部，用法线指向外
            # 找到最近的边
            dx1 = circle.center.x - aabb.min.x
            dx2 = aabb.max.x - circle.center.x
            dy1 = circle.center.y - aabb.min.y
            dy2 = aabb.max.y - circle.center.y
            
            min_d = min(dx1, dx2, dy1, dy2)
            if min_d == dx1:
                normal = Vector2(-1, 0)
            elif min_d == dx2:
                normal = Vector2(1, 0)
            elif min_d == dy1:
                normal = Vector2(0, -1)
            else:
                normal = Vector2(0, 1)
        
        penetration = circle.radius - distance
        
        return CollisionManifold(
            body_a=None,
            body_b=None,
            normal=normal,
            penetration=penetration,
            contact_points=[closest]
        )
    
    @staticmethod
    def aabb_vs_aabb(aabb_a: AABB, aabb_b: AABB) -> Optional[CollisionManifold]:
        """
        AABB vs AABB 碰撞检测
        
        Args:
            aabb_a: AABB A
            aabb_b: AABB B
        
        Returns:
            碰撞流形，无碰撞则返回 None
        """
        if not aabb_a.intersects(aabb_b):
            return None
        
        # 计算穿透深度
        overlap_x = min(aabb_a.max.x, aabb_b.max.x) - max(aabb_a.min.x, aabb_b.min.x)
        overlap_y = min(aabb_a.max.y, aabb_b.max.y) - max(aabb_a.min.y, aabb_b.min.y)
        
        # 确定碰撞法线（选择穿透最小的轴）
        if overlap_x < overlap_y:
            penetration = overlap_x
            center_a = aabb_a.center.x
            center_b = aabb_b.center.x
            normal = Vector2(1, 0) if center_b > center_a else Vector2(-1, 0)
        else:
            penetration = overlap_y
            center_a = aabb_a.center.y
            center_b = aabb_b.center.y
            normal = Vector2(0, 1) if center_b > center_a else Vector2(0, -1)
        
        # 接触点
        contact_x = max(aabb_a.min.x, aabb_b.min.x) + overlap_x / 2
        contact_y = max(aabb_a.min.y, aabb_b.min.y) + overlap_y / 2
        contact = Vector2(contact_x, contact_y)
        
        return CollisionManifold(
            body_a=None,
            body_b=None,
            normal=normal,
            penetration=penetration,
            contact_points=[contact]
        )


class CollisionResponse:
    """
    碰撞响应计算器
    
    提供弹性碰撞和非弹性碰撞的响应计算
    """
    
    @staticmethod
    def resolve_collision(
        body_a: RigidBody,
        body_b: RigidBody,
        manifold: CollisionManifold,
        use_friction: bool = True
    ) -> None:
        """
        解决两个刚体之间的碰撞
        
        Args:
            body_a: 刚体 A
            body_b: 刚体 B
            manifold: 碰撞流形
            use_friction: 是否使用摩擦
        """
        normal = manifold.normal
        penetration = manifold.penetration
        
        # 分离重叠
        total_inv_mass = body_a.inverse_mass + body_b.inverse_mass
        if total_inv_mass == 0:
            return
        
        # 根据质量比例分离
        if not body_a.is_static and not body_b.is_static:
            separation = normal * (penetration / 2)
            body_a.position = body_a.position - separation
            body_b.position = body_b.position + separation
        elif not body_a.is_static:
            body_a.position = body_a.position - normal * penetration
        else:
            body_b.position = body_b.position + normal * penetration
        
        # 计算相对速度
        relative_velocity = body_b.velocity - body_a.velocity
        velocity_along_normal = relative_velocity.dot(normal)
        
        # 如果物体正在分离，不处理
        if velocity_along_normal > 0:
            return
        
        # 计算弹性系数
        e = min(body_a.restitution, body_b.restitution)
        
        # 计算冲量
        j = -(1 + e) * velocity_along_normal / total_inv_mass
        impulse = normal * j
        
        # 应用冲量到速度
        if not body_a.is_static:
            body_a.velocity = body_a.velocity - impulse * body_a.inverse_mass
        if not body_b.is_static:
            body_b.velocity = body_b.velocity + impulse * body_b.inverse_mass
        
        # 摩擦处理
        if use_friction:
            CollisionResponse._apply_friction(body_a, body_b, normal, j)
    
    @staticmethod
    def _apply_friction(
        body_a: RigidBody,
        body_b: RigidBody,
        normal: Vector2,
        normal_impulse: float
    ) -> None:
        """
        应用摩擦力
        
        Args:
            body_a: 刚体 A
            body_b: 刚体 B
            normal: 碰撞法线
            normal_impulse: 法向冲量大小
        """
        # 计算切向速度
        relative_velocity = body_b.velocity - body_a.velocity
        
        # 切向量（垂直于法线）
        tangent = relative_velocity - normal * relative_velocity.dot(normal)
        tangent_length_sq = tangent.magnitude_squared()
        
        if tangent_length_sq < 1e-10:
            return
        
        tangent = tangent.normalized()
        
        # 计算摩擦冲量
        mu = (body_a.friction + body_b.friction) / 2
        jt = -relative_velocity.dot(tangent) / (body_a.inverse_mass + body_b.inverse_mass)
        
        # 库仑摩擦（静摩擦和动摩擦）
        friction_impulse: Vector2
        if abs(jt) < abs(normal_impulse) * mu:
            friction_impulse = tangent * jt
        else:
            friction_impulse = tangent * (-normal_impulse * mu)
        
        # 应用摩擦冲量
        if not body_a.is_static:
            body_a.velocity = body_a.velocity - friction_impulse * body_a.inverse_mass
        if not body_b.is_static:
            body_b.velocity = body_b.velocity + friction_impulse * body_b.inverse_mass
    
    @staticmethod
    def resolve_inelastic_collision(
        body_a: RigidBody,
        body_b: RigidBody,
        manifold: CollisionManifold
    ) -> None:
        """
        非弹性碰撞响应（物体合并速度）
        
        Args:
            body_a: 刚体 A
            body_b: 刚体 B
            manifold: 碰撞流形
        """
        normal = manifold.normal
        penetration = manifold.penetration
        
        # 分离重叠
        total_inv_mass = body_a.inverse_mass + body_b.inverse_mass
        if total_inv_mass == 0:
            return
        
        if not body_a.is_static and not body_b.is_static:
            separation = normal * (penetration / 2)
            body_a.position = body_a.position - separation
            body_b.position = body_b.position + separation
        elif not body_a.is_static:
            body_a.position = body_a.position - normal * penetration
        else:
            body_b.position = body_b.position + normal * penetration
        
        # 计算合并后的速度（动量守恒）
        total_mass = body_a.mass + body_b.mass
        if total_mass == 0:
            return
        
        combined_velocity = (body_a.velocity * body_a.mass + body_b.velocity * body_b.mass) / total_mass
        
        if not body_a.is_static:
            body_a.velocity = combined_velocity
        if not body_b.is_static:
            body_b.velocity = combined_velocity
