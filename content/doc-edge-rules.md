# Edge Rules

**Closed beta:** Edge Rules is available only to enabled WP Cloud partner accounts. This documentation is a preview. Requests from accounts that are not enabled receive HTTP `403`.

Edge Rules control HTTP traffic at WP Cloud's edge before it reaches a site's origin server. Partners can block or challenge requests, redirect or rewrite URLs, change headers, and bypass Edge Cache. The partner's API integration creates and manages rules for its sites and can expose those controls in its own panel.

Use the [rule-type reference](/docs/security/traffic-protection/edge-rule-types/) to choose an action and the [conditions reference](/docs/security/traffic-protection/edge-rule-conditions/) to select matching requests. [Verify Edge Rules](/docs/security/traffic-protection/verify-edge-rules/) explains how to check deployment and request behavior.

## Discover available rule types

The [Edge Rule catalog](https://wp.cloud/docs/api/#tag/edge-rules/GET/edge-rule-catalog) returns the types available to the calling API key. Availability depends on the partner account and the key's access. An entry that is not enabled for the caller is omitted. Custom rules require separate enablement and appear only when available.

Each `data.catalog` entry describes its `rule_key`, phase, supported scopes, risk, and verification method. Its `input_schema` defines `rule_definition.input`, including defaults; `constraints` describes additional validation rules. `data.matchers` describes condition fields, operators, limits, ordering, and request-header placeholders.

Build partner controls from the returned catalog rather than assuming that every account has the same types or inputs.

## Choose the scope and order

| Scope | Applies to |
| --- | --- |
| `site` | Every current and future domain attached to the site. This is the default when creating a rule. |
| `domain` | One domain attached to the site. Supply `scope=domain` and `domain_name`. |

The domain helper path `/site-edge-rules/{site}/domains/{domain}/rules/...` fixes the scope and target domain. A conflicting scope or domain parameter is rejected. The domain must belong to the site.

Requests pass through these phases in order: redirect, rewrite, security, request headers, cache, and response headers. A rule's type determines its phase. In redirect, rewrite, and security phases, the first matching rule acts and evaluation of that phase stops. Header and cache rules apply in sequence. The last applied value stands.

`rule_order` ranges from `0` through `65535`, with a default of `0`. Within the same phase and scope, lower values take precedence. They are evaluated first in first-match phases and applied last in header/cache phases. Ties are deterministic. The default list response sorts by scope, domain name, and rule name. That display order does not describe request evaluation.

## Create and verify a first rule

Use a non-production site in an enabled account. You need an API key authorized for the relevant endpoints and the site's Atomic Site ID. The [API quick start](/docs/api-automation/api-quick-start/) explains authentication and example variables.

This example sets a response header only for `/edge-rule-check`. Check the catalog before using it. Creating the rule changes responses for matching traffic. Choose a test path and domain you control.

1. Set the example values and retrieve the catalog:

   ```bash
   export WP_CLOUD_API_KEY='<api-key>'
   export WP_CLOUD_SITE_ID='<site-id>'
   export WP_CLOUD_TEST_DOMAIN='test.example.com'

   curl --fail-with-body --silent --show-error \
     --header "Auth: ${WP_CLOUD_API_KEY}" \
     'https://atomic-api.wordpress.com/api/v1.0/edge-rule-catalog'
   ```

2. Confirm that `managed.response_header` is available, then prepare its definition:

   ```bash
   WP_CLOUD_RULE_DEFINITION='{"version":1,"input":{"operation":"set","header":"X-Edge-Rule-Check","value":"enabled","conditions":[{"field":"http.path","op":"eq","value":"/edge-rule-check"}]}}'
   ```

3. Send the definition to [Validate a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/validate):

   ```bash
   curl --fail-with-body --silent --show-error \
     --request POST \
     --header "Auth: ${WP_CLOUD_API_KEY}" \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --data-urlencode 'rule_key=managed.response_header' \
     --data-urlencode "rule_definition=${WP_CLOUD_RULE_DEFINITION}" \
     "https://atomic-api.wordpress.com/api/v1.0/site-edge-rules/${WP_CLOUD_SITE_ID}/rules/validate"
   ```

   Validation does not save a rule or queue a deployment. A successful response has `data.valid=true` and a `normalized_rule_definition`. Resolve validation errors before creating or updating a rule. The API can report field details in `data.errors`.

4. Create the rule with [Add a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/add):

   ```bash
   curl --fail-with-body --silent --show-error \
     --request POST \
     --header "Auth: ${WP_CLOUD_API_KEY}" \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --data-urlencode 'rule_name=edge-rule-check' \
     --data-urlencode 'rule_key=managed.response_header' \
     --data-urlencode "rule_definition=${WP_CLOUD_RULE_DEFINITION}" \
     "https://atomic-api.wordpress.com/api/v1.0/site-edge-rules/${WP_CLOUD_SITE_ID}/rules/add"
   ```

   Send form-encoded fields. `rule_definition` is a JSON-encoded string within that form, rather than a top-level JSON request body. The rule is site-scoped unless you select a domain scope.

5. Save the returned `data.response_ticket` and `data.rule.atomic_edge_rule_id`. The accepted response means the change is stored and queued, not yet applied. Set the ticket value and poll the [Get Response Ticket Summary endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/summary):

   ```bash
   export WP_CLOUD_RESPONSE_TICKET_ID='<response-ticket>'

   curl --fail-with-body --silent --show-error \
     --request POST \
     --header "Auth: ${WP_CLOUD_API_KEY}" \
     --data-urlencode "response-ticket-id=${WP_CLOUD_RESPONSE_TICKET_ID}" \
     'https://atomic-api.wordpress.com/api/v1.0/response-ticket/get/summary'
   ```

   Continue waiting while `data.status` is `null`. Wait for `success` before testing the change. On `failure`, stop and inspect the ticket details. HTTP `202` from the summary endpoint means no response has arrived yet. Wait one second before querying again.

6. Follow [Verify Edge Rules](/docs/security/traffic-protection/verify-edge-rules/) to read the current edge state and request the matching URL. Check for `X-Edge-Rule-Check: enabled`, then disable or delete the test rule when finished.

## Manage rules and limits

Use an `atomic_edge_rule_id` or a `rule_name` when addressing a rule. Names can occur at different targets. Use the numeric ID or disambiguate with the documented scope/domain parameters. An ID from another target returns `404`.

| API reference | Effect |
| --- | --- |
| [List site edge rules](https://wp.cloud/docs/api/#tag/edge-rules/GET/site-edge-rules/{site}/rules) | Shows site and domain rules affecting the site. Filter by scope, domain, or phase. `sort=updated` shows recent changes first. |
| [Get a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/GET/site-edge-rules/{site}/rules/{rule}) | Returns the stored rule and its resolved edge state unless verification is skipped. |
| [Update a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/{rule}/update) | Changes `rule_definition`, `rule_order`, `description`, or `desired_state` (`enabled` or `disabled`). |
| [Enable a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/{rule}/enable) | Queues an enabled rule, including recovery of a suspended rule. |
| [Disable a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/{rule}/disable) | Removes its effect from the edge while retaining its stored definition. |
| [Delete a site edge rule](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/{rule}/delete) | Deletes the stored rule and queues removal from the edge. Retain the definition separately if you may need to recreate it. |

`rule_name`, `rule_key`, `scope`, owner, and target fields are immutable. Delete and recreate a rule to change them. Rule names must match `[a-z0-9][a-z0-9_-]{0,190}` and cannot be all numeric. The action names `add`, `validate`, `preview`, `bulk`, `suspend-all`, and `restore-all` are reserved. Descriptions can contain at most 255 characters.

The list is a cross-scope view, not a site-only collection. It can also show visible WP Cloud-owned rules, which the partner cannot modify. The `managed.*` prefix identifies a catalog type. It does not make a partner-created instance WP Cloud-owned.

Default quotas are 20 rules per site and five per domain. Read `data.quota` for usage and limits. A domain-filtered listing also reports that domain's quota. A duplicate name or duplicate normalized configuration at the same target returns `409`. Exceeding quota also returns `409`. Contact [WP Cloud Support](/docs/getting-started/get-support/) to discuss limits for your account.

## Apply a batch of changes

The [Bulk site edge rule operations endpoint](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/bulk) accepts one through 100 create, update, or delete operations. It returns per-item results and one reconciliation ticket for accepted work.

Inspect every result. Invalid items can be rejected while valid items apply. If none are accepted, the response is `400` and no ticket is issued. A batch whose net effect exceeds a target's quota is rejected in full with `409`. Its results still report individual validation outcomes.

Accepted deletes apply first, followed by updates and then creates, in submission order within each group. A batch can reuse a name or configuration removed by one of its deletes. When an update releases a configuration for another item to reuse, place that update before the reuse. Duplicate checks also apply within the submitted batch.

## Suspend rules during an incident

Disabling rules can restore legitimate traffic, but it also removes their protection. First identify the affected site and preserve the rule definitions and observed behavior.

The [Suspend all site rules endpoint](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/suspend-all) marks enabled, partner-owned rules on the site as `suspended`. Already-disabled rules and WP Cloud-owned rules are untouched. Suspension is queued ahead of normal reconciliation traffic, but still requires completion checks.

Re-enable individual rules to isolate the problem, or use [Restore suspended site rules](https://wp.cloud/docs/api/#tag/edge-rules/POST/site-edge-rules/{site}/rules/restore-all) to return suspended rules to `enabled`. Rules disabled before suspension remain disabled. Do not set `desired_state=suspended` through the update endpoint. Use suspend-all.

## Cloning and domain changes

Site-scoped rules apply to the site's domains. Domain-scoped rules follow their domain when it moves within the same partner account. Rules for a removed domain are cleaned up automatically.

The [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}) provides these options when [cloning a site](/docs/sites/cloning/):

| Parameter | Behavior |
| --- | --- |
| `edge_rules_skip` | `1` skips copying site-scoped rules. The default is `0`. |
| `edge_rules_domain_disposition` | `retarget_primary` (default) copies the source primary-domain rules onto the destination primary domain and drops alias-domain rules. `leave` skips domain-scoped rules during cloning, for a rollback workflow that moves the real domain separately afterward. |
| `edge_rules_copy_disabled` | `1` forces all copied rules to `disabled` for review. The default, `0`, preserves their states. |

Review the destination's rules and domains after clone completion. A rule appropriate for production can block a staging test or affect the wrong URLs after a domain change.
