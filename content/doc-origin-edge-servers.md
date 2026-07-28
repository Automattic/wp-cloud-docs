# Origin and edge servers

WP Cloud uses origin servers to run WordPress and produce uncached responses,
and edge servers to receive requests and serve eligible cached responses near
visitors. A site's origin location does not determine the DNS address or edge
location that a visitor reaches.

## Origin servers

WP Cloud maintains origin data centers in several regions. The origin server
holds the current state of a site's content, settings, database, and files. A
partner can request a preferred origin region when creating a site.

Each origin server is self-sufficient: NGINX, PHP, the site's document root
and files, MariaDB, the site's database, and Memcached all run on the server.
Keeping these services together avoids adding a remote service call to every
uncached WordPress request.

When [Edge Cache](/docs/performance/cache/edge-cache/) already has an eligible
response, the edge can return it without contacting the origin. Requests that
are not served at the edge continue to the origin. [Page
Cache](/docs/performance/cache/page-cache/) can return a cached full-page
response from the origin without running WordPress again. If Page Cache misses
or the request bypasses it, WordPress generates a new response.

Page Cache and Edge Cache are separate layers, but Page Cache behavior affects
Edge Cache. Page Cache lifetime and bypass rules influence which responses can
be stored at the edge and how long those responses remain eligible. An
eligible origin response can be cached for later requests at both layers.

[Web server logs](/docs/monitoring-logs/logs/web-server-logs/) and
[Metrics](/docs/monitoring-logs/metrics/) describe requests that reach
the origin, their duration, resource use, and Page Cache behavior. Requests
served entirely by Edge Cache are represented in Metrics rather than normal
origin web server logs.

## Edge servers

WP Cloud's edge network accepts inbound traffic close to the requester. Each
edge location uses a load balancer to decide whether to return an Edge Cache
response or route the request to the site's origin data center. An origin data
center can also act as an edge location for sites whose origin is elsewhere.

All inbound requests use [Anycast](https://en.wikipedia.org/wiki/Anycast)
routing. The address published in DNS does not identify the site's physical
origin or the server's address; the network routes the request to an
appropriate edge location first.

## Choose an origin region

The `geo_affinity` field on the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}) requests the preferred origin region. WP Cloud assigns the site's primary pool server in that region when the requested location is available.

Use the [Get Available Datacenters endpoint](https://wp.cloud/docs/api/#tag/servers/GET/get-available-datacenters/{client}) to retrieve the currently allowed values. The available origin codes include:

- `ams` — Amsterdam
- `bur` — Los Angeles
- `dca` — Ashburn
- `dfw` — Dallas

The origin preference cannot be changed on the existing site after creation.
To place the site in another origin region, [clone the site](/docs/sites/cloning/)
and select the new `geo_affinity` value during creation. [Automated
failover](/docs/infrastructure/automated-failover/) can also move the active
origin temporarily. WP Cloud may also relocate sites between server pools to
replace hardware, balance resource use, or improve performance, so partners
should not treat a specific origin server or data center as permanent.

## Server locations

The WP Cloud network includes the following origin and edge locations. Network
capacity and available locations can change; use the API for the current
origin choices rather than treating this table as the allowed
`geo_affinity` list.

| City | Code | Role |
| --- | --- | --- |
| Amsterdam | `AMS` | Origin and edge |
| Ashburn | `DCA` | Origin and edge |
| Atlanta | `ATL` | Edge |
| Chicago | `MDW` | Edge |
| Dallas | `DFW` | Origin and edge |
| Denver | `DEN` | Edge |
| Frankfurt | `HHN` | Edge |
| Hong Kong | `HKG` | Edge |
| Johannesburg | `JNB` | Edge |
| London | `LHR` | Edge |
| Los Angeles | `BUR` | Origin and edge |
| Madrid | `MAD` | Edge |
| Miami | `MIA` | Edge |
| Milan | `MXP` | Edge |
| Mumbai | `BOM` | Edge |
| New Jersey | `EWR` | Edge |
| New York | `JFK` | Edge |
| Osaka | `KIX` | Edge |
| Paris | `CDG` | Edge |
| San Jose | `SJC` | Edge |
| Santiago | `SCL` | Edge |
| São Paulo | `GRU` | Edge |
| Seattle | `SEA` | Edge |
| Singapore | `SIN` | Edge |
| Stockholm | `ARN` | Edge |
| Sydney | `SYD` | Edge |
| Tokyo | `NRT` | Edge |
| Toronto | `YYZ` | Edge |
| Vienna | `VIE` | Edge |

## Data location and failover

WP Cloud can store site data on servers in both the United States and the
European Union. Because the redundant copy used for automated failover is in a
different region, a partner cannot restrict all data associated with a site to
one geographic location through `geo_affinity`.
