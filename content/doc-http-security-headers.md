# HTTP and security headers

HTTP headers carry information and instructions with a browser request or a
server response. WP Cloud supplies platform headers for transport security,
caching, and other managed behavior. WordPress code can add many application
headers, but it cannot replace every platform-controlled value.

A request header describes the browser and what it is asking for. For example:

```http
GET /support/ HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.5
Cookie: wordpress_logged_in_example=value
Cache-Control: no-cache
```

The server answers with response headers before the response body:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Vary: Cookie
Cache-Control: max-age=60, must-revalidate
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=15552000; preload
```

The exact values depend on the URL, login state, cache state, site code, and
WP Cloud services that handled the request. Inspect the response you need to
change rather than copying a header set from another site.

## Common response headers

| Header | Purpose | Site code can set it? |
| --- | --- | --- |
| `X-Robots-Tag` | Controls search-engine indexing for PHP-generated responses. It does not apply to static assets through the same path. | Yes |
| `Access-Control-Allow-Origin` | Identifies the origin whose frontend code may read a cross-origin response. | Yes |
| `Access-Control-Allow-Headers` | Identifies request headers allowed by a CORS preflight response. | Yes |
| `Access-Control-Allow-Methods` | Identifies methods allowed by a CORS preflight response. | Yes |
| `Access-Control-Allow-Credentials` | Tells the browser whether frontend code may receive a response to a credentialed request. | Yes |
| `Access-Control-Expose-Headers` | Identifies response headers that cross-origin frontend code may read. | Yes |
| `X-Frame-Options` | Restricts framing to reduce clickjacking. WP Cloud returns `SAMEORIGIN` for wp-admin; frontend policy can be set by the site. | Yes, for the frontend |
| `X-Content-Type-Options` | Prevents browsers from guessing a different MIME type. | Yes |
| `Referrer-Policy` | Controls how much referrer information accompanies another request. | Yes |
| `Content-Security-Policy` | Restricts the origins from which a page may load scripts and other resources. | Yes, with careful testing |
| `X-XSS-Protection` | Controls an older browser XSS filter. Modern sites should rely on a tested Content Security Policy instead. | Yes, but usually unnecessary |
| `Strict-Transport-Security` | Tells browsers to use HTTPS. WP Cloud manages the base HSTS header. | Only the supported subdomain and preload controls |
| `Cache-Control` | Controls browser and proxy caching. WP Cloud Page Cache and Edge Cache can supply this for cached responses. | Not through Redirection or `custom-redirects.php` |

See [MDN's HTTP header reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers)
for header syntax and browser behavior. Test security headers against every
required frontend, API, embedded resource, and third-party integration. A
strict CSP or CORS rule can break legitimate requests when its allowed origins
or directives are incomplete.

## Add headers with a plugin

The [Redirection plugin](https://wordpress.org/plugins/redirection/) can add
response headers without creating a redirect:

1. Open **Tools → Redirection → Site** in wp-admin.
2. Find **HTTP Headers** and choose **Add Header**.
3. Select where the header applies. **Site** is appropriate for most rules.
4. Select a predefined header or choose a custom header and enter its value.
5. Save the change and clear the applicable [Page
   Cache](/docs/performance/cache/page-cache/), [Edge
   Cache](/docs/performance/cache/edge-cache/), and browser cache before
   testing.

A name appearing in the plugin does not guarantee that WP Cloud permits it or
that it can override a platform header.

The plugin's **Location** value controls where the rule applies. **Site** is
usually appropriate for a site-wide response header. Its **Header** field
contains common presets and a custom option; **Value** contains either the
selected preset's choices or a value supplied by the site owner. Adding a
header here does not create a redirect.

## Add headers in custom-redirects.php

Advanced integrations can set PHP response headers in
[`custom-redirects.php`](/docs/wordpress/configuration/custom-redirects/):

```php
<?php

header( 'X-Content-Type-Options: nosniff' );
header( 'X-Frame-Options: SAMEORIGIN' );
header( 'Referrer-Policy: no-referrer-when-downgrade' );
```

Treat these as examples, not a complete security policy. Test the exact site
and response paths. WP Cloud handles `Cache-Control` for cached HTML, so do not
try to replace cache headers in `custom-redirects.php`.

The file belongs in the site's `htdocs` directory. A syntax error runs before
WordPress and can affect every matching request, so keep the file small and
test it on a staging site before copying it to production. See [Configure
redirects and headers with
custom-redirects.php](/docs/wordpress/configuration/custom-redirects/) for file
loading behavior and redirect examples.

## Check the response

Request the exact public URL and inspect its response headers:

```bash
curl -sS -D - -o /dev/null https://example.com/path/
```

Run the request while logged out so WordPress login cookies do not change Page
Cache or Edge Cache behavior. If the response can be cached, clear the relevant
site and browser cache after changing a header, then request the URL more than
once. Compare an origin response with an Edge Cache response when the header
must be present in both.

For CORS, test from the real requesting origin. A successful direct request or
`curl` response does not prove that a browser will expose it to frontend code.
Check the preflight response when the browser sends `OPTIONS`, and confirm that
the allowed origin, method, headers, and credential behavior agree with the
application. Avoid reflecting arbitrary origins when credentials are allowed.

For Content Security Policy, start with a report-only policy when practical,
review violations, and add only the origins and directives the application
requires. Test wp-admin, login, REST API, forms, embeds, analytics, payment
flows, and other third-party resources before enforcing it.

Retest after a plugin, theme, or third-party service changes the resources a
page loads. A header that was correct for an earlier version of the site can
later block a required script, font, API request, frame, or payment flow. Keep
the policy with the site code or configuration that depends on it so changes
can be reviewed together.

## HSTS controls

WP Cloud adds the HSTS header. Host partners can use the [HSTS subdomain
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-hsts-subdomain/{domain}/{enable})
to toggle `includeSubDomains`. The public API also provides an endpoint to
[disable the preload directive](https://wp.cloud/docs/api/#tag/sites/POST/ssl-hsts-preload/{domain}/false).

Do not enable `includeSubDomains` or browser preload until every present and
future subdomain supports HTTPS. Browsers can remember the policy long after a
site configuration changes.
