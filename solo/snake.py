from collections import deque
from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


pygame.init()
screen = pygame.display.set_mode((400, 300))
screen.fill((0, 0, 0))  # black

pellet = pygame.Rect(randint(0, 39) * 10, randint(0, 29) * 10, 10, 10)
myboxes = deque([pygame.Rect(200, 150, 10, 10)])  # start: middle of the screen
dx, dy = 0, 10  # start direction: down

clock = pygame.time.Clock()

while True:
    clock.tick(5)  # frames per second
    
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key == K_UP:
                dx, dy = 0, -10
            elif key == K_DOWN:
                dx, dy = 0, 10
            elif key == K_LEFT:
                dx, dy = -10, 0
            elif key == K_RIGHT:
                dx, dy = 10, 0
    
    headbox = myboxes[-1].copy()
    headbox.move_ip(dx, dy)  # move head
    myboxes.append(headbox)
    if headbox.colliderect(pellet):  # ate pellet: place new pellet
        pellet = pygame.Rect(randint(0, 39) * 10, randint(0, 29) * 10, 10, 10)
    else:  # no collision: remove last box
        myboxes.popleft()
    
    screen.fill((0, 0, 0))  # black
    [pygame.draw.rect(screen, (255, 0, 0), box) for box in myboxes]  # red
    pygame.draw.rect(screen, (0, 255, 0), pellet)  # green
    pygame.display.update()