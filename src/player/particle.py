"""
PlayerParticle - 玩家质点系统
属性：质量、电荷、自旋、动能槽、连接端口
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from .connections import Connection


@dataclass
class Vector2:
    """二维向量，用于表示位置和速度"""
    x: float
    y: float

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        """返回向量的模"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, other: Vector2) -> float:
        """返回到另一个向量的距离"""
        return (self - other).magnitude()

    def normalize(self) -> Vector2:
        """返回单位向量"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0.0, 0.0)
        return Vector2(self.x / mag, self.y / mag)


class PlayerParticle:
    """玩家控制的质点

    属性:
        position: 位置向量
        velocity: 速度向量
        mass: 质量，影响加速度计算 (F=ma)
        charge: 电荷，影响电磁相互作用
        spin: 自旋角动量
        kinetic_energy: 动能槽
        connections: 当前连接列表
    """

    def __init__(self, x: float, y: float) -> None:
        """
        初始化质点

        Args:
            x: 初始 x 坐标
            y: 初始 y 坐标
        """
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.mass: float = 1.0
        self.charge: float = 0.0
        self.spin: float = 0.0
        self.kinetic_energy: float = 0.0
        self.connections: List[Connection] = []

    def apply_force(self, fx: float, fy: float) -> None:
        """
        施加力到质点

        Args:
            fx: x 方向力分量
            fy: y 方向力分量
        """
        self.velocity.x += fx / self.mass
        self.velocity.y += fy / self.mass

    def update(self, dt: float) -> None:
        """
        更新质点状态

        Args:
            dt: 时间步长（秒）
        """
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        # 更新动能
        speed = self.velocity.magnitude()
        self.kinetic_energy = 0.5 * self.mass * speed ** 2

    def connect_to(
        self, other: PlayerParticle, conn_type: str, **kwargs: float
    ) -> Connection:
        """
        与另一个质点建立连接

        Args:
            other: 目标质点
            conn_type: 连接类型（字符串）
            **kwargs: 连接参数（如弹簧的 k 和 rest_length）

        Returns:
            新建的 Connection 对象
        """
        from .connections import Connection, ConnectionType

        # 将字符串转换为枚举
        type_map = {
            "spring": ConnectionType.SPRING,
            "hinge": ConnectionType.HINGE,
            "fusion": ConnectionType.FUSION,
            "phase": ConnectionType.PHASE,
            "gravity": ConnectionType.GRAVITATIONAL,
        }
        conn_enum = type_map.get(conn_type, ConnectionType.SPRING)

        conn = Connection(self, other, conn_enum, **kwargs)
        self.connections.append(conn)
        other.connections.append(conn)
        return conn

    def disconnect(self, conn: Connection) -> None:
        """
        断开指定连接

        Args:
            conn: 要断开的连接
        """
        if conn in self.connections:
            self.connections.remove(conn)
        if conn in conn.b.connections:
            conn.b.connections.remove(conn)

    def get_kinetic_energy(self) -> float:
        """获取当前动能"""
        return self.kinetic_energy
