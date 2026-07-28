# Server specifications and settings

WP Cloud runs WordPress on managed NGINX origin servers with NVMe storage,
redundant networking, regional replicas, and platform-controlled PHP settings.
Hardware and software are upgraded over time. This reference lists current
values and describes the platform's configuration boundaries.

## Infrastructure specifications

| Component | Platform specification |
| --- | --- |
| Web server | NGINX |
| Processor | AMD EPYC processors; exact hardware may vary by pool. |
| PHP concurrency | Configurable default PHP workers (threads), with optional full bursting that can use more than 110 workers based on available capacity. |
| Network | Redundant 25 Gbit connectivity per server. |
| Storage | NVMe solid-state drives. |
| Scaling and redundancy | Bare-metal primary and secondary servers in different regions, with vertical scaling and [automated failover](/docs/infrastructure/automated-failover/). |
| Origin network | Four [origin locations](/docs/infrastructure/origin-edge-servers/). |
| Edge network | More than 27 [edge locations](/docs/infrastructure/origin-edge-servers/) and growing, including origin locations. |
| PHP memory | 512 MB per request by default; supported site-meta values extend to 2048 MB. |
| Caching | [Page Cache](/docs/performance/cache/page-cache/), [Object Cache](/docs/performance/cache/object-cache/), [Edge Cache](/docs/performance/cache/edge-cache/), and PHP OPcache. |

WP Cloud can generate and serve intermediate image sizes through its edge image
service without counting those generated sizes against the site's filesystem
quota.

Use [site meta](/docs/sites/site-meta/) to configure the supported per-site PHP
connection count, bursting setting, PHP memory limit, and filesystem quota.
For example, a partner can raise one site's per-request PHP memory limit
without changing the platform-managed `php.ini`.

## PHP settings

The platform controls the following PHP and web-server settings. A site cannot
override them through `.htaccess`, NGINX configuration, or a custom `php.ini`.

| Setting or capability | Value |
| --- | --- |
| `memory_limit` | 512 MB by default; configurable to 1024 MB, 1536 MB, or 2048 MB through site meta |
| `post_max_size` | 2 GB |
| `max_execution_time` | 850 seconds |
| `max_input_vars` | 6144 |
| cURL | 8.10.1 or later |
| Database server | MariaDB |
| Maximum upload size | 2 GB |
| SUHOSIN | Not installed |
| ionCube Loader | Not installed |
| ImageMagick PHP extension | Not installed; the `gmagick` module is available |
| Ghostscript | Not installed |
| Sodium | Available |
| Default time zone | UTC |
| PDO MySQL | Available |
| GD | Available |
| `fsockopen` and cURL | Available |
| `SoapClient` | Available |
| `DOMDocument` | Available |
| Brotli and gzip | Available; Brotli is preferred and gzip is the fallback |
| Multibyte String | Available |
| Remote HTTP POST and GET | Available |

When an exact runtime value matters, create a temporary `phpinfo.php` file in
the site's document root:

```php
<?php
phpinfo();
?>
```

Load the file over HTTPS, record the needed value, and remove the file
immediately. `phpinfo()` exposes detailed environment information and should
not remain publicly accessible.

## PHP modules

WP Cloud includes these active modules:

| | | | |
| --- | --- | --- | --- |
| `apcu` | `bcmath` | `calendar` | `cgi-fcgi` |
| `Core` | `ctype` | `curl` | `date` |
| `dom` | `exif` | `fileinfo` | `filter` |
| `gd` | `gmagick` | `gmp` | `hash` |
| `iconv` | `imap` | `intl` | `json` |
| `libxml` | `mbstring` | `mcrypt` | `memcache` |
| `mysqli` | `mysqlnd` | `openssl` | `pcntl` |
| `pcre` | `PDO` | `pdo_mysql` | `pdo_sqlite` |
| `Phar` | `posix` | `Reflection` | `session` |
| `shmop` | `SimpleXML` | `soap` | `sockets` |
| `sodium` | `SPL` | `sqlite3` | `standard` |
| `sysvsem` | `sysvshm` | `timezonedb` | `tokenizer` |
| `xml` | `xmlreader` | `xmlwriter` | `xsl` |
| `Zend OPcache` | `zip` | | |

## Server configuration boundaries

### `.htaccess`

NGINX does not read Apache `.htaccess` files. A plugin or configuration that
depends on `.htaccess` rules must use a WordPress- or application-level method
that works with NGINX.

### NGINX and `php.ini`

Sites cannot modify the managed NGINX configuration or PHP settings through a
site-level `php.ini` file. Use a supported WP Cloud setting when one exists.

### PHP memory

The per-request PHP memory limit is configured through the
`php_memory_limit` site-meta key. Supported values are `512`, `1024`, `1536`,
and `2048` MB; the default is `512` MB.

Increasing the limit can allow a memory-intensive request to finish, but
repeated memory exhaustion usually warrants checking the site's plugins,
themes, custom code, and database work rather than treating a larger limit as
the only fix.

### Compression

WP Cloud enables Brotli compression at the server level. When the client does
not support or accept Brotli, the server can use gzip instead.

### Binary PHP loaders and image extensions

WP Cloud does not install ionCube Loader or ZendGuard Loader. The Imagick PHP
extension is not available; use the installed image capabilities, including GD
and `gmagick`, where compatible with the application.
