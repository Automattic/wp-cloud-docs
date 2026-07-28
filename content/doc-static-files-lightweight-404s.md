# Configure lightweight 404s for static files

WP Cloud can return a lightweight web-server response when a requested static
file does not exist. This avoids loading WordPress and PHP for missing images,
fonts, JavaScript, CSS, and other assets that a visitor does not see.

Without this feature, each missing static-file request can load WordPress and
render a normal 404 page. A page with several broken asset URLs can therefore
consume PHP workers and CPU for responses that do not help the visitor.

## Choose the 404 behavior

Set the `static_file_404` value with the [Site Meta
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}):

- `lightweight` returns a small 404 response from the web server without
  loading WordPress.
- `wordpress` sends the request through WordPress. This is the default.

Host partners should default sites to `lightweight` whenever their product
does not require WordPress to handle missing static files. This reduces
unnecessary PHP and CPU use and improves performance when pages contain broken
asset URLs.

Lightweight responses are useful when a high-traffic site has many missing
asset requests. They can reduce unnecessary resource use and lower the chance
that a burst of broken requests contributes to [rate
limiting](/docs/security/traffic-protection/rate-limiting/) or [HTTP 429 and 599
errors](/docs/troubleshooting/429-599-errors/). The site owner should still
repair the broken URLs.

The feature applies to common static extensions, including:

```text
.css, .gif, .eot, .jpg, .jpeg, .js, .mp3, .mp4, .otf, .png, .svg,
.swf, .ttf, .webm, .webp, .woff, .woff2
```
