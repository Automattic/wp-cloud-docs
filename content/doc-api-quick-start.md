# WP Cloud API quick start

Use the WP Cloud API to create and inspect sites, manage domains and certificates, change common site settings, and work with access and backups. The examples use `curl`, show representative responses, and link each operation to the current [WP Cloud API reference](https://wp.cloud/docs/api/).

The examples use a non-production site. Some operations change or delete a site, so check the site ID and domain before running them.

## Requirements

You need:

- your WP Cloud client identifier;
- a developer API key;
- a static IP address or Classless Inter-Domain Routing (CIDR) range included in the key's allowed IP list;
- a non-production domain that you control; and
- `curl` on the system making the requests.

Use a developer key for manual testing. Use a platform key only in the production service that manages your hosting product. Do not paste either key into source code, screenshots, shell history, or support requests.

Use separate keys for a production panel, test automation, and individual developers. [Manage and secure API keys](/docs/api-automation/api-access/) explains where to create or request a key, the current Partner Portal fields and IP-range limits, and how to replace or revoke a key without unexpectedly interrupting its users. Static office gateways, private VPNs, proxy servers, automation servers, and bastion hosts are suitable. Home internet connections with changing addresses, public Wi-Fi, and consumer VPNs are not.

## Set the example values

Set environment variables for the values used throughout the examples:

```bash
export WP_CLOUD_CLIENT='<client-identifier>'
export WP_CLOUD_API_KEY='<developer-api-key>'
export WP_CLOUD_DOMAIN='<unused-test-domain>'
export WP_CLOUD_ALIAS='<secondary-test-domain>'
export WP_CLOUD_ADMIN_USER='<wordpress-admin-username>'
export WP_CLOUD_ADMIN_EMAIL='<wordpress-admin-email>'
export WP_CLOUD_WEBHOOK_URL='https://panel.example.com/webhooks/wp-cloud'
```

The client identifier is the lowercase identifier assigned to the partner account. It is not a site ID or domain. Replace every placeholder before running a request.

All requests authenticate with the `Auth` header:

```bash
--header "Auth: ${WP_CLOUD_API_KEY}"
```

## Set up Client SSH access

[Client SSH](/docs/site-access/ssh-sftp/client-ssh/) gives a partner's developers, support teams, panels, and automation full SSH and SFTP access to a selected partner site. Before using it, configure the partner's authorized public keys and strongly consider restricting connections to stable, known network addresses. The Client SSH article covers key aliases, the client firewall, per-key address rules, and connection examples.

## Configure webhooks for production

Webhooks let your integration respond when an asynchronous WP Cloud operation finishes or a site changes. Configure an HTTPS receiver before moving an integration to production, and allow it to accept event names and data fields it does not yet recognize.

Set the receiver URL with the [Add Client Metadata endpoint](https://wp.cloud/docs/api/#tag/client-meta/POST/client-meta/{client}/{key}/add):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "value=${WP_CLOUD_WEBHOOK_URL}" \
  "https://atomic-api.wordpress.com/api/v1.0/client-meta/${WP_CLOUD_CLIENT}/webhook_url/add"
```

Example response:

```json
{
  "message": "OK",
  "data": []
}
```

If `webhook_url` already exists, replace it with the [Update Client Metadata endpoint](https://wp.cloud/docs/api/#tag/client-meta/POST/client-meta/{client}/{key}/update). The receiving endpoint should return HTTP 200 after it accepts an event. A non-200 response causes WP Cloud to schedule up to two more delivery attempts.

Webhook payloads include an `event`, `timestamp`, and `data`, and most site-specific events also include an `atomic_site_id`. Common events include:

- `site_provisioned` when requested site provisioning completes;
- `over_quota` when a site is over its quota; and
- `domain_name_changed` when a site's primary domain changes.

WP Cloud sends additional event types, so do not reject an event only because your integration does not act on it. HMAC signing is also available for production integrations that need to verify webhook authenticity; the dedicated Webhooks documentation will cover its configuration and validation.

## Create a site

Send a `POST` request to the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "domain_name=${WP_CLOUD_DOMAIN}" \
  --data-urlencode "admin_user=${WP_CLOUD_ADMIN_USER}" \
  --data-urlencode "admin_email=${WP_CLOUD_ADMIN_EMAIL}" \
  --data-urlencode 'software[themes/twentytwentyfive/latest]=activate' \
  "https://atomic-api.wordpress.com/api/v1.0/create-site/${WP_CLOUD_CLIENT}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "job_id": 1234,
    "atomic_site_id": 5678,
    "domain_name": "test.example.com"
  }
}
```

The response confirms that WP Cloud accepted the request. It does not mean provisioning has finished. Save the returned identifiers for later requests:

```bash
export WP_CLOUD_JOB_ID='1234'
export WP_CLOUD_SITE_ID='5678'
```

The site ID is the stable identifier for the site. Keep it after changing the site's primary domain.

### Create Site parameters

The example uses only the fields needed for a working test site. The endpoint also accepts the following parameters:

- `domain_name` sets the site's primary domain. Some clients can use `demo_domain` to request a generated demo domain instead.
- `admin_user`, `admin_email`, and the optional `admin_pass` configure the first WordPress administrator.
- `db_charset` accepts `latin1`, `utf8`, or `utf8mb4`. The current default is `utf8mb4`.
- `db_collate` must match the selected character set. Supported values are `latin1_swedish_ci`, `utf8_general_ci`, and `utf8mb4_general_ci`.
- `php_version` selects an available PHP version. Use the [Get PHP Versions endpoint](https://wp.cloud/docs/api/#tag/servers/GET/get-php-versions/{client}[/verbose]) rather than keeping a version list in your integration.
- `wordpress-version` selects the `latest`, `previous`, or `beta` managed WordPress track for a fresh site.
- `space_quota` sets the storage quota with a value such as `50G`. The current default is `200G`.
- `software[...]` installs, activates, deactivates, locks, unlocks, or removes plugins and themes. Keys use paths such as `plugins/akismet/latest` and `themes/twentytwentyfive/latest`.
- `clone_from` creates the site from another WP Cloud site ID or domain.
- `restore_from` accepts one filesystem backup ID and one database backup ID. Do not combine it with `clone_from`.
- `firewall_profile`, `geo_affinity`, `persist_data`, and `meta[...]` set supported platform and site options during provisioning.

The API reference lists the accepted combinations, current enums, and fields that cannot be used during a clone or restore.

## Check the provisioning job

Use the returned job ID with the [Get Job Statuses endpoint](https://wp.cloud/docs/api/#tag/jobs/GET/job-status/{id}):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/job-status/${WP_CLOUD_JOB_ID}"
```

Example response after provisioning succeeds:

```json
{
  "message": "OK",
  "data": {
    "_status": "success",
    "id": "1234"
  }
}
```

Wait while `_status` is `queued` or running. Continue only after it reports `success`. If it reports `failure`, retain the job ID and complete response while investigating the failure.

## Retrieve the site

After the job succeeds, request the site record from the [Get Site Details endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-site/{site}[/extra]):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-site/${WP_CLOUD_SITE_ID}"
```

Example response, shortened to the fields needed here:

```json
{
  "message": "OK",
  "data": {
    "atomic_site_id": 5678,
    "domain_name": "test.example.com",
    "db_charset": "utf8mb4",
    "db_collate": "utf8mb4_general_ci",
    "php_version": "8.4",
    "wp_admin_user": "test-admin",
    "wp_admin_email": "admin@example.com"
  }
}
```

Confirm that `atomic_site_id` and `domain_name` match the values returned by the create request. The complete response may contain credentials and internal site details. Do not log it or return it through a customer-facing interface.

## Review site defaults

The Create Site endpoint currently defaults to PHP 8.4, the latest managed WordPress track, the `utf8mb4` database character set, a matching collation, a 200 GB storage quota, and a 512 MB PHP memory limit when those values are not supplied.

WP Cloud sites also use site meta for PHP connection limits, bursting, resource limits, and partner-specific `_data`. Set the following values explicitly when your hosting product requires something different from the platform defaults:

- `default_php_conns` sets the site's normal concurrent PHP connection limit.
- `burst_php_conns` controls whether a site configured below the platform default can use additional available PHP connections.
- `php_memory_limit` accepts `512`, `1024`, `1536`, or `2048`, in megabytes.
- `space_quota` sets the storage quota.
- `_data` stores partner site metadata, including the versioned `site_type` value used for billing classification.

Sites without a `site_type` value in `_data` are treated as billable. Check these settings during provisioning instead of relying on a partner panel to add them later.

Use the [Manage Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}) to change a supported value after provisioning. The API reference identifies which meta keys can be set during site creation and which require an existing site.

## Work with domains

A site has one primary domain and can have secondary domains. Secondary domains normally redirect to the primary domain.

[Manage site domains and aliases](/docs/sites/domains/manage-domains-aliases/)
covers the complete domain workflow, including eligibility checks, DNS
addresses, secondary domains, and primary-domain changes. The examples below
show those operations as part of the end-to-end API quick start.

### Add, list, and remove aliases

Use the [Manage Site Aliases endpoint](https://wp.cloud/docs/api/#tag/sites/GET/site-alias/{service}/{identifier}/{action}/{domain}) to add a secondary domain:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-alias/domain/${WP_CLOUD_DOMAIN}/add/${WP_CLOUD_ALIAS}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "domains": ["www.test.example.com"]
  }
}
```

List the current aliases:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-alias/domain/${WP_CLOUD_DOMAIN}/list"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "domains": ["www.test.example.com"]
  }
}
```

Remove an alias:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-alias/domain/${WP_CLOUD_DOMAIN}/remove/${WP_CLOUD_ALIAS}"
```

A successful response returns the aliases that remain on the site.

### Retrieve the domain IP addresses

Use the [Get Client IP Addresses endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-ips/{client}/{domain}) to retrieve the WP Cloud address range and suggested A record addresses for a domain:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-ips/${WP_CLOUD_CLIENT}/${WP_CLOUD_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "ips": ["192.0.78.128/25"],
    "suggested": ["192.0.78.150", "192.0.78.200"]
  }
}
```

Use the `suggested` addresses for the domain's A records unless your partner configuration specifies otherwise.

### Change the primary domain

Add and verify the new domain as an alias before promoting it. Send a `POST` request to the [Update Site Domain endpoint](https://wp.cloud/docs/api/#tag/sites/POST/update-site-domain/{service}/{identifier}/{domain}/{keep}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/update-site-domain/domain/${WP_CLOUD_DOMAIN}/${WP_CLOUD_ALIAS}/keep"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "job_id": 2345,
    "atomic_site_id": 5678,
    "domain_name": "www.test.example.com",
    "old_domain_name": "test.example.com"
  }
}
```

The old primary domain remains as an alias by default. Pass `false` instead of `keep` to remove it. Check the returned job before updating DNS or dependent systems.

### Check for domain collisions

Call the [Validate Domain Eligibility endpoint](https://wp.cloud/docs/api/#tag/sites/GET/check-can-host-domain/{client}/{domain}) before creating a site or adding an alias:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/check-can-host-domain/${WP_CLOUD_CLIENT}/${WP_CLOUD_DOMAIN}"
```

An available domain returns:

```json
{
  "message": "OK",
  "data": {
    "allowed": true
  }
}
```

A restricted domain or one already assigned elsewhere returns a message explaining why it cannot be used. A domain assigned to another WP Cloud client may require Domain Name System (DNS) TXT verification:

```json
{
  "message": "Domain name already used [test.example.com]. TXT record verification is required to bypass this check.",
  "data": []
}
```

Request the TXT value from the [Get Domain Verification Code endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-domain-verification-code/{client}/{domain}):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-domain-verification-code/${WP_CLOUD_CLIENT}/${WP_CLOUD_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": "atomic-domain-<verification-code>"
}
```

Publish the returned value as the required TXT record, wait for DNS propagation, and repeat the eligibility check.

## Check TLS certificates

WP Cloud provisions Let's Encrypt certificates for a site's domains. Use the [Fetch SSL Certificate Information endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-info/{domain}) to inspect a domain:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssl-info/${WP_CLOUD_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "force_ssl": "2304",
    "acme_certificate_id": "3137610",
    "validation_expiration": "2026-08-17 16:20:33",
    "options": ["ACME_OPT_HSTS_1D", "ACME_OPT_REDIRECT_TO_HTTPS"],
    "certificate_expiration_date": "2026-10-16 15:20:41",
    "broken_record": null
  }
}
```

If `broken_record` reports a provisioning failure and the domain's DNS is correct, queue another attempt with the [Retry SSL Provisioning endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-retry/{domain}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssl-retry/${WP_CLOUD_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "queued": true
  }
}
```

## Audit sites

Use the [List Client Sites endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+) to inventory the sites assigned to a client:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-sites/${WP_CLOUD_CLIENT}"
```

Example response, shortened for readability:

```json
{
  "message": "OK",
  "data": [
    {
      "atomic_site_id": "5678",
      "domain_name": "test.example.com",
      "created": "2026-07-16 14:00:00",
      "space_used": "10240"
    }
  ]
}
```

Append supported meta keys to the request path when an audit needs them. This example adds the PHP version, PHP connection limit, and partner `_data`:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-sites/${WP_CLOUD_CLIENT}/php_version/default_php_conns/_data"
```

WP Cloud may create canary sites in a client account to test platform and client-configuration changes. Do not remove a canary site. Its `site_type` identifies it as a platform-managed canary rather than a customer site.

Use the [Get Site Details endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-site/{site}[/extra]) for one site. You can identify the site by domain or site ID. The complete response may include decrypted database credentials, so restrict and redact its output.

## Manage sites

The following examples cover common operations from the original quick start. Each operation has its own endpoint reference for current fields, response schemas, and error states.

### Manage plugins and themes

Send form-encoded software paths and actions to the [Manage Site Software endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'plugins/woocommerce/latest=activate' \
  "https://atomic-api.wordpress.com/api/v1.0/site-manage-software/atomic/${WP_CLOUD_SITE_ID}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "job_id": 3456,
    "response_ticket_id": "abcd"
  }
}
```

Check the returned operation identifier before assuming the plugin or theme change has finished.

### Suspend and unsuspend a site

The [Manage Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/GET/site-meta/{site}/{key}/{action}) returns the current suspension value:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/suspended/get"
```

An unsuspended site normally returns:

```json
{
  "message": "OK",
  "data": null
}
```

Suspend the site with one of the supported HTTP status codes: `403`, `404`, `410`, `451`, `480`, or `503`.

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'value=451' \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/suspended/update"
```

Example response:

```json
{
  "message": "OK",
  "data": []
}
```

Confirm the public response:

```bash
curl --head "https://${WP_CLOUD_DOMAIN}"
```

The first response line should contain the selected status, such as:

```text
HTTP/2 451
```

Status `480` disables web access while retaining SFTP and phpMyAdmin access for export work. Remove the suspension when the site should serve web traffic again:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/suspended/remove"
```

### Change the PHP version

List the versions available to the client with the [Get PHP Versions endpoint](https://wp.cloud/docs/api/#tag/servers/GET/get-php-versions/{client}[/verbose]):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-php-versions/${WP_CLOUD_CLIENT}"
```

Example response:

```json
{
  "message": "OK",
  "data": ["8.2", "8.3", "8.4", "8.5"]
}
```

Read the site's current value:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/php_version/get"
```

Example response:

```json
{
  "message": "OK",
  "data": "8.4"
}
```

Set a supported version with the [Manage Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'value=8.3' \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/php_version/update"
```

### Delete a site

**Warning:** Deleting a site is destructive. Confirm the site ID and domain, and preserve any required backups before continuing.

Send a `POST` request to the [Delete Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/delete-site/{service}/{identifier}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/delete-site/domain/${WP_CLOUD_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "job_id": 9876
  }
}
```

The response means the deletion request was accepted. Check the returned job ID until it succeeds or fails.

## Use common site operations

### Reset a database password

If a site can no longer connect because its managed database password was changed, send a `POST` request to the [Reset Database Password endpoint](https://wp.cloud/docs/api/#tag/sites/POST/reset-db-password/{type}/{site}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/reset-db-password/atomic/${WP_CLOUD_SITE_ID}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "job_id": 4567
  }
}
```

Check the returned job and retrieve the site's current managed credentials after it succeeds.

### Manage SSH and SFTP users

WP Cloud supports password and public-key authentication for site SSH and SFTP users. Usernames must be unique across WP Cloud, so include a partner or site identifier in each name. [User SSH and SFTP access](/docs/site-access/ssh-sftp/user-ssh-sftp/) covers credential options, the SFTP-only default, connection examples, and access limits.

The [Create or Update Public Key endpoint](https://wp.cloud/docs/api/#tag/ssh/POST/alias-pkey/set/{client}/{category}/{name}) stores a reusable public-key alias. Sites and client authorized-key records that reference the alias use its updated key without changing every reference separately.

Create a user with the [Add Site SSH/SFTP User endpoint](https://wp.cloud/docs/api/#tag/ssh/POST/ssh-user/{service}/{identifier}/add):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'user=example-client-test-5678' \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/add"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "user": "example-client-test-5678",
    "pass": "<generated-password>"
  }
}
```

List users with the [List Site SSH/SFTP Users endpoint](https://wp.cloud/docs/api/#tag/ssh/GET/ssh-user/{service}/{identifier}/list):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/list"
```

Example response:

```json
{
  "message": "OK",
  "data": ["example-client-test-5678"]
}
```

Remove the user with the [Remove Site SSH/SFTP User endpoint](https://wp.cloud/docs/api/#tag/ssh/POST/ssh-user/{service}/{identifier}/remove/{username}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/remove/example-client-test-5678"
```

Example response:

```json
{
  "message": "OK",
  "data": []
}
```

### Create a phpMyAdmin URL

Use the [Get Site phpMyAdmin URL endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-phpmyadmin/{site}) to create a time-limited login URL:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-phpmyadmin/${WP_CLOUD_SITE_ID}"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "url": "https://test.example.com/_pma_login?timestamp=<timestamp>&nonce=<nonce>&token=<token>"
  }
}
```

Treat the URL as a credential. Do not log, cache, or reuse it. See [phpMyAdmin](/docs/site-access/database-access/phpmyadmin/) for the complete access workflow and database-change precautions.

### List and download backups

Use the [List Site Backups endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backups-list/{service}/{identifier}) to retrieve filesystem and database backups:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-backups-list/domain/${WP_CLOUD_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": [
    {
      "atomic_backup_id": "1234",
      "atomic_site_id": "5678",
      "backup_timestamp": "2026-07-16 00:00:00",
      "type": "db"
    },
    {
      "atomic_backup_id": "1235",
      "atomic_site_id": "5678",
      "backup_timestamp": "2026-07-16 00:00:00",
      "type": "fs"
    }
  ]
}
```

Pass an `atomic_backup_id` to the [Get Site Backup Data endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backup-get/{service}/{identifier}/{backup_id}):

```bash
export WP_CLOUD_BACKUP_ID='1234'

curl --fail --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --output "${WP_CLOUD_SITE_ID}-${WP_CLOUD_BACKUP_ID}-db.sql.gz" \
  "https://atomic-api.wordpress.com/api/v1.0/site-backup-get/domain/${WP_CLOUD_DOMAIN}/${WP_CLOUD_BACKUP_ID}"
```

The download response is the backup file, not a JSON object. Database backups are gzip-compressed SQL. Filesystem backups are bzip2-compressed tar archives. Use the `type` from the list response to choose the correct filename and decompression tool.

### Test API authentication

Test authentication and network access with a read-only operation that your integration will use, such as [Get PHP Versions](https://wp.cloud/docs/api/#tag/servers/GET/get-php-versions/{client}[/verbose]) or [List Client Sites](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+).

A successful request confirms that the API received the key from an allowed IP address. It does not verify that the key can perform every operation or access every site.

## Verify the complete workflow

The initial site workflow is complete when:

- the create request returns a site ID and job ID;
- the job reaches `success`;
- the webhook receiver records the matching `site_provisioned` event, when webhooks are configured;
- the site lookup returns the expected site ID and domain;
- the site responds after DNS and certificate provisioning finish; and
- your inventory records the site ID, site type, resource settings, and any customer-facing domain.

Production integrations should also monitor webhooks for provisioning, domain-name changes, quota notifications, and other asynchronous operations. Use those events to keep the integration's site inventory current.

Delete the test site when your team no longer needs it. Check the deletion job before removing the site from your own inventory.
