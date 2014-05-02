# surfarray relies on numpy 
# also available at http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

from random import randint
from time import time
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT
import numpy
import base64

pygame.init()
screen = pygame.display.set_mode((400, 300))
buffer = pygame.Surface((400, 300))
clock = pygame.time.Clock()

borders = [pygame.Rect(0, 0, 2, 300), pygame.Rect(0, 0, 400, 2),
           pygame.Rect(398, 0, 2, 300), pygame.Rect(0, 298, 400, 2)]
pellets = [pygame.Rect(randint(10, 380), randint(10, 280), 5, 5) for _ in range(4)]
mybox = pygame.Rect(200, 150, 10, 10)  # start in middle of the screen
dx, dy = 0, 1  # start direction: down
delay = 0  # start moving right away 


def Base64Encode(ndarray):
    return json.dumps([str(ndarray.dtype),
                       base64.b64encode(ndarray),
                       ndarray.shape])

def Base64Decode(jsonDump):
    loaded = json.loads(jsonDump)
    dtype = np.dtype(loaded[0])
    arr = np.frombuffer(base64.decodestring(loaded[1]),dtype)
    if len(loaded) > 2:
        return arr.reshape(loaded[2])
    return arr


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

    delay -= 4
    if mybox.collidelist(borders) != -1:  # game over
        mybox = pygame.Rect(200, 150, 10, 10)  # back to middle of the screen
        delay = 0  # move right away
    if delay <= 0:
        mybox.move_ip(dx, dy)  # update position
        delay = (mybox.width - 10) / 2  # number of pellets eaten so far
    indices = mybox.collidelistall(pellets)
    for p_index in indices:  # ate a pellet: grow, and replace a pellet
        pellets[p_index] = pygame.Rect(randint(10, 380), randint(10, 280), 5, 5)
        mybox.size = mybox.width * 1.2, mybox.height * 1.2

    buffer.fill((0, 0, 64))  # dark blue
    pygame.draw.rect(buffer, (0, 191, 255), mybox)  # Deep Sky Blue
    [pygame.draw.rect(buffer, (255, 192, 203), p) for p in pellets]  # pink
    [pygame.draw.rect(buffer, (0, 191, 255), b) for b in borders]  # deep sky blue

    #screen.blit(buffer, (0,0,400,300))
    before = time()
    pg_array = pygame.surfarray.array3d(buffer) # serialize
    
    ######################################
    
    # base64 encoding takes 10-20ms
    # from http://stackoverflow.com/a/19271311/856897
    # encode
    msg = [str(pg_array.dtype), base64.b64encode(pg_array), pg_array.shape]
    # decode
    dtype = numpy.dtype(msg[0])
    arr = numpy.frombuffer(base64.b64decode(msg[1]), dtype)
    array = arr.reshape(msg[2])

    # tolist + asarray take 100 ms 
    #l = pg_array.tolist() # encode
    #array = numpy.asarray(l) # decode
    
    ######################################
    print '%1.5f' % (time() - before)
    screen.blit(pygame.surfarray.make_surface(array), (0, 0, 400, 300))
    
    pygame.display.update()
