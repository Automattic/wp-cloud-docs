# Troubleshoot PDF thumbnail generation

WP Cloud does not provide the ImageMagick and Ghostscript combination that
WordPress normally uses to create image thumbnails from uploaded PDF files.
Uploading a PDF can succeed without WordPress generating a preview image.

The symptom is a PDF attachment without the expected image subsize or preview.
The cause is the unavailable PDF-rendering extensions rather than a failed
media upload. Check that the original PDF exists and opens before changing the
upload workflow.

When a product requires PDF previews, generate them outside the WP Cloud site
and store the resulting image with the document. A media service such as
[Cloudinary](https://cloudinary.com/) can render the PDF and return a thumbnail,
or the host partner can build that step into its own upload workflow.

This limitation applies to rendering a PDF into an image. It does not prevent
the site from storing, linking to, or serving PDF files.

After moving thumbnail generation to the external service, retry an upload and
confirm that the returned preview loads. The issue is resolved when the
external workflow supplies the image while WordPress continues to serve the
original PDF.
