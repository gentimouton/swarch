"""
Thin client: 
- send my inputs (if any) every tick
- display the screenshot received from the server
"""
import base64
from network import Handler, poll
import time
import zlib

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


pygame.init()

WIDTH, HEIGHT = 400, 300  # pixels
TICK_DURATION = 0.02  # seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Client(Handler):
    """ Send player inputs in JSON,
    receive screenshots in base64 + gzip.
    """
    def decode(self, msg):
        return zlib.decompress(base64.b64decode(msg))

    def on_msg(self, msg):
        surface = pygame.image.fromstring(msg, (WIDTH, HEIGHT), 'RGB')
        screen.blit(surface, (0, 0, WIDTH, HEIGHT))
        
        
client = Client('localhost', 8888)  # connect asynchronously

valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right'}

while 1:
    loop_start = time.time()
    
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
    
    # poll until tick is over
    while time.time() - loop_start < TICK_DURATION:
        poll(TICK_DURATION - (time.time() - loop_start))

    pygame.display.update()    
