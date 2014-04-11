"""
input: stream of commands 
output: game state

One thread blocks, listening for inputs from stdin.
The other thread updates the game simulation at regular intervals,
and prints the game state in JSON:
{'mybox': [1,2,3,4], 
 'borders': [ [1,2,3,4], [2,3,4,5] ], 
 'pellets': [ [1,2,3,4] ] }
"""
import json
from random import randint
import sys
from threading import Thread
from time import sleep


dir_vectors = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

dims = 300, 400
borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = [ [randint(10, 380), randint(10, 280), 5, 5] for _ in range(4) ]
mybox = [200, 150, 10, 10]  # start in middle of the screen
myvector = dir_vectors['D']  # start direction: down 
game_over = False  # True when the pipe from inputs is closed 


def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
    
    
def update_sim():
    global mybox  # move me
    mybox[0] += myvector[0]
    mybox[1] += myvector[1]
    for b in borders:  # potential collision with a border
        if collide_boxes(mybox, b):
            mybox = [200, 150, 10, 10]
    for index, pellet in enumerate(pellets):  # potential collision with pellet
        if collide_boxes(mybox, pellet):
            mybox[2] *= 1.2
            mybox[3] *= 1.2
            pellets[index] = [randint(10, 380), randint(10, 280), 5, 5]


def read_stdin():
    global myvector, game_over
    while not game_over:
        # readline and rstrip: http://stackoverflow.com/a/2813530/856897
        new_dir = sys.stdin.readline().rstrip()  # blocking; remove trailing \n
        if new_dir:
            myvector = dir_vectors[new_dir]
        else:  # readline returns '' when I read EOF, ie the pipe closed
            game_over = True

thread = Thread(target=read_stdin)
thread.daemon = True  # die when the main thread dies 
thread.start()
# on non-Windows OS, I could also use select on stdin
# http://repolinux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-python/    


while not game_over:
    update_sim()
    game = {'borders': borders, 'pellets': pellets, 'mybox': mybox} 
    print json.dumps(game)
    sys.stdout.flush()  # don't buffer output
    sleep(0.02)  # in seconds
    
