# Defensive Mode

Defensive Mode adds an on-demand browser challenge when a site needs more protection from automated traffic. It works with WP Cloud's platform-level [DDoS protection](/docs/security/traffic-protection/ddos-protection/) and requires [Edge Cache](/docs/performance/cache/edge-cache/).

## How Defensive Mode works

You can enable Defensive Mode for 30 minutes through seven days. It uses proof of work: a visitor briefly sees a page that says the browser is being checked, then the browser completes the challenge and redirects the visitor to the requested page. This may take up to five seconds.

The challenge reduces spam and DDoS requests from clients that cannot complete the work. It also applies to legitimate visitors. Browser-based visitors normally continue automatically, but API clients, webhooks, uptime monitors, and other automated clients may be unable to complete it.

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

WP Cloud may enable Defensive Mode automatically when a site uses too many resources. This reduces unwanted requests reaching WordPress and can help legitimate traffic continue to reach the site instead of receiving rate-limit responses.

Automatic Defensive Mode runs for 60 seconds at a time. WP Cloud may enable it again or extend it if conditions do not improve. A legitimate visitor is challenged no more than once per hour while automatic Defensive Mode is active.

## Check the site after enabling Defensive Mode

After enabling Defensive Mode:

1. Check `wp edge-cache status` or the API status endpoint.
2. Open the site in a logged-out browser and confirm that the challenge appears and then loads the requested page.
3. Test important automated clients. A client without a browser may be unable to complete the challenge.
4. Compare request volume, rate-limit metrics, PHP use, and visitor errors with the period before you enabled it.
5. End Defensive Mode when the additional challenge is no longer needed, then repeat the checks.

If legitimate traffic still receives HTTP 429 responses, or WP Cloud records HTTP 599 errors during the event, use [Troubleshoot HTTP 429 and 599 errors](/docs/troubleshooting/429-599-errors/).
