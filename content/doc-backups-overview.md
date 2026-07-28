# Backups overview

WP Cloud automatically creates filesystem and database backups for sites. Backup generation and downloads run from a replica server, so they do not consume the production site's storage quota or reduce its performance.

## Backup types

WP Cloud provides several backup options:

- **Automatic platform backups:** WP Cloud creates filesystem and database backups according to the schedules below.
- **On-demand platform backups:** Partners can [create an on-demand filesystem or database backup](/docs/backups-restores/on-demand-backups/) for a specific point in time.
- **Jetpack backups:** [Jetpack VaultPress Backup](/docs/backups-restores/jetpack-backups/) is a separate backup system with its own backup and recovery workflows.

Use [Restore a backup](/docs/backups-restores/restore-backup/) to recover a WP Cloud platform backup into a new site or over the existing site that owns it.

## Backup schedules, retention, and limits

Filesystem and database backups use separate schedules:

- **Filesystem backups:** Created daily at 00:00 UTC whether or not files changed. WP Cloud retains each daily backup for the last seven days, then one backup per week.
- **Database backups:** Created hourly when changes are detected.

WP Cloud retains backups for 30 days. That 30-day guarantee is the retention limit. Older backups may remain available for up to 60 days, but availability beyond 30 days is not guaranteed.

**Warning:** Deleting a site through the Delete Site endpoint permanently removes the site, its site meta, and its backups. Preserve any backup that must remain available before deleting the site.

## List and download backups

Use the [List Site Backups endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backups-list/{service}/{identifier}) to retrieve the available filesystem and database backups:

```bash
export WP_CLOUD_SITE_DOMAIN='example.com'

curl --fail-with-body --silent --show-error \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/site-backups-list/domain/${WP_CLOUD_SITE_DOMAIN}"
```

Example response:

```json
{
  "message": "OK",
  "data": [
    {
      "atomic_backup_id": "1234",
      "atomic_site_id": "5678",
      "backup_timestamp": "2019-08-03 00:00:00",
      "type": "db"
    },
    {
      "atomic_backup_id": "1235",
      "atomic_site_id": "5678",
      "backup_timestamp": "2019-08-02 00:00:00",
      "type": "fs"
    }
  ]
}
```

Use the returned `atomic_backup_id` and `type` to select a backup. The [Get Site Backup Details endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backup-info/{service}/{identifier}/{backup_id}) returns details for one backup. The [Get Site Backup Data endpoint](https://wp.cloud/docs/api/#tag/backups/GET/site-backup-get/{service}/{identifier}/{backup_id}) downloads its contents:

```bash
export WP_CLOUD_BACKUP_ID='1234'

curl --fail --silent --show-error \
  --header 'Auth: API_AUTH_TOKEN' \
  --output "${WP_CLOUD_BACKUP_ID}-db.sql.gz" \
  "https://atomic-api.wordpress.com/api/v1.0/site-backup-get/domain/${WP_CLOUD_SITE_DOMAIN}/${WP_CLOUD_BACKUP_ID}"
```

Filesystem backups are bzip2-compressed tar archives. Database backups are MySQL dumps returned with gzip content encoding. The download is the backup file itself, not a JSON response. Choose the filename and decompression tool from the backup `type` returned by the list or details endpoint.

## Redundancy and real-time failover

WP Cloud also maintains an inaccessible copy of each site in another region through real-time replication. If a pool, data center, or region fails, [automated failover](/docs/infrastructure/automated-failover/) can move traffic to the site's secondary pool.

The secondary copy powers backup generation and downloads, but it is not a customer-accessible backup or a replacement for retained recovery points.
