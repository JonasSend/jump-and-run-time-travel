import pygame

from Constants import SCREEN_HEIGHT, ORANGE


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(ORANGE)
        self.rect = self.surf.get_rect(center=(100, SCREEN_HEIGHT - 100))
        self.velocity = pygame.math.Vector2((0, 0))
        self.on_ground = False
        self.speed = 5  # Horizontal movement speed

    def update(self, blocks):
        self.velocity.y += 1  # Apply gravity
        self.rect.y += self.velocity.y  # Apply vertical movement

        # Vertical collision detection
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0:  # Falling
                    self.on_ground = True
                    self.velocity.y = 0
                    self.rect.bottom = block.rect.top
                elif self.velocity.y < 0:  # Jumping and hit the ceiling
                    self.velocity.y = 0
                    self.rect.top = block.rect.bottom

        # Horizontal movement
        self.rect.x += self.velocity.x
        # Horizontal collision detection
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0:  # Moving right
                    self.rect.right = block.rect.left
                elif self.velocity.x < 0:  # Moving left
                    self.rect.left = block.rect.right

    def jump(self):
        if self.on_ground:
            self.velocity.y = -20  # Jump velocity

    def move(self, x_direction):
        self.velocity.x = x_direction * self.speed