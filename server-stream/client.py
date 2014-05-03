"""
Thin client: 
- send my inputs (if any) every tick
- display the buffer received from the server  
Pygame's surfarray relies on numpy. 
numpy 64 bit MSI available at http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
"""
from base64 import b64decode
from network import Handler, poll
import time

from numpy import dtype, frombuffer
from pygame import Rect, init as init_pygame
from pygame.display import set_mode, update as update_pygame_display
from pygame.event import get as get_pygame_events
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.surfarray import make_surface
import pygame

init_pygame()
screen = set_mode((80, 60))


class Client(Handler):
            
    def on_msg(self, msg):
        # base64 codec snippet from http://stackoverflow.com/a/19271311/856897
        # Encoding/Decoding surfarray to a list takes 100 ms. b64 is 10-20 ms. 

        before = time.time()
        
        dt = dtype(msg['dtype'])
        array = frombuffer(b64decode(str(msg['b64array'])), dt)
        surfarray = array.reshape(msg['shape'])

        print 'make array %3.0f ms' % ((time.time() - before) * 1000)
        before = time.time()
        
        surface = make_surface(surfarray)
        
        print 'make surface %3.0f ms' % ((time.time() - before) * 1000)
        before = time.time()
        
        screen.blit(surface, (0, 0, 400, 300))

        print 'blit surface %3.0f ms' % ((time.time() - before) * 1000)
        
        
client = Client('localhost', 8888)  # connect asynchronously

valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right'}

while 1:

    poll()

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
    
    time.sleep(0.1)