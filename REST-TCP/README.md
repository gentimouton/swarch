Constraints:
---
- Client-server
- Stateless
- Layered
- Caching
- Code-on-demand (optional)
- Uniform interface

Uniform interface can be broken down into interface-specific sub-constraints:
- Identification of resources. A resource is any named information, aka the content as in form-and-content, aka the conceptual data. In the case of the Web, the identifier of a resource is its URL. 
- Manipulation of resources through their representations, ie separate presentation from content. A client may request a particular format from the server (using the HTTP accept header of JSON, XML, text, etc) for a given resource (e.g. /article/5), but the server may not always be able to deliver that representation (HTTP error code 406).
- Hypermedia as the engine of application state: the representation (HTML) provides links to accompanying representations (e.g. <img src="photo.jpg">, <link rel="stylesheet" href="main.css">), links to other states (<a href="/article/6">), or controls to transition to other states (<form method="get/post" action="/articles">name: <input type="text" name="FirstName" value="Mickey"> <input type="submit" value="Submit"> </form> The browser understands that it will have to URL-encode the argument(s) and value(s) into /articles?FirstName=Mickey). Gains: rel=prefetch improves user-perceived latency, can cache images
- Universal interaction semantics: the same methods work on all resources. HTTP GET, POST, PUT, etc. can be applied on any URL with no surprises.
- Self-descriptive messages: enables intermediaries (= layers) to cache, filter, or do any processing they want on the messages. This requires that all layers understand a standard protocol (HTTP). Responses can explicitly indicate cacheability.

History:
---
Before 1994, the architecture of the Web was client-server stateless with cache. http://www.sciencedirect.com/science/article/pii/016975529290039S

REST is a reverse-engineering of the architecture of the Web as it was in the late 90s: mostly about Web pages. At the time, the 3 pillars of the Web were HTML (a text format containing links; used to write Web pages), HTTP (a protocol to transfer HTML), and URL (a location/identifier scheme for Web pages). REST-TCP is an effort to write an application following the REST style, but replacing HTML by custom media types, and HTTP by TCP.


See also
----

http://stackoverflow.com/a/671132/856897
http://roy.gbiv.com/talks/200804_REST_ApacheCon.pdf

JSON is nice, but:
- it is only a container format (like XML), not a media type with semantics,
- as a format, it has no standard for links (yet). 
https://www.mnot.net/blog/2011/11/25/linking_in_json

Misc
---

If an API is RESTful, then:
- it has clear app states (e.g. game modes, rooms, or levels).
- it is crawlable (hypermedia constraint)
- back button works, and brings the client to a valid state

For games, what is a valid app state? 
- /game/1, /game/2, /lobby, /help
- game modes: inventory, social, or crafting tabs. If modes are overlayed on top of main game, their HTML equivalent is an <iframe>.
- the whole game state, as in the coordinates and HP of each player, is not a valid app state. Let's take the example of a 2-player Chess game. Both Black and White can GET /state/1, and White can POST on /state/1. If either GETs /state/2, they will receive 404: **future game states do not exist yet**. It's only after White POSTs that /state/2 would be created. Black only knows it should now GET /state/2 because it receives a REDIRECT from /state/1 to /state/2. White or Black can't POST on /state/1 because **past states are invalid**. So really, it's the same as if Black and White were GETting a resource called /state, and changing it every turn. Thus the whole Chess game state is a resource in itself. It is not a good candidate for an application state.


