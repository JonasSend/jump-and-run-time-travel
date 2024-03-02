import pygame
import sys

# Initialize Pygame
from Constants import BLACK, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, VIOLET
from pygame.locals import RESIZABLE, DOUBLEBUF, HWSURFACE
from Level import Level
from PastPlayer import PastPlayer
from Player import Player
from util.timer import format_time

GAME_NAME = "TIME JUMPER"

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), RESIZABLE | DOUBLEBUF | HWSURFACE)
# Screen is a copy, where we draw our sprites on and later fit to the window
SCREEN = WINDOW.copy()
CLOCK = pygame.time.Clock()
timer_font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 54)
font_level_complete = pygame.font.Font(None, 96)
pygame.display.set_caption(GAME_NAME)

level = Level()


def init_game():
    start_ticks = pygame.time.get_ticks()
    past_players = []
    recording = PastPlayer()
    player = Player()
    return start_ticks, past_players, recording, player


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
                    pp.fade_colour()
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
    text_timer_surface = timer_font.render(timer_text, True, WHITE)
    text_name_surface = name_font.render(GAME_NAME, True, WHITE)

    # Drawing
    SCREEN.fill(BLACK)
    level.draw(SCREEN)
    text_timer_rect = text_timer_surface.get_rect(topright=(WINDOW_WIDTH - 64, 64))
    text_name_rect = text_name_surface.get_rect(topleft=(64, 64))
    SCREEN.blit(text_timer_surface, text_timer_rect)
    SCREEN.blit(text_name_surface, text_name_rect)
    SCREEN.blit(player.surf, player.rect)

    for pp in past_players:
        if pp.visible:
            SCREEN.blit(pp.surf, pp.rect)  # Draw virtual player during replay

    # Display the message if level is complete
    if level.complete:
        # Render the text to a surface
        text_timer_surface = font_level_complete.render('Level Complete!', True, VIOLET)  # White text
        # Position the text in the center of the SCREEN
        text_timer_rect = text_timer_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))
        SCREEN.blit(text_timer_surface, text_timer_rect)

    WINDOW.blit(pygame.transform.scale(SCREEN, WINDOW.get_rect().size), (0, 0))
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
