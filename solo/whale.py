from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


pygame.init()
screen = pygame.display.set_mode((400, 300))

pellet = pygame.Rect(randint(0, 390), randint(0, 290), 10, 10)
mybox = pygame.Rect(200, 150, 10, 10)  # start in middle of the screen
dx, dy = 0, 1  # start direction: down
delay = 1 # start by moving every frame
speed = 20

clock = pygame.time.Clock()

while True:
    clock.tick(100)  # frames per second
    
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


    if (delay >= speed):
        delay = 1
    else:
        mybox.move_ip(dx, dy)  # update position
        delay += 1
    if mybox.colliderect(pellet): # ate a pellet: grow, and place new pellet
        pellet = pygame.Rect(randint(0, 180), randint(0, 180), 10, 10)
        mybox.inflate_ip(2, 2)
        speed -= 1 # move slower as you grow bigger
        delay = 1
    
    screen.fill((0, 0, 64))  # dark blue
    pygame.draw.rect(screen, (0, 191, 255), mybox)  # Deep Sky Blue
    pygame.draw.rect(screen, (255, 192, 203), pellet)  # pink
    pygame.display.update()
