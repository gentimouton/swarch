from time import sleep

from network import Listener, Handler, poll


done = False

class MyHandler(Handler):
    
    def on_open(self):
        print 'srv on open'
        
    def on_close(self):
        print 'srv on close'
    
    def on_msg(self, data):
        print 'srv received %s' % str(data)
        msg = {12: 3, 'hello': (1, 2)}
        self.do_send(msg)
        print 'srv sent %s' % str(msg)
        self.close_when_done()
        global done
        done = True
    
    
class Serv(Listener):
    handlerClass = MyHandler


port = 8888
server = Serv(port)
while not done:
    poll()
    sleep(.1)
server.stop() # cleanup