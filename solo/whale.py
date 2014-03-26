from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

borders = [pygame.Rect(0, 0, 2, 300), pygame.Rect(0, 0, 400, 2),
           pygame.Rect(398, 0, 2, 300), pygame.Rect(0, 298, 400, 2)]
pellets = [pygame.Rect(randint(10, 380), randint(10, 280), 5, 5) for _ in range(4)]
mybox = pygame.Rect(200, 150, 10, 10)  # start in middle of the screen
dx, dy = 0, 1  # start direction: down
delay = 0  # start moving right away 

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

    delay -= 4
    if mybox.collidelist(borders) != -1:  # game over
        mybox = pygame.Rect(200, 150, 10, 10)  # back to middle of the screen
        delay = 0  # move right away
    if delay <= 0:
        mybox.move_ip(dx, dy)  # update position
        delay = (mybox.width - 10) / 2  # number of pellets eaten so far
    p_index = mybox.collidelist(pellets)
    if p_index != -1:  # ate a pellet: grow, and replace a pellet
        pellets[p_index] = pygame.Rect(randint(10, 380), randint(10, 280), 5, 5)
        mybox.size = mybox.width * 1.2, mybox.height * 1.2
    
    screen.fill((0, 0, 64))  # dark blue
    pygame.draw.rect(screen, (0, 191, 255), mybox)  # Deep Sky Blue
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
    pygame.display.update()
