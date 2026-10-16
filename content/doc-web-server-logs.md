# Web server logs

WP Cloud web server logs record requests that reach a site's origin web server. Partner developers and support teams can retrieve them through the WP Cloud API to investigate traffic, errors, and slow requests or to provide log views in a partner-owned interface.

Requests served entirely by [Edge Cache](/docs/performance/cache/edge-cache/) do not reach the origin and are not fully represented in these logs. Use [Edge request logs](/docs/monitoring-logs/logs/edge-request-logs/) for recent individual requests handled at the edge, including cached responses. Use [Metrics](/docs/monitoring-logs/metrics/) for request counts, cache ratios, and other time-series data.

## Retrieve logs through the API

Log endpoints use `POST`. Choose a site or the partner's WP Cloud client account:

| Scope | Endpoint |
| --- | --- |
| One site | [Get Site Web Server Logs](https://wp.cloud/docs/api/#tag/logs/POST/logs/site/{site}) |
| Client account | [Get Client Web Server Logs](https://wp.cloud/docs/api/#tag/logs/POST/logs/client/{client}) |

Use an Atomic Site ID or domain for `{site}`, or a client ID or client name for `{client}`. Both endpoints require `start` and `end`, as Unix timestamps or date strings accepted by PHP's `strtotime()` function. The start is inclusive and the end is exclusive. Logs are guaranteed for 28 days; an earlier start time may return incomplete data.

### Filter origin requests

Both endpoints support these filters:

- **Cache status** (`filter[cached][]`): Select cache status values, such as `true` or `false`.
- **Renderer** (`filter[renderer][]`): Select the component that handled the request, such as `php` or `static`.
- **HTTP method** (`filter[request_type][]`): Select methods, such as `GET` or `POST`.
- **HTTP status** (`filter[status][]`): Select response status codes, such as `404` or `503`.
- **Visitor IP address** (`filter[user_ip][]`): Find requests from specific source IP addresses.
- **TLS fingerprints** (`filter[ja3_hash][]` and `filter[ja4_hash][]`): Find requests with specific JA3 or JA4 fingerprint hashes.

These filters depend on the endpoint:

- **Request URL** (`filter[request_url][]`): Select request URLs. Available on the site endpoint only.
- **Site** (`filter[atomic_site_id][]`): Select sites by Atomic Site ID. Available on the client endpoint only.

The client endpoint also supports numeric ranges:

- **Request time** (`range[request_time][<operator>]`): Filter by request duration in seconds.
- **Response size** (`range[body_bytes_sent][<operator>]`): Filter by response size in bytes.
- **HTTP status** (`range[status][<operator>]`): Filter by a range of response status codes.

Replace `<operator>` with `gte` (greater than or equal to), `lte` (less than or equal to), `gt` (greater than), or `lt` (less than). For example, `range[request_time][gte]=1` selects requests that took at least one second.

### Page through origin logs

For raw logs, set `page_size` and `sort_order` (`asc` or `desc`). To retrieve another page, send the returned `scroll_id` with the same fixed timestamps, filters, ranges, page size, and sort order. Continue until `scroll_id` is `null`. Avoid relative time values that shift the window between requests.

A successful raw response includes the request URL, method, status, request time, renderer, cache state, host, referrer, user agent, visitor address, and a `scroll_id` when more records are available. Treat visitor addresses, requested URLs, referrers, and user agents as potentially sensitive customer data.

Read the fields together to reconstruct an origin request. For example, `renderer` identifies the component that handled it, while `request_time` describes how long it took; neither value alone identifies the cause of a slow page.

## Summarize origin requests

Use a summary when you need request counts rather than individual log records. Apply the same time range and supported filters:

| Scope | Request parameters | Response |
| --- | --- | --- |
| One site | `summary=over_time`; optional `resolution` in seconds, at least `60` | `data.timeseries` contains timestamp and count buckets; `data.resolution` gives their length. |
| Client account | `summary=top_hosts`; optional `top_n` from `1` to `100`, default `10` | `data.top_hosts` ranks hosts by request count; `data.total_results` gives the total matching count. |

The site endpoint chooses a resolution automatically when omitted. Summary modes return aggregates instead of raw logs and a scroll cursor; they ignore `page_size`, `scroll_id`, and `sort_order`.

## Retrieve Edge request logs

For individual requests handled at the edge, including cached responses and challenges, use [Edge request logs](/docs/monitoring-logs/logs/edge-request-logs/). That guide covers the endpoint, query limits, filters, and an example request.

## Interpret Googlebot HTTP 408 responses

When a request from Googlebot produces an HTTP `5xx` response at the origin, WP Cloud returns HTTP `408` to Googlebot. This response handling is designed to prevent a temporary site error from being interpreted as a signal that the URL should not be indexed.

A Googlebot request recorded as `408` can therefore represent an underlying application error. Do not assume that the crawler exceeded a request or concurrency limit based on the `408` alone.

Compare the request timestamp, URL, and user agent with the site's [Error logs](/docs/monitoring-logs/logs/error-logs/). Look for a fatal error or other plugin, theme, or application failure at the same time. Correct the underlying error, then ask the search engine to crawl the affected URL again when appropriate.

## Use Metrics and Insights with origin logs

[Metrics](/docs/monitoring-logs/metrics/) includes requests served at the edge as well as requests sent to the origin. Use it when an investigation needs Edge Cache hit and miss ratios, request trends, traffic dimensions, or PHP and database resource measurements.

The [Insights section in the WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud) provides account-wide and site-specific metrics and statistics. Use it for an initial visual review, then retrieve the exact log or Metrics time range when you need request-level detail.
