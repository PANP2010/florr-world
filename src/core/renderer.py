"""Core renderer module."""
import pygame


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def draw_text(self, text, pos, color=(255, 255, 255)):
        """Draw text at screen position."""
        img = self.font_medium.render(str(text), True, color)
        self.screen.blit(img, pos)
