import json
from network import Listener, Handler, poll
import sqlite3
from random import randint

HOST_NAME = 'localhost'  
PORT_NUMBER = 8888
SALT = 'secret salt'

db_conn = sqlite3.connect('whale.sqlite3')
db_cur = db_conn.cursor()
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS players
    (url TEXT, name TEXT, x INT, y INT, size INT, PRIMARY KEY (url, name));
    ''')
# TODO: also add an expiration timestamp
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS pellets 
    (id INTEGER PRIMARY KEY, x INT, y INT, size INT);
    ''')
for pellet_id in range(4):
    try:
        db_cur.execute('''
            INSERT OR ABORT INTO pellets VALUES (?, ?, ?, ?);
            ''', (pellet_id, randint(10, 380), randint(10, 280), 5))
    except sqlite3.IntegrityError:  # primary key conflict: row already exists
        pass
db_conn.commit()


class MyHandler(Handler):
    
    def on_msg(self, req):
        method = req['method']
        resource = req['resource']
        args = req['args']
        if (method, resource) == ('GET', '/game/1'):
            repr = {'borders': {'link': '/borders'},
                    'pellets': {'link': '/pellets'},
                    'players': {'link': '/players'}
                    }
            if 'name' in args:  # TODO: how do clients know to submit their name?
                name = args['name']  # TODO: also add password/token detection
                players = db_cur.execute('''
                    SELECT name, url FROM players
                    ''').fetchall()
                name2url = {p[0]: p[1] for p in players}
                if name in name2url:
                    url = name2url[name]
                else:
                    url = '/player/' + str(hash(name + SALT))
                    db_cur.execute('''
                        INSERT INTO players(url, name, x, y, size) 
                        VALUES (?, ?, ?, ?, ?);
                        ''', (url, name, 150, 150, 10))
                    db_conn.commit()
                repr['you'] = {'form': {'method': 'POST',
                                        'url': url,
                                        'args': ['dir']}
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
            pellets = db_cur.execute('''
                SELECT x, y, size FROM pellets;
                ''').fetchall()
            repr = [ [p[0], p[1], p[2], p[2]] for p in pellets]
            response = {'resource': resource,
                        'type': 'app/boxlist+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/players'):
            # players always change, fetch them from DB
            players = db_cur.execute('SELECT name, x, y, size, url FROM players;').fetchall()
            box_dict = { p[0]: [p[1], p[2], p[3], p[3]] for p in players}
            response = {'resource': resource,
                        'type': 'app/boxdict+json',
                        'representation': box_dict
                        }
        elif method == 'POST' and resource.startswith('/player/'):
            if 'dir' in args:
                d = args['dir']
                input_map = {'up': (0, -1), 'down': (0, 1),
                             'left': (-1, 0), 'right': (1, 0)}
                dx, dy = input_map[d]
                # TODO: detect collisions with borders, pellets, and players
                db_cur.execute('''
                    UPDATE players SET x = x + ?, y = y + ? WHERE url = ?;
                    ''', (dx, dy, resource))
            p = db_cur.execute('''
                SELECT name, x, y, size, url FROM players WHERE url = ?;
                ''', (resource,)).fetchone()
            box_dict = { p[0]: [p[1], p[2], p[3], p[3]]}
            response = {'resource': resource,
                        'type': 'app/boxdict+json',
                        'representation': box_dict
                        }
        else:  # invalid resource 
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
