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


References
===

inf123
https://github.com/gentimouton/swarch
http://en.wikipedia.org/wiki/Distributed_data_flow
http://en.wikipedia.org/wiki/Software_architecture_styles_and_patterns
http://en.wikipedia.org/wiki/Architectural_pattern_(computer_science)
http://en.wikipedia.org/wiki/Architectural_style#Examples_of_styles
http://en.wikipedia.org/wiki/Category:Distributed_computing_architecture
https://github.com/crista/exercises-in-programming-style
https://grape.ics.uci.edu/wiki/asterix/wiki/cs222-2014-winter
http://www.ics.uci.edu/~lopes/teaching/inf123S10/
https://github.com/gentimouton/swarch/wiki/todo
http://www.pygame.org/project-bitSnake-2158-.html
http://code.google.com/p/podsixnet/source/browse/podsixnet/examples/ChatServer.py
http://stackoverflow.com/questions/18196745/how-to-re-establish-asyncore-connection-with-server-solved
http://stackoverflow.com/questions/18280571/python-asyncore-not-keeping-up-with-high-data-rates?rq=1
http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7
http://www.softwarearchitecturebook.com/svn/main/slides/ppt/
http://sourceforge.net/p/pyrogue/code/HEAD/tree/trunk/
http://sourceforge.net/projects/pyunicurses/files/unicurses-1.2/
http://effbot.org/zone/console-handbook.htm
http://urwid.org/
http://www.npcole.com/npyscreen/
https://github.com/gentimouton/INF123-example-repo-for-assignments
http://www.cs.berkeley.edu/~brewer/cs262/
http://pcsupport.about.com/od/commandlinereference/p/netstat-command.htm
https://eee.uci.edu/toolbox/messageboard/m15623/
http://www.pygame.org/wiki/CookBook
https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor
http://www.ferg.org/thinking_in_tkinter/all_programs.html
http://se.inf.ethz.ch/courses/2011a_spring/soft_arch/
http://roy.gbiv.com/talks/webarch_9805/sld011.htm
http://www.ics.uci.edu/~fielding/pubs/dissertation/net_arch_styles.htm
REST
http://blueprintforge.com/blog/2012/01/01/a-short-explanation-of-hypermedia-controls-in-restful-services/
http://www.slideshare.net/alan.dean/separating-rest-facts-from-fallacies-presentation
http://tools.ietf.org/wg/httpbis/
http://www.looah.com/source/view/2284
http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
http://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven
http://roy.gbiv.com/talks/200804_REST_ApacheCon.pdf
http://restcookbook.com/HTTP%20Methods/put-vs-post/
http://stackoverflow.com/questions/671118/what-exactly-is-restful-programming?rq=1
https://github.com/kevinswiber/siren
http://stateless.co/hal_specification.html
http://stackoverflow.com/questions/16066987/why-do-we-need-a-custom-media-type-when-using-hypermedia-links
http://www.w3schools.com/html/tryit.asp?filename=tryhtml_form_submit
http://www.ianbicking.org/blog/2008/10/hypertext-driven-urls.html
https://kenai.com/projects/suncloudapis/pages/Home
https://blogs.oracle.com/craigmcc/entry/why_hateoas
http://ruben.verborgh.org/phd/hypermedia/
http://thisweekinrest.wordpress.com/
http://ivanzuzak.info/2010/04/03/why-understanding-rest-is-hard-and-what-we-should-do-about-it-systematization-models-and-terminology-for-rest.html#par28
http://www.bjoernrochel.de/2012/10/16/the-pain-of-a-non-hypermedia-http-api/
https://www.mnot.net/blog/2011/11/25/linking_in_json
http://stateless.co/hal_specification.html
http://amundsen.com/media-types/collection/examples/#ex-item
