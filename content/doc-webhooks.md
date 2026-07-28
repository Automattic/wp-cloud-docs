# Webhooks

WP Cloud sends webhooks when asynchronous platform work or a site event reaches a state that a partner may need to handle. For example, `site_provisioned` tells a partner that provisioning finished and its post-provisioning setup can begin.

Webhook signing and validation are available to verify that events came from WP Cloud.

Build the receiver to accept event types and data fields it does not recognize. WP Cloud can add events, and each event type can carry different data.

## Configure the webhook URL

Set one HTTPS receiver URL for the WP Cloud host client account with the `webhook_url` client meta key. Add it with the [Add Client Metadata endpoint](https://wp.cloud/docs/api/#tag/client-meta/POST/client-meta/{client}/{key}/add):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'value=https://partner.example/webhooks/wp-cloud' \
  "https://atomic-api.wordpress.com/api/v1.0/client-meta/${WP_CLOUD_CLIENT}/webhook_url/add"
```

If the key already exists, use the [Update Client Metadata endpoint](https://wp.cloud/docs/api/#tag/client-meta/POST/client-meta/{client}/{key}/update). Use the Remove Client Metadata operation when the account should no longer receive webhooks.

The receiver should return HTTP 200 after it accepts an event. That response confirms delivery to the configured receiver; it does not prove that later application processing succeeded. A non-200 response causes WP Cloud to schedule up to two more delivery attempts.

## Read webhook events

Every webhook has an `event`, `timestamp`, and event-specific `data` value:

```json
{
  "timestamp": 1751333700,
  "event": "site_provisioned",
  "atomic_site_id": 123456789,
  "data": []
}
```

`atomic_site_id` is present when the event applies to a particular site. The shape of `data` depends on the event. Store the complete event before dispatching known event types so an unfamiliar event or added field does not make the receiver fail.

WP Cloud currently sends events including:

- `site_provisioned` when site provisioning finishes;
- `over_quota` for a site over its storage quota;
- `domain_name_changed` after a primary domain or alias change;
- `wp_version_changed` after a requested switch between managed WordPress version channels;
- `on-demand-backup`, with data for acknowledged, created, and deleted states;
- `chroot_updates`;
- `tasks`; and
- `sasl_block` for email abuse detection blocks.

The list can change. Do not reject a webhook only because its event name is not in this list.

## Interpret common events

The event name identifies what changed, while the event-specific `data` object provides the values needed to interpret it. The examples below show how that data changes by event.

### Site provisioned

```json
{
  "event": "site_provisioned",
  "timestamp": 1751333700,
  "atomic_site_id": 123456789,
  "data": []
}
```

### Primary domain or alias changed

```json
{
  "event": "domain_name_changed",
  "timestamp": 1751333848,
  "atomic_site_id": 123456789,
  "data": {
    "passed_old": "old.example.com",
    "passed_new": "new.example.com",
    "then_api_current": "new.example.com",
    "then_db_siteurl": "old.example.com"
  }
}
```

### WordPress version changed

```json
{
  "event": "wp_version_changed",
  "timestamp": 1751334043,
  "atomic_site_id": 123456789,
  "data": {
    "version": "previous"
  }
}
```

`wp_version_changed` reports a version-channel change requested through WP Cloud, such as switching from `latest` to `previous`. It does not report every WordPress release installed behind the `latest` channel.

## Sign webhook events

Set a secret `webhook_hmac_key` with the Add Client Metadata endpoint. Choose a strong, random value and store it in the same secrets system used by the receiver:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode "value=${WP_CLOUD_WEBHOOK_HMAC_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/client-meta/${WP_CLOUD_CLIENT}/webhook_hmac_key/add"
```

After the key is set, each payload includes a `signature` object:

```json
{
  "signature": {
    "signature": "011958d09315f3b...92ab98e4ad12",
    "timestamp": "29848839199040411",
    "salt": "3cfd5d7d47e...b3f79d8890bd9b344db0"
  }
}
```

The HMAC key is write-only. The API cannot return its value after it is set, but a partner can update or remove it.

## Validate webhook signatures

For each signed payload:

1. Read the top-level `event` as the event type and the `timestamp` and `salt` values inside `signature`.
2. Construct this input string exactly: `{event_type}:{signature->timestamp}:{signature->salt}`.
3. Compute an HMAC-SHA256 digest of that string with the account's `webhook_hmac_key`.
4. Compare the computed digest with `signature->signature`. Process the event only when they match.

Treat `signature->timestamp`, `signature->salt`, and `signature->signature` as strings. In particular, do not convert the timestamp to a JavaScript number before constructing the input string; doing so can change its value and make a valid signature fail.

If events do not arrive, compare the receiver URL with the configured `webhook_url`, check the receiver's deployment, authentication, and routing, and review the HTTP status it returned at the event time. A successful delivery does not imply that WP Cloud will replay the event after a later processing failure, so store accepted events before processing them.

Update or remove the key with the corresponding Client Metadata operation. Coordinate a planned key change with the receiver because events signed with the new key will fail validation anywhere that still uses the old value.
