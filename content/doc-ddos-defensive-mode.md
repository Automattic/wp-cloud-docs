# Defensive Mode

Defensive Mode uses browser challenges to reduce unwanted automated traffic reaching a site. WP Cloud also challenges certain traffic independently of Defensive Mode. Seeing a "Checking your browser" page does not by itself mean that manual or Automatic Defensive Mode is active.

Defensive Mode works with WP Cloud's platform-level [DDoS protection](/docs/security/traffic-protection/ddos-protection/) and requires [Edge Cache](/docs/performance/cache/edge-cache/).

## How Defensive Mode works

WP Cloud uses the same challenge system in these situations:

| Situation | What triggers the challenge |
| --- | --- |
| Manual Defensive Mode | A partner enables Defensive Mode through WP-CLI or the API for 30 minutes through seven days. |
| Automatic Defensive Mode | WP Cloud temporarily enables Defensive Mode after a resource-limit event recorded internally as HTTP `599`. |
| Traffic classification | WP Cloud identifies a request pattern with a very high probability of being malicious, fake, or spoofed, such as a spoofed crawler. Neither manual nor Automatic Defensive Mode needs to be active. |

Most challenges are automated browser checks that use proof of work. A visitor briefly sees the browser-check page, then the browser completes the challenge and redirects to the requested page. The usual automated check may take up to five seconds. WP Cloud can escalate to a harder challenge, which may require an action such as selecting a checkbox.

A legitimate visitor whose request matches a suspicious pattern can continue after passing the challenge. API clients, webhooks, uptime monitors, and other automated clients may be unable to complete a browser challenge.

Challenge responses use HTTP `403`. A request that fails or cannot complete the challenge does not reach the requested page. HTTP `429` indicates [rate limiting](/docs/security/traffic-protection/rate-limiting/). It is a different response from a challenge.

Many traffic patterns and fingerprints can trigger a classification challenge. A challenge can occur even when neither manual nor Automatic Defensive Mode is active.

WP Cloud allows certain recognized legitimate traffic through Defensive Mode to help keep essential ecommerce operations working. If real users or an essential service receives an unexpected challenge, follow [Report unexpected challenges](#report-unexpected-challenges).

The normal Defensive Mode crawler exceptions also apply to [Edge Rules that challenge requests](/docs/edge/edge-rules/types/#security-fence). Edge Rule challenges can operate while manual and Automatic Defensive Mode are inactive.

The platform's challenge system cannot be fully disabled. Ending Defensive Mode does not stop challenges triggered by traffic classification. WP Cloud Support can review false positives and assess whether an exception or another adjustment is appropriate.

## Test with an accurate User-Agent

Use a specific, accurate `User-Agent` for every service you build, including uptime monitors, scheduled content syncs, webhooks, and API integrations. This applies whether requests come from a server or your computer. Replace library defaults, such as Python or Go HTTP library User-Agents, with your service's own identifier.

For example, a monitor could send `ExampleMonitor/1.0`, and a sync service could send `ExampleContentSync/2.0`. Use your own service name and version.

Never impersonate a browser, Googlebot, or another service by copying its `User-Agent`.

For example, a `curl` request with Googlebot's `User-Agent` from outside Google's network is spoofed crawler traffic. Expect a challenge and HTTP `403`. This test does not show how WP Cloud handles real Googlebot requests. Impersonating other well-known service providers can also trigger spoofed-traffic challenges.

An accurate `User-Agent` helps distinguish legitimate automation from abuse, but does not bypass challenges or rate limits. If your service still receives unexpected challenges, provide the request details below to Support.

## When to use Defensive Mode

Use Defensive Mode during a suspected bot or DDoS event when unwanted traffic is still reaching the site or using PHP resources. Check [Metrics](/docs/monitoring-logs/metrics/), [web server logs](/docs/monitoring-logs/logs/web-server-logs/), and the site's normal traffic pattern before and after enabling it.

Keep Defensive Mode active only as long as needed. Check important site, API, webhook, monitoring, and checkout workflows after enabling it.

## Manage Defensive Mode with WP-CLI

The installed `wp edge-cache` command accepts durations in minutes, hours, or days. The supported range is 30 minutes through seven days.

Enable Defensive Mode for a duration:

```bash
wp edge-cache defensive-mode --time=<time>
```

For example:

```bash
wp edge-cache defensive-mode --time=35m
wp edge-cache defensive-mode --time=2h
wp edge-cache defensive-mode --time=3d
```

End it early:

```bash
wp edge-cache defensive-mode --end
```

Check the current Edge Cache and Defensive Mode state:

```bash
wp edge-cache status
```

Run `wp edge-cache` without a subcommand to see the usage installed on the site. The current command uses `defensive-mode`; do not use the obsolete `defensive_mode` form.

## Manage Defensive Mode through the API

Use the [Configure Defensive Mode endpoint](https://wp.cloud/docs/api/#tag/edge-cache/POST/edge-cache/{site}/ddos_until) to set the state for a site. WP Cloud partners can use this endpoint to provide Defensive Mode controls in their own dashboards.

Supply the expiration as a Unix timestamp at least 30 minutes and no more than seven days in the future. A value of `0` disables Defensive Mode. The site-level route uses the primary domain by default. Use the domain-specific route documented in the same API group when the setting should apply to another domain on the site.

Use the [Get Defensive Mode status endpoint](https://wp.cloud/docs/api/#tag/edge-cache/GET/edge-cache/{site}/ddos_until) to retrieve the current `ddos_until` value. A future timestamp records when the mode is set to end; `0` means it is not active.

## Automatic Defensive Mode

WP Cloud temporarily enables Automatic Defensive Mode after a resource-limit event recorded internally as HTTP `599`. A 599 means a PHP connection was not available in time. It does not require CPU usage to reach its limit.

See [Understand PHP workers and backlog](/docs/troubleshooting/site-performance/#understand-php-workers-and-backlog) for a six-worker example and guidance on adding capacity or optimizing the site.

Automatic Defensive Mode reduces unwanted requests reaching WordPress to protect the site's resources. This can help legitimate requests reach the site instead of being resource limited. Requests that receive a challenge must still pass it before continuing.

WP Cloud may enable Automatic Defensive Mode again or extend it if conditions do not improve. A legitimate visitor is challenged no more than once per hour while Automatic Defensive Mode is active.

## Check the site after enabling Defensive Mode

After enabling Defensive Mode:

1. Check `wp edge-cache status` or the API status endpoint.
2. Open the site in a logged-out browser. If challenged, confirm that the browser passes the challenge and loads the requested page.
3. Test important automated clients, including payment-provider callbacks. A client without a browser may be unable to complete the challenge.
4. Compare request volume, rate-limit metrics, PHP use, and visitor errors with the period before you enabled it.
5. End Defensive Mode when the additional challenge is no longer needed, then repeat the checks.

If legitimate traffic still receives HTTP 429 responses, or WP Cloud records HTTP 599 errors during the event, use [Troubleshoot HTTP 429 and 599 errors](/docs/troubleshooting/429-599-errors/).

## Report unexpected challenges

Contact [WP Cloud Support](/docs/getting-started/get-support/) if real users or essential services, such as payment-provider callbacks, receive a challenge that they should not encounter. Provide the following details together for each example request:

- The correct Atomic Site ID and affected domain.
- The exact timestamp with the time zone, preferably UTC.
- The request URL.
- The complete `User-Agent` header.
- The source IP address. This is essential for finding the exact request.
- What failed and how it affected the visitor or service. Include any third-party proxy or headless setup involved in the request.

Request counts or reports that many sites are affected do not identify which requests failed for legitimate users. Logs also contain expected blocks, challenges, and rate limits.

The timestamp, source IP, URL, and `User-Agent` together let Support locate the exact request, investigate why it was challenged, and assess possible adjustments. Without these details, identifying a false positive takes longer and may not be possible.
