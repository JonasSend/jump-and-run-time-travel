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
font_level_complete = pygame.font.Font(None, 72)

# Game setup

level = Level()

def init_game():
    start_ticks = pygame.time.get_ticks()
    past_players = []
    recording = PastPlayer()
    player = Player()
    return start_ticks,past_players,recording, player

start_ticks, past_players, recording, player = init_game()

# Main game loop
running = True
while running:
    recording.record(player.rect.topleft)
    for pp in past_players:
        pp.play()

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
            if event.key == pygame.K_LALT:  # Press 'R' to start the replay
                start_ticks = pygame.time.get_ticks()  # reset timer
                player.rect.topleft = recording.movement_record[0]
                past_players.append(recording)
                recording = PastPlayer()
                for pp in past_players:
                    pp.reset()
            if event.key == pygame.K_q:
                start_ticks, past_players, recording, player = init_game()
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and player.velocity.x < 0) or (
                event.key == pygame.K_RIGHT and player.velocity.x > 0
            ):
                player.move(0)  # Stop moving

    # Game logic
    collision_objects = level.blocks.copy()
    for pp in past_players:
        if pp.visible:
            collision_objects.add(pp)
    player.update(collision_objects)
    
    if player.rect.colliderect(level.goal.rect):
        level.complete = True

    # Format and render the time
    timer_text = format_time(elapsed_seconds)
    text_surface = timer_font.render(timer_text, True, WHITE)

    # Drawing
    screen.fill(BLACK)
    level.draw(screen)
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 64, 64))
    screen.blit(text_surface, text_rect)
    screen.blit(player.surf, player.rect)
    
    for pp in past_players:
        if pp.visible:
            screen.blit(pp.surf, pp.rect)  # Draw virtual player during replay


    # Display the message if level is complete
    if level.complete:        
        # Render the text to a surface
        text_surface = font_level_complete.render('Level Complete!', True, WHITE)  # White text
        # Position the text in the center of the screen
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
