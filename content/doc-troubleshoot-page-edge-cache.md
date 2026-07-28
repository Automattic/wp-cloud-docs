# Troubleshoot Page and Edge Cache

When a page is not served from cache, first identify whether [Page
Cache](/docs/performance/cache/page-cache/) or [Edge
Cache](/docs/performance/cache/edge-cache/) missed or bypassed the request.
The two layers have different response signals, but a Page Cache bypass also
prevents Edge Cache from storing the response.

Test an exact public URL while logged out of WordPress. Record the time, URL,
response status, headers, and whether the result changes between requests.

## Check Edge Cache

Request the URL from a terminal without browser cookies:

```bash
curl -sS -L -D - -o /dev/null -H 'Cookie:' https://example.com/path
```

Find the final `x-ac` header. Its last token describes the request:

- `HIT`, `STALE`, `EXPIRED`, or `UPDATING` means Edge Cache had a stored
  response or was refreshing one.
- `MISS` means that edge location did not have a usable response.
- `BYPASS` means the request was not served from Edge Cache. This is expected
  for logged-in WordPress administrators and can also mean the feature is
  disabled or the response is not cacheable.

Use `wp edge-cache status` or the [Get Edge Cache Settings
endpoint](https://wp.cloud/docs/api/#tag/edge-cache/GET/edge-cache/{site}) to
check the configured state. The setting and `x-ac` answer different questions:
the setting shows whether the feature is enabled, while `x-ac` shows what
happened to one request at one edge location.

A new or recently purged edge location may return `MISS` before it has received
enough eligible requests. Repeat the same request several times before treating
one miss as a fault.

## Check Page Cache

[Page Cache](/docs/performance/cache/page-cache/) normally stores a page after
two eligible origin requests within two minutes and serves it for five minutes.
Request the same URL more than once, then inspect the HTML source for a Batcache
comment:

```bash
curl -sS -L -H 'Cookie:' https://example.com/path | tail -n 12
```

A cached response normally contains `served from batcache` near the end. If the
comment is absent, inspect the final response headers for:

```text
x-nananana: Batcache-Hit
```

The comment may not always be present, so use the header as the second check.
If Edge Cache serves the response first, you may see an edge hit without new
origin activity. Clear or bypass only the layer needed for the test; avoid a
full-domain purge during high traffic.

## Rule out logged-in sessions

Page Cache and Edge Cache normally bypass requests from a browser logged in to
WP Admin. Test with a private browser window or `curl` without a `Cookie`
header. Do not use the result from a logged-in tab as proof that public visitors
miss cache.

Also compare the exact host, scheme, path, and query string. A hit for
`https://example.com/` does not prove that another hostname or URL variant is
populated at the same edge location.

## Inspect cookies

Responses that start a PHP session or set certain cookies may be ineligible for
cache. Common causes include:

- `PHPSESSID` created by `session_start()`.
- A `Set-Cookie` header sent on every request.
- Cookies with `wp_` or `wordpress_` prefixes.
- Cart, checkout, account, language, or personalization cookies.

Inspect both request and response headers in browser developer tools or with
`curl -v`. Compare a fresh logged-out request with the affected browser.

If a harmless plugin cookie causes the bypass, [Page
Cache](/docs/performance/cache/page-cache/#allow-selected-cookies-without-bypassing-page-cache)
describes `noskip_cookies`. Ignore a cookie only when different values cannot
change private, cart, account, localized, or personalized content.

If a public URL must return different content for different cookie values,
Edge Cache can serve the first cached version regardless of the cookie. Use
the [`A8C-Edge-Cache: no-cache` response
header](/docs/performance/cache/edge-cache/#prevent-specific-pages-from-being-cached-at-the-edge)
to prevent the affected pages from being cached at the edge. Configure Page
Cache separately if it must retain distinct variants at the origin.

## Inspect response cache headers

Plugins and custom code can send headers that make a response uncacheable.
Look for:

```text
Pragma: no-cache
Cache-Control: no-cache
Cache-Control: max-age=0
```

These general cache headers are different from the Edge Cache-specific
`A8C-Edge-Cache: no-cache` response header.

Trace the header to the plugin, theme, or custom code that sets it. Do not
remove a no-cache header until you know why it exists; login, account, checkout,
preview, and personalized responses often require it.

After changing the responsible code, clear the affected URL and repeat the
logged-out request. Confirm both the Page Cache and Edge Cache signals.

## Find explicit cache bypasses

Search maintained site code for functions or settings that cancel caching:

```bash
rg -n "batcache_cancel|session_start|nocache_headers|wp_cache_flush|max_age" \
  wp-content/plugins wp-content/themes wp-content/mu-plugins
```

Relevant patterns include:

- `batcache_cancel()`.
- `$batcache->max_age = 0` or `$batcache['max_age'] = 0`.
- `session_start()`.
- `nocache_headers()` or another no-cache response header.
- `wp_cache_flush()` on a frequently run hook.

Review when the code runs, not only whether the string exists. A bypass limited
to an account page may be correct. A flush on every public request or every
minor content action can prevent stable cache population.

If the responsible code is third-party, test the workflow on a staging site
with that component disabled or replaced. Do not run a broad production
conflict test without a rollback plan.

## Handle Edge Cache plugin errors

The prefix in an Edge Cache WP Admin error points to the component that
reported it:

- `Edge Cache API:` refers to a WP Cloud API request.
- `Edge Cache:` refers to the edge authorization service.
- An unprefixed message usually comes from local plugin validation.

A message saying that the cache was cleared recently means the purge was rate
limited; wait at least a minute before trying again. For a generic request or
AJAX failure, retry once after the stated wait, check the browser network
response and PHP error log, and avoid repeated purge attempts.

If the error persists, record the full message, action, time and time zone,
site ID, domain, current Edge Cache status, and browser network response. Do
not keep retrying a purge while the error remains unchanged.

## Verify recovery

After a change:

1. Clear only the affected URL when possible.
2. Make several logged-out requests from the same client.
3. Confirm the Page Cache comment or `x-nananana: Batcache-Hit`.
4. Confirm the expected final `x-ac` result.
5. Test logged-in, cart, checkout, account, API, and other intentionally
   uncached workflows so a broader cache rule does not expose private content.
6. Check [Time Series
   Metrics](https://wp.cloud/docs/api/#tag/metrics/POST/metrics/{type}/{key})
   for cache-hit and cache-miss trends after enough normal traffic has passed.

Requests served by Edge Cache do not appear in origin web server logs. Use
Metrics for edge cache ratios and the `x-ac` header for one request.
