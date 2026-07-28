# Configure redirects and headers with custom-redirects.php

WP Cloud loads an optional `custom-redirects.php` file before WordPress for
requests handled by PHP. A site can use this file for redirects, response
headers, or narrowly scoped access rules without loading WordPress first.

Avoid `custom-redirects.php` when another supported platform, WordPress, or
web-server configuration can produce the same result. Use it sparingly and
test every change thoroughly. Planned Edge Rules functionality is intended to
replace most `custom-redirects.php` use cases.

Create `custom-redirects.php` in the site's `htdocs` directory and begin the
file with `<?php`. Test every change while logged out and with [Page
Cache](/docs/performance/cache/page-cache/) and [Edge
Cache](/docs/performance/cache/edge-cache/) enabled. A redirect or header can
be cached and affect more visitors than the original request.

The examples below are illustrative pseudocode, not an exhaustive set of
production-ready rules. Partners and site owners use them at their own risk
and are responsible for adapting and testing them. The file can support other
redirects, file and path handling, and response headers. Several compatible
rules can share the file, but each rule should send its response and call
`exit` when no later code should run.

## Redirect one path

```php
<?php

if ( '/subdir' === $_SERVER['REQUEST_URI'] ) {
    header( 'HTTP/1.1 301 Moved Permanently' );
    header( 'Location: /subdir-new' );
    exit;
}
```

Use a temporary status while testing when browsers or caches should not retain
the redirect. Change it to a permanent redirect only after confirming the
destination.

## Add response headers

```php
header( 'X-Content-Type-Options: nosniff' );
header( 'X-Frame-Options: SAMEORIGIN' );
header( 'Referrer-Policy: no-referrer-when-downgrade' );
```

WP Cloud sets the base HTTP Strict Transport Security header. Manage its
`includeSubDomains` behavior with the [HSTS subdomain
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-hsts-subdomain/{domain}/{enable}).
Do not attempt to replace the platform HSTS header in
`custom-redirects.php`.

## Redirect a site's home page

`HTTP_HOST` contains a hostname, not a URL scheme:

```php
if (
    'example.com' === $_SERVER['HTTP_HOST']
    && '/' === $_SERVER['REQUEST_URI']
) {
    header( 'HTTP/1.1 301 Moved Permanently' );
    header( 'Location: https://destination.example/news' );
    exit;
}
```

## Limit a path by country

WP Cloud makes the request country available as an ISO 3166-1 alpha-2 code in
`GEOIP_COUNTRY_CODE`. This example allows requests from the United States and
Canada. It bypasses the check for WP-CLI, where no browser request exists.

```php
$allowed_countries = array( 'US', 'CA' );

if ( 'cli' === PHP_SAPI ) {
    return;
}

$country_code = $_SERVER['GEOIP_COUNTRY_CODE'] ?? 'Unknown';

if ( ! in_array( $country_code, $allowed_countries, true ) ) {
    header( 'HTTP/1.1 404 Not Found', true, 404 );
    exit;
}
```

Country detection is not an identity or authentication control. Use it only
for a geographic access policy that can tolerate imperfect location data.

## Block a file or directory pattern

```php
if ( false !== strpos( $_SERVER['REQUEST_URI'], '/private-export/' ) ) {
    http_response_code( 410 );
    exit;
}
```

## Limit a path by IP address

```php
$allowed_ips = array( '192.0.2.10', '198.51.100.20' );

if (
    false !== strpos( $_SERVER['REQUEST_URI'], '/sandbox' )
    && ! in_array( $_SERVER['REMOTE_ADDR'], $allowed_ips, true )
) {
    header( 'HTTP/1.0 403 Forbidden' );
    echo '403 Forbidden';
    exit;
}
```

Replace the documentation-only addresses with the exact trusted addresses.
Do not use a broad range when the service can provide stable individual IPs.
