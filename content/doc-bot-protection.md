# Bot protection

WP Cloud Bot Protection helps defend standard WordPress login and password-reset
forms from credential stuffing, brute-force attempts, and reset spam. It scores
each protected request and either allows it, presents a browser challenge, or
blocks it.

## Availability and rollout

WP Cloud Bot Protection is available on WP Cloud and is **off by default on
every site**. A site must opt in explicitly by defining the
`WPC_BOT_PROTECTION_ENABLED` constant. Bot Protection does not require Jetpack.

WP Cloud may offer host-client-level default enablement in the future. Before
such a default is enabled, the host partner should set
`WPC_BOT_PROTECTION_ENABLED` to `false` on every site that runs automation or
testing. Uptime monitors, synthetic logins, CI or end-to-end tests, and scripted
provisioning that submit the login or password-reset forms can look like bot
activity. Those requests may be challenged, which non-interactive automation
cannot complete, or blocked.

## What Bot Protection does

WP Cloud evaluates each protected authentication request and applies one of
three results:

- **Allow:** The request proceeds normally.
- **Challenge:** The visitor must complete an **I am not a robot** checkbox
  before the request continues.
- **Block:** WordPress rejects the request with an error.

Bot Protection currently applies to standard `wp-login.php` submissions for:

- signing in; and
- requesting a password reset.

The decision applies to the request rather than a specific WordPress role. It
does not cover XML-RPC, application-password authentication, or every custom
login, registration, membership, and SSO flow.

An allowed request continues normally. A challenged visitor must complete an
**I am not a robot** checkbox. A blocked login shows `Error: Sign-in blocked.
If this looks wrong, contact support.` A blocked password reset uses the same
message with `Password reset blocked`.

If a visitor submits a challenged form before completing the checkbox,
WordPress holds the request and shows `Error: Please complete the verification
step and try again.` The visitor can complete the challenge and resubmit; the
site does not need to create another account or change the password.

## Reliability and lockout avoidance

If the verification service is unavailable or misconfigured, Bot Protection
fails open and allows the request. Only an explicit block response from a
successful evaluation stops a visitor.

This fail-open behavior is intended to avoid accidental lockouts during a
service or network problem. It also means the absence of a challenge is not
proof that a suspicious request was evaluated. Use the browser request and PHP
logs when confirming the integration.

## Privacy

A small browser client collects browser and behavioral signals on the login
page. The browser encrypts that telemetry and exchanges it for an opaque,
short-lived session identifier. The site sends that identifier—not the account
password—to the verification service. Each site authenticates with a per-site
key that is not transmitted over the network.

## Enable Bot Protection

Add the following above the final stop-editing comment in `wp-config.php` or
the equivalent site-level configuration:

```php
define( 'WPC_BOT_PROTECTION_ENABLED', true );
```

Set the value to `false` to disable Bot Protection for the site:

```php
define( 'WPC_BOT_PROTECTION_ENABLED', false );
```

Do not enable the feature on a site whose uptime monitors, synthetic logins,
CI tests, or other automation submit the protected forms unless that automation
can be excluded. Automated requests can be challenged or blocked. A custom
mu-plugin can use the `wpcloud_bot_protection_enable` filter to disable the
check for a narrowly identified request while leaving it enabled elsewhere.

## Error logs and monitoring activity

WP Cloud writes certain Bot Protection events to the site's [PHP error
logs](/docs/monitoring-logs/logs/error-logs/). Entries begin with
`Bot Protection:`, including transport and HTTP errors such as:

```text
Bot Protection: verify transport error: {message}
Bot Protection: verify HTTP {code}: {response}
```

## Test the protected flows

Use this sequence:

1. Choose a non-production or otherwise low-risk site.
2. Confirm `WPC_BOT_PROTECTION_ENABLED` is `true`.
3. Use a throwaway account rather than a real user's credentials.
4. Open the standard WordPress login form and submit a normal login.
5. Open **Lost your password?** and submit a password-reset request.
6. Look for `/collect` requests in the browser network activity while viewing
   and submitting the forms.
7. Review PHP error logs for entries that begin with `Bot Protection`.
8. Remove the site-level override when the site should no longer use Bot
   Protection.

A normal test might not trigger the challenge because only requests classified
as suspicious show the checkbox. A successful `/collect` request confirms that
the browser client is active even when the verdict is allow.

Remove the temporary constant after the test if the site should return to its
previous state.

## Troubleshoot Bot Protection

If Bot Protection does not run:

- Confirm that `WPC_BOT_PROTECTION_ENABLED` is `true`.
- Test a core WordPress login or password-reset form before testing a custom
  authentication flow.
- Check the PHP error log for entries beginning with `Bot Protection:`.
- Remember that an unavailable verification service fails open and does not
  produce a challenge.

If a legitimate workflow is unexpectedly challenged or blocked:

- Have the visitor complete the **I am not a robot** checkbox if shown, then
  retry.
- Check whether a custom login, registration, SSO, or user-management flow
  changes the normal WordPress login flow.
- For automation such as uptime monitors, synthetic logins, CI or end-to-end
  tests, and scripted provisioning, set `WPC_BOT_PROTECTION_ENABLED` to `false`
  for that site.
- Before contacting WP Cloud Support about a reproducible platform block,
  gather the exact error text, site URL, timestamp and timezone, protected
  form, source address, user agent, and related PHP log entries.
- If necessary, disable Bot Protection by setting
  `WPC_BOT_PROTECTION_ENABLED` to `false` while investigating the problem.

## Common questions

**Can one site remain enabled while a specific action bypasses the check?** A
custom mu-plugin can filter `wpcloud_bot_protection_enable` after it has
identified the exact request. Keep the exception narrow; a broad bypass can
remove the protection from real login attempts.

**What happens when the service is unavailable?** The check fails open and
allows the attempt. Users are not locked out by a temporary integration error.

**Does the password leave the site?** No. Bot Protection scores browser and
request signals and does not inspect or transmit the account password.

**Is Bot Protection enabled by default?** No. Each site must opt in with
`WPC_BOT_PROTECTION_ENABLED`. If WP Cloud later enables a host-client default,
a site can still opt out by setting the constant to `false`.

**Does it protect XML-RPC or application-password authentication?** No. The
feature protects the standard WordPress login and password-reset forms served
through `wp-login.php`.

**Does it require Jetpack?** No. Bot Protection is part of the WP Cloud
platform and operates independently of Jetpack.
