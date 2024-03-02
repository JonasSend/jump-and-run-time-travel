import pygame

from Constants import PEACH


class PastPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(PEACH)  # Different color to distinguish
        self.rect = self.surf.get_rect()
        self.position_index = 0  # To track the current position in the recording

    def update(self, recorded_positions):
        if self.position_index < len(recorded_positions):
            self.rect.topleft = recorded_positions[self.position_index]
            self.position_index += 1