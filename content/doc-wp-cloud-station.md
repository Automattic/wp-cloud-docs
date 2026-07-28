# WP Cloud Station

[WP Cloud Station](https://github.com/Automattic/wpcloud-station) is an
open-source WordPress plugin and block theme that demonstrates a dashboard
built with the WP Cloud API. It can help a partner explore API usage or
prototype a management experience.

Station is experimental and is not recommended as a production customer
panel. Some WP Cloud features are missing or incomplete, and its example text
and interface are intended to be customized.

## Install Station

Use a separate WordPress test site and a dedicated WP Cloud API key. Station's
current plugin and theme packages are available from [GitHub
Releases](https://github.com/Automattic/wpcloud-station/releases).

1. Upload and activate the `wpcloud-station` plugin.
2. Open `/wp-admin/admin.php?page=wpcloud_admin_settings`.
3. Enter the WP Cloud client name, dedicated API key, and a default primary
   domain.
4. Add the Station server's static egress address to the API key's allowed IP
   ranges in [Manage and secure API
   keys](/docs/api-automation/api-access/).
5. Upload and activate the optional `wpcloud-station` block theme.
6. Use the Site Editor to replace example content and adjust the demonstration
   interface.

After the settings are saved, you should see the configured client connection
and can open `/sites` to view WP Cloud site records available to the key. Test
site creation and management only after that connection result is correct.

The frontend login is available at `/login`, and the site list is available at
`/sites` when the corresponding Station components are active.

Use an API key created for Station rather than a key shared with production
automation. Its endpoint scope should include only the actions being tested.
Revoking or changing the key immediately affects the Station connection.

## Extend the example

Station exposes a `wpcloud_site` custom post type, WordPress REST API behavior,
blocks, hooks, and callbacks that can be adapted in a partner prototype. Its
source is useful for examining one way to call WP Cloud, but the [public WP
Cloud API reference](https://wp.cloud/docs/api/) remains the authority for
endpoint behavior.

## Support and reporting bugs

Station is an open-source example rather than a supported production panel.
Report reproducible Station defects and feature requests in the [GitHub issue
tracker](https://github.com/Automattic/wpcloud-station/issues). Use the WP
Cloud API documentation when an example in Station differs from the current
public API contract.

## Contributing

Issues and pull requests can be submitted through the [Station
repository](https://github.com/Automattic/wpcloud-station). Follow the
repository's [contribution
guide](https://github.com/Automattic/wpcloud-station/blob/trunk/CONTRIBUTING.md)
before proposing a change.
