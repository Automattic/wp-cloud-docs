# Respond to a compromised site

WP Cloud protects managed WordPress core through read-only symlinks, but a site
can still be compromised through vulnerable plugins or themes, custom code,
stolen administrator credentials, or exposed SSH and SFTP access. A compromised
site can host malware, inject content into files or the database, redirect
visitors, phish users, or add unauthorized accounts.

The host partner and site owner should contain and clean the site promptly.
Agree on who will preserve evidence, communicate with the end user, clean the
site, and decide whether a temporary suspension is necessary. A maintained
scanner such as Jetpack Scan can provide continuous detection and cleanup
assistance. WP Cloud also offers a [one-site malware
scan](/docs/security/site-security/malware-scanning/) for partner support investigations.

## Recognize a compromise

Common signs include:

- a malware scanner or security plugin alert;
- redirects to spam, scam, or unfamiliar sites;
- pages or content the owner did not add;
- unknown administrator accounts, plugins, or themes;
- randomly named or unexpected PHP files visible over SSH or SFTP;
- suspicious requests paired with high CPU use;
- PHP errors from unfamiliar code; and
- unexpected activity in [Metrics](/docs/monitoring-logs/metrics/),
  [web server logs](/docs/monitoring-logs/logs/web-server-logs/), or
  [PHP error logs](/docs/monitoring-logs/logs/error-logs/).

Treat a suspicious file as evidence, not proof by filename alone. Legitimate
plugins can use obfuscation, dynamic execution, or names that resemble common
malware indicators.

## Contain the site

Before broad cleanup, take a backup or otherwise preserve the evidence needed
to understand the entry point. Then:

1. Remove or downgrade unknown administrator accounts.
2. Revoke or replace compromised SSH/SFTP credentials.
3. Reset WordPress administrator passwords and invalidate active sessions.
4. Patch, replace, deactivate, or remove the vulnerable extension or custom
   code that allowed the compromise.
5. Consider temporarily setting [PHP filesystem
   permissions](/docs/security/site-security/filesystem-permissions/) to `ro` while
   investigating. WordPress writes will fail until normal access is restored.

Reset administrator passwords without loading site code:

```bash
wp --skip-plugins --skip-themes user reset-password --skip-email \
  $(wp --skip-plugins --skip-themes user list --role=administrator --field=id)
```

Review custom roles with `wp role list` and reset any other account with
administrator-equivalent capabilities. The site owner should also secure its
email account, identity provider, WordPress.com account when used, and any
other system that can restore access to WordPress.

Invalidate WordPress cookies and sessions by changing the authentication salts:

```bash
wp --skip-plugins --skip-themes config shuffle-salts
```

This logs out every WordPress session. When WP-CLI cannot edit the file, create
unique values at [WordPress.org's salt generator](https://api.wordpress.org/secret-key/1.1/salt/)
and replace the matching definitions in `wp-config.php`.

## Replace extensions with clean copies

List plugins and themes before deleting anything. Preserve custom and premium
packages until the owner has a clean original. Reinstall a WordPress.org plugin
from its official source with:

```bash
wp --skip-plugins --skip-themes plugin install plugin-slug --force
```

Reinstall a WordPress.org theme with:

```bash
wp --skip-plugins --skip-themes theme install theme-slug --force
```

`--force` overwrites local modifications. Do not run a bulk reinstall when a
premium or custom package shares a WordPress.org slug or when the site relies
on modified extension files. [Symlinked managed
software](/docs/wordpress/software-versions/managed-software/) can
also produce expected permission warnings and should remain on its managed
path.

Remove unneeded inactive software only after the site owner confirms it:

```bash
wp --skip-plugins --skip-themes plugin delete \
  $(wp --skip-plugins --skip-themes plugin list --status=inactive --field=name)

wp --skip-plugins --skip-themes theme delete \
  $(wp --skip-plugins --skip-themes theme list --status=inactive --field=name)
```

For additional protection during cleanup, the owner can disable the built-in
plugin and theme editors above the stop-editing line in `wp-config.php`:

```php
define( 'DISALLOW_FILE_EDIT', true );
```

## Inspect custom files and the database

Check the site root, `wp-content`, plugins, themes, and uploads for files that
do not belong. PHP files in an uploads directory, web-accessible backup files,
recently modified copies of `index.php` or `license.php`, and code that is not
present in an official package deserve review.

SSH search tools can narrow the inspection. Limit the directory and file type
so the search remains practical:

```bash
ag -RQ "getallheaders" --php htdocs/wp-content/plugins htdocs/wp-content/themes
ag -RQ "base64_" --php htdocs/wp-content
```

Strings such as `eval(`, `exec(`, `base64_`, and `getallheaders` also appear in
legitimate software. Read the surrounding code and compare it with a trusted
package before removing it. Review the database for injected administrator
accounts, options, posts, widgets, and scheduled events as well as filesystem
changes.

## Extended cleanup steps

The commands above address common compromises, but they do not prove that the
site is clean. Use the following checks when the infection is widespread,
reappears after an initial cleanup, or cannot be traced to one extension or
credential.

Work from reversible changes and record what was changed, when it was changed,
and why. A fast cleanup that destroys the only useful evidence can leave the
entry point open and make a second compromise harder to diagnose. Preserve a
copy before removing unfamiliar files or database values.

### Review every account with elevated access

List administrators and inspect custom roles before resetting passwords:

```bash
wp --skip-plugins --skip-themes user list --role=administrator
wp --skip-plugins --skip-themes role list
```

Remove an account only when the site owner confirms that it is unauthorized.
When ownership is uncertain, lower its role and block its access while the
owner investigates. Review application passwords, SSO connections, and any
external control panel that can create or change WordPress users.

Changing WordPress passwords alone does not secure a compromised mailbox,
identity provider, SSH key, or SFTP credential. Rotate each affected access
method and remove credentials whose owner or purpose cannot be established.

### Compare active software with trusted packages

Record the active plugin and theme lists before changing them:

```bash
wp --skip-plugins --skip-themes plugin list
wp --skip-plugins --skip-themes theme list
```

Reinstalling from WordPress.org is appropriate only when that package is the
site's real source. Premium plugins and themes, custom packages, forks, and
modified code need a clean copy from their owner or vendor. Reinstalling a
WordPress.org package with the same slug can overwrite the wrong software and
remove legitimate customizations.

Inspect the active theme and its parent separately. If either contains custom
work, compare it with the owner's known-good repository or backup instead of
using a bulk `--force` reinstall. Do not treat expected read-only errors from
WP Cloud's symlinked managed software as evidence of malware.

### Search outside the obvious paths

Check the site root and `wp-content` for recent or unexpected files, including
PHP in uploads, executable files inside cache directories, abandoned backup
archives, and altered bootstrap files. File timestamps can help narrow the
review, but an attacker can change them and a normal deployment can update many
files at once.

Search for several indicators rather than relying on one string:

```bash
ag -RQ "eval\\(" --php htdocs/wp-content
ag -RQ "exec\\(" --php htdocs/wp-content
ag -RQ "error_reporting\\(E_ALL" --php htdocs/wp-content
ag -RQ "getallheaders" --php htdocs/wp-content
```

Read every match in context. Legitimate packages can contain the same
functions. Compare suspicious code with an official release, a trusted source
repository, or a backup from before the first known sign of compromise.

### Check persistence in WordPress data

Malicious code can be stored in the database even after infected files are
replaced. Review recently created administrator users, active plugins, theme
settings, widgets, posts, options that contain scripts or unfamiliar domains,
and scheduled cron events. Confirm that important changes belong to the site
owner before deleting them.

Avoid a single combined “quick clean” command on an unfamiliar site. Separate
commands make their effects reviewable and allow the partner to stop when a
premium package, custom role, or unexpected file needs owner input. A backup
restore can be useful when its date predates the compromise, but the vulnerable
extension or stolen credential still needs to be fixed before the restored
site returns to service.

## Finish the cleanup

Run another maintained malware scan, test logged-out and administrator flows,
and confirm that redirects, unexpected content, error logs, and resource use
have returned to normal. Restore the intended filesystem-permission mode and
remove temporary restrictions only after the site is clean.

The owner should update every affected credential, enable multi-factor
authentication where available, remove unused application connections, and
keep WordPress, plugins, and themes on supported versions. Continued or repeat
abuse may require the host partner to apply its own warning or suspension
policy.
