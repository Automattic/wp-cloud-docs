# Edge Cache preload

Edge Cache preload fetches pages before visitors request them and refreshes them after cache purges. It can reduce the time visitors wait when a response is missing from an edge location's cache.

**Closed beta:** This feature is available only to enabled WP Cloud partner accounts. Partners without access can contact [WP Cloud Support](/docs/getting-started/get-support/) to express interest in exploring or testing it.

## How preloading works

The preloader starts at the site's front page and follows links to find pages to fetch. It stores responses in a secondary cache at the site's origin data center. When a request misses the local [Edge Cache](/docs/performance/cache/edge-cache/), WP Cloud checks this preload cache before forwarding the request to WordPress.

The preloader also watches cache purges and refreshes affected pages. A completed crawl does not stop these individual page refreshes.

Preloading can help sites with frequent Edge Cache misses on pages that the crawler can find through internal links, such as a WooCommerce product catalog. It is less likely to help when misses come from unpredictable query parameters, such as campaign markers or ad hoc searches.

## Enable preloading and check progress

Your partner account must have access to the closed beta. Make requests through your partner's authenticated [WP Cloud API integration](/docs/api-automation/api-quick-start/). Replace `<site-id>` with the site's Atomic Site ID. These beta endpoints are not yet listed in the public API reference.

Send this request with an `application/x-www-form-urlencoded` body. Use `enable=1` to enable preloading, or `enable=0` to disable it:

```text
POST /edge-cache/<site-id>/preload
```

Omitting the POST body also enables preloading. The response's `data.enabled` field confirms the setting. Enabling the feature starts background work. The crawler needs time to fetch the site's pages.

Check progress with:

```text
GET /edge-cache/<site-id>/preload
```

Without a domain in the path, these requests use the site's primary domain. To control or check another domain on the site, replace `<domain>` with that domain:

```text
POST /edge-cache/<site-id>/preload/<domain>
GET /edge-cache/<site-id>/preload/<domain>
```

The POST request uses the same `enable` field. The GET response's `data` object can contain these fields:

| Field | Meaning |
| --- | --- |
| `enabled` | Whether preloading is enabled. |
| `state` | `pending`, `running`, `finished`, or `error`. |
| `urls_preloaded` | Number of URLs preloaded. |
| `urls_found` | While running, the number of URLs found and queued for preloading. |
| `searching` | While running, whether the crawler is still finding URLs. |
| `error` | A description of the problem when `state` is `error`. |
| `finished_time` | UTC timestamp when full-site preloading finished. Present when `state` is `finished`. |

`pending` means the crawl is scheduled but has not started. `running` means the preloader is finding and fetching pages. `finished` means the crawl has completed, while refreshes after purges continue. If `state` is `error`, inspect the `error` field before retrying or reporting the issue to WP Cloud Support.

If a settings update returns HTTP `500`, check the current setting with GET before retrying. Report persistent failures to WP Cloud Support.

## Verify page responses and results

Inspect response headers in your browser's developer tools. `x-ac` reports the local Edge Cache result, and `x-sc` reports the preload cache result.

| Headers | Meaning |
| --- | --- |
| `x-ac: MISS` and `x-sc: HIT` | The response came from the preload cache. |
| `x-ac: HIT` and `x-sc: HIT` | The response came from the local Edge Cache and originally came from the preload cache when that entry was populated. |

The `x-sc` header can also report states such as `MISS` or `BYPASS`. An `x-ac` miss alone does not tell you whether WordPress handled the request.

Depending on site size, a full crawl can take minutes or, for large sites, a few days. Already preloaded pages can serve responses before the crawl finishes.

Compare real-user time to first byte (TTFB) before and after enabling preloading. Check results after one, three, six, and 12 hours as the crawler covers more pages. The benefit depends on the site's URLs, cache misses, and visitor browser profiles. Judge the result from your site's measurements.
