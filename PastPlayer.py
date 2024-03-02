import pygame

from Constants import PEACH


class PastPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(PEACH)  # Different color to distinguish
        self.rect = self.surf.get_rect()
        self.position_index = 0  # To track the current position in the recording
        self.movement_record = []
        self.visible = True

    def play(self):
        if self.position_index < len(self.movement_record):
            self.rect.topleft = self.movement_record[self.position_index]
            self.position_index += 1
            self.visible = True
        else:
            self.visible = False
            
    def reset(self):
        self.position_index = 0
            
            
    def record(self, topleft_position):
        self.movement_record.append(topleft_position)
            