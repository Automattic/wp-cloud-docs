# Install Composer and WP-CLI packages

WP-CLI is already installed on WP Cloud sites. A partner developer or support
engineer with [Client SSH access](/docs/site-access/ssh-sftp/client-ssh/) can
add Composer and optional WP-CLI packages for a site-scoped development or
diagnostic workflow. An end user with [User SSH and SFTP
access](/docs/site-access/ssh-sftp/user-ssh-sftp/) can install them for the
site as well.

The steps below are examples. Profile behavior, package installation, command
availability, and results can vary. Composer and third-party WP-CLI packages
are outside WP Cloud's support scope. WP Cloud does not guarantee their
performance or security; the host partner or site owner is responsible for
installing, maintaining, securing, and supporting them.

Do not use a production WP Cloud site to compile projects such as themes.
Composer-based compilation may not work as expected, and WP Cloud does not
recommend using its hosting servers as build systems.

**Important:** If `.profile` is deleted or corrupted, installed commands may
not remain available in later SSH sessions. The commands can work immediately
after installation but may need to be registered again after reconnecting.

## Install Composer and configure paths

Connect to the site over SSH, then create the configuration directory:

```bash
mkdir -p "$HOME/.config"
```

Download the Composer installer:

```bash
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
```

For production use, follow [Composer's installer verification
instructions](https://getcomposer.org/download/) before running the downloaded
file.

Add the Composer and WP-CLI package directories to `.profile`:

```bash
printf '\n# Composer\nexport COMPOSER_HOME="$HOME/.config/composer"\n\n# WP-CLI\nexport WP_CLI_PACKAGES_DIR="$HOME/.config/wp-cli/packages"\n' >> "$HOME/.profile"
```

Confirm that the profile contains:

```bash
# Composer
export COMPOSER_HOME="$HOME/.config/composer"

# WP-CLI
export WP_CLI_PACKAGES_DIR="$HOME/.config/wp-cli/packages"
```

Load the profile and run the installer:

```bash
source "$HOME/.profile"
php composer-setup.php
```

If a later SSH session cannot find an installed package, confirm that
`.profile` still contains the variables and is loaded for that session. These
profile commands are examples and may need to be adapted to the user's shell
and session behavior.

## Install WP-CLI packages

Use [`wp package`](https://developer.wordpress.org/cli/commands/package/) after
Composer and the package path are configured. Two packages useful for
performance investigations are:

```bash
wp package install wp-cli/doctor-command:@stable
wp package install wp-cli/profile-command:@stable
```

The [Doctor command](https://github.com/wp-cli/doctor-command) runs configurable
site checks. The [Profile command](https://developer.wordpress.org/cli/commands/profile/)
measures stages and hooks during a WordPress request. Use their output with the
broader workflow in [Troubleshoot site
performance](/docs/troubleshooting/site-performance/).

When the newest package release requires a newer WP-CLI version than the site
provides, install the last compatible release instead of `@stable`. For
example:

```bash
wp package install "wp-cli/profile-command:<2.1.7"
```

Choose the version from the package's release and compatibility information;
the example is not a recommendation to pin every site to that release.
