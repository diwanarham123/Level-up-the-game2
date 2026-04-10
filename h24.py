import pygame
import random
import os

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
player_width = 64
player_height = 64
enemy_width = 32
enemy_height = 32
num_of_enemies = 7

screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Player-Enemy Collision Game")

COLLISION_SOUND_PATH = 'collision.wav'
BACKGROUND_MUSIC_PATH = 'background_music.mp3'
BACKGROUND_IMAGE_PATH = 'background.jpg'

collision_sound = None
try:
    collision_sound = pygame.mixer.Sound(COLLISION_SOUND_PATH)
except pygame.error as e:
    print(f"Warning: Could not load collision sound {COLLISION_SOUND_PATH}: {e}")
    print("Game will run without collision sound.")

try:
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Warning: Could not load background music {BACKGROUND_MUSIC_PATH}: {e}")
    print("Game will run without background music.")

background_image = None
try:
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Warning: Could not load background image {BACKGROUND_IMAGE_PATH}: {e}")
    print("Game will run without background image, using black background.")

player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height - 10

enemy_x_positions = []
enemy_y_positions = []
enemy_velocities_y = []

for i in range(num_of_enemies):
    enemy_x_positions.append(random.randint(0, screen_width - enemy_width))
    enemy_y_positions.append(random.randint(-screen_height, -enemy_height))
    enemy_velocities_y.append(random.uniform(0.5, 2.5))

score = 0
font = pygame.font.Font(None, 36)

print("Pygame initialized. Starting game loop. Close the Pygame window to stop.")

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    for i in range(num_of_enemies):
        enemy_y_positions[i] += enemy_velocities_y[i]
        if enemy_y_positions[i] > screen_height:
            enemy_y_positions[i] = random.randint(-enemy_height * 2, -enemy_height)
            enemy_x_positions[i] = random.randint(0, screen_width - enemy_width)
            enemy_velocities_y[i] = random.uniform(0.5, 2.5)

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for i in range(num_of_enemies):
        enemy_rect = pygame.Rect(enemy_x_positions[i], enemy_y_positions[i], enemy_width, enemy_height)

        if player_rect.colliderect(enemy_rect):
            score += 1
            print(f"Collision detected! Score: {score}")
            if collision_sound:
                collision_sound.play()
            enemy_y_positions[i] = random.randint(-enemy_height * 2, -enemy_height)
            enemy_x_positions[i] = random.randint(0, screen_width - enemy_width)
            enemy_velocities_y[i] = random.uniform(0.5, 2.5)

    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (0, 0, 255), player_rect)

    for i in range(num_of_enemies):
        enemy_rect_to_draw = pygame.Rect(enemy_x_positions[i], enemy_y_positions[i], enemy_width, enemy_height)
        pygame.draw.rect(screen, (255, 0, 0), enemy_rect_to_draw)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
print("Game finished. Pygame quit.")
