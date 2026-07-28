# Manage and secure API keys

A WP Cloud API key authenticates requests for one WP Cloud host client account. Create separate keys for separate uses, restrict each key to known static addresses and only the endpoints it needs, and store it as a secret.

## Manage keys in the Partner Portal or through Support

Self-serve WP Cloud partners and managed partners with access to the [WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud) manage keys in the portal's API key management screen.

Some managed partners do not yet have a Partner Portal account. In that case, contact [WP Cloud Support](/docs/getting-started/get-support/) to:

- request a new key;
- add, replace, or remove an allowed IP address or CIDR; or
- change which API endpoints the key may access.

Partners must also contact WP Cloud Support when an allowed CIDR range needs to be larger than `/24`.

## Configure a key

Create separate keys for separate uses. Common examples include a production hosting panel, test automation, and an individual developer. Do not share one developer key across a team or reuse a production key for local development.

The Partner Portal currently provides these settings when you create a key:

- **Key name.** Use letters, numbers, and hyphens. The name must start with a letter.
- **Allowed endpoints.** Enter one endpoint per line. New keys include `default` endpoint access unless you remove it. Keep only the access required by the key's intended use.
- **Allowed IP ranges.** Enter one IPv4 address or CIDR range per line. The portal treats a single IP address as `/32` and accepts CIDR prefixes from `/24` through `/32`.

Good network sources include a static office gateway, an automation server, a bastion host, or a private VPN with stable egress addresses. Do not allow dynamic home addresses, consumer VPNs, or public Wi-Fi networks.

## Store and test the key

Store the key in a secrets manager or another server-side credential store. Keep it out of source control, browser code, command history, application logs, and customer-facing error messages.

WP Cloud API requests send the key in the `Auth` header:

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/get-sites/${WP_CLOUD_CLIENT}/+"
```

The [List Client Sites endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-sites/{client}/+) is a useful read-only check when it is included in the key's endpoint access. A successful request returns a `data` array. A `403` response means the key, source address, partner account, or endpoint access does not allow the request.

## Change, rekey, or revoke a key

Assume that changes to a key take effect immediately. Changing its allowed endpoints or IP ranges, rekeying it, or revoking it can immediately interrupt every server, portal, application, or developer that relies on the key and its current configuration.

For a planned rekey:

1. Create a new key.
2. Configure its allowed endpoints and IP ranges.
3. Replace the old key in every server, portal, application, and developer environment that uses it.
4. Verify that each integration works with the new key.
5. Remove the old key.

For an emergency involving a lost, exposed, or compromised key, revoke or rekey it immediately, then replace it everywhere it was used.
