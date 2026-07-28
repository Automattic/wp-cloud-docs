# Metrics

WP Cloud Metrics provides high-resolution, time-series telemetry for individual sites and an entire WP Cloud host client account. Partners can use Metrics for dashboards, reporting, traffic analysis, cache measurements, and performance investigations.

The [Metrics feature announcement](https://wp.cloud/2025/05/05/introducing-wp-clouds-next-gen-metrics-high-resolution-analytics-now-live/) provides additional background on the current telemetry system.

Use the [Time Series Metrics endpoint](https://wp.cloud/docs/api/#tag/metrics/POST/metrics/{type}/{key}[/summarize]) under `/metrics/`.

## Choose a site or client query

The endpoint supports two scopes:

| Scope | Path |
| --- | --- |
| Site | `/metrics/site/{atomic_site_id-or-primary_domain}` |
| Host client account | `/metrics/client/{atomic_client_id-or-client_slug}` |

A site query can use an Atomic Site ID or primary domain. Use the persistent Atomic Site ID in stored integrations so a domain change does not break the query.

Each response contains a series of periods. A period's `timestamp` is the start of its time bucket, and `data._meta.resolution` gives the bucket length in seconds. A dimension splits each metric into values such as hostname, HTTP status, request path, or visitor operating system.

Metrics can come from different data sources. Only compatible metrics and dimensions can be combined; a mixed or invalid combination returns HTTP 400.

## Set request parameters

`start` and `end` are required. They accept Unix timestamps or date strings parsed by PHP's `strtotime()` function, and `start` must be earlier than `end`.

| Parameter | Type | Default | Purpose |
| --- | --- | --- | --- |
| `start` | Number or date string | Required | Beginning of the requested range. |
| `end` | Number or date string | Required | End of the requested range. |
| `metric` | String or array | `response_time_average` | One or more metrics from the same data source. |
| `dimension` | String or array | `http_host` | One dimension for multiple metrics, or up to five dimensions for one metric. |
| `resolution` | Integer, in seconds | Automatic | Requests a larger time bucket. It cannot force a finer bucket than the available data. |
| `summarize` | Path suffix | Off | Uses `/summarize` to return one aggregate bucket. |
| `filters[...]` | Array of clauses | None | Restricts results by supported dimensions. |
| `max_bucket_size` | Integer from 1 through 20 | `20` | Limits the number of dimension values returned for each time bucket. |

The endpoint returns at most 100 time periods. It selects a bucket size from the query range, requested age, and available stored resolution. Current data sources provide resolutions up to:

- 10 seconds for data from the last seven days;
- five minutes for data from the last 30 days;
- one hour for data from the last 90 days; and
- one day for older data.

`resolution` can request a larger bucket. For example, if the endpoint selects 240 seconds, a requested resolution of 300 seconds is accepted, while a request for a smaller bucket is ignored.

When a chart or calculated value looks impossible, preserve the exact query window, requested resolution, returned `data._meta.resolution`, metrics, dimensions, and filters before changing the query. Values from different windows or bucket sizes cannot be compared directly.

`max_bucket_size` works like a top-X limit for each period, such as the top 10 referrers or top five autonomous system numbers (ASNs). Its maximum and default are both 20.

## Filter a metric

Each filter contains a `column`, `operator`, and `value`. All filters are joined with `AND`; the endpoint does not support `OR`.

| Field | Type | Notes |
| --- | --- | --- |
| `filters[n][column]` | String | Must be a supported dimension or filter column for the selected metric source. |
| `filters[n][operator]` | String | `IN`, `NOT IN`, `=`, `!=`, `>`, `>=`, `<`, or `<=`. |
| `filters[n][value]` | String, number, or array | Arrays are supported with `IN` and `NOT IN`. |

For example, this filter restricts a request metric to POST requests:

```text
filters[0][column]=request_method
filters[0][operator]=%3D
filters[0][value]=POST
```

When form-encoded, the equality operator is sent as `%3D`.

## Edge request metrics and dimensions

Edge request metrics include:

| Metric | Unit | Meaning |
| --- | --- | --- |
| `requests` | Count | Total HTTP requests. |
| `requests_persec` | Count per second | Request rate. |
| `response_bytes` | Bytes | Total response bandwidth. |
| `response_bytes_persec` | Bytes per second | Response bandwidth rate. |
| `response_bytes_average` | Bytes | Average response size. |
| `response_time_average` | Seconds | Average response time and the default metric. |
| `php_response_time_sum` | Seconds | Total PHP rendering time for requests handled by PHP. |
| `edge_cache_hit_percentage` | Percent | Requests reported as Edge Cache hits. |
| `edge_cache_miss_percentage` | Percent | Requests reported as Edge Cache misses. |

Available dimensions and aliases include:

| Dimension | Alias | Meaning |
| --- | --- | --- |
| `http_version` | `server_protocol` | HTTP version used by the client. |
| `http_verb` | `request_method` | HTTP request method. |
| `http_host` | — | Request hostname and the default dimension. |
| `http_status` | — | HTTP response status. |
| `http_user_agent` | — | Request user agent. |
| `http_referer` | `referer_domain` | Request referrer. |
| `page_renderer` | `request_renderer` | Backend that handled the request, such as PHP or a static-file handler. |
| `page_is_cached` | `is_upstream_cached` | Whether an upstream cache served the response. |
| `wp_admin_ajax_action` | — | Action supplied to `/wp-admin/admin-ajax.php`. |
| `visitor_asn` | `asn` | ASN associated with the request. |
| `visitor_country_code` | `country_code` | Visitor country inferred through GeoIP. |
| `visitor_is_crawler` | `is_crawler` | Whether the visitor appears to be an automated crawler. |
| `visitor_device_type` | — | Detected device type. |
| `visitor_is_logged_in` | — | Whether the visitor appears to be logged in. |
| `visitor_os` | — | Detected operating system. |
| `visitor_browser` | — | Detected browser. |
| `edge_cache_status` | — | Edge result such as `HIT`, `STALE`, `EXPIRED`, `UPDATING`, `MISS`, or `BYPASS`. |
| `is_rate_limited` | — | Whether WP Cloud rate limited the request. |
| `rate_limit_reason` | — | Recorded reason for rate limiting. |
| `datacenter` | — | Edge point-of-presence code. |
| `path` | — | Request path without the query string. |
| `remote_address` | — | Visitor address associated with the request. |
| `atomic_site_id` | — | WP Cloud Atomic Site ID. |
| `proxy_type` | — | Detected proxy type. |

Boolean dimensions are serialized as the strings `"true"` and `"false"` in responses.

## PHP metrics and dimensions

PHP metrics include:

| Metric | Meaning |
| --- | --- |
| `php_cpu_time` | Total PHP CPU time. |
| `php_cpu_time_persec` | PHP CPU time per second. |
| `php_response_time` | Total PHP response time. |
| `php_requests` | Number of PHP requests. |
| `php_requests_persec` | PHP requests per second. |
| `php_workers_average` | Average PHP workers in use. |
| `php_workers_min` | Minimum PHP workers in use. |
| `php_workers_max` | Maximum PHP workers in use. |
| `php_request_burst_percentage` | Percentage of requests in burst mode. |
| `php_request_limited_percentage` | Percentage of requests limited from burst mode. |
| `php_request_normal_percentage` | Percentage of requests not in burst mode. |

PHP dimensions are `http_verb`, `http_host`, `datacenter`, `atomic_site_id`, and `burst_status`. `burst_status` reports `BURST`, `LIMITED`, or `-`.

## Visitor metrics

`uniques` reports unique visitors, and `views` reports page views. Both are aggregated from edge data as daily statistics and use `hostname` as their dimension.

## MySQL metrics and dimensions

MySQL user-statistics metrics are available only for `/metrics/site`; `/metrics/client` does not support them. Every metric also has a `_persec` variant that reports its rate per second.

| Metric | Meaning |
| --- | --- |
| `mysql_total_connections` | Total connections. |
| `mysql_concurrent_connections` | Concurrent connections. |
| `mysql_connected_time` | Cumulative seconds with active connections. |
| `mysql_busy_time` | Cumulative seconds with activity on connections. |
| `mysql_cpu_time` | Cumulative CPU time spent servicing connections. |
| `mysql_bytes_received` | Bytes received. |
| `mysql_bytes_sent` | Bytes sent. |
| `mysql_binlog_bytes_written` | Bytes written to the binary log. |
| `mysql_rows_read` | Rows read from tables. |
| `mysql_rows_sent` | Rows sent from tables. |
| `mysql_rows_deleted` | Rows deleted. |
| `mysql_rows_inserted` | Rows inserted. |
| `mysql_rows_updated` | Rows updated. |
| `mysql_select_commands` | `SELECT` commands. |
| `mysql_update_commands` | `UPDATE` commands. |
| `mysql_other_commands` | Other commands. |
| `mysql_commit_transactions` | `COMMIT` commands. |
| `mysql_rollback_transactions` | `ROLLBACK` commands. |
| `mysql_denied_connections` | Denied connections. |
| `mysql_lost_connections` | Connections terminated without a clean close. |
| `mysql_access_denied` | Commands denied by the database. |
| `mysql_empty_queries` | Empty queries. |
| `mysql_total_ssl_connections` | Connections that used SSL. |
| `mysql_max_statement_time_exceeded` | Queries that exceeded the maximum statement time. |

MySQL dimensions are `pool`, `server`, and `atomic_site_id`.

## PHP cgroup metrics and dimensions

Cgroup user statistics describe PHP process CPU use and are available only for `/metrics/site`.

| Metric | Meaning |
| --- | --- |
| `cgroup_cpu_usage` | PHP CPU usage. |
| `cgroup_cpu_usage_persec` | PHP CPU usage per second. |

Cgroup dimensions are `pool`, `server`, and `atomic_site_id`.

## Interpret responses

Response metadata describes the returned periods:

| Field | Meaning |
| --- | --- |
| `data._meta.start` | Start of the returned range. |
| `data._meta.end` | End of the returned range. |
| `data._meta.resolution` | Seconds represented by each period. |
| `data._meta.metric` or `metrics` | Requested metric or metrics. |
| `data._meta.dimension` or `dimensions` | Requested dimension or dimensions. |
| `data._meta.took` | Backend query time. |
| `data.periods[].timestamp` | Start of that period. |
| `data.periods[].dimension` | Dimension values and their metric values for the period. |

A single-metric response has this form:

```json
{
  "message": "OK",
  "data": {
    "_meta": {
      "start": 1685577600,
      "end": 1685581200,
      "resolution": 300,
      "metric": "response_time_average",
      "dimension": "http_host",
      "took": 123
    },
    "periods": [
      {
        "timestamp": 1685577600,
        "dimension": {
          "example.com": 0.03431913399587993
        }
      }
    ]
  }
}
```

With multiple metrics and one dimension, the dimension contains a value group for each metric:

```json
{
  "message": "OK",
  "data": {
    "_meta": {
      "start": 1685577600,
      "end": 1685581200,
      "resolution": 300,
      "metrics": [
        "response_bytes_average",
        "response_time_average"
      ],
      "dimensions": ["http_verb"],
      "took": 123
    },
    "periods": [
      {
        "timestamp": 1685577600,
        "http_verb": {
          "response_bytes_average": {
            "GET": 42957.75494847475,
            "POST": 1990.5416771631374
          },
          "response_time_average": {
            "GET": 0.06258511425461395,
            "POST": 0.4576846168664701
          }
        }
      }
    ]
  }
}
```

Common errors include:

| HTTP status | Cause |
| --- | --- |
| `400` | Missing time range, unsupported metric, incompatible source combination, invalid dimension, or a request that combines multiple metrics with multiple dimensions. |
| `403` | The API key, source address, host client account, or endpoint scope does not allow the request. |
| `404` | The site was not found. |
| `500` | WP Cloud could not complete the metrics query. |

## Example requests

Replace the timestamps and identifiers with values for the time range and WP Cloud host client account or site you need to inspect.

Requests by visitor operating system:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'metric=requests' \
  --data-urlencode 'dimension=visitor_os' \
  --data-urlencode 'start=1740084605' \
  --data-urlencode 'end=1740581405' \
  "https://atomic-api.wordpress.com/api/v1.0/metrics/site/${WP_CLOUD_SITE_ID}"
```

MySQL CPU use:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'metric=mysql_cpu_time_persec' \
  --data-urlencode 'dimension=atomic_site_id' \
  --data-urlencode 'start=1740084605' \
  --data-urlencode 'end=1740581405' \
  "https://atomic-api.wordpress.com/api/v1.0/metrics/site/${WP_CLOUD_SITE_ID}"
```

Unique visitors and views in one response:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'metric[]=uniques' \
  --data-urlencode 'metric[]=views' \
  --data-urlencode 'dimension=hostname' \
  --data-urlencode 'start=1740084605' \
  --data-urlencode 'end=1740581405' \
  "https://atomic-api.wordpress.com/api/v1.0/metrics/site/${WP_CLOUD_SITE_ID}"
```

Device-type requests restricted to POST:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'metric=requests' \
  --data-urlencode 'dimension=visitor_device_type' \
  --data-urlencode 'start=1740084605' \
  --data-urlencode 'end=1740581405' \
  --data-urlencode 'filters[0][column]=request_method' \
  --data 'filters[0][operator]=%3D' \
  --data-urlencode 'filters[0][value]=POST' \
  "https://atomic-api.wordpress.com/api/v1.0/metrics/site/${WP_CLOUD_SITE_ID}"
```
