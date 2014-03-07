import socket
from time import sleep, time

from rencode import loads, dumps


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(1)
sock.connect(('localhost', 8888))
print '%3.3f Connected to server' % (time() % 1000)
line = {'action': 'name', 'name': 'tho'} 
sock.sendall(dumps(line) + '\0')
print '%3.3f Sent %s ' % (time() % 1000, str(line))
sock.close()
print '%3.3f Closed conn to server' % (time() % 1000)