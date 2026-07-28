# Troubleshoot duplicate core files, wp-config.php, and wp-admin 403 errors

Duplicate WordPress core files or a missing or broken `wp-config.php` can make
WP-CLI report `wp-config.php not found`, claim that `wp-settings.php` is not
loaded directly, return `xargs: sudo: exited with status 255`, or make
`/wp-admin/` return HTTP 403. After migrations, duplicate core files are often
the cause even when `wp-config.php` is present.

Start with the filesystem because these symptoms can share the same cause. Do
not assume that an error naming `wp-config.php` proves the file is missing.
Archive confirmed duplicate core files before rebuilding configuration, then
move to the next check only when the symptom remains.

## Check for duplicate core files

A normal WP Cloud site root contains the managed core symlink, site content,
and bootstrap files. It commonly looks like:

```text
__wp__/
jetpack-temp/
wp-config.php
wp-content/
wp-load.php
```

The exact site can contain intentional custom files and directories. Do not
delete an unfamiliar file merely because it is absent from this short list.

The following are common duplicate core paths after an imported copy of
WordPress is placed over WP Cloud's managed core:

```text
wp-admin/
wp-includes/
index.php
wp-activate.php
wp-blog-header.php
wp-comments-post.php
wp-config-sample.php
wp-cron.php
wp-links-opml.php
wp-login.php
wp-mail.php
wp-settings.php
wp-signup.php
wp-trackback.php
xmlrpc.php
```

Confirm that each path is an unnecessary duplicate rather than customer code.
Create an `.old-imported` directory and move confirmed duplicates there instead
of deleting them immediately. This provides a rollback if the classification
was wrong.

Flush Page Cache after moving the files:

```bash
wp cache flush
```

Then check `/wp-admin/` and the original WP-CLI command again.

## Check wp-config.php

If the duplicate files were not the cause, confirm that `wp-config.php` exists
in the site root. Restore it from a known-good backup when it contains required
custom configuration. If the file exists but every WP-CLI command fails, check
its PHP syntax and compare it with [Default
wp-config.php](/docs/wordpress/configuration/default-wp-config/).

When no usable backup exists, start from that default example and generate a
unique set of authentication keys and salts at [WordPress.org's salt
service](https://api.wordpress.org/secret-key/1.1/salt/). Never reuse salts from
another site. Upload the completed file through SSH or SFTP, then rotate the
values once more if appropriate:

Replace every placeholder in the authentication section, including all eight
key and salt values:

```php
define( 'AUTH_KEY',         'unique value' );
define( 'SECURE_AUTH_KEY',  'unique value' );
define( 'LOGGED_IN_KEY',    'unique value' );
define( 'NONCE_KEY',        'unique value' );
define( 'AUTH_SALT',        'unique value' );
define( 'SECURE_AUTH_SALT', 'unique value' );
define( 'LOGGED_IN_SALT',   'unique value' );
define( 'NONCE_SALT',       'unique value' );
```

The salt service supplies the complete definitions; the placeholders above
only show which entries must exist. Do not publish, copy between sites, or
commit the generated values to a shared repository.

```bash
wp config shuffle-salts
```

## Check the database prefix

If WordPress starts but does not find the expected site data, inspect the
database tables and the `$table_prefix` value in `wp-config.php`. The value must
match the actual prefix. Do not assume it is `wp_` after a migration.

When the prefix is correct, WordPress should load the existing site's users,
options, and content rather than presenting a fresh installation. If the site
still behaves like a new installation, compare the selected database and
table names before changing data.

Keep `.old-imported` until the site owner confirms that the site, wp-admin,
scheduled tasks, and WP-CLI work normally. It can then be removed after any
needed custom files have been recovered.

The issue is resolved when `/wp-admin/` loads, WP-CLI works without the original
configuration error, and WordPress reads the expected database tables.
