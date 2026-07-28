# Symlinks and managed software

WP Cloud uses symbolic links, or symlinks, for WordPress core and other
software that the platform or a host client manages across many sites. A
symlink points a site to a shared, versioned package instead of placing another
writable copy of the package in the site's filesystem.

Symlinked files are read-only to the host client's end users. This protects
managed code from accidental changes and malware, keeps sites on a known
version, excludes shared packages from the customer's filesystem usage, and
allows an update to be deployed consistently without storing the same files on
every site.

Custom chroots for external repositories and client-level managed deployments
are available only to Managed WP Cloud partners. A Managed partnership does
not automatically include a custom chroot; WP Cloud must approve and configure
it for the client account. Self-Service partners cannot use custom chroots.
They can deploy their own software through SSH automation or install supported
externally hosted packages with the [Manage Site Software
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site}).

## Types of managed software

WP Cloud sites can contain three distinct kinds of symlinked or client-managed
software.

### WP Cloud-managed software

WP Cloud owns the platform-level packages, including:

- WordPress core selected through the site's managed `wp_version` channel;
- infrastructure and cache drop-ins such as `object-cache.php` and
  `advanced-cache.php`; and
- the platform-managed copies of Jetpack and Akismet.

The WordPress core directory is never writable. In a site's `htdocs`
directory, `__wp__` points to the active managed channel:

```text
lrwxrwxrwx 1 root root 24 Aug 22 01:50 __wp__ -> ../wordpress/core/latest
-rw-r--r-- 1 123456789 site123456789 3.6K Jan 8 22:06 wp-config.php
drwxrwxr-t 11 root site123456789 14 Aug 29 17:52 wp-content
lrwxrwxrwx 1 root root 18 Feb 12 2023 wp-load.php -> __wp__/wp-load.php
```

The site owns `wp-config.php` and `wp-content`, while WordPress core remains in
the managed path. This is why [ABSPATH](/docs/wordpress/configuration/abspath/)
does not identify the site's writable content directory.

The full directory listing also contains ownership and permission details for
the site ID, its group, and the platform-owned symlinks. Those values vary by
site; the important boundary is that root owns the platform links while the
site owns its writable configuration and content.

### Client-level mu-plugins

A managed host client with a custom chroot can place always-on code directly
in an external repository's `mu-plugins` directory. WP Cloud loads this code
for sites using that chroot before normal per-site plugin management.

Direct client-level mu-plugins do not appear in the site's plugin list and
cannot be disabled by the site user, the Manage Site Software endpoint, or WP
Cloud's software-management WP-CLI commands. Use this location only for code
that must apply broadly at the client or chroot level.

### Client-managed plugins and themes

A host client can provide selected plugins and themes as versioned packages in
its chroot. A site can install or activate those packages during creation,
through the Manage Site Software endpoint, or with [WP Cloud's managed-software
WP-CLI commands](/docs/wordpress/wp-cli/managed-software-wp-cli/).

Unlike platform-level core and cache files, ordinary client-managed plugins and
themes belong to the site. An end user can remove the symlink and install an
unmanaged copy. Software installed normally through WordPress is not
automatically converted to a managed package, even when a package with the
same slug exists in the client chroot.

For example, a plugin directory can contain both managed symlinks and normal
site-owned directories:

```text
lrwxrwxrwx 1 root root 41 Aug 22 01:50 akismet -> ../../../wordpress/plugins/akismet/latest
drwxr-xr-x 5 149906491 site123456789 10 Jan 24 18:56 gutenberg
lrwxrwxrwx 1 root root 41 Aug 22 01:50 jetpack -> ../../../wordpress/plugins/jetpack/latest
lrwxrwxrwx 1 123456789 site123456789 58 Oct 3 18:13 partner-login -> ../../../wordpress/plugins/partner-login/latest
drwxr-xr-x 11 149906491 site123456789 24 Jan 5 18:58 redirection
```

Akismet, Jetpack, and `partner-login` are managed. Gutenberg and Redirection
in this example are site-owned directories. WP Cloud can configure advanced
client behavior that automatically restores selected managed symlinks, but a
host partner should request that behavior only after deciding how it affects
customer ownership and support workflows.

An ordinary client-managed plugin such as `partner-login` is still owned by
the site even though its directory is a symlink. It can be removed through
SFTP or the supported software-management command and replaced with an
unmanaged copy. Platform packages such as the cache drop-ins do not share that
per-site ownership behavior.

## Build an external repository

Managed partners with custom chroots can supply a public or private GitHub
repository. The [WP Cloud external repository
example](https://github.com/Automattic/wpcloud-externals-example/) shows the
required layout. The `scripts`, `usr/local/bin`, and `.gitmodules` paths are
optional advanced features; `scripts` accepts files rather than nested
directories.

Package each plugin or theme as a complete WordPress package. Version
directories should sit behind a release-channel symlink:

```text
wordpress/plugins/example-plugin/
|-- latest -> 1.4.0
|-- previous -> 1.3.2
|-- beta -> 1.5.0-beta.1
|-- 1.3.2/
|-- 1.4.0/
`-- 1.5.0-beta.1/
```

The `latest` symlink is required. Optional channels such as `previous` and
`beta` give the host partner more control over testing and rollbacks between
external deployments. A partner can define other channels that match its
release process. Changing a channel symlink in Git does not immediately change
a running chroot. WP Cloud must deploy the external repository update before a
site can switch to the new channel.

Private repositories use a deploy key so WP Cloud can monitor and deploy
updates. Generate a deploy key without a passphrase from:

```text
https://github.com/{github-username}/{repo-name}/settings/keys
```

Transfer the key through the secure method agreed with the WP Cloud team. Do
not place a private key in the repository, documentation, support request, or
site filesystem.

An external can also include Git submodules, custom PHP scripts under
`scripts`, and executable tools under `usr/local/bin`. These options affect the
client chroot and should be used only when an ordinary plugin, theme, mu-plugin,
or site automation cannot meet the requirement.

## Add a third-party package

A managed partner can request a plugin or theme that is maintained outside its
external repository. The package must be available from WordPress.org or a
public GitHub repository. A GitHub release ZIP must have the same layout as a
WordPress.org-generated package. For a plugin named `myplugin`, the ZIP should
contain the repository files inside a top-level `myplugin` directory. The
[Jetpack Beta deployment layout](https://github.com/Automattic/jetpack-beta#deployment)
is one example.

WP Cloud then adds the package to the chroot configuration, includes it in the
version-monitoring process and client filter, and deploys the rebuilt WordPress
portion of the chroot. The host partner remains responsible for deciding when
that third-party software is appropriate for its customers.

In concrete terms, the platform work adds the package to `packages-config`,
monitors its latest release, updates the client's chroot inclusion rules, and
rebuilds and deploys the WordPress portion of the chroot. A package is not
available to sites merely because a repository release exists.

## Install managed packages on sites

A package being present in every client chroot makes it available, including
under `/wordpress/` over SSH or SFTP; it does not install the package on every
site. Install or activate a managed plugin or theme through the software array
on the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client})
or after provisioning through the [Manage Site Software
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site}).
Supported [WP Cloud managed-software WP-CLI
commands](/docs/wordpress/wp-cli/managed-software-wp-cli/) can also
change plugin and theme symlink state.

For most per-site mu-plugin needs, keep the package under the external's normal
plugin path and install it as a site-managed mu-plugin. Common keys include:

```text
mu-plugins/{slug}/{version-or-channel}
mu-plugins/{slug}/{version-or-channel}/{loader-file}
```

An ordinary `install` action creates a site-managed mu-plugin that can later be
removed through the API. Use `install-locked` when production or customer sites
must not remove the package. A locked package requires API unlock or removal;
the end user and WP Cloud WP-CLI commands cannot fully delete it.

Test managed software before installing or activating it across customer
sites. Direct client-level mu-plugins and site-managed mu-plugins run without a
separate activation step. Direct client-level code is especially sensitive
because it applies to the chroot, does not appear in the plugin list, and
cannot be removed from one site. Active normal plugins can also break sites,
but their per-site state is easier to see and change.

## Restore managed symlinks

Use the [Manage Site Software
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site})
to restore a plugin or theme symlink that an end user removed. For routine
end-user support, supported [WP Cloud managed-software WP-CLI
commands](/docs/wordpress/wp-cli/managed-software-wp-cli/) can
return eligible software to a managed channel when the package is already
available in the host client's chroot.

## Updates and rollback channels

WP Cloud processes updates for client-managed externals, mu-plugins, plugins,
and themes Monday through Friday in the United States. Internal update alerts
are generated at 14:00 and 19:00 UTC and handled by the WP Cloud team. A Git
commit or release-channel change is not available to sites until that external
update is deployed.

Keep an alternate deployed channel such as `previous` for an important package
when the partner needs a quick rollback. If that channel already exists in the
chroot, an affected site can switch to it through the API or WP-CLI without
waiting for another external deployment. Prefer this managed rollback when an
end user needs an older version.

Without a deployed alternate, the partner must correct the external repository
and wait for an emergency or scheduled deployment. Removing a managed symlink
and installing an old unmanaged copy is another possible short-term response,
but the site then leaves the managed update path and can retain insecure or
incompatible code.

Managed plugins and themes supplied by a host client should be packaged as
complete releases in the repository. The host client owns the readiness and
quality of those releases; WP Cloud's deployment process does not replace
plugin or theme testing.

When no managed rollback channel exists and the host partner and end user
accept the security and compatibility risks, a support engineer can remove the
symlink through SSH or SFTP and install a WordPress.org or ZIP copy. The
supported WP Cloud command can also select an unmanaged version. Record that
exception: the site will no longer receive that package through the managed
symlink until it is returned to a deployed channel. The end user can also
ignore future updates, so unmanaged downgrades should remain a last resort.
