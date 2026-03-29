"""
Renderer - Pygame 渲染引擎
"""
import pygame
from typing import Tuple

class Renderer:
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Florr World"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
    def clear(self, color: Tuple[int,int,int] = (20, 20, 30)):
        self.screen.fill(color)
        
    def draw_text(self, text: str, pos: Tuple[int,int], color=(255,255,255)):
        img = self.font.render(text, True, color)
        self.screen.blit(img, pos)
        
    def draw_particle(self, x: float, y: float, radius: int, color=(100,200,255)):
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
        
    def draw_rect(self, x: float, y: float, w: float, h: float, color=(200,200,100)):
        pygame.draw.rect(self.screen, color, (int(x), int(y), int(w), int(h)), 2)
        
    def flip(self):
        pygame.display.flip()
        
    def tick(self, fps: int = 60):
        self.clock.tick(fps)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True