# DDoS protection

WP Cloud uses edge routing, traffic classification, rate limiting, and network-level mitigation to protect sites from denial-of-service and distributed denial-of-service (DDoS) attacks. These protections operate at the platform level without requiring a site administrator to enable them.

## How WP Cloud handles DDoS traffic

Inbound requests use an Anycast range of IP addresses. Anycast connects a visitor to a nearby WP Cloud edge data center and limits direct exposure of origin server addresses.

At the edge, an NGINX load balancer decides whether to serve an eligible response from [Edge Cache](/docs/performance/cache/edge-cache/) or send the request to the site's origin. WP Cloud can also change how traffic is routed when demand changes. This edge layer filters and distributes traffic before it reaches WordPress.

Most sites can absorb a large increase in traffic without any manual action. Traffic classification, [rate limiting](/docs/security/traffic-protection/rate-limiting/), and Edge Cache increase the amount of unwanted or repeated traffic the platform can handle. A dedicated WP Cloud team monitors the network, responds to alerts, and adjusts platform resources and DDoS mitigations when needed.

## Add a browser challenge when needed

[Defensive Mode](/docs/security/traffic-protection/defensive-mode/) provides an additional on-demand challenge during a suspected bot or DDoS event. It can reduce automated requests that are still reaching the site or using PHP resources.

## Avoid third-party proxying when possible

Enable Edge Cache and send traffic directly to WP Cloud whenever possible. A third-party proxy can hide request information that WP Cloud uses for traffic classification and DDoS mitigation. It can also prevent visitors from connecting directly to the nearest WP Cloud edge data center.

If Cloudflare proxying is required, follow the [recommended Cloudflare configuration](/docs/sites/domains/cloudflare/).
