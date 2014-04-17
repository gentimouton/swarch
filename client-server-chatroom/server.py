from network import Listener, Handler, poll
from time import sleep
 
 
handlers = {}  # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        print msg
 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll()
    sleep(0.05)  # seconds

