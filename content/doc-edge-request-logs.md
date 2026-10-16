# Edge request logs

The [Get Site Edge Logs endpoint](https://wp.cloud/docs/api/#tag/logs/POST/logs/site/{site}/edge) returns individual requests handled by WP Cloud's edge network. Records include HTTP status, visitor IP address, URL, user agent, country, Edge Cache status, rate-limit details, and Defensive Mode challenge details. These logs can show requests that never reach the origin. For requests that reach the origin web server, use [Web server logs](/docs/monitoring-logs/logs/web-server-logs/).

Each query covers one domain. It defaults to the site's primary domain. To query another mapped domain, pass it in the `domain` request parameter. Using that domain as `{site}` in the URL only identifies the site; it does not change which domain is queried.

Edge Logs retain the past 24 hours. Each request requires `start` and `end` within that period and can cover at most one hour. The start is inclusive and the end is exclusive. A response contains at most 5,000 records, with no pagination, cursor, or offset. `data.result_count` is the returned count, not the total matching count. A response at the cap may omit matching records. Shorter windows and filters reduce the matches but do not guarantee a complete export. For adjacent windows, reuse the previous end as the next start.

## Filter Edge requests

Use these filters with the Edge Logs endpoint:

- **Visitor IP address** (`filter[remote_addr][]`): Find requests from specific IPv4 or IPv6 source addresses.
- **TLS fingerprint** (`filter[ja3_hash][]`): Find requests with a specific JA3 fingerprint hash. Use exactly 32 hexadecimal characters. Matching converts the value to lowercase.
- **HTTP method** (`filter[request_method][]`): Select methods, such as `GET` or `POST`. Matching converts values to uppercase.
- **HTTP status** (`filter[http_status][]`): Select response status codes, such as `403` or `429`.
- **User-Agent** (`filter[http_user_agent][]`): Match the complete `User-Agent` header value exactly.
- **Network** (`filter[asn][]`): Select autonomous system numbers (ASNs) associated with source IP addresses.

Edge and origin filters use different names. For Edge Logs, use `http_status` instead of `status`, and `remote_addr` instead of `user_ip`.

Sort with `sort_field` (default `dt`, the request timestamp) and `sort_order` (`asc` by default, or `desc`).

## Find HTTP 429 responses

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
