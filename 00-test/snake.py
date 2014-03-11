from random import randint
from time import sleep

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

from PodSixNet.Connection2 import Client


myname = randint(0, 10 ** 9)  # avoid name collisions
other_players = {}  # map names to rectangles
connected = False

class SnakeClient(Client):
    
    def Network_connected(self, data):  # connected: send my name
        global connected
        connected = True
        self.send({'action': 'name',
                   'name': myname})
        
    def Network_login(self, data):  # someone joined
        name = data['name']
        if name != myname:  # ignore messages about me
            other_players[name] = pygame.Rect(200, 150, 10, 10)
        
    def Network_pos(self, data):
        name = data['name']
        if name != myname:  # ignore messages about me
            top, left = data['topleft']
            other_players[name] = pygame.Rect(top, left, 10, 10)
        

client = SnakeClient()
client.connect('localhost', 8888)


# gfx
pygame.init()
screen = pygame.display.set_mode((400, 300))
screen.fill((0, 0, 0))  # black

myrect = pygame.Rect(200, 150, 10, 10)  # start position: middle of the screen
dx, dy = 0, 1  # starting direction: down

clock = pygame.time.Clock()

while True:
    clock.tick(20)

    client.pump() # network
    
    for event in pygame.event.get():  # keyboard inputs
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
        
    if not connected:  # wait until we're connected
        continue
    
    # update game state and forward it to other players
    myrect.move_ip(dx, dy)
    client.send({'action': 'pos',
                 'topleft': myrect.topleft})
    
    # gfx
    screen.fill((0, 0, 0))  # black
    pygame.draw.rect(screen, (255, 0, 0), myrect) # red
    for name, rect in other_players.items():
        pygame.draw.rect(screen, (255, 255, 255), rect) # white
    pygame.display.update()
    
