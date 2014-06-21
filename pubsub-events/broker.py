"""
Nodes subscribe to some types of events and publish events as well.
Event types: move, grow, place pellet, state request, state response.
Broker delivers an event to a node if that node subscribed to this event type.
"""
from network import poll, Listener, Handler


subs = {}  # map subscription to handlers 

class MyHandler(Handler):
    
    def on_msg(self, data):
        mtype, mdata = data
        if mtype == '_sub':  # reserved mtype
            if mdata not in subs:
                subs[mdata] = set()
            subs[mdata].add(self)
        elif mtype == '_unsub' and mdata in subs:  # reserved mtype
            subs[mdata].remove(self)
        elif mtype in subs:  # non-reserved mtypes are for publishing
            [h.do_send((mtype, mdata)) for h in subs[mtype]]
    
Listener(8888, MyHandler)

while 1:
    poll(timeout=.1)  # seconds
