# Application performance monitoring

WP Cloud application performance monitoring (APM) captures traces for individual requests so your team can inspect where a site spends its time. Enable trace collection for a short window, reproduce the slow request, then open the temporary APM trace viewer.

Your team is responsible for capturing and interpreting traces and implementing site-specific fixes. Access to APM does not include WP Cloud Support performing site-specific APM investigations or performance optimization. If your findings suggest a platform fault, [contact Support with the evidence collected](/docs/getting-started/get-support/#include-useful-evidence). See [Support scope](/docs/getting-started/get-support/#support-scope) for the division of responsibilities.

## Choose the APM version

WP Cloud has two APM versions. The site's `apm_driver` site meta value selects the version that collects traces for that site.

| `apm_driver` value | APM version | Status |
| --- | --- | --- |
| No value or `elastic` | Legacy APM | Default. Deprecated, and receives only bug fixes and security updates. |
| `pfx` | Next Gen APM | Available for testing. |

The Next Gen APM uses the [PFX](https://github.com/Automattic/pfx) PHP extension to collect profiling data. It records more detail than the legacy APM. Its trace viewer adds filtering, search, and grouping, and you can download traces in OTLP, PFX, and speedscope formats for analysis in other tools.

### Switch a site to the Next Gen APM

**Warning:** While `apm_driver` is set to `pfx`, the legacy APM does not create span files for the site. Any integration that reads legacy APM span files receives no data for that site. Check your integrations before you switch.

Set the site's `apm_driver` site meta value to `pfx` with the [Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}). Use `add` when the value does not exist and `update` to replace an existing value:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode "value=pfx" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/apm_driver/add"
```

Then capture traces and open the trace viewer as described in the following sections. The `apm_until` value, the APM URL request, and the format of the returned APM URL are the same for both versions.

### Switch a site back to the legacy APM

Remove the site's `apm_driver` site meta value, or update it to `elastic`:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/apm_driver/remove"
```

## Capture traces

Set the site's `apm_until` site meta value to a future Unix timestamp, written as digits only. The timestamp can be no more than about 24 hours in the future. Use a short window measured in minutes or seconds so the capture includes the request you need without collecting unnecessary traces.

The [Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}) accepts the Atomic Site ID or domain, the `apm_until` key, and the `add` or `update` action. Use `add` when the value does not exist and `update` to replace an existing value:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode "value=${APM_UNTIL_UNIX_TIME}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/apm_until/add"
```

After WP Cloud accepts the value, visit the affected page or repeat the specific action during the capture window. Reproducing the exact request makes it easier to find the relevant trace.

To extend the capture window, update `apm_until` again with a later timestamp. To end APM early, update `apm_until` to `0`.

## Open the trace viewer

Request a temporary APM URL for the site with the [Get Site APM URL endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-apm/{site}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
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

In the legacy APM, the Traces page lists captured requests. In the Next Gen APM, the **Transactions** tab of the **Trace Explorer** lists them. Select the request that matches the reproduced URL and time, then inspect the trace to find slow application work such as WordPress hooks, database queries, or external requests.

Compare the trace with [Metrics](/docs/monitoring-logs/metrics/), [web server logs](/docs/monitoring-logs/logs/web-server-logs/), and [error logs](/docs/monitoring-logs/logs/error-logs/) for the same time range. APM explains one captured request; the other sources show whether the behavior is repeated or correlated with traffic and resource use.
