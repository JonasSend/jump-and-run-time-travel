import pygame
import sys

# Initialize Pygame
from Constants import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from Level import Level
from PastPlayer import PastPlayer
from Player import Player
from util.timer import format_time

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer_font = pygame.font.Font(None, 36)

# Game setup
player = Player()
level = Level()
replay = False  # Flag to control replay
start_ticks = pygame.time.get_ticks()
past_players = [PastPlayer()]

# Main game loop
running = True
while running:
    if not replay:
        past_players[-1].record(player.rect.topleft)
    else:
        for pp in past_players:
            pp[-1].play()
        if virtual_player.position_index >= len(movement_record):
            replay = False  # Stop replay when done

    # Calculate elapsed time
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    elapsed_seconds = elapsed_ticks // 1000  # Convert milliseconds to seconds

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
                start_ticks = pygame.time.get_ticks()  # reset timer
                player.rect.topleft = past_players[-1].movement_record[0]
                past_players.append = PastPlayer()
            if event.key == pygame.K_q:
                player = Player()
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

    # Format and render the time
    timer_text = format_time(elapsed_seconds)
    text_surface = timer_font.render(timer_text, True, WHITE)

    # Drawing
    screen.fill(BLACK)
    level.draw(screen)
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 64, 64))
    screen.blit(text_surface, text_rect)
    screen.blit(player.surf, player.rect)
    
    if replay:
        screen.blit(virtual_player.surf, virtual_player.rect)  # Draw virtual player during replay

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
