# PHP filesystem access permissions

WP Cloud can control whether PHP requests may write to a site's filesystem.
The `php_fs_permissions` [site meta](/docs/sites/site-meta/) value changes the
filesystem mount used while WP Cloud handles PHP requests; it does not replace
normal SSH or SFTP access controls.

## Supported values

The following table describes each allowed value and gives an example of when
it can be appropriate.

| Value | Behavior | Typical use |
| --- | --- | --- |
| `rw` | PHP can read and write the site's filesystem. | The default and appropriate setting for most sites. |
| `ro` | PHP can read files but cannot write them. | Temporary containment or hardening while a site is investigated. Many WordPress updates, uploads, and other PHP write operations will fail. |
| `loggedin` | Changes PHP filesystem write behavior for some logged-in WordPress requests. | Additional protection where current site behavior has been tested. |

The `loggedin` mode is an evolving platform feature. Test the site's plugins,
themes, upload flows, scheduled work, and integrations before using it broadly.
Code that writes during logged-out requests may need `rw`.

These values affect filesystem writes made by PHP while handling web requests.
They do not change SSH or SFTP permissions, make the database read-only, block
database changes made through WordPress administration, remove malware, or
rotate compromised credentials. Use `ro` as a containment or hardening control,
not as a substitute for investigation and cleanup.

Set or remove `php_fs_permissions` with the same WP Cloud API site-meta
operations used for other site settings. See [Configure resources, site type,
and billing with site meta](/docs/sites/site-meta/) for the request pattern.
