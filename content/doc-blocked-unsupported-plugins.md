# Blocked and unsupported plugins

WP Cloud generally allows host partners and their customers to install the
plugins and themes they choose. A small number of plugins are blocked because
they conflict with the platform, perform excessive database writes, duplicate
built-in caching or security features, or create other infrastructure risks.

## Platform-blocked plugins

| Plugin slug | Reason |
| --- | --- |
| `bwp-minify` | Platform compatibility |
| `e-mail-broadcasting` | Excessive resource use |
| `send-email-from-admin` | Excessive resource use |
| `stopbadbots` | Conflicts with built-in security |
| `mailit` | Excessive resource use |
| `nginx-helper` | Conflicts with the server environment |
| `w3-total-cache` | Conflicts with built-in caching |
| `wp-fastest-cache` | Conflicts with built-in caching |
| `wp-super-cache` | Conflicts with built-in caching |
| `wp-rest-api-log` | Excessive database writes |
| `website-file-changes-monitor` | Excessive database writes and storage |

The plugin-slug and reason values identify the platform restriction. This
means a partner-specific restriction should not be added to this table unless
WP Cloud also blocks that slug at the infrastructure level.

## Caching and optimization plugins

WP Cloud provides [Page Cache](/docs/performance/cache/page-cache/) and
[Object Cache](/docs/performance/cache/object-cache/) as managed platform
features. Plugins that require their own `advanced-cache.php` or
`object-cache.php` file do not provide a supported replacement for those
features.

Optimization features that do not replace the complete caching system can
still work. For example, WP Rocket features outside its full-page caching can
be used, but its cache is only partially functional because it must write to
files reserved for WP Cloud's built-in caching.

Plugins must also work within the [WP Cloud server specifications and
settings](/docs/infrastructure/server-specs-settings/). ionCube Loader is not
available because of its performance and security implications.

## Partner-specific restrictions

A host partner may maintain an additional disallowed-plugin policy for its
customers. Those restrictions can reflect the partner's products, policies,
abuse controls, or managed plugins and do not mean that every listed plugin is
incompatible with WP Cloud.

Examples include the [Pressable disallowed-plugin
list](https://pressable.com/knowledgebase/disallowed-plugins/) and the
[WordPress.com incompatible-plugin
list](https://wordpress.com/support/plugins/incompatible-plugins/).

Managed partners can apply additional blocks through managed environment
plugins in a custom chroot. See [Symlinks and managed
software](/docs/wordpress/software-versions/managed-software/) for
the client-level and site-managed options. Self-service partners can enforce
their own restrictions through custom plugins deployed with the [Manage Site
Software endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site}).
