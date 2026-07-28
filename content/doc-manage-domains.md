# Manage site domains and aliases

A WP Cloud site has one primary domain and can have secondary domains. Requests
to a secondary domain normally redirect to the primary domain. Host partners
can use the WP Cloud API to check whether a domain is available, manage
secondary domains, retrieve suggested DNS addresses, and change the primary
domain.

The examples use these placeholders:

- `<api-key>` is a WP Cloud API key with access to the site.
- `<client>` is the host client's WP Cloud identifier.
- `<site-id>` is the site's Atomic Site ID.
- `<current-domain>` is the site's current primary domain.
- `<new-domain>` is the domain being added or promoted.

Keep the Atomic Site ID as the site's permanent identifier in partner systems.
The site ID does not change when its primary domain changes.

## Check whether WP Cloud can host the domain

Before creating a site or adding a domain, use the [Validate Domain Eligibility
endpoint](https://wp.cloud/docs/api/#tag/sites/GET/check-can-host-domain/{client}/{domain}):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: <api-key>" \
  "https://atomic-api.wordpress.com/api/v1.0/check-can-host-domain/<client>/<new-domain>"
```

An available domain returns `allowed: true`:

```json
{
  "message": "OK",
  "data": {
    "allowed": true
  }
}
```

The check returns false for a domain that is already hosted on WordPress.com or
WP Cloud, even when the domain is valid. Check eligibility before site creation
as well as before adding a secondary domain to avoid a domain collision.

## Add, list, or remove a secondary domain

Use the [Manage Site Aliases
endpoint](https://wp.cloud/docs/api/#tag/sites/GET/site-alias/{service}/{identifier}/{action}/{domain})
to add a secondary domain. This example finds the site by its Atomic Site ID:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: <api-key>" \
  "https://atomic-api.wordpress.com/api/v1.0/site-alias/<client>/<site-id>/add/<new-domain>"
```

A successful response includes the site's secondary domains:

```json
{
  "message": "OK",
  "data": {
    "domains": ["www.example.com"]
  }
}
```

List the current secondary domains with the `list` action:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: <api-key>" \
  "https://atomic-api.wordpress.com/api/v1.0/site-alias/<client>/<site-id>/list"
```

Remove a secondary domain with the `remove` action:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: <api-key>" \
  "https://atomic-api.wordpress.com/api/v1.0/site-alias/<client>/<site-id>/remove/<new-domain>"
```

The API does not allow the primary domain to be removed as an alias. Change the
primary domain first when the old primary domain should be removed from the
site.

WP Cloud secondary domains redirect to the primary domain. They do not make
WordPress generate page and post links for each secondary hostname. A partner
that needs different domain behavior must provide that behavior separately and
account for WordPress's absolute URLs.

## Control alias canonicalization

WP Cloud normally canonicalizes secondary domains by redirecting them to the
primary domain. The `canonicalize_aliases` site-meta value controls this
behavior.

Set `canonicalize_aliases` to `false` only when the WordPress installation must
serve its secondary domains directly. The main use case is a domain-based
[WordPress multisite network](/docs/wordpress/multisite/), where
different domains are mapped to different subsites.

Disabling canonicalization removes WP Cloud's normal alias-to-primary
redirects. WordPress, a plugin, or partner-maintained code must then handle any
required `www`, non-`www`, or domain-to-domain redirects. The setting does not
define individual redirect rules; it determines whether WP Cloud redirects all
secondary domains to the primary domain before WordPress handles the request.
Setting it back to `true` on a site that serves several domains redirects those
aliases to the primary domain with HTTP 301 responses.

Change the value with the [Site Meta
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-meta/{site}/{key}/{action}).
Do not disable it for an ordinary site when every secondary domain should
continue redirecting to the primary domain.

## Retrieve suggested DNS addresses

Use the [Get Client IP Addresses
endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-ips/{client}/{domain}) to
retrieve the WP Cloud range and suggested A record addresses for a domain:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: <api-key>" \
  "https://atomic-api.wordpress.com/api/v1.0/get-ips/<client>/<new-domain>"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "ips": ["192.0.78.128/25"],
    "suggested": ["192.0.78.150", "192.0.78.200"]
  }
}
```

Use the `suggested` addresses for the domain's A records unless the host
client's WP Cloud configuration specifies otherwise. [Domain verification
records](/docs/sites/domains/domain-verification-records/) explains the TXT
record WP Cloud may require when another host client already uses the domain.

## Change the primary domain

Add the new domain as a secondary domain and configure its DNS before promoting
it. Confirm that WP Cloud can serve the domain and provision its [TLS
certificate](/docs/sites/domains/tls-certificates/).

Send a `POST` request to the [Update Site Domain
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/update-site-domain/{service}/{identifier}/{domain}/{keep}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: <api-key>" \
  "https://atomic-api.wordpress.com/api/v1.0/update-site-domain/<client>/<site-id>/<new-domain>/keep"
```

The response identifies the queued job, the site, and both domains:

```json
{
  "message": "OK",
  "data": {
    "job_id": 2345,
    "atomic_site_id": 5678,
    "domain_name": "www.example.com",
    "old_domain_name": "example.com"
  }
}
```

The `keep` value retains the old primary domain as a secondary domain. Pass
`false` instead when the old domain should be removed. Check the returned job
with the [Get Job Statuses
endpoint](https://wp.cloud/docs/api/#tag/jobs/GET/job-status/{id}) before
updating systems that depend on the new primary domain.

Changing the WP Cloud primary domain does not replace every domain stored by
WordPress, plugins, themes, or partner systems. Update any affected URLs as
part of the host partner's domain-change process.
