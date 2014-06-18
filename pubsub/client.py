from network import Handler, poll_for
import time

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


borders = []
pellets = []
players = {}  # map player name to box
myname = None
frustum = [0, 0, 0, 0]  # nothing visible

pygame.display.init()
screen = pygame.display.set_mode((400, 300))
TICK_DURATION = 0.02  # seconds

class Client(Handler):

    def on_msg(self, data):
        global borders, pellets, players, myname, frustum
        borders = data['borders']
        pellets = data['pellets']
        players = data['players']
        myname = data['myname']
        frustum = data['frustum']
        
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

def draw_everything():
    screen.fill((0, 0, 0))  # black
    pygame.draw.rect(screen, (0, 0, 64), frustum)  # dark blue
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
    poll_for(TICK_DURATION - (time.time() - loop_start))  # poll until tick is over
    
