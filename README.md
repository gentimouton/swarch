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

Software architecture works with surveys of architectural styles:
- Design and use of software architectures, by Jan Bosch. Looks at pipe and filter, layers, blackboard, OO, and implicit invocation. Framework: performance, maintainability, reliability, safety, and security.
- Software architecture, by Taylor et al. Same as Bosch + call and return (main and subroutines), virtual machines, client-server, batch, rule-based, interpreter, mobile code, and pub-sub. Framework: summary, components, connectors, data elements, topology, additional constraints imposed, qualities yielded, typical uses, cautions, and relations to programming languages or environments.
- Software architecture, by Shaw and Garlan.


Backlog
----

- turn-based (A's turn, sends his move, then B's turn, then C joins and is added to the end of the player list after B, then B sends his move, then C's turn, then A's turn, ...)
- p2p with lockstep (sync vs async)
- p2p with one pellet owner, others have copies: one "host"
- p2p with rollback
- p2p a la Chord
- p2p with vector clocks/Lamport
- p2p with mesh/arbitrary graph
- p2p with NAT punching/surrogate, like Semigod
- p2p with superpeers, like Skype
- pubsub without broker: each node maintains a list of subscriptions (DSG sort of does that)
- timewarp
- spatial pubsubs: static, dynamic BSP, dynamic Voronoi (Pikko), DSG (operational partitioning: physics vs script vs client manager)
- RPC
- one server for live actions, one server for storage, like Realm of the Mad God (or like DSG's persistence actor vs script actor, except in DSG, clients connect to a client manager, whereas in RotMG, they send messages directly to both servers)
- SOA: game vs chat service?
- operational transform (between N clients and 1 server, or p2p)
- reverse proxy to load-balance 
- redirect asset requests to CDN (intermediaries are easy to add in REST)
- stream assets vs fat client
- clients pull updates vs server pushes updates
- plugin
- blackboard
- sense compute control (avionics)
- replication of data vs computation, Paxos, virtual synchrony
- CAP, NOSQL, ACID, BASE
- shared disk (ie servers share same DB) vs shared nothing (each server has its own DB)
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
