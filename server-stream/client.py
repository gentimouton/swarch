"""
Thin client: 
- send my inputs (if any) every tick
- display the buffer received from the server every tick 
"""
from network import Handler, poll

from pygame import Rect, init as init_pygame
from pygame.display import set_mode, update as update_pygame_display
from pygame.draw import rect as draw_rect
from pygame.event import get as get_pygame_events
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.time import Clock


borders = []
pellets = []
players = {}  # map player name to rectangle
myname = None
     
init_pygame()
screen = set_mode((400, 300))
clock = Clock()

def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return Rect(x, y, w, h)
    
class Client(Handler):
            
    def on_msg(self, data):
        global borders, pellets, players, myname
        borders = [make_rect(b) for b in data['borders']]
        pellets = [make_rect(p) for p in data['pellets']]
        players = {name: make_rect(p) for name, p in data['players'].items()}
        myname = data['myname']
        
client = Client('localhost', 8888)  # connect asynchronously

valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right'}

while 1:
    
    poll()  # push and pull network messages

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
    
    # draw everything
    screen.fill((0, 0, 64))  # dark blue
    [draw_rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [draw_rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    for name, p in players.items():
        if name != myname:
            draw_rect(screen, (255, 0, 0), p)  # red
    if myname:
        draw_rect(screen, (0, 191, 255), players[myname])  # deep sky blue
    
    update_pygame_display()
    
    clock.tick(50)  # frames per second, independent of server frame rate
