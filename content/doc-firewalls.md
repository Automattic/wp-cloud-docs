# Network and web application firewalls

WP Cloud protects sites with network firewalls and a web application firewall
(WAF). Network controls limit inbound services and outbound connections. The
WAF evaluates HTTP requests for patterns associated with attacks and other
unsafe traffic.

## Inbound network access

WP Cloud accepts public web traffic on TCP ports 80 and 443. SSH and SFTP use
TCP port 22 through their documented access endpoints. Direct external access
to a site's database is not available; use [phpMyAdmin](/docs/site-access/database-access/phpmyadmin/)
or an authorized SSH workflow instead.

## Outbound connections

Without custom egress rules, sites can make outbound TCP connections on:

- 80 and 443 for HTTP and HTTPS;
- 465 and 587 for SMTP;
- 110 and 995 for POP3; and
- 143 and 993 for IMAP.

Other outbound traffic is rejected and logged. A host partner can add allow or
deny rules when a site needs to connect on another port or block a specific
destination.

## Custom outbound firewall rules

Custom outbound firewall rules let a host partner allow or deny connections
for a destination IP address or CIDR range, protocol, and port. Use the
[Add Firewall Rule endpoint](https://wp.cloud/docs/api/#tag/security/POST/firewall-rules/{site}/add).
The API supports TCP and UDP rules, and each site can have up to 128 rules.

Use a narrow destination whenever possible. `0.0.0.0/0` allows the selected
port for every IPv4 destination and should be reserved for services whose
addresses cannot be constrained safely.

Rules belong to the Atomic Site ID. They remain with that site through
`clone_from` clones, API backup restores using `restore_from`, geographic
failover, and pool movement, and are removed when that site ID is deleted.

### Add a firewall rule

```bash
curl -H "Auth: ${WP_CLOUD_API_KEY}" -X POST \
  --data "direction=egress" \
  --data "action=allow" \
  --data "protocol=tcp" \
  --data "port=3306" \
  --data "destination=10.20.30.40/32" \
  "https://atomic-api.wordpress.com/api/v1.0/firewall-rules/${WP_CLOUD_SITE}/add"
```

### List existing firewall rules

List a site's rules with the [List Firewall Rules
endpoint](https://wp.cloud/docs/api/#tag/security/GET/firewall-rules/{site}/list):

```bash
curl -H "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/firewall-rules/${WP_CLOUD_SITE}/list"
```

### Remove a firewall rule by ID

Remove a rule by its returned `rule_id` with the [Remove Firewall Rule
endpoint](https://wp.cloud/docs/api/#tag/security/POST/firewall-rules/{site}/remove):

```bash
curl -H "Auth: ${WP_CLOUD_API_KEY}" -X POST \
  --data "rule_id=2368992788" \
  "https://atomic-api.wordpress.com/api/v1.0/firewall-rules/${WP_CLOUD_SITE}/remove"
```

## Web application firewall

WP Cloud's WAF uses ModSecurity with an Automattic-managed rule set that
includes industry and Jetpack WAF protections. A rejected request can receive
HTTP 406 with the message `Not Acceptable. Our sentries tell us that you should
not be doing this.`

When legitimate functionality consistently receives HTTP 406, record the site
ID, domain, affected URL, request method, timestamp and timezone, source IP,
user agent, and a reproducible example. Also record the exact user action, the
affected plugin, theme, or application and its version, and a safe description
of the submitted payload type. Do not include credentials, exploit payloads,
or sensitive customer data. The host partner can use that evidence to
distinguish a WAF false positive from an application error and identify which
layer returned the response.
