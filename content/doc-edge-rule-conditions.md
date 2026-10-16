# Edge Rule conditions

**Closed beta:** Edge Rules is available only to enabled WP Cloud partner accounts. This documentation is a preview. Requests from accounts that are not enabled receive HTTP `403`. Partners without access can contact [WP Cloud Support](/docs/getting-started/get-support/) to express interest in exploring or testing it.

Conditions select the requests an [Edge Rule](/docs/security/traffic-protection/edge-rules/) acts on. Retrieve the [Edge Rule catalog](https://wp.cloud/docs/api/#tag/edge-rules/GET/edge-rule-catalog) and use `data.matchers` for the current fields, operators, limits, and placeholder vocabulary.

## Write a condition

| Key | Value |
| --- | --- |
| `field` | A supported request field. |
| `op` | An operator allowed for that field. |
| `value` | A string for a single-value operator. Omit it for `exists`. |
| `values` | An array for `in` or `in_cidr`, instead of `value`. |
| `key` | The header, cookie, or query-parameter name for a keyed field. |
| `negate` | Optional boolean that reverses this condition. |

This condition matches countries outside the given set:

```json
{"field":"geo.country","op":"in","values":["US","CA"],"negate":true}
```

This condition requires a named request header:

```json
{"field":"http.header","key":"x-api-client","op":"exists"}
```

Text comparisons are case-insensitive. Header names are also case-insensitive. Cookie and query-parameter names are case-sensitive.

## Fields and allowed operators

| Field | Operators | Meaning |
| --- | --- | --- |
| `ip.src` | `eq`, `neq`, `in`, `in_cidr` | Requester's IP address. Use `in_cidr` for network ranges. |
| `geo.country` | `eq`, `neq`, `in` | ISO 3166-1 alpha-2 country code, such as `US`. |
| `geo.asn` | `eq`, `neq`, `in` | Autonomous System Number as a decimal string, such as `16276`. |
| `tls.ja3` | `eq`, `in`, `exists` | JA3 TLS fingerprint, a 32-character hexadecimal value. Origin logs expose it as `ja3_hash`. |
| `tls.ja4_stable` | `eq`, `in`, `exists` | JA4 fingerprint based on the sorted ClientHello. It remains stable when extensions are reordered. Origin logs expose it as `ja4_hash`. |
| `http.method` | `eq`, `neq`, `in` | HTTP method, such as `GET` or `POST`. |
| `http.host` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard` | Request Host header. |
| `http.path` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard` | Path without its query string. |
| `http.query` | `eq`, `neq`, `contains`, `starts_with`, `ends_with`, `wildcard` | Raw query string without the leading `?`. |
| `http.uri` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard` | Path and query string together. |
| `http.user_agent` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard`, `exists` | User-Agent header. |
| `http.referer` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard`, `exists` | Referer header. `exists` with `negate=true` matches its absence. |
| `http.header` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard`, `exists` | A named request header. Requires `key`. |
| `http.cookie` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard`, `exists` | A named cookie. Requires `key`. |
| `http.query.param` | `eq`, `neq`, `in`, `contains`, `starts_with`, `ends_with`, `wildcard`, `exists` | A named, percent-decoded query parameter. Requires `key`. If repeated, the last occurrence wins. |
| `http.path.extension` | `eq`, `neq`, `in`, `exists` | Lowercased final path extension without its dot, such as `pdf`. |

Use [origin web server logs](/docs/monitoring-logs/logs/web-server-logs/) when investigating the JA3 and JA4 fields above. Condition names differ from log field names. The Edge Logs endpoint has its own filters. Do not assume that every condition field is an Edge Logs filter.

## Operators

| Operator | Match |
| --- | --- |
| `eq` | Exact value. |
| `neq` | Not equal to the value. |
| `in` | Any entry in `values`. |
| `in_cidr` | Any network in `values`. Available only for `ip.src`. |
| `contains` | Substring. |
| `starts_with` | Prefix. |
| `ends_with` | Suffix. |
| `wildcard` | Glob pattern: `*` matches any run of characters; `\*` matches a literal asterisk. |
| `exists` | The field is present. Supply neither `value` nor `values`. |

The field table determines which operators are allowed. For example, `http.query` does not support `in`, and `geo.country` does not support `wildcard`.

## Combine conditions

Set `condition_logic` inside `rule_definition.input`:

- `all`, the default, requires every condition to match.
- `any` requires at least one condition to match.

`negate=true` reverses one condition, not the whole list. A single condition list does not express nested combinations. To match “path starts with `/shop` AND (a selected user agent OR no referer),” use two rules. One matches the path and user agent. The other matches the path and missing referer.

Review the resulting rules' order and actions together. A country-only or method-only rule can affect a large share of legitimate traffic.

## Input limits

| Input | Limit |
| --- | --- |
| Conditions per rule | 50 |
| String value | 4,096 bytes |
| Entries in `values` | 1,000 |
| Header names in one `remove` operation | 32 |
| Header, cookie, or query-parameter key | 128 bytes |

Use the catalog's current `matchers.limits` when building input validation. The [validation endpoint](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/validate) checks the complete rule before it is saved.

## Request-header placeholders

A [request-header rule](/docs/security/traffic-protection/edge-rule-types/#request-header) can use a literal value or exactly one placeholder as its entire value. Keyed fields use `{{field:name}}`:

```json
{"value":"{{geo.country}}"}
```

```json
{"value":"{{http.header:x-request-id}}"}
```

Use `matchers.placeholders` from the catalog for valid placeholder fields. Surrounding text, concatenation, and multiple placeholders are not supported. Response-header rules accept literal values only.
