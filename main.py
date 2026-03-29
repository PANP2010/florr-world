"""
florr-world 主程序

演示物理引擎基础功能
"""
import pygame
import sys
from typing import Optional

# 物理引擎模块
from src.physics import Vector2, RigidBody, PhysicsEngine


class Game:
    """
    游戏主类
    
    初始化 Pygame 窗口并运行游戏循环
    """
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "florr-world"):
        """
        初始化游戏
        
        Args:
            width: 窗口宽度
            height: 窗口高度
            title: 窗口标题
        """
        # 初始化 Pygame
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 初始化物理引擎
        self.physics = PhysicsEngine(gravity=Vector2(0, 980))
        
        # 颜色定义
        self.colors = {
            'background': (30, 30, 40),
            'ball': (220, 80, 80),
            'ball2': (80, 200, 120),
            'ground': (60, 60, 80),
            'text': (220, 220, 220),
        }
        
        # 创建测试场景
        self._create_test_scene()
    
    def _create_test_scene(self) -> None:
        """创建测试场景"""
        # 创建几个测试球体（自由落体）
        self.balls = []
        
        # 红色球 - 中心位置
        ball1 = RigidBody(mass=5, position=Vector2(self.width // 2, 100))
        ball1.radius = 25
        ball1.restitution = 0.8  # 弹性
        self.balls.append(ball1)
        self.physics.add_body(ball1)
        
        # 绿色球 - 左侧
        ball2 = RigidBody(mass=3, position=Vector2(self.width // 3, 50))
        ball2.radius = 20
        ball2.restitution = 0.6
        self.balls.append(ball2)
        self.physics.add_body(ball2)
        
        # 蓝色球 - 右侧
        ball3 = RigidBody(mass=8, position=Vector2(2 * self.width // 3, 80))
        ball3.radius = 30
        ball3.restitution = 0.5
        self.balls.append(ball3)
        self.physics.add_body(ball3)
    
    def handle_events(self) -> None:
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # 空格键重置球的位置
                    self._reset_scene()
                elif event.key == pygame.K_r:
                    # R 键添加一个新球
                    self._add_random_ball()
    
    def _reset_scene(self) -> None:
        """重置场景"""
        positions = [
            (self.width // 2, 100),
            (self.width // 3, 50),
            (2 * self.width // 3, 80)
        ]
        
        for i, ball in enumerate(self.balls[:3]):
            ball.position = Vector2(*positions[i])
            ball.velocity = Vector2(0, 0)
    
    def _add_random_ball(self) -> None:
        """添加随机球"""
        import random
        
        x = random.randint(100, self.width - 100)
        y = random.randint(50, 150)
        mass = random.uniform(2, 10)
        radius = random.uniform(15, 35)
        
        ball = RigidBody(mass=mass, position=Vector2(x, y))
        ball.radius = radius
        ball.restitution = random.uniform(0.3, 0.9)
        ball.friction = random.uniform(0.05, 0.2)
        
        self.balls.append(ball)
        self.physics.add_body(ball)
    
    def update(self, dt: float) -> None:
        """
        更新游戏状态
        
        Args:
            dt: 时间步长（秒）
        """
        # 更新物理引擎
        self.physics.update(dt)
        
        # 边界检测和响应
        ground_y = self.height - 50
        for ball in self.balls:
            radius = getattr(ball, 'radius', 20)
            
            # 下边界
            if ball.position.y + radius > ground_y:
                ball.position = Vector2(ball.position.x, ground_y - radius)
                
                # 反弹
                if ball.velocity.y > 0:
                    ball.velocity = Vector2(
                        ball.velocity.x,
                        -ball.velocity.y * ball.restitution
                    )
                    
                    # 摩擦力
                    ball.velocity = Vector2(
                        ball.velocity.x * (1 - ball.friction),
                        ball.velocity.y
                    )
            
            # 左右边界
            if ball.position.x - radius < 0:
                ball.position = Vector2(radius, ball.position.y)
                ball.velocity = Vector2(-ball.velocity.x * ball.restitution, ball.velocity.y)
            elif ball.position.x + radius > self.width:
                ball.position = Vector2(self.width - radius, ball.position.y)
                ball.velocity = Vector2(-ball.velocity.x * ball.restitution, ball.velocity.y)
            
            # 上边界
            if ball.position.y - radius < 0:
                ball.position = Vector2(ball.position.x, radius)
                ball.velocity = Vector2(ball.velocity.x, -ball.velocity.y * ball.restitution)
    
    def render(self) -> None:
        """渲染游戏画面"""
        # 清屏
        self.screen.fill(self.colors['background'])
        
        # 绘制地面
        ground_y = self.height - 50
        pygame.draw.rect(
            self.screen,
            self.colors['ground'],
            (0, ground_y, self.width, 50)
        )
        
        # 绘制分隔线
        pygame.draw.line(
            self.screen,
            (80, 80, 100),
            (0, ground_y),
            (self.width, ground_y),
            2
        )
        
        # 绘制所有球
        for ball in self.balls:
            radius = getattr(ball, 'radius', 20)
            pos = (int(ball.position.x), int(ball.position.y))
            
            # 绘制填充
            pygame.draw.circle(self.screen, self.colors['ball'], pos, radius)
            
            # 绘制边框
            pygame.draw.circle(self.screen, (255, 255, 255), pos, radius, 2)
            
            # 绘制速度向量（可选）
            if ball.velocity.magnitude() > 5:
                vel_norm = ball.velocity.normalized()
                end_point = (
                    int(pos[0] + vel_norm.x * radius * 1.5),
                    int(pos[1] + vel_norm.y * radius * 1.5)
                )
                pygame.draw.line(
                    self.screen,
                    (255, 255, 100),
                    pos,
                    end_point,
                    2
                )
        
        # 绘制信息
        self._draw_info()
        
        # 刷新
        pygame.display.flip()
    
    def _draw_info(self) -> None:
        """绘制信息面板"""
        font = pygame.font.Font(None, 24)
        
        # FPS
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, self.colors['text'])
        self.screen.blit(fps_text, (10, 10))
        
        # 球数量
        ball_text = font.render(f"Balls: {len(self.balls)}", True, self.colors['text'])
        self.screen.blit(ball_text, (10, 35))
        
        # 控制说明
        controls = [
            "SPACE: Reset balls",
            "R: Add random ball",
            "ESC: Quit"
        ]
        
        for i, ctrl in enumerate(controls):
            text = font.render(ctrl, True, (150, 150, 150))
            self.screen.blit(text, (10, self.height - 80 + i * 20))
    
    def run(self, target_fps: int = 60) -> None:
        """
        运行游戏主循环
        
        Args:
            target_fps: 目标帧率
        """
        while self.running:
            # 计算 delta time
            dt = self.clock.tick(target_fps) / 1000.0  # 转换为秒
            
            # 限制最大 dt 防止物理爆炸
            dt = min(dt, 0.05)
            
            # 处理事件
            self.handle_events()
            
            # 更新
            self.update(dt)
            
            # 渲染
            self.render()
        
        # 退出
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    print("=" * 50)
    print("florr-world 物理引擎演示")
    print("=" * 50)
    print()
    print("控制说明:")
    print("  SPACE - 重置球的位置")
    print("  R - 添加随机球")
    print("  ESC - 退出程序")
    print()
    print("按窗口关闭按钮或 ESC 退出")
    print("-" * 50)
    
    # 创建并运行游戏
    game = Game(width=800, height=600, title="florr-world - Physics Demo")
    game.run(target_fps=60)


if __name__ == '__main__':
    main()
