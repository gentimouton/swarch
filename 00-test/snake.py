import pygame
from pygame.locals import *

pygame.init()

# gfx
WHITE = (250, 250, 250) # rgb
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((400, 300))
screen.fill(WHITE)
pygame.display.set_caption('Snake')


head_rect = pygame.Rect(200, 150, 10, 10)
dx, dy = 0, 1 # original direction: down

# clock
clock = pygame.time.Clock()

while True:
    clock.tick(20)
    
    # inputs
    for event in pygame.event.get():
        if (event.type == QUIT):
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key == K_UP:
                dx, dy = 0, -1
            elif key == K_DOWN:
                dx, dy = 0, 1
            elif key == K_LEFT:
                dx, dy = -1, 0
            elif key == K_RIGHT:
                dx, dy = 1, 0
    
    # update game state
    head_rect.move_ip(dx, dy)
    
    # gfx
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, head_rect)
    pygame.display.update()
    