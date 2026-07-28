# Decoupled and headless WordPress

WP Cloud can serve WordPress as the content management system for a decoupled
frontend. This guide focuses on WPGraphQL with applications built using
Next.js or Nuxt. Other headless architectures can work, but their request and
caching behavior may differ.

The frontend's build strategy matters to the WordPress origin. Large bursts of
uncached API requests can consume PHP workers or encounter [rate
limiting](/docs/security/traffic-protection/rate-limiting/), even when the visitor-facing site is
static.

## Use the standard WPGraphQL endpoint

[WPGraphQL](https://www.wpgraphql.com/) provides a GraphQL API for WordPress.
WP Cloud requires the plugin's standard `/graphql` endpoint for optimal
performance. Alternative routes may not receive the same platform handling
and can be rate limited during a build.

An HTTP 429 response during a build indicates that requests are being rate
limited. Confirm that the frontend uses `/graphql`, then reduce concurrent and
repeated requests before retrying. See [Troubleshoot HTTP 429 and 599
errors](/docs/troubleshooting/429-599-errors/) for the platform metrics and
logs that identify the reason.

Framework-specific starting points include the [Next.js WordPress
guide](https://vercel.com/guides/wordpress-with-vercel) and a [headless
WordPress JAMstack guide](https://www.smashingmagazine.com/2020/02/headless-wordpress-site-jamstack/).
These are third-party resources; their hosting and framework behavior is not a
WP Cloud platform guarantee.

## Identify the frontend

Set a custom `User-Agent` header on frontend and build requests instead of
using the framework or HTTP client's default. Use a value that identifies the
application and version, such as:

```text
name-of-your-app/1.0
```

A consistent application identifier helps distinguish the frontend's traffic
from browsers, crawlers, and other integrations during monitoring and
troubleshooting.

## Reduce build requests

Fetch only the fields and content required by each frontend route. For Next.js
sites, [Incremental Static
Regeneration](https://nextjs.org/docs/pages/building-your-application/data-fetching/incremental-static-regeneration)
can update pages without rebuilding the complete site. WPGraphQL's
[`nodeByUri` query](https://www.wpgraphql.com/2021/12/23/query-any-page-by-its-path-using-wpgraphql)
can retrieve content for a known WordPress path.

Limit build concurrency on services that send many requests at once. A
starting configuration used by some Netlify builds is concurrency below 1,000
with a request interval of 100 milliseconds. Treat those values as a starting
point rather than a platform limit; lower concurrency when Metrics or HTTP 429
responses show that the build is overwhelming the site.

## Cache GraphQL responses

Review [WPGraphQL's caching
guidance](https://www.wpgraphql.com/2022/12/20/introducing-wpgraphql-smart-cache)
even when the site does not use the Smart Cache extension. Reusing a response
is generally better than repeatedly asking WordPress to build it.

When using [WPGraphQL Smart
Cache](https://github.com/wp-graphql/wp-graphql-smart-cache):

1. Configure the client to use `GET` for cacheable GraphQL requests instead of
   `POST`.
2. In **GraphQL → Settings → Cache**, set a suitable Cache-Control `max-age`.
   A value of at least 1,800 seconds is a useful starting point.
3. Enable **Use Object Cache**.
4. Set Object Cache expiration to at least 1,800 seconds unless the
   application's freshness requirements need a shorter lifetime.

WP Cloud [Page Cache](/docs/performance/cache/page-cache/) and [Edge
Cache](/docs/performance/cache/edge-cache/) can also reduce origin work when
the method, response headers, and cache rules make a request eligible.
