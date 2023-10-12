# Libs
import pygame
from sys import exit

# Functions
def display_score():
    current_time = int(pygame.time.get_ticks() / score_div_modifier) - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, 'Light Blue')
    score_rect = score_surf.get_rect(topright = (750, 10))
    screen.blit(score_surf, score_rect)

    return current_time

# Game init
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Jumper')

# Game vars
clock = pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score_div_modifier = 100
game_floor = 300
x_spawn_pos = 800
score = 0

# Env vars
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()

# Snail vars
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (x_spawn_pos, game_floor))
snail_speed = 5

# Player vars
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,game_floor))
player_gravity = 0
player_jump_height = -20

# Main menu
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surf = game_font.render("Pixel Runner", False, '#8bcfba')
title_rect = title_surf.get_rect(midtop = (400,50))

restart_game_surf = game_font.render("Press Space to Restart!", False, '#8bcfba')
restart_game_rect = restart_game_surf.get_rect(midbottom = (400,350))

# Timer
obstacle_timer = pygame.USEREVENT + 1

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint((event.pos)):
                    if player_rect.bottom == game_floor:
                        player_gravity = player_jump_height   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == game_floor:
                        player_gravity = player_jump_height  
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.left = x_spawn_pos
                start_time = int(pygame.time.get_ticks() / score_div_modifier)
                game_active = True
                        
    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,game_floor))

        snail_rect.x -= snail_speed
        if snail_rect.right <= 0: snail_rect.left = x_spawn_pos
        screen.blit(snail_surf, snail_rect)
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= game_floor:
            player_rect.bottom = game_floor
        screen.blit(player_surf, player_rect)

        # Collisions
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('#5c9785')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(restart_game_surf, restart_game_rect)
        score_surf = game_font.render(f'Score: {score}', False, '#8bcfba')
        score_rect = score_surf.get_rect(midtop = (400,15))

        if score > 0:
            screen.blit(score_surf, score_rect)
            
    pygame.display.update()
    clock.tick(60)