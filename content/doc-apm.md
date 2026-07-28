# Application performance monitoring

WP Cloud application performance monitoring (APM) captures traces for individual requests so partner developers, support teams, and their customers can inspect where a site spends its time. Enable trace collection for a short window, reproduce the slow request, then open the temporary APM trace viewer.

## Capture traces

Set the site's `apm_until` site meta value to a future Unix timestamp. Use a short window measured in minutes or seconds so the capture includes the request you need without collecting unnecessary traces.

The [Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}) accepts the Atomic Site ID or domain, the `apm_until` key, and the `add` or `update` action. Use `add` when the value does not exist and `update` to replace an existing value:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode "value=${APM_UNTIL_UNIX_TIME}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/apm_until/add"
```

After WP Cloud accepts the value, visit the affected page or repeat the specific action during the capture window. Reproducing the exact request makes it easier to find the relevant trace.

## Open the trace viewer

Request a temporary APM URL for the site:

```bash
curl --fail-with-body --silent --show-error \
  --request GET \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-apm/${WP_CLOUD_SITE_ID}"
```

The response contains a time-sensitive, tokenized URL:

```json
{
  "message": "OK",
  "data": {
    "url": "https://example.com/_apm/?timestamp=1738080031&nonce=<nonce>&token=<token>"
  }
}
```

You can generate and open this URL after trace collection ends. The site must already have captured traces for the viewer to contain useful data. Opening the URL sets an `_apm_auth` cookie and grants temporary access to `/_apm/`; treat the URL as a credential and do not share or log it.

## Examine a trace

The Traces page lists captured requests. Select the request that matches the reproduced URL and time, then inspect the trace to find slow application work such as WordPress hooks, database queries, or external requests.

Compare the trace with [Metrics](/docs/monitoring-logs/metrics/), [web server logs](/docs/monitoring-logs/logs/web-server-logs/), and [error logs](/docs/monitoring-logs/logs/error-logs/) for the same time range. APM explains one captured request; the other sources show whether the behavior is repeated or correlated with traffic and resource use.
