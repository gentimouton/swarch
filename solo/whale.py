from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


pygame.init()
screen = pygame.display.set_mode((400, 300))
screen.fill((0, 0, 0))  # black

pellet = pygame.Rect(randint(0, 390), randint(0, 290), 10, 10)
mybox = pygame.Rect(200, 150, 10, 10)  # start in middle of the screen
dx, dy = 0, 1  # start direction: down

clock = pygame.time.Clock()

while True:
    clock.tick(50)  # frames per second
    
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
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
    
    mybox.move_ip(dx, dy)  # update position
    if mybox.colliderect(pellet): # ate a pellet: grow, and place new pellet
        pellet = pygame.Rect(randint(0, 390), randint(0, 290), 10, 10)
        mybox.inflate_ip(2, 2) 
    
    screen.fill((0, 0, 0))  # black
    pygame.draw.rect(screen, (255, 0, 0), mybox)  # red
    pygame.draw.rect(screen, (0, 255, 0), pellet)  # green
    pygame.display.update()
