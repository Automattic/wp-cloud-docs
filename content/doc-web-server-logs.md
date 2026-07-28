# Web server logs

WP Cloud web server logs record requests that reach a site's origin web server. Partner developers and support teams can retrieve them through the WP Cloud API to investigate traffic, errors, and slow requests or to provide log views in a partner-owned interface.

Requests served entirely by [Edge Cache](/docs/performance/cache/edge-cache/) do not reach the origin and are not fully represented in these logs. Use [Metrics](/docs/monitoring-logs/metrics/) for edge request counts, cache ratios, and other time-series data.

## Retrieve logs through the API

The [Get Web Server Logs endpoint](https://wp.cloud/docs/api/#tag/logs/POST/site-logs/{site}) accepts an Atomic Site ID or domain and a required `start` and `end` time range. Both values can be Unix timestamps or date strings accepted by PHP's `strtotime()` function. Logs are guaranteed for 28 days; an earlier start time may return incomplete data.

The endpoint supports pagination, ascending or descending sort order, and filters for:

- cache status;
- renderer, such as PHP or a static file;
- HTTP request method;
- HTTP status code; and
- visitor IP address.

A successful response includes the request URL, method, status, request time, renderer, cache state, host, referrer, user agent, visitor address, and a `scroll_id` when more records are available. Treat visitor addresses, requested URLs, referrers, and user agents as potentially sensitive customer data.

Read the fields together to reconstruct an origin request. For example, `renderer` identifies the component that handled it, while `request_time` describes how long it took; neither value alone identifies the cause of a slow page.

## Interpret Googlebot HTTP 408 responses

When a request from Googlebot produces an HTTP `5xx` response at the origin, WP Cloud returns HTTP `408` to Googlebot. This response handling is designed to prevent a temporary site error from being interpreted as a signal that the URL should not be indexed.

A Googlebot request recorded as `408` can therefore represent an underlying application error. Do not assume that the crawler exceeded a request or concurrency limit based on the `408` alone.

Compare the request timestamp, URL, and user agent with the site's [PHP error logs](/docs/monitoring-logs/logs/error-logs/). Look for a fatal error or other plugin, theme, or application failure at the same time. Correct the underlying error, then ask the search engine to crawl the affected URL again when appropriate.

## Use Metrics and Insights with origin logs

[Metrics](/docs/monitoring-logs/metrics/) includes requests served at the edge as well as requests sent to the origin. Use it when an investigation needs Edge Cache hit and miss ratios, request trends, traffic dimensions, or PHP and database resource measurements.

The [Insights section in the WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud) provides account-wide and site-specific metrics and statistics. Use it for an initial visual review, then retrieve the exact log or Metrics time range when you need request-level detail.
