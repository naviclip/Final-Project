import pygame
import sys
import os

# window size and FPS
W, H = 640, 360
FPS = 60

# game states
MENU = 0
START = 1
GAME = 2
WIN = 3
LOSE = 4

# start pygame
pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Agnis Adventure")
clock = pygame.time.Clock()
state = MENU

# main loop
while True:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0,0,0))
    pygame.display.update()
