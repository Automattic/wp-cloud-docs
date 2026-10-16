# Verify Edge Rules

**Closed beta:** Edge Rules is available only to enabled WP Cloud partner accounts. This documentation is a preview. Requests from accounts that are not enabled receive HTTP `403`. Partners without access can contact [WP Cloud Support](/docs/getting-started/get-support/) to express interest in exploring or testing it.

Verify both deployment and request behavior after an [Edge Rule](/docs/edge/edge-rules/overview/) changes. An accepted API request confirms that the change was stored, not that the edge already applies it. Test a matching request and a legitimate request that should remain unaffected.

## Confirm deployment

1. Save `data.response_ticket` from the rule mutation. Poll the [Get Response Ticket Summary endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/summary), sending the ticket as `response-ticket-id` in a form-encoded `POST`. Continue waiting while `data.status` is `null`. Proceed after `success`. Stop and inspect the full details on `failure`. If the summary returns HTTP `202`, wait one second before querying again.
2. Read the rule with `verify=bypass` for a current edge-state check. Replace the site and rule placeholders with the Atomic Site ID and `atomic_edge_rule_id`:

   ```bash
   export WP_CLOUD_SITE_ID='<site-id>'
   export WP_CLOUD_EDGE_RULE_ID='<edge-rule-id>'

   curl --fail-with-body --silent --show-error \
     --header "Auth: ${WP_CLOUD_API_KEY}" \
     "https://atomic-api.wordpress.com/api/v1.0/site-edge-rules/${WP_CLOUD_SITE_ID}/rules/${WP_CLOUD_EDGE_RULE_ID}?verify=bypass"
   ```

The [Get a site edge rule endpoint](https://wp.cloud/docs/api/#tag/edge-rules/GET/site-edge-rules/{site}/rules/{rule}) returns the rule in `data`. The [list endpoint](https://wp.cloud/docs/api/#tag/edge-rules/GET/site-edge-rules/{site}/rules) returns entries in `data.rules`.

`desired_state` is the configured state: `enabled`, `disabled`, or `suspended`. `edge_state` describes the resolved deployment state:

| `edge_state` | Meaning and action |
| --- | --- |
| `live` | The rule matches its configured state at every applicable domain. Continue with a behavior test. |
| `pending` | At least one applicable domain is not up to date. Check the ticket and affected domains before assuming the change is fully deployed. |
| `disabled` | The rule is disabled at the edge. Compare with the intended configuration. |
| `invalid` | The definition no longer builds a valid edge rule, for example after required enablement is removed. It is removed from the edge on reconciliation. Update and enable are rejected. Disable and delete remain available. |

A site-scoped rule is `live` only when every domain attached to the site is current. An alias the edge cannot serve can leave that rule `pending` even when it works on other domains.

`verify=cached`, the default, uses a short read-through cache. `verify=bypass` reads the live edge. `verify=skip` omits `edge_state`. It cannot confirm deployment.

## Build a matching test

Use public DNS so the request passes through WP Cloud's edge. An override that connects directly to the origin does not test an Edge Rule.

You can construct a URL, method, User-Agent, Referer, header, or cookie to match the rule. Request the correct mapped domain for a host condition. Send or omit a field to test an `exists` or negated condition.

The source IP, its country and ASN, and the TLS client's fingerprints come from the actual connection. They cannot be replaced by setting a request header. Use a matching network or TLS client, or review observed traffic when those conditions cannot be reproduced directly.

With `condition_logic=all`, every condition must match your test. With `any`, one matching condition is enough. Check [field and operator meanings](/docs/edge/edge-rules/conditions/) before interpreting a mismatch.

For the response-header example in the Edge Rules guide:

```bash
export WP_CLOUD_TEST_DOMAIN='test.example.com'

curl --silent --show-error --dump-header - --output /dev/null \
  "https://${WP_CLOUD_TEST_DOMAIN}/edge-rule-check"
```

Look for `X-Edge-Rule-Check: enabled`. Also request a path outside that rule's condition and check that it did not receive the header.

## Check the effect for each rule type

The catalog's `verification` and `verification_note` identify the observation method. A `response_observable` effect appears in responses. An `origin_observable` effect requires origin inspection. `not_measurable` means no rule hit count is available. Use request and traffic evidence.

| Rule | Expected observation |
| --- | --- |
| Security fence: block | A matching request receives the configured status code, default `403`, instead of the site's page. |
| Security fence: challenge | A matching request receives a challenge. Command-line tools cannot complete the browser proof-of-work. Test the successful browser flow separately. |
| Redirect | The configured redirect status and `Location` target. With `preserve_query=true`, the request's query string is appended. |
| Rewrite | The origin receives the replacement path/query while the browser URL stays unchanged. Check origin logs or the rendered content. |
| Request header | The specified header is set or removed on the origin request. A response-header check cannot verify this. |
| Response header | The specified header is set or removed in the response received by the visitor. |
| Cache bypass | Repeated matching requests are not Edge Cache hits. Use the cache result in `x-ac`, as explained in [Verify Edge Cache](/docs/performance/cache/edge-cache/#verify-edge-cache). |

For an origin-header test, use controlled logs or a temporary test handler that records only the expected field. Do not expose the full request environment, cookies, or authorization headers. Remove temporary diagnostics after testing.

## Compare security-rule traffic

Rule hit counts are not currently reported. Before enabling a security rule, identify the affected traffic by time, path, user agent, source, or TLS fingerprint. Preserve the query and compare equivalent windows after the reconciliation ticket completes.

Requests blocked or held at a challenge do not reach the origin at that stage. A drop in matching origin traffic can support the investigation, but missing origin records alone do not prove that the rule caused it. Traffic volume and caching can also change what reaches the origin.

Use [Edge Logs](/docs/monitoring-logs/logs/web-server-logs/#retrieve-edge-request-logs) for recent requests handled at the edge, alongside origin web server logs and [Metrics](/docs/monitoring-logs/metrics/). Edge Logs have 24-hour retention, one-hour query windows, and capped results without pagination. They are request evidence, not per-rule hit counters. Keep these limits in mind when comparing samples.

Confirm that legitimate logins, checkout flows, webhooks, and monitoring requests still work where relevant. Redact visitor addresses and sensitive request data before sharing evidence.

## Resolve an unexpected result

Check the rule's ticket and current `edge_state` first. Then check the requested domain, actual condition values, and other rules that can act earlier. WP Cloud-owned rules can redirect, block, or challenge traffic before a partner rule takes effect. The observed response reflects their combined behavior.

A previously cached response can hide a header or redirect change. Test an appropriate uncached path that still matches the conditions. A cache-buster query parameter can change a rule based on `http.query`, `http.query.param`, or `http.uri`. Do not change the match while trying to avoid cache.

For a redirect, inspect the first response before following it so the `Location` header remains visible. For a challenge, a command-line result that is not the site's page is expected. Use a browser to check completion.

If a rule disrupts legitimate traffic, use the [disable or suspend controls](/docs/edge/edge-rules/overview/#suspend-rules-during-an-incident), wait for reconciliation, and repeat the affected request. Preserve the rule definition, ticket ID, timestamps, and test conditions for further investigation.
