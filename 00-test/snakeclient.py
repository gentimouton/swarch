from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

from network import Handler, poll


myname = randint(0, 10 ** 9)  # avoid name collisions
other_players = {}  # map names to rectangles

class Client(Handler):
    
    def on_open(self):
        self.do_send({'msgtype':'join', 'name':myname})
    
    def on_close(self):
        pass
    
    def on_msg(self, data):
        msgtype = data['msgtype']
        name = data['name']
        if msgtype == 'join':  # someone joined
            if name != myname:  # ignore messages about me
                other_players[name] = pygame.Rect(200, 150, 10, 10)
        elif msgtype == 'leave':  # someone left
            del other_players[name]
        elif msgtype == 'move':  # someone moved
            if name != myname:  # ignore messages about me
                top, left = data['top'], data['left']
                other_players[name] = pygame.Rect(left, top, 10, 10)

client = Client('localhost', 8888)

pygame.init()
screen = pygame.display.set_mode((400, 300))
screen.fill((0, 0, 0))  # black

myrect = pygame.Rect(200, 150, 10, 10)  # start position: middle of the screen
dx, dy = 0, 1  # starting direction: down

clock = pygame.time.Clock()

while True:
    clock.tick(20)
    poll()  # push and pull network messages
    
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
        
    if not client.connected:  # display only after we connect
        continue
    
    myrect.move_ip(dx, dy)  # update my game state and forward it to others
    client.do_send({'msgtype': 'move', 'name': myname,
                    'top': myrect.top, 'left': myrect.left})
    
    screen.fill((0, 0, 0))  # black
    pygame.draw.rect(screen, (255, 0, 0), myrect)  # red
    for rect in other_players.values():
        pygame.draw.rect(screen, (255, 255, 255), rect)  # white
    pygame.display.update()