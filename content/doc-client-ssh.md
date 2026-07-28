# Client SSH

Client SSH gives a WP Cloud host partner's developers, engineers, support teams, panels, and automation full SSH and SFTP access to a selected site. It is intended for partner-operated work such as site management, provisioning commands, support investigations, and custom restore tools.

Connect with the site's WP Cloud ID as the username:

```text
<site-id>@client-ssh.atomicsites.net
```

A Client SSH credential can be authorized for sites across the partner account, so treat it as a high-privilege credential. Client SSH accepts public keys only. Password authentication is disabled.

## Manage public keys

Manage Client SSH keys with the [`client-authorized-keys` operations](https://wp.cloud/docs/api/#tag/ssh/POST/client-authorized-keys/{client}/{action}). Each record is equivalent to a line in an OpenSSH `authorized_keys` file.

You can store either an aliasable public key or a complete `authorized_keys` line.

### Aliasable public keys

An aliasable key uses this form:

```text
pub://<client>/<category>?<name>
```

Examples include:

```text
pub://example-host/employees?tina
pub://example-host/automation?provisioning
pub://example-host/support?primary
```

Create or update an alias with the [`alias-pkey` operation](https://wp.cloud/docs/api/#tag/ssh/POST/alias-pkey/set/{client}/{category}/{name}). Use broad categories such as `employees`, `support`, or `automation`, then give each key a distinct name.

Aliases simplify rotation. Updating the key stored behind an alias updates every place that references it. Removing an alias prevents those references from authenticating, but it does not remove the references themselves. Track where each alias is used so you can also remove obsolete authorized-key records.

### Raw public keys

You can supply a complete public-key line instead of an alias. A raw key works normally, but WP Cloud cannot rotate every copy for you. If the same key is added to several records, your integration must find and update each one.

Use RSA keys between 2,048 and 16,384 bits, ECDSA P-256 keys, or Ed25519 keys. Keep private keys out of API requests, source control, logs, and support requests.

## Restrict connections by network

The Client SSH firewall is optional, but WP Cloud strongly recommends limiting Client SSH to known addresses because of the access it provides.

Good sources include:

- static proxy or automation servers;
- bastion or jump hosts;
- an office with a static public address; and
- a private VPN with stable egress addresses.

Avoid relying on home connections with changing addresses, consumer VPNs, public Wi-Fi, or other networks that require frequent allowlist changes.

WP Cloud supports three layers of source-address restrictions:

- `client_ssh_firewall` defines the outer address boundary for the Client SSH service. A key cannot allow an address outside this boundary.
- `client_ssh_default_from` supplies a default restriction for keys that do not have their own `from=` option.
- An OpenSSH `from=` option restricts one authorized key and overrides `client_ssh_default_from` for that key.

The most restrictive applicable settings determine whether a connection is accepted. A per-key `from=` value can narrow the client firewall, but it cannot widen it.

Manage `client_ssh_firewall` and `client_ssh_default_from` with the [`client-meta` operations](https://wp.cloud/docs/api/#tag/client-meta/POST/client-meta/{client}/{key}/add). Use `add` when the metadata key does not exist, `update` to replace an existing value, `get` to inspect it, and `remove` to delete it. The [Update Client Metadata endpoint](https://wp.cloud/docs/api/#tag/client-meta/POST/client-meta/{client}/{key}/update) accepts a comma-separated address or CIDR value.

An update replaces the entire comma-separated allowlist. Read the current value, prepare the complete desired list, and send every address or range that should remain allowed.

For example, this value allows one automation host and one office range:

```text
192.0.2.10/32,198.51.100.0/24
```

An individual authorized key can include its own restriction:

```text
from="192.0.2.10/32" ssh-ed25519 AAAA... partner-automation
```

Changing a per-key restriction requires updating that authorized-key entry. Client metadata is usually easier to maintain when several keys share the same network rules.

## Common network configurations

The following examples use the documentation-only ranges `192.0.2.0/24`, `198.51.100.0/24`, and `203.0.113.0/24`.

### Allow one address for every key

Set either `client_ssh_firewall` or `client_ssh_default_from` to a single address:

```text
192.0.2.10/32
```

Using `client_ssh_firewall` creates an outer boundary that no key can override. Using only `client_ssh_default_from` lets an individual key replace the default with its own `from=` restriction.

### Allow several addresses or ranges

Separate addresses and CIDR ranges with commas:

```text
192.0.2.10/32,198.51.100.0/24,203.0.113.8/32
```

### Limit one key to a smaller range

Set `client_ssh_firewall` to the complete approved network range, then add a narrower `from=` value to the key:

```text
client_ssh_firewall: 198.51.100.0/24
key from=:             198.51.100.30/32
```

The key works from `198.51.100.30` only. It cannot be used from another address in the larger firewall range.

### Add an exception to the default

Set an outer firewall that contains both the normal range and the exception. Set the default to the normal range, then give the exception key its own address:

```text
client_ssh_firewall:     198.51.100.0/24
client_ssh_default_from: 198.51.100.30/32,198.51.100.31/32
exception key from=:     198.51.100.212/32
```

Keys without a `from=` option use the two default addresses. The exception key uses `.212`. All three addresses remain inside the client firewall.

An exception can also be a separate address or range:

```text
client_ssh_firewall:     198.51.100.0/24,203.0.113.8/32
client_ssh_default_from: 198.51.100.0/24
exception key from=:     203.0.113.8/32
```

### Restrict every key individually

You can omit `client_ssh_default_from` and add `from=` to every key. This is precise, but every address change requires updating the affected key records. A client firewall still provides a useful outer boundary.

If no client firewall, default, or per-key restriction is configured, a valid authorized key is not limited by these source-address controls. Do not use that arrangement for production Client SSH access.

## Connect to a site

Use the WP Cloud site ID, not the site's domain, as the Client SSH username:

```bash
ssh -i ~/.ssh/wpcloud-client <site-id>@client-ssh.atomicsites.net
```

Use the same identity and hostname for SFTP:

```bash
sftp -i ~/.ssh/wpcloud-client <site-id>@client-ssh.atomicsites.net
```

Client SSH provides full shell and SFTP access even if site users are configured for SFTP only. Client SSH and site-user credentials are separate; a key authorized for Client SSH does not automatically work at `ssh.atomicsites.net`.

## Check a new configuration

After adding or changing a key:

1. List the client's authorized-key records and confirm that the intended alias or public key is present.
2. Connect from an allowed address and confirm that the session reaches the expected site ID.
3. If a firewall or `from=` rule is configured, try the credential from an address outside that rule and confirm that it is rejected.
4. Rotate or remove a test key and confirm that the previous key no longer authenticates.

The expected result is that the key works only from the addresses allowed by every applicable rule. A rejection from an address inside the client firewall can indicate that `client_ssh_default_from` or the key's own `from=` value is narrower. A key that works outside the intended boundary indicates that one of those restrictions is missing or broader than expected.
