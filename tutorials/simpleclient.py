from time import sleep

from network import Handler, poll


done = False

class Conn(Handler):
    
    def on_open(self):
        print 'cli on open'
        msg = [1, 2, 3] 
        self.do_send(msg)
        print 'cli sent %s' % str(msg)
        
    def on_close(self):
        print 'cli on close'
        
    def on_msg(self, data):
        print 'cli received %s' % str(data)
        self.close_when_done()
        global done 
        done = True
        
host, port = 'localhost', 8888
client = Conn(host, port)
while not done:
    poll()
    sleep(.1)
client.do_close() # cleanup