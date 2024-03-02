import pygame

from Block import Block
from Constants import WINDOW_WIDTH, WINDOW_HEIGHT
from Goal import Goal

BLOCK_WIDTH = 75
BORDER_WIDTH = 32
GOAL_WIDTH = 100
GOAL_HEIGHT = 16


class Level:
    def __init__(self):
        self.blocks = pygame.sprite.Group()
        self.load_level()
        self.complete = False

    def load_level(self):
        # Example level layout
        level_layout = [
            # Ground
            (0, WINDOW_HEIGHT - BORDER_WIDTH, WINDOW_WIDTH, BORDER_WIDTH),
            # Ceiling
            (0, 0, WINDOW_WIDTH, BORDER_WIDTH),
            # Left wall
            (0, 0, BORDER_WIDTH, WINDOW_HEIGHT),
            # Right wall
            (WINDOW_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, WINDOW_HEIGHT),
            # Obstsacles
            (250, WINDOW_HEIGHT - 100 - BORDER_WIDTH, BLOCK_WIDTH, 100),
            (250 + BLOCK_WIDTH, WINDOW_HEIGHT - 200 - BORDER_WIDTH, BLOCK_WIDTH, 200),
            (250 + 2 * BLOCK_WIDTH, WINDOW_HEIGHT - 420 - BORDER_WIDTH, BLOCK_WIDTH, 420),
            (650, WINDOW_HEIGHT - 220 - BORDER_WIDTH, BLOCK_WIDTH, 220)
        ]
        
        for block in level_layout:
            self.blocks.add(Block(*block))
            
        self.goal = Goal(WINDOW_WIDTH - GOAL_WIDTH - BORDER_WIDTH, WINDOW_HEIGHT - BORDER_WIDTH - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)

    def draw(self, screen):
        for block in self.blocks:
            screen.blit(block.surf, block.rect)
        screen.blit(self.goal.surf, self.goal.rect)