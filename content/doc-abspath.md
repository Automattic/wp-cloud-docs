# ABSPATH

WordPress core is symlinked to platform-managed files on WP Cloud. As a
result, `ABSPATH` points to the managed WordPress directory rather than the
site's writable `htdocs` directory. Plugins and themes that use `ABSPATH` to
locate files under `wp-content` can therefore build the wrong path.

## Understand the WP Cloud path

The following test shows where `ABSPATH` points:

```php
<?php var_dump( ABSPATH );
```

On a WP Cloud site, it returns:

```text
string(19) "/srv/htdocs/__wp__/"
```

The `__wp__` directory is the symlinked WordPress core location. Use
`ABSPATH` when code needs a WordPress core path, but not to find a plugin,
theme, upload, or other file under `wp-content`.

This means the constant's value is valid, but its meaning differs from the
site-root assumption made by some portable WordPress code.

## Use WP_CONTENT_DIR for site-owned files

This path is incorrect on WP Cloud because it assumes `wp-content` is inside
the managed core directory:

```php
$target_path = ABSPATH . 'wp-content/plugins/order-tracking/order-sheets/';
```

Build the path from `WP_CONTENT_DIR` instead:

```php
$target_path = WP_CONTENT_DIR . '/plugins/order-tracking/order-sheets/';
```

`ABSPATH` includes a trailing slash; `WP_CONTENT_DIR` does not. Include the
separator when appending a path to `WP_CONTENT_DIR`.

## Define a portable site-root constant

Code that needs the site root rather than `wp-content` can define its own
constant from `WP_CONTENT_DIR`:

```php
define( 'EXAMPLE_SITE_ROOT', str_replace( 'wp-content', '', WP_CONTENT_DIR ) );
```

On WP Cloud, `EXAMPLE_SITE_ROOT` resolves to `/srv/htdocs/`. It can then be
used without depending on WP Cloud's symlinked core path:

```php
$target_path = EXAMPLE_SITE_ROOT . 'wp-content/plugins/order-tracking/order-sheets/';
```

The [WordPress filesystem reference](https://developer.wordpress.org/reference/classes/wp_filesystem_base/)
and [`WP_Filesystem_Base::wp_content_dir()`](https://developer.wordpress.org/reference/classes/wp_filesystem_base/wp_content_dir/)
provide additional options for code that works with the WordPress filesystem.
