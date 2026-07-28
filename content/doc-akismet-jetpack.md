# Akismet and Jetpack

Every WP Cloud site includes platform-managed copies of WordPress core,
Akismet, and Jetpack. The packages are read-only and symlinked from shared
platform storage. An inactive Akismet or Jetpack plugin does not use the
customer's filesystem quota or consume processing resources.

All WP Cloud sites include active Akismet protections. Keep Akismet installed
and active so the site continues to receive that protection.

Jetpack is optional. WP Cloud partners can enroll in a Jetpack partnership,
offer a Jetpack Lite plan, and provide paid upgrade paths that generate
additional revenue. See [Jetpack backups](/docs/backups-restores/jetpack-backups/)
for one optional service available through a Jetpack partnership.

## Remove a managed plugin

Akismet or Jetpack must be unlocked before it can be deleted. Send the
`unlock` action for the plugin to the [Manage Site Software
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site}),
then remove the plugin from the site.

Unlocking and removing a managed package leaves that site without the
platform-managed copy. Confirm that a partner product or customer workflow
does not depend on the plugin before removing it.

In practice, this means an inactive managed package can remain installed at no
filesystem cost. For example, a host partner can leave Jetpack inactive until
a customer selects a plan that uses it.
