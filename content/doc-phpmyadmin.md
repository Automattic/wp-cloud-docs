# phpMyAdmin

WP Cloud partners can generate a time-limited phpMyAdmin login URL for a site. The URL opens the site's database with read and write access, so give it only to someone authorized to change that site.

## Generate a login URL

You need an API key authorized for the site and the site's WP Cloud site ID or domain. Make the request from an IP address allowed to use that API key.

Send a `POST` request to the [`site-phpmyadmin/{site}` endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-phpmyadmin/{site}):

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: <api-key>' \
  'https://atomic-api.wordpress.com/api/v1.0/site-phpmyadmin/<site-id>'
```

Replace `<api-key>` with an authorized developer or platform API key and `<site-id>` with the site ID. A successful response returns the login URL in `data.url`. An HTTP error or a response without that value means the portal or integration must not redirect the user.

Open the URL promptly. Do not store it in logs, analytics, chat messages, or tickets. Generate another URL when a different authorized person needs access instead of reusing a copied link.

## Work safely in phpMyAdmin

phpMyAdmin can change or delete WordPress data. Before a destructive or wide-ranging query:

- confirm the site ID and domain;
- create or verify a current database backup;
- export the affected tables when a smaller rollback is useful;
- use a transaction when the storage engine and operation support it;
- avoid changing WordPress's managed database connection values.

Partners decide which customers and support staff may receive phpMyAdmin access. WP Cloud does not provide a read-only phpMyAdmin session for this workflow.

## Recover from a password change

Changing the database user's password inside phpMyAdmin can break WordPress because the managed site environment still contains the prior value. Use the [Database credentials](/docs/site-access/database-access/database-credentials/) procedure and the API's password-reset operation to restore a managed password.
