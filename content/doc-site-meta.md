# Configure resources, site type, and billing with site meta

Site meta controls a WP Cloud site's resource limits, runtime options, and billing classification. WP Cloud invoices are calculated based on each site's resource configuration and site type.

Set these values during provisioning when the Create Site operation supports them, or update them after provisioning with the Site Meta operation.

## Configure resource values

The [Site Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}) manages the following values. Unless a partner sets different values, a new site has 10 default PHP connections, bursting enabled, a 512 MB per-request PHP memory limit, and a 200 GB filesystem quota.

| Site meta | Purpose and accepted values | Default |
| --- | --- | --- |
| `default_php_conns` | Sets the normal number of concurrent PHP workers or connections. More workers allow more PHP requests to run at once; they do not make one request, database query, or external call finish faster. Accepts an integer from `2` through `10`. Higher allocations require coordination with WP Cloud. | `10` |
| `burst_php_conns` | Allows automatic scaling of PHP workers beyond `default_php_conns` when capacity is available. Set it to `1` to enable bursting or `0` to disable it. | `1` (enabled) |
| `php_memory_limit` | Sets the per-request PHP memory limit in megabytes. Accepted values are `512`, `1024`, `1536`, and `2048`. | `512` MB |
| `space_quota` | Sets a hard filesystem quota using an integer and size suffix, such as `50G` or `200G`. The technical minimum is 1 GB, and the billable minimum is 25 GB. Quotas above 200 GB require coordination with WP Cloud. | `200G` |
| `space_used` | Read-only compressed, charged usage for the site's writable ZFS user space, in bytes. It is refreshed approximately every 12 hours. | Reported by the platform. |
| `_data` → `site_type` | Stores the site's billing classification as versioned JSON. See [Set the site type and billing classification](#set-the-site-type-and-billing-classification). | No value; the site is billable by default. |

For example, set a site to four normal PHP connections:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'value=4' \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/default_php_conns/update"
```

Resource settings can change without reprovisioning the site. Before reducing `space_quota`, check the site's current filesystem use and do not set a quota below it.

Before requesting a PHP allocation above the normal self-service range, compare PHP worker saturation or backlog, request rate, PHP CPU, burst use, and the slowest request classes over the same time window. Additional concurrency can help when otherwise-healthy requests are waiting for a worker, but it does not correct slow code or database work. See [Troubleshoot site performance](/docs/troubleshooting/site-performance/).

WP Cloud applies filesystem quotas per site. If a hosting plan shares a larger storage allowance across several sites, the partner's product must track that allowance and prevent the combined site quotas from exceeding it.

The filesystem quota does not include the site's database, WP Cloud backups, redundant replicas used for failover, or image subsizes handled by the edge image service. Refer to the partner's current commercial agreement or billing policy for storage pricing.

### Interpret `space_used`

`space_used` is the compressed storage charged to the site's writable ZFS user space. WP Cloud gets the value from ZFS user-space accounting rather than adding the sizes of specific directories or running a recursive `du` scan.

The value includes site-owned files regardless of their path. Examples include:

- uploads, themes, plugins, and other files in `wp-content`;
- files outside `wp-content`, including site-owned files in the document root;
- temporary files; and
- cache files, build artifacts, and dependencies such as `node_modules`.

The value does not include:

- the site's database;
- shared, managed WordPress core files;
- shared platform software, managed plugins, and runtime or system files; or
- the contents of a symlink target outside the site's writable storage.

A small symlink or its metadata can count when it is stored in the site's writable space, but the shared files it points to do not.

An immediate `du` total over SSH can differ from `space_used`. The filesystem visible over SSH combines the site's writable files with shared platform files, symlinks, mounts, and other runtime layers. In addition, `du` does not represent the compressed storage charged by ZFS. The `space_used` value is refreshed approximately every 12 hours, so recent file additions or deletions might not appear until the next update.

## Set the site type and billing classification

The `_data` site-meta value contains versioned JSON used for inventory and billing classification. The documented `v1` object requires a `site_type` property.

| `site_type` value | Purpose | Billing behavior |
| --- | --- | --- |
| No value or `null` | No site type has been assigned. | Billable by default. |
| `billable` | A production site or any other site that should be billed. | Billable. |
| `staging` | An eligible non-production staging site associated with a billable site. | One staging site may be non-billable for each billable site. |
| `internal` | Reasonable partner testing, demos, or development. Do not use it for a partner's customer sites. | Non-billable and subject to usage review. |
| `canary` | Reserved for WP Cloud monitoring. Partners must not set or delete canary sites. | Non-billable. |

### Staging billing rules

**Important:** A WP Cloud host partner may offer only one non-billable staging site per billable site.

- A non-billable staging site must not be used as a live or production site.
- Additional staging sites must be marked as `billable`.
- If the number of staging sites exceeds the number of billable sites, each additional staging site is billed.

A staging value has this form:

```json
{
  "v1": {
    "site_type": "staging"
  }
}
```

This request marks a site as billable:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --data-urlencode 'value={"v1":{"site_type":"billable"}}' \
  "https://atomic-api.wordpress.com/api/v1.0/site-meta/${WP_CLOUD_SITE_ID}/_data/update"
```

## Store other site data in `_data`

Partners may use `_data` for other site-specific information, but its primary purpose is to track site billing status for WP Cloud accounting. `_data` is account-level inventory metadata; it is different from [Persistent data](/docs/sites/persistent-data/) and is not available to code running inside the site.

When storing custom properties in `_data`:

- keep every property required by the current WP Cloud `_data` version;
- do not reuse property names reserved by WP Cloud;
- prefix custom property names with the host client's name, such as `<client-name>_custom_property`, to reduce the chance of a future conflict;
- send the complete JSON object, including its version and existing properties, with every update; and
- keep the encoded value at or below 1 MB.

The [List Client Sites endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+{meta}/) can return `_data` when it is requested. `_data` is not part of the Get Site Details record and is not available from within the WordPress site.

## Verify the configuration

Retrieve resource values individually with the Site Meta operation. To audit `_data` across the host client account, request it through the List Client Sites endpoint. The returned field contains the JSON-encoded value:

```json
{
  "_data": "{\"v1\":{\"site_type\":\"billable\"}}"
}
```

Confirm that each site's resource values match the hosting product it was sold and that every non-billable staging site is paired with a billable site in the host client's inventory.
