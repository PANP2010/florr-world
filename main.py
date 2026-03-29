#!/usr/bin/env python3
"""
Florr World - 主入口
"""
import pygame
from src.physics.engine import PhysicsEngine, RigidBody, Vector2
from src.player.particle import PlayerParticle
from src.core.world import GameWorld, Region
from src.renderer import Renderer

def main():
    r = Renderer(1280, 720, "Florr World")
    world = GameWorld(1280, 720)
    
    # 添加重力异常区
    world.add_region(Region("gravity_well", (400, 200, 600, 400), 1.5, 1.0))
    
    # 创建玩家
    player = PlayerParticle(640, 360)
    world.player = player
    
    running = True
    while running:
        running = r.handle_events()
        
        # 更新物理
        world.physics.update(1/60)
        player.update(1/60)
        
        # 渲染
        r.clear()
        r.draw_text("Florr World - 2D 奇异物理游戏", (20, 20))
        r.draw_particle(player.position.x, player.position.y, 15, (100, 220, 255))
        r.draw_text(f"质量:{player.mass:.1f} 电荷:{player.charge:.1f} 动能:{player.kinetic_energy:.0f}", (20, 60))
        r.draw_text("WASD移动 | 空格相位态 | ESC退出", (20, 700))
        
        r.flip()
        r.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()