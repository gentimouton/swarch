from random import randint

from pygame import Rect, init as pygame_init
from pygame.display import set_mode
from pygame.time import Clock
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

from network import Handler, poll


myname, mybox = None, None  # myname is given by the server
players = {}  # map player name to rectangle
pellets = []
        
class Client(Handler):
    
    def on_msg(self, data):
        msgtype, name = data['msg_type'], data['name']
        
        if msgtype == 'welcome':
            for id, state in data['pellets']:  # create all pellets
                left, top, width, height = tuple(state)
                pellets.append(Rect(left, top, width, height))
            for name, state in data['players']:  # create all players
                left, top, width, height = tuple(state)
                players[name] = Rect(left, top, width, height)
            myname, mybox = name, players[name]
                
        elif msgtype == 'join' and name != myname:  # ignore my join message
            left, top, width, height = tuple(data['state']) 
            players[name] = Rect(left, top, width, height)
            
        elif msgtype == 'leave':
            del players[name]
            
        elif msgtype == 'move' and name != myname:  # ignore my move messages
            left, top, width, height = tuple(data['state'])
            players[name] = Rect(left, top, width, height)
            
        elif msgtype == 'eat':
            # TODO: if name is myname, don't update my left,top  
            left, top, width, height = tuple(data['state'])
            players[name] = Rect(left, top, width, height)
            pellets[data['pellet_index']] = data['new_pellet']
            
            
        

client = Client('localhost', 8888)

pygame_init()
screen = set_mode((400, 300))
clock = Clock()

borders = [Rect(0, 0, 2, 300), Rect(0, 0, 400, 2),
           Rect(398, 0, 2, 300), Rect(0, 298, 400, 2)]
dx, dy = 0, 1  # start direction: down
delay = 0  # start moving right away 

while True:
    clock.tick(50)  # frames per second
    
    for event in pygame.event.get():  # inputs
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
    
    if not myname:  # until we receive a 'welcome' message
        continue
    
    delay -= 4
    
#     if mybox.collidelist(borders) != -1:  # game over
#         mybox = Rect(200, 150, 10, 10)  # back to middle of the screen
#         delay = 0  # move right away
        
    if delay <= 0:
        mybox.move_ip(dx, dy)  # update position
        delay = (mybox.width - 10) / 2  # number of pellets eaten so far
        client.do_send({'msg_type': 'move',
                        'state': [mybox.left, mybox.top, mybox.w, mybox.h]})
        
    p_index = mybox.collidelist(pellets)
    if p_index != -1:  # ate a pellet: grow, and replace a pellet
        client.do_send({'msg_type': 'eat',
                        'pellet_index': p_index})
        
    
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    [pygame.draw.rect(screen, (255, 0, 0), p) for p in other_players]  # red
    pygame.draw.rect(screen, (0, 191, 255), mybox)  # Deep Sky Blue
    pygame.display.update()
