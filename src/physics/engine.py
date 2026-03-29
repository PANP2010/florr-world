"""
PhysicsEngine - 2D 物理引擎核心
支持：刚体动力学、碰撞检测、引力系统
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import math


@dataclass
class Vector2:
    """
    2D 向量类，支持基本向量运算
    """
    x: float
    y: float
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        """向量加法"""
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        """向量减法"""
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2':
        """标量乘法"""
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector2':
        """标量乘法（右乘）"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2':
        """标量除法"""
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector2':
        """向量取负"""
        return Vector2(-self.x, -self.y)
    
    def dot(self, other: 'Vector2') -> float:
        """点积"""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Vector2') -> float:
        """叉积（返回标量）"""
        return self.x * other.y - self.y * other.x
    
    def magnitude(self) -> float:
        """向量的模（长度）"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def magnitude_squared(self) -> float:
        """向量长度的平方（避免开方运算）"""
        return self.x ** 2 + self.y ** 2
    
    def normalized(self) -> 'Vector2':
        """返回单位向量"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def distance_to(self, other: 'Vector2') -> float:
        """到另一个向量的距离"""
        return (self - other).magnitude()
    
    def distance_squared_to(self, other: 'Vector2') -> float:
        """到另一个向量的距离的平方"""
        return (self - other).magnitude_squared()
    
    def angle(self) -> float:
        """返回向量的角度（弧度）"""
        return math.atan2(self.y, self.x)
    
    def rotated(self, angle: float) -> 'Vector2':
        """绕原点旋转指定角度（弧度）"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def clamp(self, min_val: 'Vector2', max_val: 'Vector2') -> 'Vector2':
        """限制向量在指定范围内"""
        return Vector2(
            max(min_val.x, min(max_val.x, self.x)),
            max(min_val.y, min(max_val.y, self.y))
        )
    
    def lerp(self, other: 'Vector2', t: float) -> 'Vector2':
        """线性插值"""
        return self + (other - self) * t
    
    def __repr__(self) -> str:
        return f"Vector2({self.x:.2f}, {self.y:.2f})"
    
    def __iter__(self):
        """支持解包"""
        yield self.x
        yield self.y
    
    def copy(self) -> 'Vector2':
        """返回副本"""
        return Vector2(self.x, self.y)


@dataclass
class RigidBody:
    """
    刚体类，表示具有质量和位置的物理实体
    
    Attributes:
        mass: 质量（kg）
        position: 位置向量
        velocity: 速度向量
        acceleration: 加速度向量
        forces: 作用在刚体上的力列表
        restitution: 弹性系数（0-1）
        friction: 摩擦系数
        is_static: 是否为静态刚体（质量无限大）
    """
    mass: float
    position: Vector2
    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    acceleration: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    forces: List[Vector2] = field(default_factory=list)
    restitution: float = 0.5  # 弹性系数
    friction: float = 0.1  # 摩擦系数
    is_static: bool = False
    _inverse_mass: float = field(init=False, repr=False)
    
    def __post_init__(self):
        """初始化计算属性"""
        if self.is_static:
            self._inverse_mass = 0.0
        else:
            self._inverse_mass = 1.0 / self.mass if self.mass > 0 else 0.0
    
    @property
    def inverse_mass(self) -> float:
        """反质量（用于物理计算）"""
        return self._inverse_mass
    
    def apply_force(self, force: Vector2) -> None:
        """
        施加一个力到刚体
        
        Args:
            force: 力向量
        """
        self.forces.append(force)
    
    def apply_impulse(self, impulse: Vector2) -> None:
        """
        施加一个冲量到刚体（瞬间速度变化）
        
        Args:
            impulse: 冲量向量
        """
        if not self.is_static:
            self.velocity = self.velocity + impulse * self._inverse_mass
    
    def clear_forces(self) -> None:
        """清除所有作用力"""
        self.forces.clear()
    
    def get_net_force(self) -> Vector2:
        """获取所有作用力的合力"""
        if not self.forces:
            return Vector2(0, 0)
        result = Vector2(0, 0)
        for force in self.forces:
            result = result + force
        return result
    
    def update(self, dt: float) -> None:
        """
        更新刚体状态（每帧调用）
        
        Args:
            dt: 时间步长（秒）
        
        Physics:
            - F = ma (牛第二定律)
            - v = v + a * dt (速度积分)
            - p = p + v * dt (位置积分)
        """
        if self.is_static:
            return
        
        # 计算合力加速度 a = F / m
        net_force = self.get_net_force()
        self.acceleration = net_force * self._inverse_mass
        
        # 速度积分 v = v + a * dt
        self.velocity = self.velocity + self.acceleration * dt
        
        # 位置积分 p = p + v * dt
        self.position = self.position + self.velocity * dt
        
        # 清除力（每帧重新计算）
        self.clear_forces()
    
    def __repr__(self) -> str:
        return f"RigidBody(mass={self.mass}, pos={self.position}, vel={self.velocity})"


class PhysicsEngine:
    """
    2D 物理引擎主类
    
    管理所有刚体，处理物理模拟更新
    
    Attributes:
        gravity: 重力加速度向量
        bodies: 刚体列表
        iterations: 碰撞迭代次数
    """
    
    def __init__(self, gravity: Optional[Vector2] = None):
        """
        初始化物理引擎
        
        Args:
            gravity: 重力加速度，默认为 (0, 980) 像素/s²
        """
        self.bodies: List[RigidBody] = []
        self.gravity = gravity or Vector2(0, 980)  # 像素/s²
        self.iterations: int = 4  # 碰撞Solver迭代次数
    
    def add_body(self, body: RigidBody) -> None:
        """
        添加刚体到物理引擎
        
        Args:
            body: 刚体实例
        """
        self.bodies.append(body)
    
    def remove_body(self, body: RigidBody) -> None:
        """
        从物理引擎移除刚体
        
        Args:
            body: 刚体实例
        """
        if body in self.bodies:
            self.bodies.remove(body)
    
    def get_bodies(self) -> List[RigidBody]:
        """返回所有刚体"""
        return self.bodies.copy()
    
    def update(self, dt: float) -> None:
        """
        更新物理世界（每帧调用）
        
        Args:
            dt: 时间步长（秒）
        """
        # 应用重力
        for body in self.bodies:
            if not body.is_static:
                body.apply_force(self.gravity * body.mass)
        
        # 更新所有刚体
        for body in self.bodies:
            body.update(dt)
    
    def check_collisions(self) -> List[Tuple[RigidBody, RigidBody]]:
        """
        检测所有刚体之间的碰撞（O(n²)）
        
        Returns:
            碰撞对列表，每个元素为 (body_a, body_b)
        """
        collisions = []
        n = len(self.bodies)
        
        for i in range(n):
            for j in range(i + 1, n):
                body_a = self.bodies[i]
                body_b = self.bodies[j]
                
                # 跳过两个静态物体
                if body_a.is_static and body_b.is_static:
                    continue
                
                if self._check_collision(body_a, body_b):
                    collisions.append((body_a, body_b))
        
        return collisions
    
    def _check_collision(self, body_a: RigidBody, body_b: RigidBody) -> bool:
        """
        检测两个刚体之间的碰撞（需要碰撞形状支持）
        默认使用AABB检测，子类可重写
        """
        # 默认使用圆形碰撞检测
        radius_a = getattr(body_a, 'radius', 10)
        radius_b = getattr(body_b, 'radius', 10)
        
        distance = body_a.position.distance_to(body_b.position)
        return distance < (radius_a + radius_b)
    
    def resolve_collisions(self, collisions: List[Tuple[RigidBody, RigidBody]]) -> None:
        """
        解决检测到的碰撞
        
        Args:
            collisions: 碰撞对列表
        """
        for body_a, body_b in collisions:
            self._resolve_collision(body_a, body_b)
    
    def _resolve_collision(self, body_a: RigidBody, body_b: RigidBody) -> None:
        """
        解决两个刚体之间的碰撞
        
        使用冲量方法进行碰撞响应
        """
        # 获取半径（默认为10）
        radius_a = getattr(body_a, 'radius', 10)
        radius_b = getattr(body_b, 'radius', 10)
        
        # 计算碰撞法线
        delta = body_b.position - body_a.position
        distance = delta.magnitude()
        
        if distance == 0:
            return  # 重叠情况
        
        normal = delta.normalized()
        
        # 计算重叠量
        overlap = (radius_a + radius_b) - distance
        
        # 分离重叠
        if not body_a.is_static and not body_b.is_static:
            separation = normal * (overlap / 2)
            body_a.position = body_a.position - separation
            body_b.position = body_b.position + separation
        elif not body_a.is_static:
            body_a.position = body_a.position - normal * overlap
        else:
            body_b.position = body_b.position + normal * overlap
        
        # 计算相对速度
        relative_velocity = body_b.velocity - body_a.velocity
        velocity_along_normal = relative_velocity.dot(normal)
        
        # 如果物体正在分离，不处理
        if velocity_along_normal > 0:
            return
        
        # 计算弹性系数
        e = min(body_a.restitution, body_b.restitution)
        
        # 计算有效质量
        inv_mass_a = body_a.inverse_mass
        inv_mass_b = body_b.inverse_mass
        inv_mass_sum = inv_mass_a + inv_mass_b
        
        if inv_mass_sum == 0:
            return  # 两个都是静态物体
        
        # 计算冲量
        j = -(1 + e) * velocity_along_normal / inv_mass_sum
        impulse = normal * j
        
        # 应用冲量
        if not body_a.is_static:
            body_a.velocity = body_a.velocity - impulse * inv_mass_a
        if not body_b.is_static:
            body_b.velocity = body_b.velocity + impulse * inv_mass_b
