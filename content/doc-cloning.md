# Clone a site

Clone a WP Cloud site by passing its site ID or domain in the Create Site operation's `clone_from` field. WP Cloud copies the source filesystem and database to a new site and rewrites the source domain to the destination domain by default.

## Create the clone

Send a `POST` request to the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}). This example uses a site ID for the source:

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
  "https://atomic-api.wordpress.com/api/v1.0/create-site/${WP_CLOUD_CLIENT}"
```

The accepted response contains the new site ID and a provisioning job:

```json
{
  "message": "OK",
  "data": {
    "job_id": 1234,
    "atomic_site_id": 5678,
    "domain_name": "staging.example.com"
  }
}
```

The expected result is a response containing the destination site ID and provisioning job ID. It means WP Cloud accepted the request, not that the clone has finished. Check the returned job, then continue after it reports success, as described in the [WP Cloud API quick start](/docs/api-automation/api-quick-start/#check-the-provisioning-job).

A clone copies WordPress users and application data from the source database. The `admin_user`, `admin_email`, and `admin_pass` fields in the Create Site request do not replace the copied users. Change credentials after provisioning when the destination needs different access.

Persistent Data survives cloning.

After the provisioning job succeeds:

- record the destination's new Atomic Site ID and domain, and confirm that the site is available;
- review its site meta, resource settings, access, and [Persistent Data](/docs/sites/persistent-data/);
- update the partner's local inventory or customer mapping to use the new Atomic Site ID; and
- review [WordPress multisite](/docs/wordpress/multisite/) configuration when cloning a network, because cloning does not rewrite every multisite constant or database value.

A high configured `space_quota` can prevent a clone even when the source currently uses much less storage. Compare the source configuration and destination capacity when a clone is rejected for space.

### Optionally skip the automatic URL rewrite

Skipping the automatic URL rewrite is optional and uncommon. WP Cloud normally searches the cloned database and replaces the source domain with the destination domain. For a large site, `skip_db_rewrite=true` can shorten provisioning, but the copied database will still contain the source URLs.

The WP Cloud host partner is responsible for performing and checking all required URL replacements when it uses this option. If the partner makes this option available to its customers, it must ensure that each end-user site's URLs are properly rewritten before the cloned site is put into use.
