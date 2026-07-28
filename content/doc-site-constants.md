# Site constants

WP Cloud defines PHP constants that identify the platform, site, and host
client. Plugins and themes can use them when behavior should apply only to WP
Cloud or to sites belonging to a particular host client.

| Constant | Value |
| --- | --- |
| `IS_ATOMIC` | Defined as `true` on WP Cloud infrastructure. |
| `ATOMIC_SITE_ID` | The site's persistent Atomic Site ID. |
| `ATOMIC_CLIENT_ID` | The ID of the WP Cloud host client that owns the site. |

Check that a constant exists before using it. For example, the following code
runs only on WP Cloud sites owned by client ID `2`:

```php
if (
    defined( 'IS_ATOMIC' )
    && IS_ATOMIC
    && defined( 'ATOMIC_CLIENT_ID' )
    && '2' === ATOMIC_CLIENT_ID
) {
    // Run WP Cloud client-specific code.
}
```

Use [Persistent Data](/docs/sites/persistent-data/) for values that vary by
site and must be supplied by the host client. Do not treat Persistent Data as
the primary source of truth.
