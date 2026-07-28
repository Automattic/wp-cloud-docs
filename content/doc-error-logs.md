# Error logs

Partners and their customers should use WP Cloud's PHP error logging instead of WordPress core debug logging for PHP error events. Configuring `WP_DEBUG_LOG` or PHP `log_errors` can interfere with the automated, API-retrievable logging WP Cloud provides and can create large log files.

WP Cloud records PHP errors for every site. Partner developers and support teams can retrieve recent errors through the WP Cloud API, inspect the site's log file over SSH or SFTP, or use WP-CLI.

## Retrieve error logs through the API

The [Get Site PHP Error Logs endpoint](https://wp.cloud/docs/api/#tag/logs/POST/site-error-logs/{site}) accepts an Atomic Site ID or domain and a required `start` and `end` time range. Both values can be Unix timestamps or date strings accepted by PHP's `strtotime()` function. Logs are guaranteed for 28 days; an earlier start time may return incomplete data.

The endpoint supports pagination, ascending or descending sort order, and severity filters for `User`, `Warning`, `Deprecated`, and `Fatal error`. A successful response includes each error's message, severity, file, line, timestamp, and Atomic Site ID. Error messages and file paths can expose customer or application details, so restrict access and redact them before sharing.

Read the severity, message, file, and line together to identify the type and location of an error. No single field identifies the complete cause.

When an error occurs during a slow request, compare the same time range with Metrics and reproduce the request with [application performance monitoring (APM)](/docs/monitoring-logs/apm/) enabled. The error log identifies the PHP event, while the APM trace shows the application work around the captured request.

The [Insights section in the WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud) can also help partner support teams inspect site behavior before retrieving a specific log range.

## Read the error log on the site

WP Cloud writes PHP errors to `/tmp/php-errors`. Partner developers and support teams can read this file through [SSH or SFTP access](/docs/site-access/ssh-sftp/).

WP Cloud also provides the `wp php-errors` command. It returns the last 100 errors by default. Use `--limit` to request a different number:

```bash
wp php-errors --limit=25
```

## Avoid conflicting WordPress debug logging

Do not configure WordPress core debug logging for routine PHP error collection on WP Cloud. Use the platform error log, API endpoint, or `wp php-errors` command instead.

If a short investigation specifically requires WordPress debug logging, locate the existing debug constants in `wp-config.php`:

```php
if ( ! defined( 'WP_DEBUG' ) ) {
    define( 'WP_DEBUG', false );
}
```

Replace that block with the following configuration. WordPress then writes events to a separate `/wp-content/debug.log` file:

```php
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
```

**Important:** Setting `WP_DEBUG_LOG` or enabling PHP `log_errors` with `ini_set()` can conflict with WP Cloud's platform logging, cause some errors to be absent from the API error log, and create a large log file.

For short, controlled browser debugging, PHP error display can also be enabled:

```php
ini_set( 'log_errors', 'On' );
ini_set( 'display_errors', 'On' );
ini_set( 'error_reporting', E_ALL );
```

Do not display PHP errors to visitors on a production site. Error output can expose file paths, code details, and other sensitive information. Remove temporary debugging changes after the investigation.

## Understand repeated and missing errors

WP Cloud condenses repeated messages as `Repeated x more times`. Each site receives two error-log message allocations per second and can bank up to 100 allocations. Messages above that allowance are skipped and represented by a message such as `Skipped x error log messages due to rate limiting`.

If expected errors are missing, first check for custom `WP_DEBUG_LOG` or `log_errors` settings. Those settings can prevent some platform-level error logging even when WordPress writes its own debug file.

Compare the API response, `wp php-errors`, and `/tmp/php-errors` over the same timestamp range. An empty API or portal result does not prove that no PHP error occurred. If the file contains an error that the API does not return, preserve the event time and time zone, API filters, sort order, and result limit before changing the logging configuration.
