import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE
from random import randint

pygame.init()
resolution = 400, 300
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

game_over = False

while not game_over:
    
    clock.tick(2)  # frames per second
    
    # check for inputs
    for event in pygame.event.get():  
        if event.type == QUIT:
            game_over = True
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                game_over = True
                
    screen.fill((0, 0, 255))  # blue
    center = randint(0, 350), randint(0, 250)
    pygame.draw.circle(screen, (255, 0, 0), center, 20)  # red
    pygame.display.update()
