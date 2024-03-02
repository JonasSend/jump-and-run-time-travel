import pygame

from Constants import GREEN


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(topleft=(x, y))