# Libs
import pygame
from sys import exit
from random import randint

# Functions
def display_score():
    current_time = int(pygame.time.get_ticks() / score_div_modifier) - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, 'Light Blue')
    score_rect = score_surf.get_rect(topright = (750, 10))
    screen.blit(score_surf, score_rect)

    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= obstacle_speed

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):     
            player_index = 0
        player_surf = player_walk[int(player_index)]
        


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
x_spawn_pos = randint(900, 1100)
score = 0

# Env vars
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()

# Obstacles

obstacle_rect_list = []
obstacle_speed = 5

    # Snail vars
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

    # Fly vars
fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Player vars
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0


player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom = (80,game_floor))
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
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                start_time = int(pygame.time.get_ticks() / score_div_modifier)
                game_active = True
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), game_floor)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), game_floor - 110)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        
                        
    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,game_floor))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= game_floor:
            player_rect.bottom = game_floor
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill('#5c9785')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(restart_game_surf, restart_game_rect)
        score_surf = game_font.render(f'Score: {score}', False, '#8bcfba')
        score_rect = score_surf.get_rect(midtop = (400,15))

        if score > 0:
            screen.blit(score_surf, score_rect)

        obstacle_rect_list.clear()
        player_rect.midbottom = (80, game_floor)
        player_gravity = 0
            
    pygame.display.update()
    clock.tick(60)