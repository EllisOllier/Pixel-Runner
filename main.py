# Libs
from typing import Any
import pygame
from sys import exit
from random import randint, choice

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.25)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):     
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): 
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destory()

    def destory(self):
        if self.rect.x < -100:
            self.kill()

# Functions
def display_score():
    current_time = int(pygame.time.get_ticks() / score_div_modifier) - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, 'Light Blue')
    score_rect = score_surf.get_rect(topright = (750, 10))
    screen.blit(score_surf, score_rect)

    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

# Game init
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Jumper')

# Class vars
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Game vars
clock = pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score_div_modifier = 100
game_floor = 300
score = 0
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.25)

# Env vars
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()

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

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = int(pygame.time.get_ticks() / score_div_modifier)
                game_active = True
                background_music.play(loops = -1)

    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,game_floor))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacle movement
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        game_active = collision_sprite()

    else:
        screen.fill('#5c9785')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(restart_game_surf, restart_game_rect)
        score_surf = game_font.render(f'Score: {score}', False, '#8bcfba')
        score_rect = score_surf.get_rect(midtop = (400,15))

        if score > 0:
            screen.blit(score_surf, score_rect)

        player_gravity = 0
        background_music.stop()
            
    pygame.display.update()
    clock.tick(60)