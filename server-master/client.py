from random import randint
import time

from pygame import Rect, init as pygame_init, event as pygame_event
from pygame.display import set_mode, update as update_display
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
    K_SPACE
from pygame.time import Clock

from network import Handler, poll


myname, mybox = None, None  # myname is given by the server
players = {}  # map player name to rectangle
pellets = []

class Client(Handler):
            
    def on_msg(self, data):
        msgtype = data['msg_type']
        global myname, mybox
        
            
client = Client('localhost', 8888)

pygame_init()
screen = set_mode((400, 300))
clock = Clock()
font = Font(None, 15)  # default pygame Font, height in pixels

borders = [Rect(0, 0, 2, 300), Rect(0, 0, 400, 2),
           Rect(398, 0, 2, 300), Rect(0, 298, 400, 2)]
dx, dy = 0, 1  # start direction: down
delay = 0  # start moving right away 

while True:
    
    clock.tick(50)  # frames per second
    poll()  # push and pull network messages

    for event in pygame_event.get():  # inputs
        if event.type == QUIT:
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
                
    if not myname:  # do nothing until the server welcomed us
        continue
    
    # draw everything
    screen.fill((0, 0, 64))  # dark blue
    [draw_rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [draw_rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    for name, hisbox in players.items():  # draw other players
        if name != myname and hisbox:
            if mybox and hisbox.width < mybox.width:
                color = 0, 255, 0  # smaller than me: green
            else:
                color = 255, 0, 0  # bigger or same size: red
            draw_rect(screen, color, hisbox)
            # anti-aliased, black
            text = font.render(str(hisbox.width), 1, (0, 0, 0))  
            screen.blit(text, hisbox)
    draw_rect(screen, (0, 191, 255), mybox)  # Deep Sky Blue
    text = font.render(str(mybox.width), 1, (0, 0, 0))  # anti-alias, black
    screen.blit(text, mybox)

    update_display()
