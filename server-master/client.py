"""
The Client is slave: 
- it sends only the player inputs to the server.
- every frame, it displays the server's last received data
Pros: the server is the only component with game logic, 
so all clients see the same game at the same time (consistency, no rollbacks).
Cons: lag between player input and screen display (one round-trip).
But the client can smooth the lag by interpolating the position of the boxes. 
"""
from network import Handler, poll_for
import time

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


borders = []
pellets = []
players = {}  # map player name to rectangle
myname = None
     
pygame.display.init()
screen = pygame.display.set_mode((400, 300))
TICK_DURATION = 0.02  # seconds

def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return pygame.Rect(x, y, w, h)
    
class Client(Handler):
            
    def on_msg(self, data):
        global borders, pellets, players, myname
        borders = [make_rect(b) for b in data['borders']]
        pellets = [make_rect(p) for p in data['pellets']]
        players = {name: make_rect(p) for name, p in data['players'].items()}
        myname = data['myname']
        
client = Client('localhost', 8888)  # connect asynchronously

valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right'}

def send_inputs():
    # send valid inputs to the server
    for event in pygame.event.get():  
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key in valid_inputs:
                msg = {'input': valid_inputs[key]}
                client.do_send(msg)

while 1:
    loop_start = time.time()
    
    send_inputs()
    
    # draw everything
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    for name, p in players.items():
        if name != myname:
            pygame.draw.rect(screen, (255, 0, 0), p)  # red
    if myname:
        pygame.draw.rect(screen, (0, 191, 255), players[myname])  # deep sky blue
    
    poll_for(TICK_DURATION - (time.time() - loop_start)) # poll until tick is over

    pygame.display.update()
    
