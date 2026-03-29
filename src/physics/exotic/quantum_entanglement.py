"""
QuantumEntanglement - 量子纠缠
两个粒子状态即时关联
"""
class QuantumEntanglePair:
    def __init__(self, particle_a, particle_b):
        self.a = particle_a
        self.b = particle_b
        self.entangled = True
        
    def propagate_state(self):
        """当一个粒子状态改变，另一个即时响应"""
        # 纠缠态：测量一个粒子，另一个立即坍缩到对应态
        # 这里模拟为：速度方向同步
        if self.entangled:
            self.b.velocity.x = self.a.velocity.x
            self.b.velocity.y = self.a.velocity.y
