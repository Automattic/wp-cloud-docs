# Migrate a site to WP Cloud

WP Cloud includes native migration tooling that copies a WordPress site from a remote server over SSH into a destination site in the partner's WP Cloud account. It supports one-off site moves and repeated migrations used to refresh a destination before production cutover.

The remote hosting environment must provide enough access for WP Cloud to connect and run the migration. Some hosting configurations or complex installations may not be compatible.

## Requirements

The remote server must provide:

- SSH shell access using a username and password, a username and identity file, or a username and passphrase-protected identity file;
- WP-CLI support, or an environment where the migration can supply WP-CLI; and
- `rsync`.

Collect the following connection values before creating the migration:

- `remote-host`: SSH hostname.
- `remote-user`: SSH username.
- `remote-port`: SSH port, which defaults to `22`.
- `remote-domain`: Optional source domain when it differs from the destination hostname.
- `remote-docroot`: Optional path to the source document root. WP Cloud attempts common paths when it is omitted.
- `remote-pass`: Password when password authentication is used.
- `ssh-id`: Identity-file contents when key authentication is used.
- `ssh-id-pass`: Passphrase when the identity file is protected.

Treat passwords, private keys, and passphrases as credentials. Do not put them in logs, screenshots, support requests, or customer-visible responses.

Use one supported authentication combination for each migration. Supply `remote-pass` for password authentication. Supply `ssh-id` for identity-file authentication and add `ssh-id-pass` only when that identity is protected by a passphrase. When `remote-domain` is an empty value, the migration uses the site's default domain. When `remote-docroot` is absent, WP Cloud tries common document-root paths on the remote host.

## Prepare the destination

Create a new destination site when possible. A new site avoids overwriting an existing site and can be created with `allow_site_migration` enabled.

**Warning:** Enabling an existing site as an SSH migration target accepts destructive replacement of its files and database. The current operation cannot be undone. Preserve the existing site and confirm the destination ID before continuing.

For an existing destination, send a `POST` request to the [Configure a site to accept an incoming SSH migration endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-allow-ssh-migration/{site}):

```bash
export WP_CLOUD_SITE='destination-domain-or-ID'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/site-allow-ssh-migration/${WP_CLOUD_SITE}"
```

A successful response reports that the site is ready for a migration. This operation only enables the destination; it does not start the migration. After a migration starts, `allow_site_migration` changes to the migration ID and prevents another migration from targeting the site at the same time.

## Create and update the migration

Create the migration with `GET /migration/create/{site_id_or_domain}` and supply the remote connection values. The operation returns a migration ID. Keep that ID with the destination site record because later updates, preflight checks, and migration runs use it.

If you do not provide an SSH identity, the migration creates a public key and returns it as `ssh-id-pub`. Add that public key to the remote user's `authorized_keys` file before preflight checks.

Update the migration with `GET /migration/update/{migration-id}` as the site owner supplies corrected host, user, document-root, domain, or authentication values. Migration details cannot be changed while the migration is actively running; pause it before changing connection data. Sensitive values such as the private identity and remote password must remain redacted when migration details are displayed.

The migration record should identify the remote host, remote user, remote port, optional remote domain, optional document root, destination site, and authentication method without exposing credential values. Confirm that the destination in this record matches the site prepared for migration before starting preflight.

## Run preflight checks

Start a preflight with `GET /migration/preflight/{migration-id}` after the remote credentials and destination are ready. Each preflight returns a new response ticket. Use the result to correct connection, document-root, WP-CLI, or `rsync` problems, then update the migration and run preflight again.

After a preflight, return to [Create and update the migration](#create-and-update-the-migration) when you need to correct or replace migration information. You can update the migration and run preflight again as many times as necessary before starting the migration.

## Check logs and status

Preflight checks and migration runs return response tickets. If webhooks are configured, they report response-ticket updates. You can also poll the response-ticket endpoints directly.

Use the [Get Response Ticket Summary endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/summary) for its state, or the [Get Response Ticket Details endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/full) when you need its messages. Both operations accept the ticket in the form-encoded `response-ticket-id` field.

```bash
export WP_CLOUD_RESPONSE_TICKET='<response-ticket-id>'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "response-ticket-id=${WP_CLOUD_RESPONSE_TICKET}" \
  'https://atomic-api.wordpress.com/api/v1.0/response-ticket/get/summary'
```

A response-ticket request returns `202` when no response is available yet; retry after one second. A completed ticket reports `success` or `failure`, while active work reports `running`.

Use the full operation only when the summary is not enough:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "response-ticket-id=${WP_CLOUD_RESPONSE_TICKET}" \
  'https://atomic-api.wordpress.com/api/v1.0/response-ticket/get/full'
```

A `400` response means the request omitted the ticket ID. A `404` response means the ticket was not found. Store the migration ID separately from each response ticket because a new preflight or migration attempt returns a new ticket.

Keep each new response ticket with the preflight attempt that created it. The summary provides the current state and response count; the full response provides the attached messages. Use those messages to distinguish an authentication failure from a missing document root, unavailable WP-CLI, or unavailable `rsync` before changing migration data.

## Run and monitor the migration

Proceed only after preflight succeeds. Mark the migration ready to run with `GET /migration/ready/{migration-id}`. The operation starts the migration and returns a new response ticket. Monitor it through configured webhooks or the response-ticket endpoints until it reports `success` or `failure`.

The migration is ready for cutover only after the response ticket reports success and the destination has been checked for the expected content, domain behavior, users, plugins, theme, and customer-facing functions.

## Retry or refresh a migration

After a preflight, return to the migration update step when you need to correct connection or source information. Run preflight again after every update instead of relying on an earlier successful result.

After a migration reports `success` or `failure`, you can repeat the update, preflight, migration, and monitoring steps as necessary. Repeat the workflow after a failure to troubleshoot a corrected configuration, or after a successful migration to copy changes made on the source site before production cutover.

**Warning:** Every retry or refresh is destructive to the destination because it pulls the source filesystem and database into the destination again. Preserve destination-only changes or move them back to the source before another run. A refresh is another full destination-changing operation, not an incremental confirmation.

## Migration API operations

The migration operations below are still being tested and are not yet included in the public WP Cloud API reference. Their contracts may change. They are documented here temporarily so partners can build and test the native migration workflow.

### Create a migration

`GET /migration/create/{site_id_or_domain}`

This operation starts a new site migration and returns a migration ID.

Request fields:

- `remote-host`: Hostname of the remote server.
- `remote-port`: Optional SSH port. The default is `22`.
- `remote-user`: Username used to connect to the remote server.
- `remote-pass`: Optional password when password authentication is used.
- `remote-docroot`: Optional path to the remote site's document root.
- `remote-domain`: Optional source domain when it differs from the destination site's domain.
- `ssh-id`: Optional SSH private-key data.
- `ssh-id-pass`: Optional passphrase for the supplied SSH private key.

If `ssh-id` is omitted, WP Cloud generates an SSH identity for the migration and returns the public key as `ssh-id-pub`. Add that public key to the remote user's `authorized_keys` file before running preflight checks.

### Get migration details

`GET /migration/get/{migration-id}`

This operation returns the current migration details. Sensitive values such as `ssh-id` and `remote-pass` are redacted.

- `migration-id`: Migration to retrieve.

### Update a migration

`GET /migration/update/{migration-id}`

This operation updates an existing migration. A migration cannot be updated while it is actively running; pause it before changing its details.

- `migration-id`: Migration to update.
- `ssh-id`: Optional replacement SSH private-key data.
- `ssh-id-pass`: Optional passphrase for the supplied SSH private key.
- `remote-host`: Optional replacement remote hostname.
- `remote-port`: Optional replacement SSH port. The default is `22`.
- `remote-user`: Optional replacement remote username.
- `remote-pass`: Optional replacement password.
- `remote-docroot`: Optional replacement remote document-root path.
- `remote-domain`: Optional replacement source domain. An explicitly supplied empty value uses the destination site's default domain.

### Set a migration to ready

`GET /migration/ready/{migration-id}`

This operation marks a migration as ready to run and returns a new response ticket.

- `migration-id`: Migration to run.

### Run preflight checks

`GET /migration/preflight/{migration-id}`

This operation tests the saved connection and migration information before the migration runs. Each preflight attempt returns a new response ticket.

- `migration-id`: Migration to test.
