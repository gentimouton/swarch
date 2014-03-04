from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from time import sleep

class ClientChannel(Channel):
    
    def __init__(self, *args, **kwargs):
        self.name = ''
        Channel.__init__(self, *args, **kwargs)

    def Network_name(self, data):
        self.name = data['name']
        print 'Name received: %s from %s' % (self.name, str(self.addr))
        self._server.send_all({'action': 'login',
                               'name': self.name})
        
    def Network_pos(self, data):
        self._server.send_all({'action': 'pos',
                               'name': self.name,
                               'topleft': data['topleft']})
        
    def Close(self):
        print 'Disconnection from: %s - %s' % (self.name, str(self.addr))
        self._server.send_all({'action': 'logout',
                               'name': self.name})
        
    
class RelayServer(Server):
    channelClass = ClientChannel
    
    def Connected(self, channel, addr):
        print 'Connection from: %s' % (str(addr))
    
    def send_all(self, data):
        for c in self.channels:
            c.Send(data)


s = RelayServer(localaddr=('localhost', 8888))
while True:
    s.Pump()
    sleep(0.05)
