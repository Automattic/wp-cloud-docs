# Restore a backup

WP Cloud can restore automatic or on-demand filesystem and database backups. Each restore uses one ready filesystem backup and one ready database backup, either to create a new site or to replace the existing site that owns the backups.

Restoring into a new site is the recommended workflow. It preserves the current production site while the partner verifies the restored copy, updates its configuration, and prepares it to replace the production site. An in-place restore is also available for operations and workflows that specifically need to roll back the existing site.

## Choose a restore workflow

| Use case | Operation | Result |
| --- | --- | --- |
| Recommended: restore, verify, and promote a separate site | [`POST /create-site/{client}`](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}) with `restore_from[]` | Creates a separate WP Cloud site and leaves the original unchanged. |
| Roll an existing site back to its own backups | [`POST /restore-site/{site}`](https://wp.cloud/docs/api/#tag/sites/POST/restore-site/{site}) with `restore_from[]` | Replaces the existing site's filesystem and database. |

Both workflows require exactly two ready backup record IDs: one filesystem backup and one database backup. The filesystem type can be `fs` or `ondemand-fs`; the database type can be `db` or `ondemand-db`. Use the [List Site Backups endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backups-list/{service}/{identifier}) to find the pair.

## Restore into a new site

Restoring into a new site is the recommended path. Use it when a customer needs a preview, a separate restored copy, or a safe way to replace the production site without overwriting it first.

The Create Site operation still requires a domain name or demo domain, `admin_user`, and `admin_email`. The restored WordPress installation comes from the backup, so those administrator values satisfy the endpoint but do not create a new WordPress user.

Send the two backup IDs as repeated `restore_from[]` fields. Their order does not matter:

```bash
export WP_CLOUD_CLIENT='client-name'
export WP_CLOUD_FS_BACKUP_ID='012345'
export WP_CLOUD_DB_BACKUP_ID='543210'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'domain_name=restored-site.example.org' \
  --data-urlencode 'admin_user=user' \
  --data-urlencode 'admin_email=user@example.org' \
  --data-urlencode "restore_from[]=${WP_CLOUD_FS_BACKUP_ID}" \
  --data-urlencode "restore_from[]=${WP_CLOUD_DB_BACKUP_ID}" \
  "https://atomic-api.wordpress.com/api/v1.0/create-site/${WP_CLOUD_CLIENT}"
```

The response identifies the new site and its asynchronous provisioning job:

```json
{
  "message": "OK",
  "data": {
    "job_id": 1234,
    "atomic_site_id": 5678,
    "domain_name": "restored-site.example.org"
  }
}
```

The response means WP Cloud accepted the request. Restoration time depends on backup size. Check the returned job with the [Get Job Status endpoint](https://wp.cloud/docs/api/#tag/jobs/GET/job-status/{id}) and continue only after it reports success.

The restored site is a separate WP Cloud site. Its PHP version, filesystem quota, and other site settings can be changed after provisioning finishes.

After provisioning succeeds:

1. Test the restored site while the production site remains unchanged.
2. Review its site meta, resource settings, access, and any partner-owned configuration that is not stored in the filesystem or database backups.
3. Sync any production data or configuration that changed after the selected backups were created.
4. Move the production site's primary and alias domains to the restored site when it is ready to serve customers.
5. Confirm that the domains, site meta, and partner systems reference the restored site's Atomic Site ID before treating it as the production site.

## Restore an existing site in place

**Warning:** An in-place restore replaces the destination site's filesystem and database. It is not a cross-site restore method. Confirm the customer chose this rollback, preserve any newer data that must survive, and verify that both backups belong to the destination site's Atomic Site ID.

Use the [Restore Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/restore-site/{site}) when the workflow specifically requires the existing site to be restored in place. The backups must belong to that same site's Atomic Site ID.

The in-place restore follows this sequence:

1. Set `allow_restore`, through site meta, to the current Unix timestamp. The value must be positive, no more than 30 days old, and no more than five minutes in the future.
2. Set `suspended`, through site meta, to `503`. The site must remain suspended until the restore finishes.
3. Send one ready filesystem backup ID and one ready database backup ID to the Restore Site endpoint.
4. Wait for the matching `site_provisioned` webhook or response ticket to confirm completion.
5. Remove the `suspended` site meta value so the site can serve requests again.

The following example sets the required site meta values and starts the restore:

```bash
export WP_CLOUD_SITE='domain-or-ID'
export WP_CLOUD_FS_BACKUP_ID='012345'
export WP_CLOUD_DB_BACKUP_ID='543210'
export WP_CLOUD_ALLOW_RESTORE="$(date +%s)"

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "value=${WP_CLOUD_ALLOW_RESTORE}" \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE}/allow_restore/update"

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'value=503' \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE}/suspended/update"

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "restore_from[]=${WP_CLOUD_FS_BACKUP_ID}" \
  --data-urlencode "restore_from[]=${WP_CLOUD_DB_BACKUP_ID}" \
  "https://atomic-api.wordpress.com/api/v1.0/restore-site/${WP_CLOUD_SITE}"
```

A successful request queues the restore:

```json
{
  "message": "OK",
  "data": {
    "atomic_job_id": 123456,
    "response_ticket_id": "67890abc.def12345..."
  }
}
```

Wait for the matching `site_provisioned` webhook before removing the suspension. If the integration records the response ticket, the [Get Response Ticket Summary endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/summary) can also identify completion. The `503` suspension does not remove itself.

After the restore completes, remove the suspension explicitly with the [GET Manage Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/GET/site-meta/{site}/{key}/{action}):

```bash
curl --fail-with-body --silent --show-error \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE}/suspended/remove"
```

The site should serve requests again after the remove operation succeeds.

## Interpret restore errors

- `400` can mean `allow_restore` is missing or stale, `restore_from[]` is invalid, a backup is not ready, or the pair lacks one filesystem or database backup.
- `403` means the API key cannot act on the site's client.
- `404` means the site or a backup was not found.
- `409` can mean a backup belongs to another site, the pair contains two backups of the same type, or the destination is not suspended with status `503`.
