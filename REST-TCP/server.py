import json
from network import Listener, Handler, poll
import sqlite3
import uuid
from random import randint

HOST_NAME = 'localhost'  
PORT_NUMBER = 8888

db_conn = sqlite3.connect('whale.sqlite3')
db_cur = db_conn.cursor()
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS players
    (name TEXT PRIMARY KEY, x INT, y INT, size INT);
    ''')
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS pellets 
    (id INTEGER PRIMARY KEY, x INT, y INT, size INT);
    ''')
for pellet_id in range(4):
    try:
        db_cur.execute('''
            INSERT OR ABORT INTO pellets 
            VALUES (?, ?, ?, ?);
            ''', (pellet_id, randint(10, 380), randint(10, 280), 5))
    except sqlite3.IntegrityError: # primary key conflict: row already exists
        pass
db_conn.commit()
     

class MyHandler(Handler):
    
    def on_msg(self, req):
        method = req['method']
        resource = req['resource']
        args = req['args']
        if (method, resource) == ('GET', '/game/1'):
            if 'name' in args:
                name = args['name']
            else:
                name = str(uuid.uuid4())[:8]
            repr = {'name': {'data': name},
                    'borders': {'link': '/borders'},
                    'pellets': {'link': '/pellets'},
                    'players': {'link': '/players'}
                    }
            response = {'resource': resource,
                        'type': 'app/game+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/borders'):
            # borders are static, can be cached, no need to store them in DB
            repr = [ [0, 0, 2, 300], [0, 0, 400, 2],
                    [398, 0, 2, 300], [0, 298, 400, 2] ]
            response = {'resource': resource,
                        'type': 'app/boxlist+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/pellets'):
            # pellets may change, fetch them from DB
            pellets = db_cur.execute('SELECT * FROM pellets').fetchall()
            repr = [ [p[1], p[2], p[3], p[3]] for p in pellets]
            response = {'resource': resource,
                        'type': 'app/boxlist+json',
                        'representation': repr
                        }
        else:
            response = {'resource': resource,
                        'type': 'text/plain',
                        'representation': 'wrong resource or method.\nGo to /'
                        }
        
        self.do_send(response)

    
    
        
if __name__ == '__main__':
    server = Listener(8888, MyHandler)
    try:
        while 1:
            poll()
    except KeyboardInterrupt:
        db_conn.close()    
