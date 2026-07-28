# TLS certificates

WP Cloud provisions, installs, and renews Transport Layer Security (TLS) certificates—often called SSL certificates—for a site's domains. Provisioning normally starts after a domain or alias is added and its DNS points to WP Cloud.

**Note:** SSL and TLS are both cryptographic protocols, and TLS is an evolution of SSL. TLS is sometimes referred to as “SSL,” as in “SSL certificate,” even though all versions of the SSL protocol are disabled on WP Cloud.

## How certificate provisioning works

WP Cloud provisions certificates through Let's Encrypt (LE) and Google Trust Services (GTS). Renewals are automatic and require no routine partner maintenance.

Certificate provisioning uses the ACME [HTTP-01 challenge](https://letsencrypt.org/docs/challenge-types/#http-01-challenge). Each hostname must resolve to WP Cloud and allow the certificate authority to retrieve its challenge over HTTP.

`example.com` and `www.example.com` are validated and managed independently. One hostname can have a certificate while another reports an error.

Failed attempts are requeued automatically. Consecutive failures increase the delay before the next attempt, and the `retry_date` returned by the API can move farther into the future. Correct the DNS or configuration error before requesting an immediate retry.

When LE itself is unavailable, check the [Let's Encrypt service status](https://letsencrypt.status.io/) before changing the site's DNS.

## Inspect certificate information

Use the [Fetch SSL Certificate Information endpoint](https://wp.cloud/docs/api/#tag/sites/POST/ssl-info/{domain}) separately for every hostname you need to inspect. The response can identify the certificate, certificate authority, expiration, validation state, HTTPS behavior, and any failed provisioning attempt.

The `ca_provider` field identifies `letsencrypt` or `google`. A browser's certificate details also show the issuer organization as Let's Encrypt or Google Trust Services.

On macOS or another system with OpenSSL, inspect the issuer from the command line:

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -issuer
```

Certificate chains and issuer common names can change. Use the issuer organization and the API's provider field rather than depending on a specific common name in an integration.

## TLS compatibility

During the TLS handshake, the server and client select the strongest mutually supported cipher from the server's preferred list. WP Cloud disables TLS 1.0 and TLS 1.1 but retains some TLS 1.2 ciphers for compatibility with older browsers and devices.

A scanner can flag one of those compatible ciphers even when modern clients negotiate a stronger choice. Evaluate a scanner finding in the context of protocol version, negotiation order, browser compatibility, and the actual exploit described by the report.

If a certificate is missing, delayed, or failing validation, use [Troubleshoot TLS certificate provisioning](/docs/troubleshooting/tls-certificate-provisioning/).
