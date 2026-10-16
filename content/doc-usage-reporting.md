# Usage reporting

Use the WP Cloud Usage API to report a site's measured resource use, build charts, and estimate current-period totals. A partner's integration makes these requests with an authorized API key for its WP Cloud client account.

Usage measurements do not define prices or change the partner's billing agreement. See [WP Cloud billing](/docs/partner-resources/wp-cloud-billing/) for billing responsibilities and allocated resources. Use [Metrics](/docs/monitoring-logs/metrics/) for operational telemetry such as request latency, traffic dimensions, and PHP worker behavior.

## Choose time buckets or totals

Both endpoints use `POST` and accept an Atomic Site ID or domain as `{site}`:

| Endpoint | Response | Use |
| --- | --- | --- |
| [Get Site Usage by Time Period](https://wp.cloud/docs/api/#tag/usage/POST/usage/{site}) | `data.periods` | Chart individual time buckets. Each bucket has a `timestamp` and the selected meters. |
| [Get Site Usage Totals](https://wp.cloud/docs/api/#tag/usage/POST/usage/{site}/summarize) | `data.totals` | Report totals for the requested range. |

Both require `start` and `end` as Unix timestamps in seconds, plus a `resolution` of `hour`, `day`, or `month`. Keep the Atomic Site ID in stored integrations so a domain change does not change which site you query.

## Select meters and interpret units

The default meters are `storage`, `compute`, `bandwidth`, `requests_uncached`, `requests_cached`, and `email`. Request component meters explicitly when you need a breakdown.

| Meter | Measurement | Raw unit |
| --- | --- | --- |
| `storage` | Combined filesystem, database, and backup storage over time. | Byte-seconds |
| `storage_fs`, `storage_db`, `storage_backup` | The corresponding storage components. | Byte-seconds |
| `compute` | Combined PHP-FPM, SSH, and database CPU time. | Seconds |
| `compute_php` | PHP-FPM and SSH CPU time. | Seconds |
| `compute_db` | Database CPU time. | Seconds |
| `bandwidth` | Billable HTTP bandwidth. | Bytes |
| `requests_uncached`, `requests_cached` | Uncached and cached HTTP requests. | Count |
| `email` | Emails sent. | Count |

Set `meters` to a comma-separated list, such as `storage_fs,storage_db,compute_php,compute_db`. PHP array notation such as `meters[]=compute&meters[]=bandwidth` is also accepted. A selection replaces the defaults: only those meters appear in the response and `data._meta.units`.

`storage` already includes its three components, and `compute` already includes `compute_php` and `compute_db`. Do not add a combined meter to its components when calculating a total.

Each meter's `usage` is a recorded amount in the unit given by `data._meta.units`. Convert units before displaying or pricing the value:

- Divide CPU seconds by `3600` for CPU-hours.
- Divide bandwidth bytes by `1,000,000,000` for decimal GB.
- Divide storage byte-seconds by `1,000,000,000 × 3600` for decimal GB-hours. One GB stored for one hour equals `3,600,000,000,000` byte-seconds.

If the report uses binary GiB-hours, divide byte-seconds by `1,073,741,824 × 3600` instead. Storage over time is not an instantaneous disk-size reading.

## Choose the UTC time range

The API rounds `start` down and `end` up to boundaries of the requested resolution, in UTC. The aligned start is inclusive and the aligned end is exclusive. Read the actual boundaries from `data._meta.start` and `data._meta.end`, and choose `end` later than `start`.

| Resolution | Supported range after alignment |
| --- | --- |
| `hour` | Less than four days, starting no earlier than seven days ago. |
| `day` | At most 31 days, starting no earlier than two months ago. |
| `month` | Starting no earlier than two years ago. |

The response echoes the resolution in `data._meta.resolution`. Time-series buckets are returned in chronological order, but not every bucket in the range is guaranteed to be present. Do not assume that a missing bucket proves zero usage.

## Know when recorded usage is final

An hour's recorded usage can change for up to two hours after that hour closes. WP Cloud reconciles late-arriving source data during that window. Periods that ended more than two hours ago are final.

Treat the current hour and recently closed hours as provisional. Retrieve the range again after the reconciliation window before closing a usage report or calculating charges from its recorded values. A forecast remains an estimate even when earlier recorded usage is final.

## Interpret forecasts

Include the current period in the range and set `forecast=avg` for a point estimate, or `forecast=band` to also request `forecast_low` and `forecast_high`. Omit `forecast` to return recorded usage without estimates.

Forecasts use a seven-day rolling average of hourly usage. Day and month forecasts are available through the end of the current month. Hourly forecasts are also accepted, without an enforced month-end limit. They do not anticipate future traffic spikes from sales, advertising, or breaking news.

A meter's `forecast` is the estimated total, including recorded usage. Do not add it to `usage`. For example, `usage=50` and `forecast=100` mean 50 recorded units and an estimated total of 100, not 150.

Forecast fields are omitted when the meter has no average statistics. `data._meta.forecast` records the requested mode; it does not prove that every meter has an estimate. In band mode, the bounds use the standard deviation of hourly usage. Missing standard deviation produces a zero-width band, which does not mean the forecast is certain.

## Retrieve a completed day's totals

Set `WP_CLOUD_API_KEY` to an authorized API key and `WP_CLOUD_SITE_ID` to the Atomic Site ID, as described in the [API quick start](/docs/api-automation/api-quick-start/). This example selects three meters for the UTC day before yesterday, keeping the entire range outside the reconciliation window:

```bash
USAGE_END=$(( $(date +%s) / 86400 * 86400 - 86400 ))
USAGE_START=$((USAGE_END - 86400))

curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "start=${USAGE_START}" \
  --data-urlencode "end=${USAGE_END}" \
  --data-urlencode 'resolution=day' \
  --data-urlencode 'meters=storage,compute,bandwidth' \
  "https://atomic-api.wordpress.com/api/v1.0/usage/${WP_CLOUD_SITE_ID}/summarize"
```

Read `data.totals.<meter>.usage` with the matching `data._meta.units` entry. For a chart of the same range, use `/usage/{site}` and read the meter values within `data.periods` instead.
