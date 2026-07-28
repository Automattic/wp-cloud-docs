# Default wp-config.php

WP Cloud creates `wp-config.php` with managed database connection values and
the standard WordPress configuration. Use this reference when a site's file
must be repaired or recreated. Do not replace the database settings that WP
Cloud supplies automatically.

## Authentication keys and salts

Generate replacement values with the [WordPress.org secret-key
service](https://api.wordpress.org/secret-key/1.1/salt/) rather than using the
placeholders below:

```php
define( 'AUTH_KEY',         'REPLACE_ME' );
define( 'SECURE_AUTH_KEY',  'REPLACE_ME' );
define( 'LOGGED_IN_KEY',    'REPLACE_ME' );
define( 'NONCE_KEY',        'REPLACE_ME' );
define( 'AUTH_SALT',        'REPLACE_ME' );
define( 'SECURE_AUTH_SALT', 'REPLACE_ME' );
define( 'LOGGED_IN_SALT',   'REPLACE_ME' );
define( 'NONCE_SALT',       'REPLACE_ME' );
```

The following WP-CLI command can also replace the salts. It signs out all
current WordPress sessions:

```bash
wp config shuffle-salts
```

## Sample file

```php
<?php
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

/** Authentication unique keys and salts. */
define( 'AUTH_KEY',         'REPLACE_ME' );
define( 'SECURE_AUTH_KEY',  'REPLACE_ME' );
define( 'LOGGED_IN_KEY',    'REPLACE_ME' );
define( 'NONCE_KEY',        'REPLACE_ME' );
define( 'AUTH_SALT',        'REPLACE_ME' );
define( 'SECURE_AUTH_SALT', 'REPLACE_ME' );
define( 'LOGGED_IN_SALT',   'REPLACE_ME' );
define( 'NONCE_SALT',       'REPLACE_ME' );

/** WordPress database table prefix. */
$table_prefix = 'wp_';

/** WordPress debugging mode. */
if ( ! defined( 'WP_DEBUG' ) ) {
    define( 'WP_DEBUG', false );
}

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', dirname( __FILE__ ) . '/' );
}

/** Sets up WordPress variables and included files. */
require_once ABSPATH . 'wp-settings.php';
```

WP Cloud injects the database connection values into the site environment;
they are intentionally absent from this file. See [Database
credentials](/docs/site-access/database-access/database-credentials/) before changing a
site's database configuration.

This means the sample is a structural example, not a file to paste over a
working site's configuration without retaining its unique salts, table prefix,
and any reviewed site-specific constants.
