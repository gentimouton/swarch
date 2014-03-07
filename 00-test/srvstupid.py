from time import sleep

import network as nw


clients = []

def on_open(handler):
    clients.append(handler)
    print 'opened'
nw.on_open = on_open

nw.listen(8888)
while 1:
    nw.receive()
    
    
