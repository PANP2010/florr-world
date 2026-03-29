"""
Florr World - Main Entry Point
2D 开放世界游戏引擎
"""
import pygame
import sys
from src.core.renderer import Renderer
from src.ui.ui import UIManager


class Player:
    """Minimal player particle for UI demonstration."""
    def __init__(self):
        self.mass = 10.0
        self.charge = 0.5
        self.spin = 1.0
        self.kinetic_energy = 100.0
        self.connections = []


class Physics:
    """Minimal physics world."""
    def __init__(self):
        self.bodies = []


class Region:
    """Minimal region for UI demonstration."""
    pass


class World:
    """Minimal world container."""
    def __init__(self):
        self.physics = Physics()
        self.regions = []


def main():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Florr World - 奇异物理开放世界")
    clock = pygame.time.Clock()

    renderer = Renderer(screen)
    ui = UIManager(renderer)
    player = Player()
    world = World()

    paused = False

    while True:
        fps = clock.get_fps()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if event.key == pygame.K_TAB:
                    # Toggle tech tree view (placeholder)
                    pass

        screen.fill((10, 10, 30))

        # Draw HUD
        ui.draw_hud(player, world)

        # Draw debug info
        ui.draw_debug_info(world, fps)

        # Draw pause menu if paused
        if paused:
            ui.draw_pause_menu()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
