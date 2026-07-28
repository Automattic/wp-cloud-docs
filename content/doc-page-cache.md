# Page Cache

WP Cloud uses Batcache to store and serve rendered WordPress pages from
Memcached. Page Cache reduces repeated PHP and database work at the origin.
It is enabled by default on every site.

Page Cache and [Edge Cache](/docs/performance/cache/edge-cache/) are separate
layers. Page Cache stores the rendered response at the origin. Edge Cache can
serve that response from a location closer to the visitor.

## Default Page Cache behavior

By default, a page becomes eligible for Page Cache after two origin requests
within two minutes. Batcache stores the rendered response for five minutes.
Logged-in WordPress sessions and responses that set certain cookies or cache
headers may bypass the cache.

If [Edge Cache](/docs/performance/cache/edge-cache/) is enabled, an eligible
response can also be stored at the edge. Edge Cache follows the Page Cache
lifetime; it does not have a separate page-lifetime setting.

## Clear Page Cache

Use WP-CLI to clear the WordPress object cache, including Batcache entries:

```bash
wp cache flush
```

If plugins or themes interfere with the command, run it without loading them:

```bash
wp --skip-plugins --skip-themes cache flush
```

When [Edge Cache](/docs/performance/cache/edge-cache/) is enabled, use its
management controls when you need to purge edge responses too. Clearing all
cached responses sends subsequent requests back to WordPress while the caches
repopulate, so prefer a targeted Edge Cache purge when only a few URLs changed.

## Verify Page Cache

Test while logged out of WordPress. A logged-in session normally bypasses Page
Cache and Edge Cache.

Request the page more than once, then view its HTML source. A response served
by Batcache normally ends with a comment similar to this:

```text
<!--
    generated 2 seconds ago
    generated in 0.180 seconds
    served from batcache in 0.002 seconds
    expires in 298 seconds
-->
```

If the comment is absent, inspect the response headers:

```bash
curl -sS -D - -o /dev/null https://example.com/
```

The following header identifies a Batcache hit:

```text
x-nananana: Batcache-Hit
```

The HTML comment and `x-nananana` describe Page Cache. The `x-ac` header
described in [Verify Edge Cache](/docs/performance/cache/edge-cache/#verify-edge-cache)
describes what happened at the edge. Check both when both cache layers are in
use.

## Change the Page Cache lifetime

Sites can change Batcache settings through the global `$batcache` value. Add
one Batcache configuration block before the `/* That's all, stop editing! */`
line in `wp-config.php`. The value may be an object or an array, so account for
both forms:

```php
// Batcache customizations.
global $batcache;

if ( is_object( $batcache ) ) {
    $batcache->max_age = 86400;
    $batcache->seconds = 0;
    $batcache->times   = 1;
} elseif ( is_array( $batcache ) ) {
    $batcache['max_age'] = 86400;
    $batcache['seconds'] = 0;
    $batcache['times']   = 1;
}
```

This example changes:

- `max_age` from five minutes to 24 hours.
- `seconds` from a two-minute population window to an immediate window.
- `times` from two qualifying requests to one.

Longer cache lifetimes can leave changed content in Page Cache and [Edge
Cache](/docs/performance/cache/edge-cache/) longer. Confirm that normal content
updates invalidate the affected URLs, and clear the relevant cache after
changing these values.

## Allow selected cookies without bypassing Page Cache

Some plugins set a cookie on every response. If that cookie matches a Batcache
skip rule, the response is not cached. When the cookie does not change the
rendered page, add its prefix to `noskip_cookies` in the site's existing
Batcache configuration block.

For example, a site using WPML may need to review these cookie prefixes:

```php
$ignored_cookie_prefixes = array(
    'wordpress_test_cookie',
    'wp-wpml_current_language',
    'wpml_browser_redirect_test',
);

if ( is_object( $batcache ) ) {
    $batcache->noskip_cookies = $ignored_cookie_prefixes;
} elseif ( is_array( $batcache ) ) {
    $batcache['noskip_cookies'] = $ignored_cookie_prefixes;
}
```

Only ignore a cookie after confirming that visitors with different cookie
values can safely receive the same page. Never ignore WordPress authentication,
cart, checkout, account, or other cookies that change private or personalized
content.

## Bypass Page Cache for selected requests

Avoid broad Page Cache bypasses. Uncached pages use PHP and database resources
on every request and cannot be served by [Edge
Cache](/docs/performance/cache/edge-cache/). WooCommerce cart, checkout, and My
Account pages are excluded automatically; ordinary product pages remain
cacheable.

### Bypass specific paths

Call `batcache_cancel()` only for the requests that must not be cached. The
following must-use plugin example bypasses two paths:

```php
<?php
/**
 * Plugin Name: Site-specific Page Cache bypasses
 */

add_action( 'init', 'site_cancel_page_cache' );

function site_cancel_page_cache() {
    $path = strtok( $_SERVER['REQUEST_URI'], '?' );

    if (
        in_array( $path, array( '/uncached-page/', '/another-page/' ), true )
        && function_exists( 'batcache_cancel' )
    ) {
        batcache_cancel();
    }
}
```

Replace the example paths with exact paths from the site. After deploying the
change, clear any existing Page Cache and Edge Cache entries for those URLs,
then verify the result while logged out.

### Exclude custom post types from Advanced Post Cache

The `advanced_post_cache_skip_for_post_type` filter applies to Advanced Post
Cache, which caches post-query results. It does not disable all Object Cache
storage. Use it only when a custom post type conflicts with cached post
queries:

```php
add_filter( 'advanced_post_cache_skip_for_post_type', 'site_skip_post_types', 10, 2 );

function site_skip_post_types( $skip, $post_type ) {
    $excluded = array( 'posttype1', 'posttype2' );

    if ( in_array( $post_type, $excluded, true ) ) {
        return true;
    }

    return $skip;
}
```

Use `wp post-type list` to find registered post-type names. Replace the example
names, test the behavior on a staging site, and remove the bypass if it does not
solve the specific conflict.

## Troubleshoot Page Cache

If a logged-out request does not produce a Page Cache hit, use [Troubleshoot
Page and Edge Cache](/docs/troubleshooting/page-edge-cache/). It covers cache
population, cookies, response headers, explicit bypass functions, and Edge
Cache plugin errors.
