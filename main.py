import pygame
import sys

# Initialize Pygame
from Constants import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from Level import Level
from PastPlayer import PastPlayer
from Player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game setup
player = Player()
level = Level()
movement_record = []
virtual_player = PastPlayer()
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
                player.rect.topleft = movement_record[0]
            if event.key == pygame.K_q:
                player = Player()
                movement_record = []
                virtual_player = PastPlayer()
                replay = False  # Flag to control replay
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and player.velocity.x < 0) or (
                event.key == pygame.K_RIGHT and player.velocity.x > 0
            ):
                player.move(0)  # Stop moving

    # Game logic
    collision_objects = level.blocks.copy()
    if replay:
        collision_objects.add(virtual_player)
    player.update(collision_objects)

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
