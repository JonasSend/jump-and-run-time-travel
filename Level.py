import pygame

from Block import Block
from Constants import WINDOW_WIDTH, WINDOW_HEIGHT
from Goal import Goal

class Level:
    def __init__(self, image_path):
        self.blocks = pygame.sprite.Group()
        self.complete = False
        self.load_level(image_path)

    def load_level(self, image_path):
        # Load the level image
        level_image = pygame.image.load(image_path).convert()
        # Get the image dimensions
        width, height = level_image.get_size()

        # Iterate over each pixel in the image
        for x in range(width):
            for y in range(height):
                # Get the color of the pixel
                color = level_image.get_at((x, y))

                # Determine what to place based on the pixel's color
                if color == (255, 255, 255, 255):  # White pixels for blocks
                    self.blocks.add(Block(x * 32, y * 32, 32, 32))  # Assuming each block is 32x32 pixels
                elif color == (0, 255, 0, 255):  # Green pixel for the goal
                    self.goal = Goal(x * 32, y * 32, 32, 32)  # Place the goal

    def draw(self, screen):
        for block in self.blocks:
            screen.blit(block.surf, block.rect)
        screen.blit(self.goal.surf, self.goal.rect)