Constraints:
---
- Client-server
- Stateless
- Layered
- Caching
- Code-on-demand (optional)
- Uniform interface

Uniform interface can be broken down into interface-specific sub-constraints:
- Identification of resources
- Manipulation of resources through representations
- Self-descriptive messages
- Hypermedia as the engine of application state


History:
---
Before 1994, the architecture of the Web was client-server stateless with cache. http://www.sciencedirect.com/science/article/pii/016975529290039S

REST is a reverse-engineering of the architecture of the Web as it was in the late 90s: mostly about Web pages. At the time, the 3 pillars of the Web were HTML (a text format containing links; used to write Web pages), HTTP (a protocol to transfer HTML), and URL (a location/identifier scheme for Web pages). REST-TCP is an effort to write an application following the REST style, but replacing HTML by custom media types, and HTTP by TCP.


Hypermedia
---

Hypermedia as the engine of application state: the representation of a resource provides a way for the client to transition between application states.
Some features of HTML illustrate its hypermedia nature.

In the <head> of the HTML document, <link rel="alternate" type="xml" href="/files/backup/article6.xml"> provides a link to an alternate version of the current document (e.g. XML instead of HTML).

Also in <head>, <link rel="stylesheet" href="main.css"> is a rendering suggestion for the current Web page.

In <body>, <a rel="next/prev/prefetch" href="/article/6"> provides transitions between steady-states (e.g. from /article/5 to /article/6).

Also in <body>, <form method="get/post" action="/articles">name: <input type="text" name="FirstName" value="Mickey"> <input type="submit" value="Submit"> </form> tells the client that submitting this form will trigger a get/post on the URL /articles. The browser understands that it will have to URL-encode the argument(s) and value(s) into /articles?FirstName=Mickey