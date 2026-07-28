# Cache slow database queries

Repeated custom database queries can be good Object Cache candidates when
regenerating the result costs more than retrieving it from cache. This tutorial
shows how to find one query, add a cache hit and miss path, invalidate the
result, and confirm that the change works.

Use a staging site and code you maintain. Do not edit a third-party plugin
directly; an update will overwrite the change, and the plugin author may need
to fix the query for all users.

## Before you begin

You need:

- Access to the site's code and WP-CLI.
- [Query Monitor](https://wordpress.org/plugins/query-monitor/) or [Debug
  Bar](https://wordpress.org/plugins/debug-bar/) on a staging site.
- A repeatable request that runs the slow query.
- A way to change the data returned by the query so you can test invalidation.

Read [Object Cache](/docs/performance/cache/object-cache/) first if you are not
familiar with cache keys, groups, expiration, and early eviction.

## Identify a cacheable query

Open the slow page with Query Monitor or Debug Bar active. Record:

- The SQL query and how long it took.
- How many times it ran during the request.
- The calling function and file.
- The inputs that change its result, such as IDs, roles, locale, page number,
  or permissions.
- The events that make the result stale.

The source function usually appears immediately before `WP_Query` or the
database API in the call stack. Repeat the same request to confirm that the
query performs the same work with the same inputs.

Do not cache a result when it contains user-specific or permission-sensitive
data unless every relevant input is represented in the cache key and the
result cannot be read by the wrong user. Do not cache a write query.

## Work in maintained code

Locate the function that builds the query. If it belongs to a third-party
theme or plugin, report the query to its author or add the change through a
supported extension point. Copying the function into an unrelated snippet can
leave two implementations that drift apart.

The following uncached example calls the database every time the function
runs:

```php
function site_get_featured_post_ids() {
    return get_posts(
        array(
            'fields'         => 'ids',
            'meta_key'       => '_site_featured',
            'meta_value'     => '1',
            'no_found_rows'  => true,
            'numberposts'    => 10,
            'post_status'    => 'publish',
            'suppress_filters' => false,
        )
    );
}
```

This neutral example returns post IDs instead of a `WP_Query` object. Small,
plain values are easier for callers to reuse and less likely to carry request
state into a later request.

## Choose the key, group, and expiration

Give the cache entry a stable key and a project-specific group. Include every
input that can change the result. Add a version to the key when a future code
change will alter the stored value's shape.

This example has no variable inputs:

```php
$cache_key   = 'featured-post-ids-v1';
$cache_group = 'site-featured-content';
```

For a function with inputs, normalize them before building the key. For
example:

```php
$role_key  = implode( ',', array_map( 'sanitize_key', $roles ) );
$cache_key = 'invisible-product-ids-v1:' . md5( $role_key );
```

Do not put secrets or personal data in a cache key. A hash prevents a long key;
it does not make sensitive source data safe to expose elsewhere.

Choose an expiration based on how long stale data would be acceptable if an
invalidation hook is missed. The example uses one hour as a backstop, not as
its primary invalidation method.

## Add the cache hit and miss paths

Use the fourth `wp_cache_get()` argument to distinguish a missing value from a
cached falsey value such as an empty array:

```php
function site_get_featured_post_ids() {
    $cache_key   = 'featured-post-ids-v1';
    $cache_group = 'site-featured-content';
    $found       = false;

    $post_ids = wp_cache_get( $cache_key, $cache_group, false, $found );

    if ( ! $found ) {
        $post_ids = get_posts(
            array(
                'fields'           => 'ids',
                'meta_key'         => '_site_featured',
                'meta_value'       => '1',
                'no_found_rows'    => true,
                'numberposts'      => 10,
                'post_status'      => 'publish',
                'suppress_filters' => false,
            )
        );

        wp_cache_set(
            $cache_key,
            $post_ids,
            $cache_group,
            HOUR_IN_SECONDS
        );
    }

    return $post_ids;
}
```

The first request runs the query and stores the IDs. Later requests read the
same IDs from Object Cache until the entry is deleted, replaced, evicted, or
expired. A cache hit means the function can return the stored IDs without
running the database query. Next, add invalidation before testing the change.

## Invalidate the result

Delete the cache entry whenever an event can change the query result. This
example invalidates it after a post is saved or deleted:

```php
function site_clear_featured_post_ids_cache() {
    wp_cache_delete(
        'featured-post-ids-v1',
        'site-featured-content'
    );
}

add_action( 'save_post', 'site_clear_featured_post_ids_cache' );
add_action( 'deleted_post', 'site_clear_featured_post_ids_cache' );
```

A production implementation can use narrower hooks when the query depends on
one post type, taxonomy, option, or metadata field. Cover every write path,
including imports and API updates. If the result depends on several inputs,
either delete all affected keys or keep an index that lets the code find them.

## Verify the change

1. Clear the test entry with
   `wp cache delete featured-post-ids-v1 site-featured-content`.
2. Load the repeatable test request. Confirm that the database query runs and
   the page returns the expected posts.
3. Load the same request again. Confirm that the query is absent from Query
   Monitor or Debug Bar and that the result is unchanged.
4. Change a post so it enters or leaves the result set.
5. Load the request again. Confirm that the query runs once and the changed
   result appears.
6. Load it one more time. Confirm another cache hit.
7. Test an empty result. The `$found` check must allow an empty array to remain
   a valid cached value.

Compare page-generation and query time across several equivalent requests.
One fast request is not enough if the original slowdown appears only with a
particular role, page number, or dataset.

## Use the Transients API when portability matters

WP Cloud has a persistent Object Cache, so both `wp_cache_*` functions and the
Transients API use persistent cache storage. Transients also fall back to the
database on a WordPress installation without a persistent Object Cache. Use
them when that portability is useful and a single expiration-oriented key fits
the data.

The same invalidation rule applies: call `delete_transient()` when the source
data changes rather than waiting only for expiration. See the [WordPress
Transients API guide](https://developer.wordpress.org/apis/transients/).
