# WordPress multisite

WP Cloud supports WordPress multisite networks using subdirectories,
subdomains, or mapped domains. WordPress controls the network and its sites;
WP Cloud domain aliases and canonicalization determine which hostnames reach
the installation.

Multisite networks, especially subdomain and mapped-domain networks, add
operational complexity. Avoid multisite unless the network model is necessary.
For the best isolation, performance, scalability, and cost control, use a
separate WP Cloud site for each WordPress site when possible.

Review the [WordPress multisite network
documentation](https://developer.wordpress.org/advanced-administration/multisite/)
before converting a production site. The conversion changes database tables,
administration, plugin behavior, and domain handling.

## Convert a single site to a network

Add the following above the `/* That's all, stop editing! */` line in the
site's `htdocs/wp-config.php` file:

```php
/* Multisite */
define( 'WP_ALLOW_MULTISITE', true );
```

In WordPress administration, open **Tools → Network Setup**. Enter the network
title and administrator email, then choose subdirectories or subdomains. For a
mapped-domain or subdomain network, finish the normal WordPress setup before
applying the WP Cloud domain configuration below.

Select **Install**. WordPress displays the network constants that must be added
to `wp-config.php`; place them above the same stop-editing line. Sign in again
after saving the file. The **My Sites** menu then provides Network Admin access
for sites, plugins, users, and network settings.

## Configure a domain-based network

Domain-based multisite disables WP Cloud's normal alias-to-primary redirects.
The host partner or site owner must add every served domain and handle
canonical `www` or non-`www` redirects. Do not enable this configuration for a
normal single-domain site.

Changing `canonicalize_aliases` to `false` on an existing site stops the
platform from redirecting aliases to the primary domain. Conversely, leaving
it enabled on an existing multi-domain network can redirect those mapped
domains to the primary hostname with HTTP 301 responses. When canonicalization
is disabled, the host partner or its end user is responsible for replacing any
required alias, `www`, non-`www`, or mapped-domain redirects that WP Cloud no
longer provides.

1. Set the `canonicalize_aliases` site-meta value to `false` with the [Site
   Meta endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}).
2. Add each mapped domain as a site alias using [Manage site domains and
   aliases](/docs/sites/domains/manage-domains-aliases/).
3. Add the following to `wp-config.php` when logins must work across the mapped
   domains:

   ```php
   define( 'COOKIE_DOMAIN', $_SERVER['HTTP_HOST'] ?? DOMAIN_NAME );
   ```

4. In Network Admin, map each subsite's Site Address to one of the aliases.

Every domain or subdomain served by the network must be added as an alias;
wildcard aliases are not supported. A subdomain of the primary domain does not
work automatically.

The answer is therefore explicit for each domain: add it to the WP Cloud site,
map it to the intended WordPress subsite, and test both anonymous and logged-in
requests. A DNS wildcard by itself does not register wildcard aliases with WP
Cloud.

Some networks also require:

```php
define( 'ADMIN_COOKIE_PATH', '/' );
define( 'COOKIEPATH', '' );
define( 'SITECOOKIEPATH', '' );
```

The `COOKIE_DOMAIN` setting may not be needed for a conventional subdomain
network. Test login, logout, administration, and cookie behavior on every
mapped domain.

WP Cloud DKIM signing applies to messages sent from the primary domain. A
subsite that sends from a mapped alias may need to use the primary-domain From
address or an [external email service
provider](/docs/wordpress/transactional-email/#use-an-email-service-provider).

## Change the network's primary domain

After changing the WP Cloud primary domain, update the WordPress network:

1. Change `DOMAIN_CURRENT_SITE` in `wp-config.php`:

   ```php
   define( 'DOMAIN_CURRENT_SITE', 'example.com' );
   ```

2. Update old-domain values in the relevant database tables. Depending on the
   network, these can include `wp_options`, `wp_blogs`, `wp_site`,
   `wp_sitemeta`, and each `wp_#_options` table.
3. Flush Page Cache and Object Cache:

   ```bash
   wp --skip-plugins --skip-themes cache flush
   ```

Use a database backup and review serialized data before a broad search and
replace. A network can store domain values in tables and formats beyond the
core rows listed here.

## Resolve database connection errors

An **Error establishing a database connection** message after enabling
multisite often means the domain in `wp-config.php` does not match values in
`wp_blogs`, `wp_site`, `wp_options`, or the subsite `wp_#_options` tables.
Correct those values and flush cache first.

If the values match but the error remains, temporarily change the
`SUBDOMAIN_INSTALL` boolean, flush cache, restore the intended value, and flush
cache again. This forces WordPress to rebuild behavior tied to the network
type:

```bash
wp cache flush
```

Do not leave `SUBDOMAIN_INSTALL` set to a value that disagrees with the
network's address structure.
