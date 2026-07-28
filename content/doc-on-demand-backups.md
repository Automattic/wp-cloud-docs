# Create an on-demand backup

WP Cloud host partners may give their customers an option to create on-demand backups. A customer can request a filesystem backup, a database backup, or both, capturing the selected data at approximately the time of each request.

## Limits and retention

By default, a site can retain one on-demand filesystem backup and one on-demand database backup. Partners that need higher limits can contact WP Cloud Support to discuss different quotas.

On-demand backups do not use the retention period for automatic platform backups. They have no defined expiration date and remain available until deleted, subject to the site's quota.

When a site reaches its quota, delete the existing on-demand backup before requesting a replacement. All on-demand backups must also be deleted before the site can be permanently deleted.

## Request the backup

Set the site ID or domain and choose `fs` for a filesystem backup or `db` for a database backup. Send a `POST` request to the [Request Backup Creation endpoint](https://wp.cloud/docs/api/#tag/backups/POST/on-demand-backup/create/{site}/{type}):

```bash
export WP_CLOUD_SITE='example.com'
export WP_CLOUD_BACKUP_TYPE='fs'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/on-demand-backup/create/${WP_CLOUD_SITE}/${WP_CLOUD_BACKUP_TYPE}"
```

The successful response contains a backup request ID:

```json
{
  "message": "OK",
  "data": {
    "atomic_backup_request_id": 12345
  }
}
```

The response confirms that WP Cloud accepted the request. It does not contain the downloadable backup record ID. An `on-demand-backup` [webhook](/docs/api-automation/webhooks/) first reports that the request was acknowledged and later reports that the backup was created. Alternatively, list the site's backups until an `ondemand-fs` or `ondemand-db` record appears before trying to download it.

A `400` response means the backup type is invalid. A `403` response means the site has reached its on-demand backup quota, and a `404` response means the site was not found.

## Replace a backup at the quota limit

When a site has reached its quota, delete the existing on-demand backup before requesting another backup of the same type. Only on-demand backups can be deleted through this operation. Retrieve the existing backup ID with the [List Site Backups endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backups-list/{service}/{identifier}), then send a `POST` request to the [Request Backup Deletion endpoint](https://wp.cloud/docs/api/#tag/backups/POST/on-demand-backup/delete/{site}/{backup_id}):

```bash
export WP_CLOUD_BACKUP_ID='12345'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/on-demand-backup/delete/${WP_CLOUD_SITE}/${WP_CLOUD_BACKUP_ID}"
```

The response contains a new request ID for the deletion:

```json
{
  "message": "OK",
  "data": {
    "atomic_backup_request_id": 67890
  }
}
```

Wait until the deleted backup no longer appears in the site's backup list before requesting its replacement. A `404` response can mean that the site or backup does not exist, or that the backup does not belong to the specified site.
