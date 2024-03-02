import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE =(255, 140, 0)
PEACH =(255, 193, 111)


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


# Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(topleft=(x, y))


# Level class
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
            
            
class VirtualPlayer(pygame.sprite.Sprite):
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



# Game setup

player = Player()
level = Level()
movement_record = []
virtual_player = VirtualPlayer()
replay = False  # Flag to control replay

# Main game loop
running = True
while running:
    if not replay:
        movement_record.append(player.rect.topleft)
    else:
        virtual_player.update(movement_record)
        if virtual_player.position_index >= len(movement_record):
            replay = False  # Stop replay when done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_LEFT:
                player.move(-1)  # Move left
            if event.key == pygame.K_RIGHT:
                player.move(1)  # Move right
            if event.key == pygame.K_LALT and not replay:  # Press 'R' to start the replay
                replay = True
                virtual_player.position_index = 0  # Reset replay
            if event.key == pygame.K_q:
                player = Player()
                movement_record = []
                virtual_player = VirtualPlayer()
                replay = False  # Flag to control replay
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and player.velocity.x < 0) or (
                event.key == pygame.K_RIGHT and player.velocity.x > 0
            ):
                player.move(0)  # Stop moving

    # Game logic
    player.update(level.blocks)

    # Drawing
    screen.fill(BLACK)
    level.draw(screen)
    screen.blit(player.surf, player.rect)
    
    if replay:
        screen.blit(virtual_player.surf, virtual_player.rect)  # Draw virtual player during replay

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
