"""
input: game state
output: none (pygame display)

Update the display every time I receive a game state in JSON.
{'mybox': [1,2,3,4], 
 'borders': [ [1,2,3,4], [2,3,4,5] ], 
 'pellets': [ [1,2,3,4] ] }
"""
import json
import sys

import pygame


def build_rect(quad):
    return pygame.Rect(quad[0], quad[1], quad[2], quad[3])

pygame.init()
screen = pygame.display.set_mode((400, 300))

while 1:
    json_msg = sys.stdin.readline().rstrip()  # blocking; remove trailing \n
    pygame.event.pump()  # required for Pygame's internal workings
    # otherwise Pygame stops: http://stackoverflow.com/q/20165492/856897
    
    if json_msg:
        game_state = json.loads(json_msg) 
        borders = [build_rect(p) for p in game_state['borders']]
        pellets = [build_rect(p) for p in game_state['pellets']]
        myrect = build_rect(game_state['mybox'])
        
        screen.fill((0, 0, 64))  # dark blue
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
        pygame.display.update()
   
    else:  # EOF is read when the pipe closes, and '' is sent 
        exit()