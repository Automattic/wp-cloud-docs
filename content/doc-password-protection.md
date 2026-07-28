# Password protection

WP Cloud Password Protection prevents elevated WordPress users and newly
created accounts from using weak or known-compromised passwords. It checks the
normal login, password reset, profile update, registration, and wp-admin user
creation flows and asks the user to choose a stronger, unique password.

Host accounts created after June 2, 2026 have Password Protection enabled by
default. Partners whose host accounts do not have Password Protection enabled
by default can contact WP Cloud to coordinate enabling it. Each site can
override its host client's default. WP Cloud also plans to provide controls
that make it easier for partners to enable or disable Password Protection on
individual sites.

## Accounts and actions covered

For existing accounts, Password Protection applies when the user can
`publish_posts` or `edit_published_posts`. New registration and wp-admin user
creation are checked regardless of the new account's role.

When an existing user attempts to sign in with a compromised password, the
login is blocked and WordPress directs the user through a password reset. A
password update or account creation that uses a known-compromised value returns:

```text
Error: This password is known to be included in compromised password lists. Please choose something more unique.
```

The affected user requests a reset, receives the normal WordPress confirmation
email, follows its link, and chooses a password that is not present in the
known-compromised data. The same rejection applies when an administrator edits
a user or creates a new account with a weak value.

## Privacy and availability

The site hashes the password locally and sends only a partial hash prefix to
the verification service. The service returns possible matching suffixes and
the site completes the comparison locally. The full password and full hash do
not leave the site.

If the verification service is unavailable or misconfigured, the check fails
open and allows the account action rather than locking out users.

Because the comparison occurs locally, a matching suffix from the service does
not by itself disclose the password or prove which possible password the user
submitted.

## Override the host default

Add the override above the final stop-editing comment in `wp-config.php` or the
equivalent site-level configuration. Enable it with:

```php
define( 'WPC_PASSWORD_PROTECTION_ENABLED', true );
```

Disable it with:

```php
define( 'WPC_PASSWORD_PROTECTION_ENABLED', false );
```

Only define the constant when a site needs to differ from its host client's
default. WP Cloud Password Protection automatically disables itself when it
detects [Jetpack Account
Protection](https://jetpack.com/support/improve-your-wp-admin-password-security-with-account-protection/)
as active.

## Test Password Protection

Use this sequence:

1. Choose a non-production or otherwise low-risk site.
2. Check whether the host client default already enables Password Protection.
3. If not, set `WPC_PASSWORD_PROTECTION_ENABLED` to `true` for the test site.
4. Create a throwaway account that can publish or edit published posts, such
   as an administrator.
5. Test the standard login, password-reset, profile password update, new-user
   registration, and wp-admin user-creation flows.
6. Use only throwaway weak test values—never a real user's password.
7. Check PHP error logs for `Password Protection` entries after a detection or
   blocked login.
8. Remove a temporary override when the site should return to the host default.

Relevant [PHP error logs](/docs/monitoring-logs/logs/error-logs/)
begin with `Password Protection:`, for example:

```text
Password Protection: Blocked login for user "{user}" (ID: {id}) with compromised password...
Password Protection: Compromised password detected...
Password Protection: API error...
```

Remove a temporary site-level override after testing when the site should
return to its host default.

## Troubleshoot Password Protection

When the check does not run for an existing user, confirm that the account can
`publish_posts` or `edit_published_posts`. Test a core WordPress account flow
before a custom login, registration, membership, SSO, or user-management flow,
then review the PHP error logs.

If a legitimate workflow is blocked, first confirm that the password is unique
and not known to be compromised. Check whether custom authentication code
changes the standard flow. The site-level constant can temporarily disable the
feature while the integration is isolated.

Record the exact error, timestamp and timezone, site URL, user role, account
flow, and related PHP log entries when a reproducible platform failure needs
WP Cloud investigation.

Follow your incident response process when a weak password may already have
led to unauthorized access.

## Common questions

**Is Password Protection enabled by default?** Host-client accounts created
after June 2, 2026 have it enabled by default. Other partners can contact WP
Cloud to coordinate enabling it for their host account. A site can override
either state with `WPC_PASSWORD_PROTECTION_ENABLED`. WP Cloud also plans to
provide easier controls for changing the setting on individual sites.

**Which users are checked?** Existing users are checked when they can
`publish_posts` or `edit_published_posts`. Registration and wp-admin user
creation are checked regardless of the new user's role because the password
is being accepted for a new account.

**Which WordPress actions are protected?** Password Protection checks the
standard login, lost-password reset, profile password update, registration,
and wp-admin user-creation flows. A custom membership, SSO, or user-management
flow may need separate testing.

**What should a blocked user do?** The user should follow the normal WordPress
password-reset flow and choose a unique password that is not present in known
compromised-password data. An administrator should not work around the block
by assigning another commonly used password.

**Does WP Cloud receive the password?** No. The site sends only a partial hash
prefix, receives possible matching suffixes, and performs the final comparison
locally. Neither the full password nor its complete hash leaves the site.

**Does it require Jetpack?** No. However, WP Cloud Password Protection turns
itself off when Jetpack Account Protection is active so the two features do
not enforce overlapping checks.

**Does the feature require Jetpack?** No. Password Protection is implemented
by WP Cloud. When Jetpack Account Protection is active, the WP Cloud feature
disables itself so the two products do not govern the same password flow.

**Can one site enable or disable it independently?** Yes. The site constant
overrides the host client default in either direction.

**What happens when verification is unavailable?** The check fails open and
allows the request rather than locking out the account.

**Does the full password leave the site?** No. The site sends a partial hash
prefix and completes the possible-match comparison locally.
