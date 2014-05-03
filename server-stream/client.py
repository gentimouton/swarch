"""
Thin client: 
- send my inputs (if any) every tick
- display the buffer received from the server  
Pygame's surfarray relies on numpy. 
numpy 64 bit MSI available at http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
"""
from base64 import b64decode
from network import Handler, poll
import zlib

from pygame import Rect, init as init_pygame
import pygame
from pygame.display import set_mode, update as update_pygame_display
from pygame.event import get as get_pygame_events
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


init_pygame()
screen = set_mode((400, 300))


class Client(Handler):
            
    def on_msg(self, msg):
        img = zlib.decompress(b64decode(msg))
        surface = pygame.image.fromstring(img, (400, 300), 'RGB')
        screen.blit(surface, (0, 0, 400, 300))
         
        
client = Client('localhost', 8888)  # connect asynchronously

valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right'}

while 1:

    poll(0.02)

    # send valid inputs to the server
    for event in get_pygame_events():  
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key in valid_inputs:
                msg = {'input': valid_inputs[key]}
                client.do_send(msg)
    
    update_pygame_display()
    
