import pygame
import random
import math
from pygame import mixer

#whenever we start a new game
pygame.init()

#Game Over
over_font = pygame.font.Font("herosita.ttf", 64)

#score
score_value = 0
font = pygame.font.Font('herosita.ttf', 32)
textX = 10
textY = 10


#creating a screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("background.jpeg")

#Background Music
mixer.music.load('back.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
    enemyImage.append(pygame.image.load("brawl.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(0.75)
    enemyY_change.append(0)

#Bullet
# ready - cant see the bullet
# fire - bullet moves
bulletImage = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = -4
bullet_state = "ready"

overStatus = False

#Boom
boomImage = pygame.image.load("boom.png")

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y):
    screen.blit(pygame.image.load("brawl.png"), (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x+16, y+10))

def boom(x, y):
    screen.blit(boomImage, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(((enemyX-bulletX)*(enemyX-bulletX)) + ((enemyY-bulletY)*(enemyY-bulletY)))
    if dist < 27:
        return True
    else:
        return False

def isCollision2(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(((enemyX-bulletX)*(enemyX-bulletX)) + ((enemyY-bulletY)*(enemyY-bulletY)))
    if dist < 35:
        return True
    else:
        return False

def show_score(x, y):
    score = font.render("Score: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over, (300, 250))


#Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            
            if event.key == pygame.K_RIGHT:
                playerX_change = 1

            if event.key == pygame.K_UP:
                playerY_change = -1

            if event.key == pygame.K_DOWN:
                playerY_change = 1
        #bullet_sound = mixer.Sound('shoot.wav')
        #bullet_sound.play()
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    screen.fill((57,62,70))
    screen.blit(background, (0, 0))
    playerX += playerX_change
    playerY += playerY_change

    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]


    if bullet_state == "fire":
        bulletY += bulletY_change
        fire_bullet(bulletX, bulletY)


    #boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    for i in range(no_of_enemies):

        #Game Over Check
        if isCollision2(playerX, playerY, enemyX[i], enemyY[i]):
            for j in range(no_of_enemies):
                enemyX[j] = 2000
            game_over_text()
            overStatus = True
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.75
            enemyY_change[i] = 40
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.75
            enemyY_change[i] = 40
        else:
            enemyY_change[i] = 0

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY + 10
    
    for i in range(no_of_enemies):
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bullet_state = "ready"
            bulletY = playerY + 10
            score_value += 1
            boomX, boomY = enemyX[i], enemyY[i]
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 250)
            boom(boomX, boomY)
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

    player(playerX, playerY)

    for i in range(no_of_enemies):
        enemy(enemyX[i], enemyY[i])

    show_score(textX, textY)

    if overStatus:
        game_over_text()

    pygame.display.update()