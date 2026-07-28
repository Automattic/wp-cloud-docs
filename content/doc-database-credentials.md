# Database credentials

WP Cloud supplies each site's database connection values automatically. WordPress code should use the standard `DB_HOST`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` constants instead of storing another copy of the credentials.

Do not replace the managed database configuration in `wp-config.php`. The file intentionally explains that WP Cloud provides these values from the site environment.

```text
/**
 * Database connection information is automatically provided.
 * There is no need to set or change the following database configuration
 * values:
 *   DB_HOST
 *   DB_NAME
 *   DB_USER
 *   DB_PASSWORD
 *   DB_CHARSET
 *   DB_COLLATE
 */
```

## Use credentials inside the site

WordPress and code loaded through WordPress can use the standard database constants. A separate application running inside the same WP Cloud site environment can also use those constants after it loads WordPress.

Do not create a public PHP file that prints the constants. Such a file exposes the database password to anyone who can request it and may remain accessible through caches, logs, or forgotten copies.

For interactive database work, use [phpMyAdmin](/docs/site-access/database-access/phpmyadmin/) or the database commands included with WP-CLI over [SSH access](/docs/site-access/ssh-sftp/). These methods avoid putting a credential in the web root.

## Reset the database password

Use the [`reset-db-password/{type}/{site}` operation](https://wp.cloud/docs/api/#tag/sites/POST/reset-db-password/{type}/{site}) when the current password was exposed or an unsupported manual change broke the site's database connection.

Before resetting or recreating a database, inspect any custom `DB_CHARSET` and `DB_COLLATE` definitions. Remove an unnecessary override or correct it to a supported value. An invalid collation can make database creation fail, for example:

```text
ERROR 1273 (HY000) at line 1: Unknown collation: 'ut8mb4_general_ci'
```

Preserve the complete creation error. A failed reset can leave the site without a usable database, which also causes later database backups and data-sync work to fail. Correct the configuration and confirm that the database exists before retrying those operations.

The reset request returns a job ID. Check the job until it succeeds before testing the site. WP Cloud then updates the managed site environment with the replacement password.

A successful job means the platform changed its managed credential. It does not update a password copied into partner-owned software.

Resetting the password can interrupt custom software that copied the old value instead of using the managed WordPress constants. Update any authorized integration that stores the password, then remove the old value from its configuration and logs.

## Direct database connections

WP Cloud does not accept inbound database connections directly from external systems. Code running inside the site's WP Cloud environment can connect with the managed constants.

An application that supports a database connection through SSH may connect through the site's SSH service. Use a site-scoped credential where possible and do not expose the database port publicly.

## Verify the connection

After a reset or integration change:

1. Wait for the password-reset job to report success.
2. Load the site and a WordPress administration page that performs a database query.
3. Run the integration's safe connection check without printing the password.
4. Confirm that the former password no longer works anywhere it was stored.
