"""
InertialSingularity - 惯性奇点
物体在极端加速下惯性归零，实现瞬间位移
"""
from ..engine import RigidBody, Vector2
import math

class InertialSingularity:
    """
    当物体的加速度超过 threshold 时，惯性项 m → 0
    导致位移突变：Δx = v₀ * dt + 0.5 * a * dt² (m→0时趋于无穷大)
    """
    def __init__(self, threshold: float = 5000.0):  # px/s²
        self.threshold = threshold
        
    def apply(self, body: RigidBody) -> bool:
        acc_mag = math.sqrt(body.acceleration.x**2 + body.acceleration.y**2)
        if acc_mag > self.threshold:
            # 惯性归零，瞬间位移
            singularity_force = Vector2(
                body.acceleration.x * body.mass * 0.99,  # 惯性接近0
                body.acceleration.y * body.mass * 0.99
            )
            body.apply_force(singularity_force)
            return True
        return False
