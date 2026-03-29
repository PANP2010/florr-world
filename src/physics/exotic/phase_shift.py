"""
PhaseShift - 相位穿透
物体进入"相位态"可穿越障碍
"""
class PhaseShift:
    def __init__(self, body):
        self.body = body
        self.phase_cooldown = 5.0  # 秒
        self.current_cooldown = 0.0
        self.is_phase_active = False
        
    def activate(self):
        if self.current_cooldown <= 0:
            self.is_phase_active = True
            # 穿越碰撞检测
            return True
        return False
    
    def update(self, dt: float):
        if self.is_phase_active:
            self.is_phase_active = False
            self.current_cooldown = self.phase_cooldown
        else:
            self.current_cooldown = max(0, self.current_cooldown - dt)
