# Automated failover

Every WP Cloud site has primary and secondary origin servers in different
geographic data centers. Real-time replication keeps the servers synchronized
so WP Cloud can redirect traffic when the primary server or its data center is
unavailable.

## Real-time replication

The primary and secondary servers mirror one another. They run the same
software and contain synchronized data for every site assigned to the server
pool. WP Cloud continuously replicates data from the primary to the secondary
in real time.

Keeping the copies in different geographic data centers protects sites from a
localized infrastructure failure or natural disaster affecting one location.

## Monitoring and traffic failover

WP Cloud continuously monitors the primary server for failures and degraded
performance. When monitoring detects a problem, WP Cloud systems assess
whether traffic must move to the secondary server.

When failover is necessary, WP Cloud immediately redirects traffic to the
secondary server in another geographic data center. A failover can change the
site's active origin location and outbound address, so integrations must not
assume those values are permanent.

After WP Cloud restores the primary server, traffic automatically returns to
it.

## Graceful failover for cached pages

Graceful failover is separate from origin server and data-center failover. If
a plugin, theme, or code error makes an origin return an HTTP 5xx response, a
site using [Edge Cache](/docs/performance/cache/edge-cache/) may serve a cached
version of the page instead.

Graceful failover can keep an already cached page available, but it does not
repair the origin error or provide a cached response for content that was not
already eligible and stored.
