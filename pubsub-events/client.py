"""
On start, subscribe to state_response messages, 
and publish a state_request message.
After having received a state_response message, 
subscribe to player_update and pellet_update messages. 
"""
from network import Handler, poll_for
import time
from uuid import uuid4

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


borders = []
pellets = []
players = {}  # map player name to box
myname = str(uuid4())[:8]

pygame.display.init()
screen = pygame.display.set_mode((400, 300))
TICK_DURATION = 0.02  # seconds

class Client(Handler):
    
    def on_open(self):
        self.do_send(('_sub', 'state'))
        self.do_send(('join', myname))

    def on_msg(self, data):
        global borders, pellets, players
        mtype, mdata = data
        borders = mdata['borders']
        pellets = mdata['pellets']
        players = mdata['players']
        
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
                msg = ('change_dir', (myname, valid_inputs[key]))
                client.do_send(msg)

def draw_everything():
    screen.fill((0, 0, 64))  # black
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    for name, p in players.items():
        if name == myname:
            pygame.draw.rect(screen, (0, 191, 255), p)  # deep sky blue
        else:
            pygame.draw.rect(screen, (255, 0, 0), p)  # red
    pygame.display.update()
    
while 1:
    loop_start = time.time()
    process_inputs()
    draw_everything()
    poll_for(TICK_DURATION - (time.time() - loop_start))  # poll until tick is over
    
