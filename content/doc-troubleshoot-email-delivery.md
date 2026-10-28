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
mailer. Each block has a `reason` and an `expires_on` time. Review the current
expiration and reason before acting on an older `sasl_block` webhook. WP Cloud
does not send that webhook when a block is lifted.

The reason explains why WP Cloud blocked the domain:

| Reason | What it means | What to fix |
| --- | --- | --- |
| `Too many bounces, sender blocked` | Many messages from the site bounced. Common causes are a form or registration page that sends to fake or mistyped addresses, and a purchased or outdated mailing list. | Find the form, plugin, or list that sends to invalid addresses. Protect the form or clean the list. |
| `Sender address blocked by DMARC settings` | Receiving servers rejected messages because the From address uses a domain whose DMARC policy does not allow WP Cloud to send for it. Free mailbox domains are a common example. | Send from an address on the site's primary domain and add the WP Cloud SPF and DKIM records. You can also send through the From domain's own email provider. |
| `Sender blocked due to automated postings through open forms on site` | Bots submitted a form on the site, and each submission sent an email. | Protect the form, then ask WP Cloud Support to lift the block. |
| `Too many Feedback Loop reports` | Recipients reported the site's email as spam to their mailbox provider. | Stop sending email that recipients did not ask for. Check forms that send email to addresses that visitors enter. |
| Other text, such as `Abuse`, `Insecure forms`, or `Misconfigured From` | WP Cloud staff added the block. The reason names the problem. | Fix the problem that the reason names, then ask WP Cloud Support to lift the block. |

Blocks for open forms and blocks that WP Cloud staff add have expiration times
years in the future. They stay in place until WP Cloud Support lifts them.
Other automatic blocks end at their `expires_on` time, but a new block can
start if the cause continues. To have a block lifted before it expires, see
[Lift a block](#lift-a-block).

If the domain is blocked, stop the abusive or compromised sending behavior and
correct its email authentication. [Transactional
email](/docs/wordpress/transactional-email/) covers SPF, DKIM,
DMARC, the default service limit, and external email providers.

## Lift a block

A partner cannot lift a block through the WP Cloud API. WP Cloud Support can
lift a long-term block, or a short-term block before it expires, after you
stop the unwanted sending and fix its cause. Fix every open form, spam, and
DNS record problem on the site before you contact WP Cloud Support.

For a block on a single recipient address, confirm that the address is correct
and can receive mail. Then go to step 9.

1. Get the block's reason and expiration from the [Email Block
   endpoint](https://wp.cloud/docs/api/#tag/email/GET/email-block/{client}/{action}/{type})
   or from the error text.
2. Find what sent the unwanted email, such as a contact form, registration
   page, comment form, plugin, or compromised account. An email logging plugin
   can show the sender, recipients, and subject of recent messages. Use it
   only while you investigate.
3. Make sure that Akismet is active and checking the site's forms. Every WP
   Cloud site includes Akismet.
4. Add a CAPTCHA or another challenge to every form that Akismet does not
   check. Include contact, registration, comment, and checkout forms.
5. Turn off form options that email a copy of a submission to the address that
   the visitor entered. With such an option, anyone can use the form to send
   email from the site to any address.
6. In **Settings > General**, clear **Anyone can register** unless the site
   needs open registration. If it does, protect the registration form as in
   step 4.
7. Delete user accounts that bots created.
8. If the reason names DMARC, the From address, or the sender, use a From
   address on the site's primary domain. Then confirm the [SPF and DKIM
   records](/docs/wordpress/transactional-email/#authenticate-mail-with-dns).
9. Contact WP Cloud Support. Include the block reason and expiration, the
   sender address and domain, and the sending path. Name the form, plugin, or
   account that sent the email, and include a sample of the unwanted messages.
   List the plugin, theme, and WordPress updates you applied, and any
   credential or two-factor authentication changes. Add any malware or
   vulnerability findings and evidence that the unwanted sending stopped.

## Read errors from the WP Cloud mailer

When the WP Cloud mailer refuses a message, `wp_mail()` returns `false` and
WordPress fires the `wp_mail_failed` action. A logging plugin that records
failed messages can show the error text while you investigate.

| Error text | Cause | What to do |
| --- | --- | --- |
| `SASL login name rejected: <reason>. Expires: <date>` | WP Cloud blocked the site's domain. The reason is the same one that the Email Block endpoint returns. | See [Check for a platform email block](#check-for-a-platform-email-block). |
| `this user is blocked from sending e-mail. please contact support.` | WP Cloud turned off sending for the site's domain. The message tells the site's users to contact their host. | Fix every open form, spam, and DNS record problem on the site. Then contact WP Cloud Support. See [Lift a block](#lift-a-block). |
| `hourly message quota exceeded` | The site reached the limit of 200 recipients per hour. | Send the message again after the hour ends. For higher volume, use an email service provider. |
| `Maximum number of foreign domain senders exceeded` | The site sent from more than four From addresses outside its own domain within 24 hours. The mailer refuses each additional outside address. | Send from addresses on the site's primary domain. |
| `Recipient address rejected: <reason>. Expires: <date>` | Earlier messages to this address failed, or the recipient reported spam. For example, the mailbox does not exist, is full, or its domain does not accept mail. WP Cloud stops sending to the address until the date shown. | Check the address for typos. If the address is correct, the block ends at the date shown. To have it lifted sooner, see [Lift a block](#lift-a-block). Messages to other recipients are not affected. |
| `Recipient address rejected: Banned domain` | WP Cloud does not deliver mail to the recipient's domain. | Use another address for that recipient. |

The Email Block endpoint lists only blocks on a site's domain. Blocks on a
single recipient address appear only in these errors.

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
- Confirm that the site has not exceeded the WP Cloud limit of 200 recipients
  per hour when it uses the default mailer.

## Record what WordPress sends

An email logging plugin can show whether WordPress created the expected
message, sender, recipient, and headers. Examples include [Email
Log](https://wordpress.org/plugins/email-log/) and [WP Mail
Logging](https://wordpress.org/plugins/wp-mail-logging/).

A WordPress log entry does not prove that the receiving mailbox accepted the
message; it confirms what the application attempted to send. Compare it with
the email-block result and the receiving provider's response when available.

Use an email logging plugin only while you debug a problem. These plugins
store a copy of each message in the site's database, including recipient
addresses and message content. Logs kept long term grow the database and hold
personal data that the site does not need. When you finish, delete the stored
logs and deactivate the plugin.

## Use an email service provider when needed

Use an SMTP plugin with a dedicated email service provider when the site sends
bulk mail, sends more than standard transactional messages, approaches or
exceeds WP Cloud's hourly limit, sends from more than four addresses outside
the site's domain, sends automated sequences, or needs higher daily volume,
delivery analytics, bounce handling, and reputation controls. A dedicated
provider is also appropriate when a custom setup does not work reliably with
PHP `mail()` or delivery failures continue after the sender and DNS records
are corrected.

See [Use an email service
provider](/docs/wordpress/transactional-email/#use-an-email-service-provider)
for provider and SMTP plugin options.

Recovery depends on the cause: correct the sender or DNS records, stop abusive
sending, wait and resend after a temporary limit, fix the responsible plugin,
or move the site to an appropriate external delivery provider.
