"""
REST constraints: 
- client-server, 
- layered, 
- stateless interactions: client stores app state, server stores resource state,
- uniform interface, 
- caching (optional), 
- code on demand (optional).

See:
http://stackoverflow.com/a/671132/856897
http://roy.gbiv.com/talks/200804_REST_ApacheCon.pdf

Uniform interface can be broken down into the following constraints:
- Each resource (= information) has one name: its URI.
- Resource-generic interaction semantics (same verbs work on all resources)
- Manipulate resources through their representations.
- Hypermedia as the engine of application state: need links between resources,
and the application must have distinct states.

JSON is nice, but:
- it is only a container format (like XML), not a media type with semantics,
- as a format, it does not support links (yet). 
https://www.mnot.net/blog/2011/11/25/linking_in_json

TODO: also provide XML or HTML representations (not just JSON).
TODO: make an HTTP version instead of TCP

# Request: resource and method are mandatory
request = {'resource': '/resource_name',
           'method': 'CREATE/READ/UPDATE/DELETE',
           'args': {'a': 5}
           }
# Response: resource, mtype,  are mandatory
response = {'resource': '/resource_name',
            'mtype': 'application/prs.players+json',
            'representation': {'data': {},
                               'links': {'next': 'URI',
                                         'parent': 'URI'
                                          },
                              },
            'options': {'last_modified': 1401729651, # timestamp
                        },
            }
    
    
"""
 
import json
import sqlite3
import uuid
from network import Listener, Handler, poll
import time

HOST_NAME = 'localhost'  
PORT_NUMBER = 8888

db_conn = sqlite3.connect('whale.sqlite3')
db_cur = db_conn.cursor()
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS players
    (name TEXT PRIMARY KEY, x REAL, y REAL, size REAL)
    ''')
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS pellets 
    (id INT PRIMARY KEY, x REAL, y REAL, size REAL)
    ''')
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS tokens 
    (token TEXT PRIMARY KEY, uri TEXT, timestamp INT)
    ''')
db_conn.commit()
     

class MyHandler(Handler):
    
    def on_msg(self, req):
        method = req['method']
        resource = req['resource']
        mr = method, resource
        # default response
        response = {'rsrc': resource,
                    'meta': {'type': 'text/plain'},
                    'repr': 'wrong resource or method.\nGo to /'
                    }
        
        if mr == ('GET', '/'):
            repr = {'next': '/borders',
                     'auth': '/token',
                     'data': []
                     }
            response = {'rsrc': resource,
                        'meta': {'type': 'app/game+json'},
                        'repr': repr
                        }
        if mr == ('GET', '/token'):
            token = str(uuid.uuid4())
            uri = '/player/' + token
            timestamp = int(time.time())  # seconds since 1970
            db_cur.execute('INSERT INTO tokens VALUES (?, ?, ?)',
                           (token, uri, timestamp))
            db_conn.commit()
            
            repr = token
            response = {'rsrc': resource,
                        'meta': {'type': 'text/plain'},
                        'repr': repr 
                        }
                
        
        self.do_send(response)

    
    
        
if __name__ == '__main__':
    server = Listener(8888, MyHandler)
    try:
        while 1:
            poll()
    except KeyboardInterrupt:
        db_conn.close()    
