# input: stream of commands 
# output: game state
import sys
import json
from random import randint
from time import sleep
from hmac import new

dir_vectors = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

dims = 300, 400
borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = [ [randint(10, 380), randint(10, 280), 5, 5] for _ in range(4) ]
mybox = [200, 150, 10, 10]  # start in middle of the screen
mydir = dir_vectors['D']  # start direction: down 


def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
    
    
def update_sim():
    # move me
    global mybox
    mybox[0] += mydir[0]
    mybox[1] += mydir[1]
    # potential collision with a border
    for b in borders:
        if collide_boxes(mybox, b):
            mybox = [200, 150, 10, 10]
    # potential collision with a pellet
    for index, pellet in enumerate(pellets):
        if collide_boxes(mybox, pellet):
            mybox[2] *= 1.2
            mybox[3] *= 1.2
            pellets[index] = [randint(10, 380), randint(10, 280), 5, 5]
            

# readline and rstrip: http://stackoverflow.com/a/2813530/856897
while 1:
    new_dir = sys.stdin.readline().rstrip()  # without trailing \n
    
    # new_dir = sys.stdin.read(1)
    # TODO: currently blocking for input read
    # use a Thread http://stackoverflow.com/a/4896288/856897
    # or select/poll http://repolinux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-python/
    # AND replace readline by os.read() http://bugs.python.org/issue1175#msg56041
    
    if new_dir:
        mydir = dir_vectors[new_dir]
        update_sim()
        game = {'borders': borders, 'pellets': pellets, 'mybox': mybox} 
        print json.dumps(game)
        sys.stdout.flush()  # don't buffer output

    else:  # readline returns '' when I read EOF
        exit()
    # sleep(0.02) # in seconds
        
