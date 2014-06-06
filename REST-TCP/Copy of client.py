"""

"""
from network import Handler, poll_for
import time

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


borders = []
pellets = []
players = {}  # map player name to rectangle
myname = None
     

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

def process_inputs():
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

pygame.display.init()
screen = pygame.display.set_mode((400, 300))

def draw_everything():
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    for name, p in players.items():
        if name != myname:
            pygame.draw.rect(screen, (255, 0, 0), p)  # red
    if myname:
        pygame.draw.rect(screen, (0, 191, 255), players[myname])  # deep sky blue
    pygame.display.update()

while 1:
    loop_start = time.time()
    process_inputs()
    draw_everything()
    poll_for(TICK_DURATION - (time.time() - loop_start)) # poll until tick is over
