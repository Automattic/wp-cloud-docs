# Rate limiting

WP Cloud rate limiting protects individual sites and the platform from
excessive requests, abusive automation, and traffic that consumes too many
resources. A matching request can receive an HTTP 429 response instead of
reaching WordPress.

Some HTTP 429 responses are expected and need no change. Investigate when a
limit blocks a legitimate visitor, monitoring check, search crawler, API
client, webhook, or other customer workflow.

## How requests can be classified

WP Cloud can classify traffic using several request characteristics rather
than relying on an IP address alone. Depending on the traffic and the rule,
signals can include:

- Request rate from a source.
- URI or route patterns.
- User agent.
- Proxy characteristics.
- Connection signals.
- Other repeated request characteristics.

Limits can apply to a request pattern, a site, or a broader platform rule.
WP Cloud may also add a manual rule for a known abusive pattern. Exact rules
and thresholds can change as traffic changes, so do not build an application
that depends on a particular undocumented limit.

Legitimate automation, webhooks, monitoring tools, and API clients should send
a specific, accurate `User-Agent` header. Requests without a `User-Agent`, or
with a generic value commonly associated with abusive traffic, provide fewer
signals that distinguish them from abuse and have a higher chance of matching
a rate limit. A `User-Agent` does not bypass rate limiting or prove the
request's identity.

## HTTP 429 responses

A true HTTP 429 is shown to the client and recorded as `429` in web server logs
and [Metrics](/docs/monitoring-logs/metrics/). WP Cloud hosts can
retrieve request logs through the [Web Server Logs API
endpoint](https://wp.cloud/docs/api/#tag/logs/POST/site-logs/{site}). A true
HTTP 429 means the request matched a rate limit. A specific browser, user
agent, function, URI pattern, or request signature may be making too many
requests.

The visitor-facing rate-limit page can also represent a WP Cloud resource-limit
event recorded internally as HTTP 599. Do not assume every visible 429 is an
ordinary request-rate limit. [Troubleshoot HTTP 429 and 599
errors](/docs/troubleshooting/429-599-errors/) explains how to distinguish the
recorded statuses using logs and current metrics.

A group of true HTTP 429 responses can also accompany a DDoS attack or repeated
requests for missing pages and assets. See [DDoS
protection](/docs/security/traffic-protection/ddos-protection/) for the platform
protections and additional controls available during an attack.
If the logs contain many 404 responses, follow [Check for expensive 404
responses](/docs/troubleshooting/429-599-errors/#check-for-expensive-404-responses).

## Bots and crawlers

It is normal to see occasional 429 responses from scanners, SEO crawlers, and
malicious bots. No action is usually needed when the site and legitimate
traffic continue to work.

If an authorized crawler is limited:

1. Confirm its user agent, source, affected URLs, and incident time in web
   server logs.
2. Reduce its crawl rate and add delay or backoff after an HTTP 429.
3. Check for a loop, repeated missing URL, or configuration that creates more
   requests than intended.
4. Verify that the tool identifies itself correctly. A user agent alone does
   not prove that a request came from the named service.
5. Contact WP Cloud Support only when the legitimate workflow remains blocked
   after correcting the client behavior.

Do not change the site's public behavior to accommodate unwanted bots. During
a larger attack, use [Defensive
Mode](/docs/security/traffic-protection/defensive-mode/) and preserve request
samples for the incident review.

## Review rate limiting in logs and Metrics

Use the [Web Server Logs API
endpoint](https://wp.cloud/docs/api/#tag/logs/POST/site-logs/{site}) to retrieve
request-level details such as URLs, user agents, source addresses, and HTTP
statuses. Use the [Time Series Metrics
endpoint](https://wp.cloud/docs/api/#tag/metrics/POST/metrics/{type}/{key}) or
the [WP Cloud host portal](https://hosts.automattic.com/wpcloud) for the same
time range as the incident. Useful dimensions include `is_rate_limited` and
`rate_limit_reason`. Group them with dimensions such as `path`,
`http_user_agent`, `http_status`, or `wp_admin_ajax_action` to find the affected
traffic. Logs show the individual requests; Metrics show the pattern over
time. Use both when the impact is not clear.
