"""
TimeDilation - 时间常数偏移
局部区域时间流速变化
"""
class TimeDilationField:
    def __init__(self, region_bounds: tuple, time_scale: float):
        self.x1, self.y1, self.x2, self.y2 = region_bounds
        self.time_scale = time_scale  # 1.0 正常, 0.5 半速, 2.0 倍速
        
    def get_effective_dt(self, base_dt: float, x: float, y: float) -> float:
        if self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2:
            return base_dt * self.time_scale
        return base_dt
