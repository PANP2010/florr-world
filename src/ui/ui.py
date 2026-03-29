"""
UI System - 游戏界面
包含：HUD、科技树界面、暂停菜单、调试信息
"""
import pygame
from typing import Dict, Any

class UIManager:
    def __init__(self, renderer):
        self.renderer = renderer
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.active_panels = []
        
    def draw_hud(self, player, world):
        """绘制 HUD（抬头显示）"""
        # 玩家属性面板（左上角）
        self._draw_panel(20, 20, 200, 150, [
            f"质量: {player.mass:.1f}",
            f"电荷: {player.charge:.1f}",
            f"自旋: {player.spin:.1f}",
            f"动能: {player.kinetic_energy:.0f}",
            f"连接: {len(player.connections)}",
        ])
        
    def _draw_panel(self, x: int, y: int, w: int, h: int, lines: list, alpha: int = 200):
        """画面板"""
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((0, 0, 0, alpha))
        self.renderer.screen.blit(surf, (x, y))
        for i, line in enumerate(lines):
            img = self.font_small.render(str(line), True, (255,255,255))
            self.renderer.screen.blit(img, (x+10, y+10+i*22))
            
    def draw_tech_tree(self, tech_tree):
        """科技树界面（覆盖层）"""
        # 半透明背景
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.renderer.screen.blit(overlay, (0, 0))
        
        self.renderer.draw_text("科技树", (540, 20), (255, 220, 100))
        
        # 绘制各纪元
        eras = ["第一纪元", "第二纪元", "第三纪元", "第四纪元"]
        for i, era in enumerate(eras):
            x = 50 + i * 300
            self.renderer.draw_text(era, (x, 80), (200, 200, 255))
            
    def draw_debug_info(self, world, fps: float):
        """调试信息"""
        self._draw_panel(20, 600, 300, 100, [
            f"FPS: {fps:.0f}",
            f"实体: {len(world.physics.bodies)}",
            f"区域: {len(world.regions)}",
        ], alpha=120)
        
    def draw_pause_menu(self):
        """暂停菜单"""
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.renderer.screen.blit(overlay, (0, 0))
        self.renderer.draw_text("⏸ PAUSED", (540, 300), (255,255,255))
        self.renderer.draw_text("按 ESC 继续", (520, 360), (180,180,180))
