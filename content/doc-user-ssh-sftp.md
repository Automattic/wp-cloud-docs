# User SSH and SFTP access

User SSH and SFTP credentials give a customer, developer, or support user access to one WP Cloud site. They are separate from [Client SSH](/docs/site-access/ssh-sftp/client-ssh/), which is intended for a host partner's teams, panels, and automation.

Site users connect with their assigned username:

```text
<username>@ssh.atomicsites.net
```

A partner may use its own hostname by pointing a CNAME record to `ssh.atomicsites.net`.

## Choose an authentication method

A site user can authenticate with a public key or password. Prefer public keys for developers and automation.

You can provide a complete public key or an alias created with the [`alias-pkey` operation](https://wp.cloud/docs/api/#tag/ssh/POST/alias-pkey/set/{client}/{category}/{name}). An alias lets you rotate a person's key everywhere it is referenced without updating each site user separately.

The Add Site SSH/SFTP User endpoint treats the `pass` field as follows:

- omit `pass` to have WP Cloud generate a password;
- send an empty `pass` value to create a key-only user; or
- send a specific value to set that password.

A key-only user must have a valid public key. Do not share one site-user credential among several people. Create separate users so access can be removed without disrupting someone else.

## Choose SFTP or shell access

WP Cloud sites are SFTP-only for site users by default. A host partner may have a different account default, and a site-specific setting takes precedence over the account and platform defaults.

The `ssh-user` operations manage credentials. Adding or updating a user does not change the site's allowed access method. Use the access-type control provided by your partner integration when a site user needs a full shell.

Client SSH always provides full shell and SFTP access to the selected partner site, regardless of the site-user access type.

## Create a site user

Usernames must contain at least five characters and cannot be entirely numeric. They must also be unique across WP Cloud. Include a partner or site identifier in each username to avoid collisions, for example `example-5678-alex`.

The [Add Site SSH/SFTP User endpoint](https://wp.cloud/docs/api/#tag/ssh/POST/ssh-user/{service}/{identifier}/add) accepts a site ID or domain as the identifier. This example creates a password user by domain:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'user=example-5678-alex' \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/add"
```

Example response:

```json
{
  "message": "OK",
  "data": {
    "user": "example-5678-alex",
    "pass": "generated-password"
  }
}
```

Store a generated password securely before continuing. To create a key-only user, supply `pkey` and an empty `pass` value:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'user=example-5678-alex' \
  --data-urlencode 'pkey=pub://example-host/customers?alex' \
  --data-urlencode 'pass=' \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/add"
```

Replace the example alias with one owned by your WP Cloud client account.

## List site users

Use the [List Site SSH/SFTP Users endpoint](https://wp.cloud/docs/api/#tag/ssh/GET/ssh-user/{service}/{identifier}/list):

```bash
curl --fail-with-body --silent --show-error \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/list"
```

Example response:

```json
{
  "message": "OK",
  "data": [
    "example-5678-alex"
  ]
}
```

## Update a user's credentials

Use the [Update Site SSH/SFTP User endpoint](https://wp.cloud/docs/api/#tag/ssh/POST/ssh-user/{service}/{identifier}/update/{username}) to replace a password, public key, or both. To change an existing user to key-only authentication, send the new `pkey` and an empty `pass` value.

Updating a credential does not change the username or the site's SFTP or shell access setting.

## Remove a site user

Use the [Remove Site SSH/SFTP User endpoint](https://wp.cloud/docs/api/#tag/ssh/POST/ssh-user/{service}/{identifier}/remove/{username}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  "https://atomic-api.wordpress.com/api/v1.0/ssh-user/domain/${WP_CLOUD_DOMAIN}/remove/example-5678-alex"
```

Example response:

```json
{
  "message": "OK",
  "data": true
}
```

Removal also queues the user's active sessions for disconnection.

A `true` result means that WP Cloud accepted the removal. Check the user list and attempt a new connection to confirm that the credential is no longer usable.

## Connect to the site

For SFTP:

```bash
sftp example-5678-alex@ssh.atomicsites.net
```

For a full shell, when shell access is enabled for the site:

```bash
ssh example-5678-alex@ssh.atomicsites.net
```

An SFTP-only user can transfer files but cannot start an interactive shell or run a remote command. Both connection types use the filesystem locations and session limits described in [SSH and SFTP access](/docs/site-access/ssh-sftp/access-models/).

All User SSH and SFTP credentials for a site share a limit of 10 concurrent connections. The limit applies to the site, not to each username. Automation must close connections promptly and prevent overlapping jobs or retries from exhausting the shared capacity. See [Session limits and intermittent connection troubleshooting](/docs/site-access/ssh-sftp/access-models/#session-limits).

## Check a new user

1. List the site's users and confirm that the new username appears.
2. Connect with the intended key or password and confirm that the session reaches the correct site.
3. Confirm that the user receives SFTP-only or full-shell access as configured.
4. Replace or remove the credential and confirm that the previous credential no longer works.
