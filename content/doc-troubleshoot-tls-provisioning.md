# Troubleshoot TLS certificate provisioning

WP Cloud normally provisions and renews [TLS certificates](/docs/sites/domains/tls-certificates/) automatically after a domain points to the platform. If a certificate is missing or delayed, inspect the exact hostname, correct its DNS or proxy configuration, and then retry provisioning.

## Inspect the hostname

Use the [Fetch SSL Certificate Information endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-info/{domain}) separately for every affected hostname:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssl-info/${WP_CLOUD_DOMAIN}"
```

The response can include:

| Field | Meaning |
| --- | --- |
| `acme_certificate_id` or `ssl_certificate_id` | A certificate identifier when issuance succeeded. The field used can vary. |
| `validation_expiration` | The platform's validation window, not the certificate's expiration date. |
| `options` | Platform behaviors such as HTTPS redirects and HTTP Strict Transport Security (HSTS). |
| `certificate_expiration_date` | When the issued certificate expires. |
| `ca_provider` | The certificate authority, such as `letsencrypt` or `google`. |
| `authz_uri` | An LE authorization URL that can provide details about a validation attempt. |
| `broken_record` | The reason provisioning failed and its retry state. |

The `broken_record` object is the main starting point for a failed attempt:

- `reason` gives the high-level cause, such as `not hosted here` or `authorization failure`.
- `last_error` records the last failed attempt.
- `retry_date` records the next scheduled attempt.
- `failcount` records the number of failures for the hostname.

If `ssl-info` returns `Not Found` or `Site not found`, WP Cloud does not recognize that hostname as a domain or alias on the site. [Add the missing hostname](/docs/sites/domains/manage-domains-aliases/), such as `www` when only the apex domain exists, then inspect it again.

## Check DNS records

Certificate provisioning uses the ACME [HTTP-01 challenge](https://letsencrypt.org/docs/challenge-types/#http-01-challenge). The certificate authority must be able to reach the exact hostname on WP Cloud over HTTP.

### A records

Check the apex domain and `www` separately when both are attached to the site:

```bash
dig A example.com +short
dig A www.example.com +short
```

An A record that points elsewhere can appear in `broken_record.reason` as `not hosted here`. Remove conflicting records, wait for the correct records to propagate, and check the hostname again.

### AAAA records

If a hostname publishes an AAAA record that does not route IPv6 traffic to WP Cloud, the certificate authority can attempt validation at that address and fail:

```bash
dig AAAA example.com +short
```

Remove or correct a conflicting AAAA record, then wait for DNS propagation.

### CAA records

Certification Authority Authorization (CAA) records restrict which certificate authorities can issue for a domain:

```bash
dig +nocmd example.com CAA +noall +answer
```

CAA policy must allow the provider WP Cloud is using. Allow `letsencrypt.org` for LE and `pki.goog` for GTS, or remove a conflicting restriction when that matches the domain owner's policy.

### DNSSEC

Broken Domain Name System Security Extensions (DNSSEC) configuration can prevent validation. Correct the delegation and DNSSEC records with the registrar or DNS provider, or disable DNSSEC until it is configured correctly.

For GTS-specific failures, [Google Public CA DNS debugging](https://developers.google.com/public-key-infrastructure/dns-debugging) describes its CAA and global DNS consistency checks.

## Inspect a Let's Encrypt authorization

For an LE validation failure, `authz_uri` can identify the address and challenge URL used by the certificate authority. It may be absent, and it does not apply to a GTS certificate.

Retrieve the returned URL with a browser or `curl`:

```bash
curl --fail-with-body --silent --show-error "${AUTHZ_URI}"
```

In the authorization JSON, check:

- `status`; `invalid` means validation failed;
- `challenges[].error.detail` for the reported cause; and
- `challenges[].validationRecord[].addressesResolved` and `addressUsed` to see which address received the HTTP-01 request.

For example, if `addressesResolved` contains the expected WP Cloud IPv4 addresses and an unrelated IPv6 address, and `addressUsed` shows that IPv6 address, correct or remove the conflicting AAAA record before retrying.

[Let's Debug](https://letsdebug.net/) can perform another public LE validation check. The [Qualys SSL Server Test](https://www.ssllabs.com/ssltest/) reports the certificate and TLS configuration visible to clients.

## Check Cloudflare and other proxies

A proxy can prevent the certificate authority from reaching WP Cloud's HTTP-01 challenge response. Avoid proxying WP Cloud domains when possible. If a site uses Cloudflare, follow the [recommended Cloudflare configuration](/docs/sites/domains/cloudflare/) and check its DNS and proxy state.

## Retry certificate provisioning

After correcting every reported DNS or configuration problem, use the [Retry SSL Provisioning endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-retry/{domain}) for the affected hostname:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssl-retry/${WP_CLOUD_DOMAIN}"
```

An accepted retry returns:

```json
{
  "message": "OK",
  "data": {
    "queued": true
  }
}
```

Retry `example.com` and `www.example.com` separately when both are affected. Do not repeatedly queue retries while DNS is incorrect or still propagating; additional failures can increase retry backoff and can trigger API rate limits.
