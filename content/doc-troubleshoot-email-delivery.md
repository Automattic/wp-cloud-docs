# Troubleshoot email delivery

A transactional email sent by WordPress can be accepted by the application but
rejected later by the WP Cloud mail service, the receiving provider, or the
recipient's filtering.
Begin by finding out whether the problem affects every message, one plugin,
one sender address, one recipient, or one receiving provider.

Common causes include a platform abuse block, a From address that does not
match the primary domain, a plugin-specific configuration problem, the hourly
sending limit, or filtering by the receiving mailbox provider.

## Confirm WP Cloud email DNS records

The site's primary domain must have the WP Cloud SPF and DKIM records for the
platform mail service to authenticate and deliver messages properly. Confirm
that the current records match the [Transactional email DNS
configuration](/docs/wordpress/transactional-email/#authenticate-mail-with-dns)
before investigating plugin or recipient behavior. Review the DMARC record as
well when the domain uses a DMARC policy.

## Check for a platform email block

Use the [Email Block
endpoint](https://wp.cloud/docs/api/#tag/email/GET/email-block/{client}/{action}/{type})
to determine whether the site's domain is blocked from the platform-provided
mailer. Review the current expiration and reason before acting on an older
`sasl_block` webhook.

If the domain is blocked, stop the abusive or compromised sending behavior and
correct its email authentication. [Transactional
email](/docs/wordpress/transactional-email/) covers SPF, DKIM,
DMARC, the default service limit, and external email providers.

## Check the sender and affected messages

- Confirm that WordPress and every sending plugin use an address on the site's
  primary domain, such as `orders@example.com`, rather than a Gmail or other
  unrelated address.
- Determine whether failures come from one plugin. Review that plugin's mail
  settings and documentation; WooCommerce maintains an [email FAQ and
  troubleshooting guide](https://woocommerce.com/document/email-faq/).
- Compare several recipients. A failure limited to one address, university,
  company, or mailbox provider often points to recipient-side filtering.
- Ask the recipient to check spam or quarantine folders.
- Confirm that the site has not exceeded the WP Cloud limit of 200 messages per
  hour when it uses the default mailer.

## Record what WordPress sends

An email logging plugin can show whether WordPress created the expected
message, sender, recipient, and headers. Examples include [Email
Log](https://wordpress.org/plugins/email-log/) and [WP Mail
Logging](https://wordpress.org/plugins/wp-mail-logging/).

A WordPress log entry does not prove that the receiving mailbox accepted the
message; it confirms what the application attempted to send. Compare it with
the email-block result and the receiving provider's response when available.

## Use an email service provider when needed

Use an SMTP plugin with a dedicated email service provider when the site sends
bulk mail, sends more than standard transactional messages, approaches or
exceeds WP Cloud's hourly limit, needs more than four sender addresses, sends
automated sequences, or needs higher daily volume, delivery analytics, bounce
handling, and reputation controls. A dedicated provider is also appropriate
when a custom setup does not work reliably with PHP `mail()` or delivery
failures continue after the sender and DNS records are corrected.

See [Use an email service
provider](/docs/wordpress/transactional-email/#use-an-email-service-provider)
for provider and SMTP plugin options.

Recovery depends on the cause: correct the sender or DNS records, stop abusive
sending, wait and resend after a temporary limit, fix the responsible plugin,
or move the site to an appropriate external delivery provider.
