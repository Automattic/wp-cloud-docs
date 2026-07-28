# Manage custom TLS certificates

WP Cloud normally provisions and renews [managed TLS certificates](/docs/sites/domains/tls-certificates/) for verified site domains. A host partner can use the Custom SSL Certificates API when a site must serve a certificate supplied by the partner or its customer.

Partners can include custom certificate support in their hosting products or offer it as a paid upgrade. If WP Cloud cannot use the custom certificate, the platform automatically falls back to a managed Let's Encrypt certificate.

Custom certificates require extra care because the workflow handles a private key and has separate validation, staging, activation, update, deactivation, and deletion states. Test the workflow on a controlled site before offering it to customers.

## Prepare the certificate

Before sending certificate material to WP Cloud:

- [verify the site's domains](/docs/sites/domains/domain-verification-records/);
- confirm that the certificate covers every hostname where it will be used;
- provide the certificate and its chain in PEM format;
- confirm that the private key matches the certificate; and
- choose a non-production site for the first integration test.

Treat the private key as a secret. Do not place it in source control, command history, application logs, support requests, or test fixtures. Limit access to the system that submits it, and remove temporary copies after the request completes.

## Validate the certificate material

Send the certificate, private key, and optional domain list to the [Validate Custom Certificate endpoint](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/POST/custom-certificates/{site}/validate). Review every validation error and warning before continuing.

A successful validation confirms that the submitted material passed the endpoint's checks. It does not store or activate the certificate.

## Stage the certificate

Send the validated material to the [Stage Custom Certificate endpoint](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/POST/custom-certificates/{site}/stage). The response returns `ssl_custom_certificate_id`, the associated domains, and an inactive state. Retain the certificate ID; later lifecycle operations use it.

Staging prepares the certificate but does not change the certificate currently served by the site.

## Inspect and activate the certificate

Use the [Get Custom Certificate Details endpoint](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/GET/custom-certificates/{site}/{id}) or [List Custom Certificates endpoint](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/GET/custom-certificates/{site}/list) to check the certificate ID, domains, active state, issuer, subject, and validity dates.

Activate the staged certificate with the [Activate Custom Certificate endpoint](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/POST/custom-certificates/{site}/{custom_certificate_id}/activate). After activation succeeds, check each configured hostname with an independent TLS client or certificate checker. Confirm that it serves the intended certificate and complete chain before directing production traffic to it.

## Renew, deactivate, or delete a certificate

Use separate lifecycle operations rather than assuming that one request performs every change:

- [Update Custom Certificate](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/POST/custom-certificates/{site}/{id}/update) replaces certificate material for renewal or rekeying. Inspect the resulting record and verify the served certificate again.
- [Deactivate Custom Certificate](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/POST/custom-certificates/{site}/{id}/deactivate) stops the selected certificate from being active. Confirm the site's TLS behavior before relying on another certificate.
- [Delete Custom Certificate](https://wp.cloud/docs/api/#tag/custom-ssl-certificates/POST/custom-certificates/{site}/{id}/delete) removes an inactive certificate record. An active custom certificate must be deactivated before it can be deleted.

Keep the certificate ID, covered domains, validity dates, and partner-owned renewal date in the system that manages the certificate. Do not rely on validation or staging alone as proof that the certificate is active or being served.
