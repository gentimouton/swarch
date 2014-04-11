import json
import sys


prevx, prevy = 0, 0

while 1:
    json_msg = sys.stdin.readline().rstrip()  # blocking; remove trailing \n
    if json_msg:
        game_state = json.loads(json_msg) 
        x, y, w, h = game_state['mybox']
        # only display my position when I pass at 10x10 grid points
        if ((x % 10 == 0 and prevx % 10) or (y % 10 == 0 and prevy % 10)):
            print game_state['mybox']
        prevx, prevy = x, y
    else:  # EOF is read when the pipe closes, and '' is sent 
        exit()
    
