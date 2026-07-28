# WordPress versions

WP Cloud manages WordPress core and normally makes a new WordPress release
available within 24 hours. Each site follows a managed version channel stored
as `wp_version`, rather than installing and updating its own copy of core.

Release changes are published in the [WP Cloud Platform Update
Schedule](https://wp.cloud/platform-update-schedule/) and announced on the
[WP Cloud blog](https://wp.cloud/blog/).

Host partners are responsible for choosing and managing each site's channel,
notifying end users about changes, and moving sites before a channel is
retired. Follow the [Platform Update
Schedule](https://wp.cloud/platform-update-schedule/) for current transition
dates, recommendations, and additional upgrade guidance.

## Available version channels

WP Cloud can provide up to three channels:

- `latest` — the current WordPress release.
- `previous` — the previous release still available on WP Cloud.
- `beta` — the current beta or release-candidate version.

The availability of `previous` and `beta` is not guaranteed. `previous` is
typically retained for 30 days, but a significant point release or platform
schedule can change that period. During a transition, `previous` and `latest`
can temporarily resolve to the same release.

These channel values describe platform-managed pointers rather than permanently
pinned WordPress versions. For example, a site on `latest` receives the new
stable release when WP Cloud advances that channel.

This means a channel name describes the site's update policy, while the
resolved WordPress release can change over time.

## Check and change a site's channel

The `wp_version` value is available through the site-meta and client-site-list
operations. Use [List Client Sites](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+)
when checking the channels across a host client's inventory.

Use the [Configure Site WordPress Version
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-wordpress-version/{site}/{version})
to move a site to an available managed channel. Host partners can expose this
operation in their developer or customer control panels.

Plan customer communication and site testing before a channel is retired.
WP Cloud follows the WordPress core release schedule, and the [Platform Update
Schedule](https://wp.cloud/platform-update-schedule/) is the source for WP
Cloud transition dates and current partner guidance.
