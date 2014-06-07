import json
from network import Listener, Handler, poll
import sqlite3
import uuid


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
            response = {'type': 'app/game+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/borders'):
            # borders are static, can be cached, no need to store them in DB
            repr = [ [0, 0, 2, 300], [0, 0, 400, 2],
                    [398, 0, 2, 300], [0, 298, 400, 2] ]
            response = {'type': 'app/boxlist+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/pellets'):
            # pellets may change, fetch them from DB
            pellets = db_cur.execute('SELECT * FROM pellets').fetchall()
            repr = [ [p.x, p.y, p.size, p.size] for p in pellets]
            response = {'type': 'app/boxlist+json',
                        'representation': repr
                        }
        else:
            response = {'type': 'text/plain',
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
