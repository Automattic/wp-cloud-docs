# Manage platform software with WP-CLI

WP Cloud adds `wp atomic` commands that switch eligible plugins and themes
between a host client's managed, symlinked package and a normal site-owned
installation. The managed package must already exist in the host client's
deployed chroot. These commands cannot turn arbitrary plugins or themes into
managed software.

## Available commands

```text
wp atomic plugin use-managed <name> [--remove-existing]
wp atomic plugin use-unmanaged <name> [--remove-existing] [--version=X.Y.Z]
wp atomic theme use-managed <name> [--remove-existing]
wp atomic theme use-unmanaged <name> [--remove-existing] [--version=X.Y.Z]
```

Each command prompts before removing an existing symlink or directory with the
same slug. `--remove-existing` confirms that replacement without an interactive
prompt. Check the slug and current installation before using it in automation.

`use-managed` is available only when that plugin or theme already exists as a
managed package in the host partner's chroot. It replaces the existing
site-owned directory with the managed symlink. `use-unmanaged` removes the
managed symlink and installs a normal site-owned copy. Use `--version` with
`use-unmanaged` when a specific available version is required.

The command fields and values mean:

- `<name>` is the plugin or theme slug;
- `--remove-existing` permits replacement of the directory at that slug; and
- `--version=X.Y.Z` selects the requested unmanaged version.

For example, the following replaces an existing site-owned copy with the
managed plugin already available in the client chroot:

```bash
wp atomic plugin use-managed example-plugin --remove-existing
```

This means the managed package replaces the directory for that slug; it does
not merge files from the two installations.

## Avoid leaving outdated software unmanaged

This guidance applies only to software available in the host partner's chroot,
including platform-provided managed packages and packages that an approved
managed partner added through its external repository. Not every plugin or
theme is available as managed software.

When a managed option exists, prefer it. An unmanaged plugin or theme no longer
follows the host client's managed release channel. Installing an older version
can expose a site to security and compatibility problems. Use an unmanaged
rollback only as a short-term measure when the host partner and site owner
understand the risk, then update the software or return it to the managed
channel.

For the symlink model, release channels, update schedule, and API alternative,
see [Symlinks and managed
software](/docs/wordpress/software-versions/managed-software/).
