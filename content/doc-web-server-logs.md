# Web server logs

WP Cloud web server logs record requests that reach a site's origin web server. Partner developers and support teams can retrieve them through the WP Cloud API to investigate traffic, errors, and slow requests or to provide log views in a partner-owned interface.

Requests served entirely by [Edge Cache](/docs/performance/cache/edge-cache/) do not reach the origin and are not fully represented in these logs. Use [Edge Logs](#retrieve-edge-request-logs) for recent individual requests handled at the edge, including cached responses. Use [Metrics](/docs/monitoring-logs/metrics/) for request counts, cache ratios, and other time-series data.

## Retrieve logs through the API

Log endpoints use `POST`. Choose a site or the partner's WP Cloud client account:

| Scope | Endpoint |
| --- | --- |
| One site | [Get Site Web Server Logs](https://wp.cloud/docs/api/#tag/logs/POST/logs/site/{site}) |
| Client account | [Get Client Web Server Logs](https://wp.cloud/docs/api/#tag/logs/POST/logs/client/{client}) |

Use an Atomic Site ID or domain for `{site}`, or a client ID or client name for `{client}`. Both endpoints require `start` and `end`, as Unix timestamps or date strings accepted by PHP's `strtotime()` function. The start is inclusive and the end is exclusive. Logs are guaranteed for 28 days; an earlier start time may return incomplete data.

Both endpoints support filters for cache status (`filter[cached][]`), renderer (`filter[renderer][]`), HTTP method (`filter[request_type][]`), HTTP status (`filter[status][]`), visitor IP address (`filter[user_ip][]`), and TLS fingerprints (`filter[ja3_hash][]` and `filter[ja4_hash][]`).

The site endpoint also supports `filter[request_url][]`. The client endpoint supports `filter[atomic_site_id][]` to select sites, plus numeric ranges for `request_time` in seconds, `body_bytes_sent`, and `status`. For example, `range[request_time][gte]=1` selects requests that took at least one second. Range operators are `gte`, `lte`, `gt`, and `lt`.

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

The [Get Site Edge Logs endpoint](https://wp.cloud/docs/api/#tag/logs/POST/logs/site/{site}/edge) returns individual requests handled by WP Cloud's edge network. Records include HTTP status, visitor IP address, URL, user agent, country, Edge Cache status, rate-limit details, and Defensive Mode challenge details. These logs can show requests that never reach the origin.

Each query covers one domain. It defaults to the site's primary domain. To query another mapped domain, pass it in the `domain` request parameter. Using that domain as `{site}` in the URL only identifies the site; it does not change which domain is queried.

Edge Logs retain the past 24 hours. Each request requires `start` and `end` within that period and can cover at most one hour. The start is inclusive and the end is exclusive. A response contains at most 5,000 records, with no pagination, cursor, or offset. `data.result_count` is the returned count, not the total matching count. A response at the cap may omit matching records. Shorter windows and filters reduce the matches but do not guarantee a complete export. For adjacent windows, reuse the previous end as the next start.

Edge filters are `filter[remote_addr][]`, `filter[ja3_hash][]`, `filter[request_method][]`, `filter[http_status][]`, `filter[http_user_agent][]` (exact match), and `filter[asn][]`. These names differ from origin filters: use `http_status` instead of `status`, and `remote_addr` instead of `user_ip`. Sort with `sort_field` (default `dt`) and `sort_order` (default `asc`).

For example, retrieve the past 10 minutes of HTTP 429 responses at the edge. Set `WP_CLOUD_API_KEY` to an authorized API key and `WP_CLOUD_SITE_ID` to the Atomic Site ID before running this command:

```bash
LOG_END=$(date +%s)
LOG_START=$((LOG_END - 600))

curl --request POST \
  "https://atomic-api.wordpress.com/api/v1.0/logs/site/${WP_CLOUD_SITE_ID}/edge" \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode "start=${LOG_START}" \
  --data-urlencode "end=${LOG_END}" \
  --data-urlencode 'filter[http_status][]=429'
```

The example queries the primary domain. Add `--data-urlencode 'domain=example.com'` for a specific mapped domain. Compare the timestamp, URL, and response fields with origin logs and Metrics when investigating a request.

## Interpret Googlebot HTTP 408 responses

When a request from Googlebot produces an HTTP `5xx` response at the origin, WP Cloud returns HTTP `408` to Googlebot. This response handling is designed to prevent a temporary site error from being interpreted as a signal that the URL should not be indexed.

A Googlebot request recorded as `408` can therefore represent an underlying application error. Do not assume that the crawler exceeded a request or concurrency limit based on the `408` alone.

Compare the request timestamp, URL, and user agent with the site's [Error logs](/docs/monitoring-logs/logs/error-logs/). Look for a fatal error or other plugin, theme, or application failure at the same time. Correct the underlying error, then ask the search engine to crawl the affected URL again when appropriate.

## Use Metrics and Insights with origin logs

[Metrics](/docs/monitoring-logs/metrics/) includes requests served at the edge as well as requests sent to the origin. Use it when an investigation needs Edge Cache hit and miss ratios, request trends, traffic dimensions, or PHP and database resource measurements.

The [Insights section in the WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud) provides account-wide and site-specific metrics and statistics. Use it for an initial visual review, then retrieve the exact log or Metrics time range when you need request-level detail.
