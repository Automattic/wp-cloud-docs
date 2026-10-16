# WordPress versions

WP Cloud manages WordPress core and normally makes a new stable release available within 24 hours. Prerelease timing depends on the selected channel. Each site follows a managed version channel stored as `wp_version`, rather than installing and updating its own copy of core.

Release changes are published in the [WP Cloud Platform Update
Schedule](https://wp.cloud/platform-update-schedule/) and announced on the
[WP Cloud blog](https://wp.cloud/blog/).

Host partners are responsible for choosing and managing each site's channel,
notifying end users about changes, and moving sites before a channel is
retired. Follow the [Platform Update
Schedule](https://wp.cloud/platform-update-schedule/) for current transition
dates, recommendations, and additional upgrade guidance.

## Available version channels

WP Cloud provides four managed version channels:

| Channel | Release and timing |
| --- | --- |
| `latest` | The current stable WordPress release. |
| `previous` | The previous release still available on WP Cloud. |
| `alpha` | A WordPress beta or release candidate (RC), available shortly after the WordPress project publishes it on WordPress.org. |
| `beta` | A WordPress beta or RC, available 24–48 hours after its publication on WordPress.org. |

The availability of `previous` and `beta` is not guaranteed. `previous` is
typically retained for 30 days, but a significant point release or platform
schedule can change that period. During a transition, `previous` and `latest`
can temporarily resolve to the same release.

Use `alpha` for dedicated test sites, automated tests, and the earliest plugin, theme, or integration compatibility checks. WP Cloud will not automatically roll back an `alpha` site if a prerelease causes significant issues.

Use `beta` when a 24–48 hour testing buffer is preferable. The buffer gives time for plugin and theme updates and core hotfixes. Sites already on `beta` remain on that channel and require no action. Security releases are the exception: WP Cloud can update channels sooner. The [version-channel announcement](https://wp.cloud/wordpress-version-channels-introducing-alpha-and-updating-beta-timing/) explains the timing change.

These channel values describe platform-managed pointers rather than permanently
pinned WordPress versions. For example, a site on `latest` receives the new
stable release when WP Cloud advances that channel.

This means a channel name describes the site's update policy, while the
resolved WordPress release can change over time.

## Check and change a site's channel

The `wp_version` value is available through the site-meta and client-site-list
operations. Use [List Client Sites](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+)
when checking the channels across a host client's inventory.

For a fresh site, set `wordpress-version` on the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}) to `latest`, `previous`, `beta`, or `alpha`. The default is `latest`. This field is ignored when `clone_from` or `restore_from` is supplied.

Use the [Configure Site WordPress Version
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-wordpress-version/{site}/{version})
to move a site to an available managed channel. Host partners can expose this
operation in their developer or customer control panels.

Plan customer communication and site testing before a channel is retired.
WP Cloud follows the WordPress core release schedule, and the [Platform Update
Schedule](https://wp.cloud/platform-update-schedule/) is the source for WP
Cloud transition dates and current partner guidance.
