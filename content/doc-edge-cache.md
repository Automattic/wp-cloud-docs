# Edge Cache

Edge Cache is WP Cloud's content delivery network (CDN). Its global network of
edge servers stores page and static responses closer to visitors. In some
locations, an origin server can also serve cached content for sites hosted in
another location. A cached response avoids a trip to the site's origin, which
can reduce time to first byte (TTFB) and origin resource use.

Edge Cache is one layer of WP Cloud's caching system. It works with [Page
Cache](/docs/performance/cache/page-cache/) at the WordPress origin, but each
edge location maintains its own cache. A response can therefore be cached at
one location and missing or stale at another.

## How Edge Cache works

When a request reaches an edge data center, its load balancer decides whether
to serve a cached response or send the request to the origin. A cache miss goes
to the origin so WordPress can produce the response. The edge can then store an
eligible response for later requests.

Edge Cache uses the [Page Cache](/docs/performance/cache/page-cache/) time to
live (TTL). Extending the Page Cache TTL also allows Edge Cache to serve a
response for longer. Because edge locations populate independently, a newly
enabled or recently purged site may need several requests at a location before
it returns a cache hit.

Like Page Cache, Edge Cache is designed to avoid caching requests that need a
dynamic response. This includes logged-in WordPress sessions and dynamic
ecommerce requests such as carts and checkouts.

Serving cached responses from the edge can:

- Reduce the distance requests travel, improving page-load time and TTFB for
  visitors and contributing to better Core Web Vitals.
- Reduce PHP and database work at the origin.
- Provide graceful failover for eligible cached responses when the origin is
  slow or temporarily unavailable.
- Absorb more repeat traffic without sending every request to WordPress.

## Prevent specific pages from being cached at the edge

Send the following response header when a specific page must not be stored in
Edge Cache:

```text
A8C-Edge-Cache: no-cache
```

Use this header when a public URL produces different content based on a cookie
or another value that Edge Cache does not include in its cache key. Edge Cache
does not create arbitrary cache variants from application cookies or the
`Vary` response header. A request header such as `Cache-Control: no-cache` is
not a substitute for the `A8C-Edge-Cache` response header.

The header bypasses only Edge Cache. [Page
Cache](/docs/performance/cache/page-cache/) can still serve the response at the
origin when it is configured to cache each variation safely. The header does
not configure Page Cache or create separate cache entries for different cookie
values.

Limit the header to the affected pages so other eligible responses retain the
performance and availability benefits of Edge Cache. After adding the header,
purge existing edge entries for those URLs. Then verify that each page variant
remains correct after refresh and navigation and that the final `x-ac` result
is not an Edge Cache hit.

## Manage Edge Cache

WP Cloud provides three management methods: the WP Admin interface installed
by the Edge Cache must-use plugin (`mu-plugin`), the WP Cloud API, and WP-CLI.
The available method depends on the access a partner gives its developers,
support teams, and customers.

### WP Admin

The Edge Cache plugin adds **Settings > Edge Cache** in WP Admin. Its direct
path is `/wp-admin/options-general.php?page=edge-cache`. The interface shows
the current state and provides controls for enabling, disabling, and clearing
Edge Cache.

### WP Cloud API

Use the [Get Edge Cache Settings endpoint](https://wp.cloud/docs/api/#tag/edge-cache/GET/edge-cache/{site})
to retrieve a site's setting. The response uses the states `Disabled`,
`Enabled`, and `DDoS`.

Use the [Update Edge Cache Settings endpoint](https://wp.cloud/docs/api/#tag/edge-cache/POST/edge-cache/{site}/{action})
to turn Edge Cache on or off or to purge cached responses. A purge can cover
the entire domain or a set of URIs supplied in `purge_uris`. Use the
domain-specific endpoint variant when the operation applies to a domain other
than the site's primary domain.

The API response confirms the settings request. It does not prove that a
particular response is present in cache or that a later request was a cache
hit. Use the response-header check in [Verify Edge Cache](#verify-edge-cache)
for that distinction.

### WP-CLI

Run `wp edge-cache` to see the complete command usage installed on the site:

```text
wp edge-cache
usage: wp edge-cache defensive-mode [--time=<time>] [--end]
   or: wp edge-cache disable
   or: wp edge-cache enable
   or: wp edge-cache purge [<urls>...] [--domain] [--yes]
   or: wp edge-cache status
```

The `defensive-mode` subcommand controls Defensive Mode rather than normal
cache behavior. See [Defensive
Mode](/docs/security/traffic-protection/defensive-mode/) for its time values,
ending the mode, and checking its state.

The purge command accepts one or more URLs or the `--domain` option:

```bash
wp edge-cache purge "https://example.com/path" "https://example.com/path?key=value"
wp edge-cache purge --domain
```

WP-CLI also provides the general `wp cache flush` command. Use the Edge Cache
command when you need the edge-specific purge options shown above.

Use a targeted purge when only a small set of responses changed. Purging the
whole domain discards more cached responses and sends more subsequent requests
to the origin while the cache repopulates.

## Automatic and manual invalidation

The Edge Cache plugin clears [Page
Cache](/docs/performance/cache/page-cache/) and purges Edge Cache when
WordPress content changes through supported events. These include:

- Switching a theme or saving Customizer changes.
- Deleting an attachment or post.
- Changing a post or comment status.
- Creating a comment.
- Updating a post.
- Clearing a term cache.
- Changing WooCommerce Coming Soon mode.

The underlying WordPress events include `switch_theme`,
`customize_save_after`, `delete_attachment`, `deleted_post`,
`transition_post_status`, `comment_post`, `transition_comment_status`,
`post_updated`, and `clear_term_cache`.

You can also invalidate Edge Cache from **Settings > Edge Cache**, with the
WP-CLI purge command, or through the WP Cloud API. An automatic invalidation or
manual clear flushes the site's Page Cache as well as Edge Cache. The plugin
performs the Page Cache flush through `$batcache->flush()`.

## Verify Edge Cache

Check the `x-ac` response header while logged out of WordPress. You can inspect
the header in browser developer tools or make a request from a terminal:

```bash
curl -LI https://example.com/
```

The final token in the header describes what happened for that request. For
example:

```text
x-ac: 3.vie _atomic_dca HIT
x-ac: 2.den _atomic_dfw BYPASS
x-ac: 1.ewr _atomic_dca MISS
x-ac: 1.atl _atomic_dca STALE
```

The possible cache results are:

- **HIT:** Edge Cache served the response.
- **STALE:** Edge Cache served a stale response while it revalidated the
  cached item.
- **EXPIRED:** Edge Cache found an item past its TTL, returned it, and removed
  it from cache.
- **UPDATING:** Another request is refreshing the item from the origin while a
  lock prevents several requests from doing the same work.
- **MISS:** Edge Cache did not have a usable response at that location. The
  response may not be eligible for Page Cache, or the edge location may not
  have received enough requests to populate it.
- **BYPASS:** Edge Cache is disabled for the request or the request belongs to
  a logged-in WordPress administrator.

`HIT`, `STALE`, `EXPIRED`, `UPDATING`, and `MISS` indicate that Edge Cache is
enabled. `BYPASS` can mean that Edge Cache is disabled, but it can also be the
expected result for a logged-in session. Test from a logged-out browser or a
terminal before treating `BYPASS` as a configuration problem.

The settings endpoint and response header answer different questions: the
endpoint reports the configured state, while `x-ac` reports what happened to
one request at one edge location.

## Troubleshoot Edge Cache

If a logged-out request does not return the expected `x-ac` result, first check
whether the request is eligible for [Page
Cache](/docs/performance/cache/page-cache/). A new or recently purged edge
location may also need several requests before it returns a hit.

Use [Troubleshoot Page and Edge
Cache](/docs/troubleshooting/page-edge-cache/) for cache misses, bypasses,
cookies or response headers that prevent caching, and errors from the Edge
Cache plugin. Keep using the response-header checks in this article to identify
which cache layer handled the request.

## Logging and cache lifetime

Requests served by Edge Cache do not reach the origin and are not included in
origin web server logs. The [Time Series Metrics
endpoint](https://wp.cloud/docs/api/#tag/metrics/POST/metrics/{type}/{key})
includes edge request data such as `edge_cache_hit_percentage`,
`edge_cache_miss_percentage`, and the `edge_cache_status` dimension. Use those
metrics to review cache ratios and changes over time. Use the `x-ac` response
header when you need to confirm how an individual request was handled.

Edge Cache follows the [Page Cache](/docs/performance/cache/page-cache/) TTL.
Change that TTL through the supported Page Cache configuration rather than
treating Edge Cache as an independent lifetime setting.
