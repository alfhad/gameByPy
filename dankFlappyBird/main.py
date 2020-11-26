import pygame
import random
import math
from pygame import mixer
import sys

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.5
bird_movement = 0
game_active = True
high_score = 0
pipeSpacing = 10000
enemyCount = 5
frame_rate = 60

what_pipe = False

pygame.display.set_caption("Dank Flappy Bird")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png").convert()
# background = pygame.transform.scale2x(background)
base = pygame.image.load("base.png").convert()
base_pos = 0
bird_upflap = pygame.transform.scale2x(pygame.image.load("redbird-upflap.png")).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load("redbird-midflap.png")).convert_alpha()
bird_downflap = pygame.transform.scale2x(pygame.image.load("redbird-downflap.png")).convert_alpha()
# bird_mid = pygame.image.load("redbird-midflap.png").convert_alpha()
# bird_mid = pygame.transform.scale2x(bird_mid)
# bird_rect = bird_mid.get_rect(center = (200, 250))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_mid = bird_frames[bird_index]
bird_rect = bird_mid.get_rect(center=(200, 150))

pipe_surface = pygame.image.load("pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

over_font = pygame.font.Font("herosita.ttf", 64)

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 400)

# bulletConfig
bulletImg = pygame.image.load('bullet.png').convert_alpha()
bulletX = bird_rect.centerx
bulletY = bird_rect.centery
bulletState = 'ready'
bulletXChange = 10

score_value = 0
highscore = 0

sucks = pygame.font.Font('herosita.ttf', 32)

textX = 10
textY = 10


def showscore(x, y):
    score = sucks.render(f'Score: {score_value}    Highscore: {highscore}', True, (255, 255, 255))
    screen.blit(score, (x, y))


# enemyConfig
enemyImg = []
enemyX = []
enemyY = []
enemyYChange = []

#bird_upflap = pygame.transform.scale2x(pygame.image.load("devil.png")).convert_alpha()
for i in range(enemyCount):
    #enemyImg.append(pygame.image.load('devil.png'))
    enemyImg.append(pygame.transform.scale2x(pygame.image.load("devil.png")).convert_alpha())
    enemyX.append(random.randint(980, 1240))
    enemyY.append(random.randint(0, 560))
    enemyYChange.append(3)


def enemy(x, y, k):
    enemy_rect = (enemyImg[k].get_rect(center=(x, y)))
    screen.blit(enemyImg[k], enemy_rect)


def bullet(x, y):
    global bulletState
    bulletState = 'fire'
    bullet_rect = bulletImg.get_rect(center=(x, y))
    screen.blit(bulletImg, bullet_rect)


def collidere(ex, ey, bx, by):
    di = math.sqrt(math.pow((ex-bx), 2)+math.pow((ey-by), 2))
    if di < 27:
        return True
    return False


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
        # if pipe.bottom >= 500:
        #    screen.blit(pipe_surface, pipe)
        # else:
        #    flip_pipe = pygame.transform.flip(pipe_surface, False, True)
        #    screen.blit(flip_pipe, pipe)
        if not what_pipe:
            # Bottom
            screen.blit(pipe_surface, pipe)
            what_pipe = True
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            what_pipe = False


pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipeSpacing)


# collision detection
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
    game_over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (500, 300))


while True:
    bulletVar = 0
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
                if score_value > highscore:
                    highscore = score_value
                score_value = 0

            if event.key == pygame.K_z:
                if bulletState == 'ready':
                    bulletY = bird_rect.centery
                    bullet(bulletX, bulletY)

        if event.type == SPAWNPIPE:
            print("Pipe Spawn")
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_mid, bird_rect = bird_animation()

    screen.fill((57, 62, 70))
    screen.blit(background, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_mid)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        if not checkCollisions(pipe_list):
            game_active = False

        for i in range(enemyCount):

            enemyY[i] += enemyYChange[i]

            if enemyY[i] >= 568:
                enemyYChange[i] = -3

            if enemyY[i] <= 0:
                enemyYChange[i] = 3

            if collidere(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletState = 'ready'
                bulletX = bird_rect.centerx
                bulletY = bird_rect.centery
                enemyX[i] = random.randint(980, 1270)
                enemyY[i] = random.randint(0, 590)
                score_value += 1

            enemy(enemyX[i], enemyY[i], i)

        if bulletX > 1240:
            bulletX = bird_rect.centerx
            bulletState = 'ready'

        if bulletState == 'fire':
            bullet(bulletX, bulletY)
            bulletX += bulletXChange

        pipeSpacing = random.randint(3500, 10000)

    if not game_active:
        game_over_text()

    # Base
    base_pos -= 1
    if base_pos <= -250:
        base_pos = 0
    screen.blit(base, (base_pos, 590))

    screen.blit(base, (base_pos, 590))


    showscore(textX, textY)
    pygame.display.update()
    clock.tick(frame_rate)
