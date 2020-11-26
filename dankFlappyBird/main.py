import pygame
import random
import math
from pygame import mixer
import sys

pygame.init()

screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

pygame.display.set_caption("Dank Flappy Bird")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png").convert()
base = pygame.image.load("base.png").convert()
base_pos = -500

bird_mid = pygame.image.load("redbird-midflap.png").convert()
bird_mid = pygame.transform.scale2x(bird_mid)
bird_rect = bird_mid.get_rect(center = (200, 250))






while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((57,62,70))
    screen.blit(background, (0, -70))
    base_pos += 1
    if base_pos >= 0:
        base_pos = -500
    screen.blit(base, (base_pos, 430))
    screen.blit(bird_mid, bird_rect)


    pygame.display.update()
    clock.tick(120)