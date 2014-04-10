import pygame
from time import sleep
import sys
import json


pygame.init()
screen = pygame.display.set_mode((400, 300))


while 1:
    json_msg = sys.stdin.readline().rstrip()  # w/o trailing \n
    pygame.event.pump() # needed for Pygame's internal workings
    
    if json_msg:
        game_state = json.loads(json_msg) 
        borders = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in game_state['borders']]
        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in game_state['pellets']]
        b = game_state['mybox']  
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        
        screen.fill((0, 0, 64))  # dark blue
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
        pygame.display.update()
        
   
    else: # EOF is read when the pipe closes, and '' is sent 
        exit()