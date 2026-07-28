# Repair Yoast indexables

After a site is cloned or its domain changes, Yoast SEO can continue to use a
former staging or production domain in canonical URLs and search results.
WP Cloud updates ordinary WordPress content during a domain change, but Yoast
stores canonical URLs in its own indexables and may need to rebuild them.

A common symptom is a search result or page source that still names a staging
hostname after the site has moved to its public domain. The visible WordPress
URL can be correct while the Yoast indexable record still contains the former
domain.

This behavior belongs to [Yoast SEO](https://wordpress.org/plugins/wordpress-seo/)
and Yoast SEO Premium rather than the WP Cloud domain system.

## Rebuild the indexables

Run the following command after the new domain has been added and WordPress is
using it:

```bash
wp yoast index --reindex
```

Yoast documents the command in its [WP-CLI indexables
guide](https://developer.yoast.com/features/wp-cli/reindex-indexables/).

Site administrators can instead use the [Yoast dashboard procedure for
resetting indexables](https://yoast.com/help/how-to-reset-yoast-indexables/).
After the rebuild, inspect the affected page's canonical URL and sitemap. A
search engine can retain an older result until it crawls the corrected page
again.

Run the rebuild only after the domain change and WordPress search-and-replace
have completed. Rebuilding before the site uses its final hostname can simply
store the staging or former domain again. On a cloned site, perform the repair
on the destination rather than altering the source site's indexables.

For plugin-specific behavior beyond rebuilding indexables, use the [Yoast help
center](https://yoast.com/help/).
