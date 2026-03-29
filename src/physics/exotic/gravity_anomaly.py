"""
GravityAnomaly - 重力异常层
不同区域有不同重力方向和强度
"""
class GravityAnomaly:
    def __init__(self, region_bounds: tuple, gravity: Vector2):
        self.x1, self.y1, self.x2, self.y2 = region_bounds
        self.gravity = gravity  # Vector2(0, 980) normal, 可以是任意方向
        
    def is_inside(self, x: float, y: float) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
        
    def get_gravity(self) -> Vector2:
        return self.gravity
