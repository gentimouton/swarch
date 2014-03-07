from time import sleep

from network import connect, send
import network

def myopen(h):
    print 'opened'
    data = {'action': 'name', 'name': 'tho'} 
    send(h, data)
    print 'sent data'
    close(h)
    
#network.on_open = myopen
connect('localhost', 8888)
sleep(1)

