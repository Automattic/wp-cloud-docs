# Image transformation

WP Cloud can resize, crop, and transform uploaded images when they are
requested. The transformed response is served and cached through WP Cloud's
[Edge Cache](/docs/performance/cache/edge-cache/), so the site does not need
to store a separate file for every variation.

The feature is enabled by default for public WP Cloud sites and does not
require Jetpack. It applies to images under `wp-content/uploads/`.

## Use transformation parameters

Append supported Site Accelerator parameters to an uploaded image URL. Common
examples include:

- `?x=200` resizes the image to an exact width of 200 pixels.
- `?fit=300,300` fits the image within a 300-by-300-pixel box while preserving
  its aspect ratio.
- `?resize=400,220` resizes and crops the image to exactly 400 by 220 pixels.

Multiple parameters can be combined on one URL. See the [Site Accelerator API
documentation](https://developer.wordpress.com/docs/site-performance/site-accelerator-cdn/#19-site-accelerator-api)
for the complete parameter reference.

Transformation parameters work only with image files in the site's uploads
directory. A site using the `wp_uploads` privacy model cannot use them because
the transformed asset would otherwise bypass the site's logged-in access
requirement.

## Reduce image download size

Serve images at dimensions appropriate for their display area and the end
user's device. Smaller image responses load faster and require less bandwidth.
For example, resizing a 28 MB original can produce a 200 KB response that
downloads in about 100 milliseconds instead of approximately 20 seconds,
depending on the connection.

Do not serve a 5000-by-3000-pixel image when the page displays it in a
500-by-300-pixel area. Add transformation parameters that produce a suitable
display size instead.

Native mobile applications should apply the same principle. When an API
response contains the original image URL, add the required transformation
parameters in the application so the end user downloads an appropriately
sized image rather than the full original.

## Jetpack Site Accelerator

Jetpack's Site Accelerator image and static-file features are not required on
WP Cloud. WP Cloud provides its own image transformation and [Edge
Cache](/docs/performance/cache/edge-cache/) from the site's domain. Enabling
Jetpack Site Accelerator instead loads those assets from `*.wp.com`, adding an
external request path.

This means a theme or plugin can request a suitable image size without first
writing that exact transformed copy into the site's uploads directory.
