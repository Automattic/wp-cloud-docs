# PHP lifecycle and supported versions

WP Cloud manages the PHP versions available to sites and follows the PHP
project's [supported-versions schedule](https://www.php.net/supported-versions.php).
Host partners choose an available version for each site and should move
customers away from a retiring version before WP Cloud removes it.

WP Cloud version additions, default changes, and removal dates are published
in the [Platform Update Schedule](https://wp.cloud/platform-update-schedule/)
and announced on the [WP Cloud blog](https://wp.cloud/blog/). Host partners
should read and follow the Platform Update Schedule for current upgrade
recommendations, best practices, and transition dates.

## Check available and active versions

Use the [Get PHP Versions
endpoint](https://wp.cloud/docs/api/#tag/servers/GET/get-php-versions/{client}[/verbose])
to retrieve the versions available to a host client. The verbose response
identifies the platform default and provides `status` and `until` details for
each version. Treat `until` as the final date that version will be available
on WP Cloud.

For example, a verbose response can identify one version as the `default`,
another as available but retiring, and give the retiring version an `until`
date. Those field values let a partner update its site-creation default and
schedule existing-site upgrades from the same platform response.

A partner can select `php_version` while creating a site. For existing sites,
read or change `php_version` with the [Site Meta
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}).
Use [List Client Sites](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+)
to audit active PHP versions across the host client's inventory.

## Plan version retirements

Review the [Platform Update Schedule](https://wp.cloud/platform-update-schedule/)
before setting a customer migration timeline. It contains the current WP Cloud
schedule and additional recommendations for the affected PHP release.

For PHP versions after 8.1, WP Cloud uses an annual platform transition date.
Host partners should move customer sites away from the retiring version by
December 15 at 12:00 UTC in the applicable year, unless the Platform Update
Schedule specifies otherwise.

Start well before that date:

1. Test sites and partner-owned software on a supported PHP version.
2. Announce the customer-facing timeline and any action customers must take.
3. Remove the retiring version from customer controls before the WP Cloud
   deadline.
4. Later, remove it from internal tools and stop using rollback to the retiring
   version as a support solution.
5. Move remaining sites to the current default with enough time to address
   compatibility problems before the platform cutoff.

Advance the default for newly created sites soon after a stable PHP release is
available. This reduces the number of sites that must be moved when an older
release reaches the end of its security-support period.

PHP itself provides two years of active support for a release branch followed
by two years of security-only fixes. WP Cloud's published platform dates
control availability on WP Cloud, even when an upstream branch remains in a
different support phase. Give customers a buffer between the partner's forced
upgrade date and the WP Cloud cutoff so application compatibility can be
addressed without a last-minute rollback.
