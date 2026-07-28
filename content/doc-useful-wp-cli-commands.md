# Useful WP-CLI commands

WP-CLI provides command-line access to WordPress over SSH. Host-partner
developers and support teams can use it to inspect or change a site without
working through each WordPress administration screen.

This reference covers common commands, not the complete interface. Use
`wp help <command>` on the site or the [WP-CLI command
reference](https://developer.wordpress.org/cli/commands/) for all parameters.
Commands that update options, content, users, plugins, themes, or files can
change a production site immediately; inspect the current state and take an
appropriate backup before a broad or destructive operation.

## Plugins and themes

Common plugin commands include:

```bash
wp plugin list
wp plugin activate PLUGIN_SLUG
wp plugin deactivate PLUGIN_SLUG
wp plugin delete PLUGIN_SLUG
wp plugin install PLUGIN_SLUG
wp plugin update PLUGIN_SLUG
wp plugin update --all
```

`wp plugin install` accepts a WordPress.org slug or a URL to an installation
ZIP. Add `--activate` to activate it after installation. An existing directory
is not overwritten unless `--force` is supplied:

```bash
wp plugin install health-check --force --activate
```

Manage plugin auto-updates with:

```bash
wp plugin auto-updates status PLUGIN_SLUG
wp plugin auto-updates enable PLUGIN_SLUG
wp plugin auto-updates disable PLUGIN_SLUG
```

See the [`wp plugin` reference](https://developer.wordpress.org/cli/commands/plugin/)
for the complete command.

Theme commands follow the same pattern:

```bash
wp theme list
wp theme activate THEME_SLUG
wp theme delete THEME_SLUG
wp theme install THEME_SLUG
wp theme install oceanwp --force
wp theme update THEME_SLUG
```

`wp theme install` also accepts an installation ZIP URL. A normal theme update
or delete applies only to a site-owned directory. A symlinked managed theme
must be changed through the [managed-software WP-CLI
commands](/docs/wordpress/wp-cli/managed-software-wp-cli/), the API,
or an appropriate file-access workflow. See the [`wp theme`
reference](https://developer.wordpress.org/cli/commands/theme/).

## Cache and rewrites

Flush Page Cache and Object Cache after a change that leaves stale WordPress
data or full-page responses:

```bash
wp cache flush
```

Do not use a cache flush as a substitute for finding a repeated invalidation
or application problem. When Edge Cache is enabled, use its own controls for
edge responses. See [Troubleshoot Page and Edge
Cache](/docs/troubleshooting/page-edge-cache/).

Inspect or rebuild WordPress rewrite rules with:

```bash
wp rewrite list --format=csv
wp rewrite flush
wp rewrite structure '/%year%/%monthnum%/%postname%/'
```

Changing the permalink structure affects public URLs. Use `wp rewrite flush`
alone when the structure is already correct and only the generated rules need
to be rebuilt.

## Jetpack

The Jetpack CLI is supplied by the Jetpack plugin, so it does not load when all
plugins are skipped.

```bash
wp jetpack module list
wp jetpack module activate MODULE_NAME
wp jetpack module deactivate MODULE_NAME
wp jetpack status
wp jetpack status full
wp jetpack sync start
wp jetpack disconnect blog
wp jetpack disconnect user USER_ID_OR_LOGIN
```

`all` can replace a module name when activating or deactivating modules.
`wp jetpack sync start` initiates a full sync and can be resource intensive;
prefer the Jetpack Debugger's incremental sync controls when they address the
problem.

## Content, options, roles, and menus

`wp site empty` removes content but does not delete plugins, themes, or their
settings:

```bash
wp site empty --yes
wp site empty --uploads --yes
```

The second form also removes media. Both commands are destructive.

WordPress options control site and plugin behavior:

```bash
wp option get OPTION_NAME
wp option update OPTION_NAME VALUE
wp option add OPTION_NAME VALUE
wp option delete OPTION_NAME
```

Check the option and its expected serialized type before an update or delete.
For example:

```bash
wp option update admin_email someone@example.com
```

An **One or more database tables are unavailable** message can mean the
options table is damaged. Restoring an earlier database copy can discard every
database change after that backup, so confirm the scope before using a restore
as the repair.

List and change posts with:

```bash
wp post list
wp post list --post_type=post,page --format=count
wp post update POST_ID --post_status=draft
wp post delete POST_ID
wp post exists POST_ID
```

`wp post list` supports filters such as `--post_type` and
`--posts_per_page`. A comma-separated `--post_type` value can include posts,
pages, attachments, products, or another registered type.

Other useful administration commands include:

```bash
wp role list
wp role reset ROLE
wp role reset --all

wp menu list
wp menu item list TERM_ID
wp menu item update MENU_ITEM_ID

wp media regenerate --only-missing
```

Resetting a role restores its capabilities to the WordPress default and can
remove intentional custom capabilities. `wp media regenerate` writes image
files and is not compatible with regeneration while [Intermediate Image
Offloading](/docs/performance/image-optimization/offload-image-sub-sizes/)
is enabled.

## Skip plugins or themes

A plugin or theme can prevent WordPress from loading far enough for WP-CLI to
run. Global flags can skip all or selected components:

```bash
wp --skip-plugins --skip-themes plugin list
wp --skip-plugins=woocommerce,code-snippets plugin list
```

Put global flags after `wp` and before the command. Skipping plugins also
changes the application state observed by the command; a result can differ
from a normal web request. In particular, `wp jetpack` is unavailable with
`--skip-plugins` because Jetpack supplies the command.

WP Cloud's PHP error command can be run while skipping site code:

```bash
wp --skip-plugins --skip-themes php-errors
wp --skip-plugins --skip-themes php-errors --limit=25
```

`wp php-errors` reads recent PHP errors recorded by the platform. It does not
report browser JavaScript, CSS, or HTML problems; use browser developer tools
for those. See [Error logs](/docs/monitoring-logs/logs/error-logs/).

## WP Cloud managed-software commands

WP Cloud provides commands for switching eligible plugins and themes between
managed symlinks and site-owned installations:

```text
wp atomic plugin use-managed <name> [--remove-existing]
wp atomic plugin use-unmanaged <name> [--remove-existing] [--version=X.Y.Z]
wp atomic theme use-managed <name> [--remove-existing]
wp atomic theme use-unmanaged <name> [--remove-existing] [--version=X.Y.Z]
```

The focused [Manage platform software with WP-CLI
guide](/docs/wordpress/wp-cli/managed-software-wp-cli/) explains
the replacement prompts, `--remove-existing`, and unmanaged-version risks.

## Diagnose CLI output

HTML printed in place of normal WP-CLI output often comes from maintenance
mode or plugin or theme code that produces output while WordPress loads. Check
for a maintenance plugin, then retry with plugins or themes skipped separately
to identify which group changes the result. Narrow the skip list to the
specific slug before changing or removing software.

WP Cloud can restrict some SSH or WP-CLI commands for platform security and
performance. A restriction is not evidence that the same operation should be
recreated through a web-accessible script. Use the supported API or WP-CLI
operation when one is available.
