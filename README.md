Requirements
-----

- Python 2.7
- Pygame 1.9.1 or 1.9.2: Windows installer on pygame.org, or `sudo apt-get install python-pygame` on Ubuntu
- network.py is in the directory above the code of the examples. You may have to add the project directory to your python path to be able to import network.py.


How to
----

Run `python whale.py` for the solo version.

Run `python server.py` in one terminal and `python client.py` in another for client-server (the server listens on port 8888).

Run `python directory.py` in one terminal and `python peer.py` in another for peer-to-peer (the directory server listens on 8888, the peers listen on a random port between 20k and 30k).


Similar works
----

- 99 literary styles in Exercises in Style, Queneau
- 207 interpretations and appearances of Catalan Numbers, Stanley, http://www-math.mit.edu/~rstan/ec/
- Exercises in Programming Styles, Lopes


Backlog
----

- p2p with lockstep
- p2p with one pellet owner, others have copies: one "host"
- p2p with rollback
- spatial pubsub
- RPC
- SOA: game vs chat service?
- operational transform (between N clients and 1 server)
- reverse proxy to load-balance 
- redirect asset requests to CDN (intermediaries are easy to add in REST)
- stream assets vs fat client
- plugin
- blackboard
- sense compute control (avionics)
- replication of data vs computation, Paxos, virtual synchrony
- CAP, NOSQL, ACID, BASE
- SOA vs service bus vs central repository vs linked data 
- grid vs cloud
- CRUD (easy to add in RPC?)

AI (make whale bots?)
- sense plan act
- subsumption
- hFSM
- robotic architectures

Security
- authentication
- access control
- injections
- impersonation

Messaging/MEP
- fire and forget
- asynchronous
- request-response
- context-free
