# Clone a site

Clone a WP Cloud site by passing its site ID or domain in the Create Site operation's `clone_from` field. WP Cloud copies the source filesystem and database to a new site and rewrites the source domain to the destination domain by default.

## Create the clone

Send a `POST` request to the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}). This example uses a site ID for the source and sets the destination's `HOST_PLAN` Persistent Data value:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "domain_name=${DESTINATION_DOMAIN}" \
  --data-urlencode "admin_user=${WP_CLOUD_ADMIN_USER}" \
  --data-urlencode "admin_email=${WP_CLOUD_ADMIN_EMAIL}" \
  --data-urlencode 'software[themes/twentytwentyfive/latest]=activate' \
  --data-urlencode "clone_from=${SOURCE_SITE_ID}" \
  --data-urlencode 'persist_data[HOST_PLAN]=business' \
  "https://atomic-api.wordpress.com/api/v1.0/create-site/${WP_CLOUD_CLIENT}"
```

The accepted response contains the new site ID and a clone response ticket ID:

```json
{
  "message": "OK",
  "data": {
    "job_id": 1234,
    "atomic_site_id": 5678,
    "domain_name": "staging.example.com",
    "response_ticket_id": "<response-ticket-id>"
  }
}
```

### Monitor clone completion

Save `response_ticket_id` from the Create Site response. The response confirms that WP Cloud accepted the request, not that the clone has finished. Use the response ticket to track clone completion; the provisioning `job_id` is not a reliable clone-completion signal.

Poll the [Get Response Ticket Summary endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/summary). Replace `<response-ticket-id>` with the returned ticket ID:

```bash
export WP_CLOUD_RESPONSE_TICKET_ID='<response-ticket-id>'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "response-ticket-id=${WP_CLOUD_RESPONSE_TICKET_ID}" \
  "https://atomic-api.wordpress.com/api/v1.0/response-ticket/get/summary"
```

| Summary `data.status` | Meaning and next action |
| --- | --- |
| `null` | The clone is queued or running. Continue polling; this value does not distinguish clone phases. |
| `success` | The clone has completed. Continue with destination-site setup and verification. |
| `failure` | The clone failed. Stop dependent setup and inspect the ticket details. |

If the endpoint returns HTTP 202, the ticket has not received a response yet. Wait one second before querying it again. Do not start site-scoped setup, including separate Persistent Data updates, until the clone ticket reports `success`.

Use summary mode for routine polling because it is lighter and faster. Use the [Get Response Ticket Details endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/full) only when you need progress messages to investigate a slow or failed clone. Retain the destination site ID and response ticket ID for troubleshooting.

A clone copies WordPress users and application data from the source database. The `admin_user`, `admin_email`, and `admin_pass` fields in the Create Site request do not replace the copied users. Change credentials after provisioning when the destination needs different access.

### Set Persistent Data for the destination

A clone is a new site. It does not inherit the source site's [Persistent Data](/docs/sites/persistent-data/). Supply destination values with `persist_data` in the same Create Site request as `clone_from`, as shown above. No follow-up Persistent Data call is needed to apply those values to the cloned site.

| Create Site clone request | Destination Persistent Data |
| --- | --- |
| `persist_data` supplied | The new values supplied in the request, even when the source has existing Persistent Data. |
| `persist_data` omitted | `null`, even when the source has existing Persistent Data. The source values are not copied. |

Set required destination site-meta values explicitly as well. Do not assume that source-specific partner metadata carries over to the new site.

After the clone response ticket reports `success`:

- record the destination's new Atomic Site ID and domain, and confirm that the site is available;
- review its site meta, resource settings, access, and [Persistent Data](/docs/sites/persistent-data/), and confirm that site code receives the intended values;
- update the partner's local inventory or customer mapping to use the new Atomic Site ID; and
- review [WordPress multisite](/docs/wordpress/multisite/) configuration when cloning a network, because cloning does not rewrite every multisite constant or database value.

A high configured `space_quota` can prevent a clone even when the source currently uses much less storage. Compare the source configuration and destination capacity when a clone is rejected for space.

### Review Edge Rules (closed beta)

For accounts in the Edge Rules closed beta, inspect the destination's copied rules before sending traffic to it. The [Edge Rules cloning options](/docs/edge/edge-rules/overview/#cloning-and-domain-changes) control copying, primary-domain retargeting, and disabling copied rules for review.

### Optionally skip the automatic URL rewrite

Skipping the automatic URL rewrite is optional and uncommon. WP Cloud normally searches the cloned database and replaces the source domain with the destination domain. For a large site, `skip_db_rewrite=1` can shorten provisioning, but the copied database will still contain the source URLs. The rewrite runs by default, so leave out `skip_db_rewrite` to keep it. Sending `0` has the same effect but is not needed. Any other non-empty value, including `false`, skips the rewrite.

The WP Cloud host partner is responsible for performing and checking all required URL replacements when it uses this option. If the partner makes this option available to its customers, it must ensure that each end-user site's URLs are properly rewritten before the cloned site is put into use.
