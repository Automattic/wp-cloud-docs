# Object Cache

Persistent Object Cache is enabled on every WP Cloud site. WordPress uses it to
store data that would otherwise need to be calculated or retrieved from the
database again. WP Cloud provides Memcached as the persistent backend, so
cached values can be reused across requests.

Object Cache stores data and query results. It does not store rendered pages;
see [Page Cache](/docs/performance/cache/page-cache/) for full-page responses.

## How Object Cache works

WordPress stores each cached value as a key-value entry under a key and an
optional group. Code looks for the value before doing the expensive work,
creates and stores the value after a miss, and deletes or replaces it when the
underlying data changes.

Use the public `wp_cache_*` functions rather than calling the
`WP_Object_Cache` class directly. The main operations are:

- `wp_cache_get()` to read a value.
- `wp_cache_add()` to store a value only when the key does not exist.
- `wp_cache_set()` to store or replace a value.
- `wp_cache_replace()` to replace an existing value.
- `wp_cache_delete()` to remove one value.
- `wp_cache_flush()` to clear the cache.

See the [WordPress Object Cache
reference](https://developer.wordpress.org/reference/classes/wp_object_cache/)
for parameters and return values.

WP Cloud loads its persistent Object Cache through a platform-managed,
symlinked `object-cache.php` drop-in. Do not replace or edit this file. Its
public source is available in the [Automattic WP
Memcached](https://github.com/Automattic/wp-memcached/blob/master/object-cache.php)
repository.

Themes and plugins decide which application data to cache. Memcached does not
automatically cache every custom database query.

WP Cloud also includes
`/wordpress/mu-plugins/advanced-post-cache.php` for backward compatibility. The
[current public Advanced Post Cache
implementation](https://github.com/Automattic/advanced-post-cache/blob/master/advanced-post-cache.php)
is deprecated and its cache methods are disabled because WordPress 6.1 added
query caching to core. Legacy Advanced Post Cache snippets do not disable or
bypass persistent Object Cache.

## Expiration and eviction

Memcached uses a [Least Recently Used (LRU)
algorithm](https://memcached.org/blog/modern-lru/) to decide which items to
evict when it needs space. Frequently used items are more likely to remain in
the cache, but application code must never assume that a cached value will
exist.

`wp_cache_add()`, `wp_cache_set()`, and `wp_cache_replace()` accept a time to
live in seconds through the `$expire` parameter. The default value is `0`,
which means that the item has no time-based expiration.

No expiration does not mean permanent. Memcached can evict the item through
its LRU algorithm, and application code can replace, delete, or flush it. Code
must always be able to rebuild a missing cached value. See the [`wp_cache_*`
functions](https://developer.wordpress.org/reference/classes/wp_object_cache/#wp_cache_-functions)
for their parameters and return values.

Use an expiration that matches how long stale data is acceptable. Also add
explicit invalidation for events that make the cached result incorrect.
Expiration limits the stale period; it does not replace invalidation.

## Transients on WP Cloud

With a persistent Object Cache, WordPress stores transients in Object Cache
instead of the options table. A plugin, theme, or script must not query the
database directly and assume it can find every transient. For the same reason,
a command that lists transients from the database may not show values held in
Memcached.

Use `set_transient()`, `get_transient()`, and `delete_transient()` rather than
reading transient rows directly. A transient's expiration is a maximum, not a
minimum: the value may disappear earlier, so the code still needs a cache-miss
path. See the [WordPress Transients API
guide](https://developer.wordpress.org/apis/transients/).

Transients are a good choice when code should also work without a persistent
Object Cache. WordPress stores them in the database when no persistent cache is
available.

### Themes and plugins must not assume transients are database rows

Some themes and plugins make this incorrect assumption and fail when a
persistent cache is present. Always use the Transients API to create, read, and
delete transients. Treat a missing transient as a normal cache miss, even when
its requested expiration time has not passed.

## Investigate high query time

[Query Monitor](https://wordpress.org/plugins/query-monitor/) and [Debug
Bar](https://wordpress.org/plugins/debug-bar/) can show repeated or slow
database queries and the functions that call them. Compare query time with the
same request's total generation time, and look for a query repeated across
requests with the same inputs.

Do not use one query count, query time, or Memcached size as a universal limit.
A large cache can be expected on a large site, while one slow uncached query can
be harmful on a smaller site. Start with the slow request and the code that
performs the work.

Use [Cache slow database
queries](/docs/troubleshooting/cache-slow-database-queries/) when a custom
query is a good candidate for application-level caching.

## Handle suspected cache conflicts

Persistent Object Cache cannot be disabled on WP Cloud. Do not attempt to
bypass it on a live site. If Object Cache appears to cause a compatibility
problem, reproduce the issue on a staging site and isolate the theme, plugin,
or custom code involved.

Do not use the legacy `$advanced_post_cache_object->flush_cache()` snippet as
an Object Cache diagnostic. In the current public Advanced Post Cache code,
that method is a no-op. A full Object Cache flush is also not a long-term fix:
it discards useful values and can increase database work until they are
rebuilt.

Report a confirmed compatibility issue to the theme or plugin author. Include
the steps that reproduce it, the affected cache keys or groups if known, and
the result of testing without the suspected code on staging.
