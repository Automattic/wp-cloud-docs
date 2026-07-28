# Offload image sub-sizes

WordPress normally creates several intermediate image files for every upload.
WP Cloud's Intermediate Image Offloading feature, also called Photon Subsizes,
stores the attachment metadata without writing each generated size to the
site's filesystem. A requested size is produced from the original image and
served through the image service instead.

This can substantially reduce filesystem use on image-heavy sites while
retaining the responsive image sizes that WordPress themes and browsers expect.

## Enable or disable the feature

Set the `photon_subsizes` value with the [Site Meta
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}):

- `1` enables Intermediate Image Offloading.
- `0` disables it.

A plugin or theme can override the site-meta value with the
`photon_subsizes_enable` filter:

```php
add_filter( 'photon_subsizes_enable', '__return_true' );
```

The `PHOTON_SUBSIZES` constant has the highest priority. A truthy value enables
the feature and a falsy value disables it, regardless of site meta or filters:

```php
define( 'PHOTON_SUBSIZES', false );
```

Use one control at a time when possible so the active behavior is clear to the
host partner's support and developer teams.

## Remove existing intermediate files

Enabling the feature does not delete files that WordPress already generated.
Test the cleanup on a staging copy before applying it to a production media
library. Begin with the dry run:

```bash
wp atomic photon-subsizes-recover-space --dry-run
```

Review the reported files and space, then run the command without `--dry-run`
to remove eligible intermediate images:

```bash
wp atomic photon-subsizes-recover-space
```

Keep the original uploads. The service needs an original image to produce a
requested intermediate size.

## Limitations

- The feature cannot be used with the WP Cloud `wp_uploads` privacy model.
  The image service must be able to request the public original.
- While enabled, it is not compatible with `wp media regenerate` or the
  Regenerate Thumbnails plugin's regeneration workflow because the
  intermediate files are intentionally absent. Thumbnail cleanup can still
  work.
- After disabling the feature, `wp media regenerate` may be needed to recreate
  intermediate files on the site.

## How requests are served

The platform mu-plugin extends the selected WordPress image editor. Its
`make_subsize()` and `multi_resize()` behavior records subsize metadata without
creating the corresponding files.

At the web-server layer, a request is eligible when its filename follows the
normal `name-WIDTHxHEIGHT.ext` pattern and the matching original exists in the
same uploads path. For example, `pine-forest-300x200.png` can be generated from
`pine-forest.png`; a missing original cannot be reconstructed.

When a browser requests a filename such as:

```text
https://example.com/wp-content/uploads/2020/07/desert-flora-200x200.jpeg
```

and the original `desert-flora.jpeg` exists, the web server sends the missing
size to the image service. The internal image-service URL includes the
original file's last-modified time:

```text
https://i0.wp.com/example.com/1594944825/wp-content/uploads/2020/07/desert-flora.jpeg?w=200&h=200&ssl=1
```

WP Cloud removes the embedded time when retrieving the original. When the
original changes, its modification time changes too, producing a new cache key
for the transformed image.

The image service caches its result by URI for an unlimited period. Including
the modification time in the internal URI is therefore the cache-busting
mechanism: the service sees a new URI after the original changes, retrieves the
latest source image, and caches the newly resized response.

Jetpack Site Accelerator can also rewrite frontend image URLs directly to the
image service, but those URLs do not include WP Cloud's modification-time cache
busting. Jetpack Site Accelerator is not required for [WP Cloud image
transformation](/docs/performance/image-optimization/image-transformation/).
