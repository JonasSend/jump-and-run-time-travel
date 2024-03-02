import pygame

from Block import Block
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Level:
    def __init__(self):
        self.blocks = pygame.sprite.Group()
        self.load_level()

    def load_level(self):
        # Example level layout
        level_layout = [
            # Ground
            (0, SCREEN_HEIGHT - 32, SCREEN_WIDTH, 32),
            # Ceiling
            (0, 0, SCREEN_WIDTH, 32),
            # Left wall
            (0, 0, 32, SCREEN_HEIGHT),
            # Right wall
            (SCREEN_WIDTH - 32, 0, 32, SCREEN_HEIGHT),
            # Obstsacle
            (400, SCREEN_HEIGHT - 250, 100, 300),
        ]
        for block in level_layout:
            self.blocks.add(Block(*block))

    def draw(self, screen):
        for block in self.blocks:
            screen.blit(block.surf, block.rect)