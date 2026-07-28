# Domain verification records

WP Cloud uses Domain Name System (DNS) TXT verification records to prevent a
domain claimed by one host client from being assigned to a site owned by
another. A partner can retrieve a domain's unique verification value through
the WP Cloud API and publish it wherever the domain's DNS is managed.

## Check whether verification is needed

Use the [Validate Domain Eligibility endpoint](https://wp.cloud/docs/api/#tag/sites/GET/check-can-host-domain/{client}/{domain}) before creating a site, adding an alias, or changing a site's primary domain.

If another WP Cloud host client already uses the domain, the eligibility check
can return an error similar to this:

```text
Domain already used on a different site [example.com]. TXT record verification is required to bypass this check.
```

Attempting to assign the domain without the preflight check can instead return:

```text
Setting domain-as-primary failed: Domain name already used [example.com]. TXT record verification is required to bypass this check.
```

These messages do not identify the other WP Cloud host client. WP Cloud does
not disclose that information.

## Retrieve and publish the TXT value

Request the value from the [Get Domain Verification Code endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-domain-verification-code/{client}/{domain}). Replace the variables with the host client identifier and exact hostname being verified:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-domain-verification-code/${WP_CLOUD_CLIENT}/${WP_CLOUD_DOMAIN}"
```

The response contains a unique value for that host client and hostname:

```json
{
  "message": "OK",
  "data": "atomic-domain-<verification-code>"
}
```

Publish the returned value as a TXT record for the requested hostname. If the
partner's product adds both the apex domain and its `www` hostname, retrieve
and publish a separate value for each:

- `example.com`
- `www.example.com`

Each value is unique. Publishing both records in advance can make later domain
changes easier, whether the partner manages DNS for the customer or displays
the values for the customer to add at another DNS provider.

Wait for the TXT records to propagate, then repeat the eligibility check or
domain operation that originally reported the collision.

## Resolve a domain held by another site

If the customer recognizes the domain as attached to an older site, first
detach the domain from that site. Do not cancel the customer's domain
registration or DNS service.

When the domain cannot be detached from its previous site, publish the
verification record for the apex hostname and, when the partner's workflow
uses it, the `www` hostname. A `www` verification record is less commonly
needed when `www` is a CNAME, but it can still be required when another site
previously claimed `www` as a separate alias.
