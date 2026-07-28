# Delete a site

Deleting a WP Cloud site through the API immediately and permanently removes the site, its Atomic Site ID, files, database, site meta, and associated backups. WP Cloud does not provide a reversible soft-delete operation, so consider all associated backups removed as well.

**Note:** Track every site by its Atomic Site ID. This persistent identifier does not change when the site's domains change, so use it throughout the site lifecycle, including deletion.

## Consider a deletion grace period

A deletion grace period is an optional partner workflow. Instead of calling Delete Site as soon as a deletion is requested, a partner might retain the site temporarily and manage its pending-deletion state in the partner's product.

For a user-driven deletion, provide a clear warning that deletion is permanent and prompt the user to download any required backups before proceeding. Automated expiration deletions may follow a partner's own retention policy, but the final API deletion is still permanent.

A partner-owned grace period might use this sequence:

1. Suspend the site with the `suspended` site-meta value.
2. Optionally remove or park its primary and alias domains.
3. Revoke the customer's access through the partner's control panel.
4. Mark the site as pending deletion in the partner's product and retain it for the stated recovery period.
5. Call Delete Site only after the recovery period expires.

During the grace period, partner API and Client SSH access remain available. To restore the site, reassign its domain if needed, remove the suspended value, and restore customer access in the partner's product. WP Cloud billing continues while the site exists because suspension does not release its allocated resources.

## Permanently delete the site

Deleting a site through the API immediately and permanently removes the site and its Atomic Site ID. Consider all associated backups removed as well.

Send a `POST` request to the [Delete Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/delete-site/{service}/{identifier}). Use the partner identifier and Atomic Site ID so the request continues to identify the correct site after a domain change:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/delete-site/${WP_CLOUD_CLIENT}/${WP_CLOUD_SITE_ID}"
```

An accepted response contains a job ID:

```json
{
  "message": "OK",
  "data": {
    "job_id": 9876
  }
}
```

Follow the job with the [Get Job Status endpoint](https://wp.cloud/docs/api/#tag/jobs/GET/job-status/{id}) until it reaches a terminal state. After it succeeds, confirm that the Atomic Site ID is absent from the partner's site inventory before removing the local site mapping or assigning its former domain to another site.

The `do_not_delete` site-meta value prevents deletion while it is set. A `400` response can mean `do_not_delete` is set or a deletion is already queued. A `412` response means on-demand backups are blocking deletion. A `423` response means another operation has locked the site.
