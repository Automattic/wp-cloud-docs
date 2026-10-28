# Edge Rule types

**Closed beta:** Edge Rules is available only to enabled WP Cloud partner accounts. This documentation is a preview. Requests from accounts that are not enabled receive HTTP `403`. Partners without access can contact [WP Cloud Support](/docs/getting-started/get-support/) to express interest in exploring or testing it.

Each [Edge Rule](/docs/edge/edge-rules/overview/) uses a catalog type identified by `rule_key`. Retrieve the [Edge Rule catalog](https://wp.cloud/docs/api/#tag/edge-rules/GET/edge-rule-catalog) for the types available to your API key. Its `input_schema`, defaults, and `constraints` are the current input contract.

The examples below are rule bodies, not complete HTTP requests. Send them as form fields, with `rule_definition` encoded as a JSON string. Follow the [create-and-verify procedure](/docs/edge/edge-rules/overview/#create-and-verify-a-first-rule), validate before saving, and check the effect on legitimate traffic.

| Type | `rule_key` | Phase | Catalog risk |
| --- | --- | --- | --- |
| Security fence | `managed.security_fence` | Security | High |
| IP allowlist | `managed.ip_allowlist` | Security | High |
| Redirect | `managed.redirect` | Redirect | Medium |
| Rewrite | `managed.rewrite` | Rewrite | Medium |
| Request header | `managed.request_header` | Request headers | Low |
| Response header | `managed.response_header` | Response headers | Low |
| Cache bypass | `managed.cache_bypass` | Cache | Medium |
| Ignore query args in cache | `managed.cache_ignore_args` | Cache | Medium |

Catalog entries also provide supported `scopes`, a `verification` method, and any `verification_note`. Use the [conditions reference](/docs/edge/edge-rules/conditions/) for shared matching fields and operators.

## Security fence

Security fences block or challenge matching requests. `action=block` returns a `status_code` from `400` through `499`, defaulting to `403`. Set `status_code` only for a block action.

`action=challenge` uses browser proof-of-work. The normal [Defensive Mode crawler exceptions](/docs/security/traffic-protection/defensive-mode/#how-defensive-mode-works) also apply to challenge Edge Rules. Requests that receive a challenge must complete it before proceeding.

At least one condition is required. `condition_logic` is `all` by default or can be `any`. Conditions can select IP addresses, networks, countries, Autonomous System Numbers (ASNs), TLS fingerprints, URLs, methods, or request headers.

A broad rule can block legitimate customers, partner support teams, API integrations, and monitors. Review login, checkout, and webhook flows before using a broad condition. Automated clients that cannot complete a challenge will not reach the site.

This example challenges requests under `/shop/` that contain an `add_to_cart` query parameter and no Referer header. The parameter name is the example's chosen key. Match the key used by your application.

```json
{
  "rule_name": "challenge-cart-crawls",
  "rule_key": "managed.security_fence",
  "rule_definition": {
    "version": 1,
    "input": {
      "action": "challenge",
      "conditions": [
        {"field": "http.path", "op": "wildcard", "value": "/shop/*"},
        {"field": "http.query.param", "key": "add_to_cart", "op": "exists"},
        {"field": "http.referer", "op": "exists", "negate": true}
      ]
    }
  }
}
```

This example blocks `/wp-login.php` requests from outside `US` and `CA`. Those countries are illustrative, not a recommended policy. Test support access and legitimate logins from other locations before applying such a rule.

```json
{
  "rule_name": "geo-limit-login",
  "rule_key": "managed.security_fence",
  "rule_definition": {
    "version": 1,
    "input": {
      "action": "block",
      "conditions": [
        {"field": "http.path", "op": "starts_with", "value": "/wp-login.php"},
        {"field": "geo.country", "op": "in", "values": ["US", "CA"], "negate": true}
      ]
    }
  }
}
```

## IP allowlist

IP allowlist rules let trusted IP addresses skip later partner security rules. `action=skip_challenge` stops challenges for matching requests, but block rules still apply. `action=allow` ends security evaluation, so later partner block and challenge rules do not run.

Supply `ips` as a list of up to 100 IP addresses or CIDR ranges. IPv4 ranges must be `/24` or narrower, and IPv6 ranges must be `/48` or narrower. A bare address is stored as `/32` or `/128`. Conditions are optional. When supplied, they narrow the match and combine with the IP match using AND.

WP Cloud-owned rules always run before partner rules, so an allowlist cannot skip them. The catalog marks this type's effect as not measurable from a response.

This example lets an office address and a monitoring range skip all later partner security rules for REST API requests:

```json
{
  "rule_name": "allow-office-rest-api",
  "rule_key": "managed.ip_allowlist",
  "rule_definition": {
    "version": 1,
    "input": {
      "action": "allow",
      "ips": ["203.0.113.10", "198.51.100.0/24"],
      "conditions": [
        {"field": "http.path", "op": "starts_with", "value": "/wp-json/"}
      ]
    }
  }
}
```

## Redirect

A redirect sends matching requests to a fixed `target_url`. The target must be an absolute HTTP(S) URL or a path beginning with `/`. Placeholders are not supported. A target equal to the matched path is rejected.

Allowed `status_code` values are `301` (default), `302`, `307`, and `308`. `preserve_query` defaults to `true`, appending the request's query string to the target. At least one condition must use `http.host`, `http.path`, or `http.uri`.

This example redirects a retired product URL to its replacement:

```json
{
  "rule_name": "legacy-widget-redirect",
  "rule_key": "managed.redirect",
  "rule_definition": {
    "version": 1,
    "input": {
      "conditions": [
        {"field": "http.path", "op": "eq", "value": "/products/legacy-widget"}
      ],
      "target_url": "/products/widget-2"
    }
  }
}
```

## Rewrite

A rewrite changes the path or query sent to the origin while leaving the visitor's URL unchanged. Supply at least one of `path` or `query`. A replacement path must start with `/`. A query string excludes the leading `?`. A rewrite that leaves the request unchanged is rejected.

This example serves a campaign page at a different public path:

```json
{
  "rule_name": "spring-sale-rewrite",
  "rule_key": "managed.rewrite",
  "rule_definition": {
    "version": 1,
    "input": {
      "conditions": [
        {"field": "http.path", "op": "eq", "value": "/spring-sale"}
      ],
      "path": "/campaigns/2026-spring",
      "query": "utm_source=edge"
    }
  }
}
```

## Request header

Request-header rules set or remove headers on requests sent to the origin. Their changes are visible at the origin, rather than in the response received by the visitor.

Set `operation` to `set` or `remove`. For `set`, supply one `header` name and a `value`. For `remove`, supply a header name or an array of up to 32 names. The edge does not permit setting restricted destination headers such as `Host`, `Authorization`, or `Cookie`.

A set value can be a literal or one whole-value [placeholder](/docs/edge/edge-rules/conditions/#request-header-placeholders). For example, `{{geo.country}}` uses the visitor's country and `{{http.header:x-request-id}}` copies a named request header. Use the catalog's `matchers.placeholders` list. Placeholders cannot be concatenated with text.

This example passes the visitor's country to the origin for one host:

```json
{
  "rule_name": "visitor-country-header",
  "rule_key": "managed.request_header",
  "rule_definition": {
    "version": 1,
    "input": {
      "operation": "set",
      "header": "X-Visitor-Country",
      "value": "{{geo.country}}",
      "conditions": [
        {"field": "http.host", "op": "eq", "value": "shop.example.com"}
      ]
    }
  }
}
```

## Response header

Response-header rules set or remove headers sent to the visitor. `operation` is `set` or `remove`. Set one header with `header` and a literal `value`. Placeholders are not supported. A remove operation accepts one name or an array of up to 32 names. Framing and security-critical headers cannot be removed.

This example sends an indexing directive for PDF paths:

```json
{
  "rule_name": "noindex-pdfs",
  "rule_key": "managed.response_header",
  "rule_definition": {
    "version": 1,
    "input": {
      "operation": "set",
      "header": "X-Robots-Tag",
      "value": "noindex, nofollow",
      "conditions": [
        {"field": "http.path.extension", "op": "eq", "value": "pdf"}
      ]
    }
  }
}
```

## Cache bypass

Cache-bypass rules skip [Edge Cache](/docs/performance/cache/edge-cache/) for matching requests, sending them to the origin. At least one condition is required. The rule does not set cache time to live (TTL) or change cache keys. Use a response-header rule for cache-related headers sent to the visitor.

The origin's [Page Cache](/docs/performance/cache/page-cache/) remains a separate layer. An edge bypass does not prove that PHP handled the request or that every cache was bypassed.

This example bypasses Edge Cache for account-area paths:

```json
{
  "rule_name": "no-cache-account",
  "rule_key": "managed.cache_bypass",
  "rule_definition": {
    "version": 1,
    "input": {
      "conditions": [
        {"field": "http.path", "op": "starts_with", "value": "/my-account"}
      ]
    }
  }
}
```

## Ignore query args in cache

These rules leave named query parameters out of the [Edge Cache](/docs/performance/cache/edge-cache/) key for matching requests, so pages that differ only in those parameters share one cached copy. The origin still receives the full query string.

Supply `args` as a list of one to 50 parameter names. Names are matched exactly as written: case-sensitive and not percent-decoded. `ignore=value` drops only the value, so pages with and without the parameter are still cached separately. `ignore=arg` drops the whole parameter, so the page without it shares the copy too.

At least one condition is required. Use `http.path` `starts_with` `/` to match the whole site.

Ignore a parameter only when the page does not depend on it. The first value cached is served for every other value until the copy expires. Tracking IDs and campaign tags are suitable. Search terms, pagination, and anything the page renders are not.

This example shares one cached copy across referral and campaign parameters for the whole site:

```json
{
  "rule_name": "ignore-tracking-args",
  "rule_key": "managed.cache_ignore_args",
  "rule_definition": {
    "version": 1,
    "input": {
      "args": ["ref", "utm_campaign"],
      "ignore": "value",
      "conditions": [
        {"field": "http.path", "op": "starts_with", "value": "/"}
      ]
    }
  }
}
```

Other catalog types may have no inputs or require separate enablement. Follow the returned schema for each entry. Use [Verify Edge Rules](/docs/edge/edge-rules/verify/) for response, origin, and traffic checks.
