# Transactional email

WP Cloud provides a transactional email service for WordPress system messages,
password resets, order notices, and contact-form messages. Mail sent with
WordPress's normal PHP mail path is relayed through WP Cloud mail servers and
signed for the site's primary domain.

Host partners can use this service as the default for their customers or
allow end users to connect an external SMTP provider. It is not intended for
email marketing campaigns or other bulk mail.

## Default delivery and limits

The platform-provided mailer accepts up to 200 messages per site per hour.
Messages over the limit are rejected and must be sent again later. The limit
does not apply when a site sends through its own SMTP provider.

Some managed host clients use a custom relay configuration in which the local
mail server sends to a third-party provider. That configuration requires
coordination when the provider does not perform DKIM signing itself and should
not be assumed for every WP Cloud client.

## Authenticate mail with DNS

Host partners should provide these records to customers or add them when the
partner manages DNS for the site's primary domain.

### SPF

When the domain has no SPF record, add:

| Type | Host | Value |
| --- | --- | --- |
| TXT | `@` | `v=spf1 include:_spf.wpcloud.com ~all` |

For a site sending from a subdomain such as `news.example.com`, use `news` as
the host rather than `@`.

A domain must have only one SPF record. If an SPF record already exists, add
`include:_spf.wpcloud.com` to that record before its final `~all`, `-all`, or
other all-mechanism instead of creating a second TXT record.

### DKIM

Add both CNAME records:

| Type | Host | Value |
| --- | --- | --- |
| CNAME | `wpcloud1._domainkey` | `wpcloud1._domainkey.wpcloud.com` |
| CNAME | `wpcloud2._domainkey` | `wpcloud2._domainkey.wpcloud.com` |

WP Cloud signs mail for the site's primary domain. A domain-based multisite
that sends from an alias or subsite domain may need to force its From address
to the primary domain or use another SMTP service.

### DMARC

DMARC policy depends on the domain owner's mail systems and enforcement plan.
The following record begins with monitoring only:

| Type | Host | Value |
| --- | --- | --- |
| TXT | `_dmarc` | `v=DMARC1; p=none;` |

Do not move directly to `p=quarantine` or `p=reject` without confirming every
authorized sender and reviewing DMARC reports. Some mailbox providers require
DMARC for high-volume senders. [DMARC.org](https://dmarc.org/overview/) and
Cloudflare's [SPF, DKIM, and DMARC
overview](https://www.cloudflare.com/learning/email-security/dmarc-dkim-spf/)
provide background on the records.

## Abuse detection and email blocks

WP Cloud can temporarily or permanently block a site that abuses the shared
transactional email service. Host partners can query the [Email Block
endpoint](https://wp.cloud/docs/api/#tag/email/GET/email-block/{client}/{action}/{type})
for blocked domains.

The `sasl_block` webhook is sent when a domain's block record changes,
including an unblock or an extension of an existing block. Review the
`expires` value before notifying a customer because a later event can replace
an earlier expiration.

```json
{
  "event": "sasl_block",
  "timestamp": 1721230550,
  "atomic_site_id": 123456789,
  "data": {
    "domain": "example.com",
    "reason": "Optional reason for block",
    "expires": "2026-02-04 15:42:14"
  }
}
```

An `expires` value in the future means the domain is currently blocked. Use
the event to start the host partner's spam and abuse workflow and to help the
customer correct missing SPF, DKIM, or DMARC records. See
[Webhooks](/docs/api-automation/webhooks/) for signing and event
handling.

Before requesting review of a WP Cloud SASL block, collect the sender address
and domain, the sending path, the abused form or compromised account, the
spam that was produced, and the block reason and expiration. Record the
plugin, theme, and WordPress updates applied; credential and two-factor
authentication changes where applicable; malware or vulnerability findings;
and evidence that the unwanted sending stopped.

A WP Cloud SASL block is different from a rejection by a remote SMTP provider
or mailbox service and from a sender-reputation problem. Check which service
returned the error before changing the site's WP Cloud mail configuration.

## Use an email service provider

An end user can install an SMTP plugin and send through a provider of their
choice. This bypasses WP Cloud's mail servers and uses the provider's limits,
authentication, reporting, and delivery controls.

An external provider is a better fit when a site:

- needs more than four sender addresses;
- needs more than 200 transactional messages per hour;
- sends automated transactional sequences through tools such as AutomateWoo;
- sends bulk or marketing email rather than standard transactional messages;
- needs more than 500 messages per day, delivery monitoring, analytics, or
  detailed bounce handling;
- has a custom configuration that does not work reliably with PHP `mail()`; or
- continues to encounter failed or filtered messages.

[MailPoet](https://www.mailpoet.com/) is the first option to consider for
WordPress newsletters and WooCommerce email. Other provider options
include SMTP.com, Brevo, Mailgun, SendGrid, SendLayer, Google Workspace, and
Zoho.

Examples of WordPress SMTP plugins include [Post
SMTP](https://wordpress.org/plugins/post-smtp/), [WP Mail
SMTP](https://wordpress.org/plugins/wp-mail-smtp/), and [Easy WP
SMTP](https://wordpress.org/plugins/easy-wp-smtp/). The host partner and end
user are responsible for selecting, configuring, securing, and supporting a
third-party service.
