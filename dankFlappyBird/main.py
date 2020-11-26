import pygame
import random
import math
from pygame import mixer
import sys

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

#Game Variables
gravity = 0.5
bird_movement = 0
game_active = True
score = 0
high_score = 0

what_pipe = False

pygame.display.set_caption("Dank Flappy Bird")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png").convert()
#background = pygame.transform.scale2x(background)
base = pygame.image.load("base.png").convert()
base_pos = 0
bird_upflap = pygame.transform.scale2x(pygame.image.load("redbird-upflap.png")).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load("redbird-midflap.png")).convert_alpha()
bird_downflap = pygame.transform.scale2x(pygame.image.load("redbird-downflap.png")).convert_alpha()
#bird_mid = pygame.image.load("redbird-midflap.png").convert_alpha()
#bird_mid = pygame.transform.scale2x(bird_mid)
#bird_rect = bird_mid.get_rect(center = (200, 250))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_mid = bird_frames[bird_index]
bird_rect = bird_mid.get_rect(center = (200, 150))

pipe_surface = pygame.image.load("pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

over_font = pygame.font.Font("herosita.ttf", 64)

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 400)

def create_pipe():
    rand_val = random.randint(220, 540)
    bottom_pipe = pipe_surface.get_rect(midtop=(1300, rand_val))
    top_pipe = pipe_surface.get_rect(midtop=(1300, rand_val - 270 - 570))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes

def draw_pipes(pipes):
    global what_pipe
    for pipe in pipes:
        #if pipe.bottom >= 500:
        #    screen.blit(pipe_surface, pipe)
        #else:
        #    flip_pipe = pygame.transform.flip(pipe_surface, False, True)
        #    screen.blit(flip_pipe, pipe)
        if what_pipe == False:
            #Bottom
            screen.blit(pipe_surface, pipe)
            what_pipe = True
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            what_pipe = False

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 4000)

#collison detection
def checkCollisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 590:
        return False
        
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def game_over_text():
    game_over = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over, (500, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (200, 250)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            print("Pipe Spawn")
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_mid, bird_rect = bird_animation()

    screen.fill((57,62,70))
    screen.blit(background, (0, 0))

    if game_active:
        #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_mid)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        if checkCollisions(pipe_list) == False:
            game_active = False

    if game_active == False:
        game_over_text()

    #Base
    base_pos -= 1
    if base_pos <= -250:
        base_pos = 0
    screen.blit(base, (base_pos, 590))

    screen.blit(base, (base_pos, 590))
    pygame.display.update()
    clock.tick(80)