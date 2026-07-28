# Persistent data

Persistent Data stores site-specific values that a partner controls through the WP Cloud API and site code can read through `Atomic_Persistent_Data`. A partner can set Persistent Data during site creation or after the site has been provisioned, using a different endpoint for each operation. A partner's customer cannot change these values from WordPress.

Persistent Data remains in place until the partner updates or removes it through the API, and it is preserved across site resets and clones. It is separate from the `_data` site-meta field used for site type, billing classification, and partner inventory metadata.

## Choose appropriate values

Partners can use Persistent Data for any site-wide value their integration needs, including:

- a hosting plan identifier;
- a partner's site or account ID;
- a feature flag used by a partner plugin; or
- a time-limited entitlement such as `PLAN_EXPIRATION`.

Persistent Data is appropriate for site-wide values that control critical behavior. A hosting plan is one example: a partner plugin can use the plan value to gate features, and a missing or stale value can deny features the customer paid for.

Do not use Persistent Data as primary storage or as the source of truth. Maintain the authoritative value in your own system and push it to Persistent Data when it changes.

Do not use Persistent Data for per-user values such as a WordPress administrator's color scheme. That would require WP Cloud to store a separate value for every applicable user on the site. Store user-specific data in the site's application database instead.

## Set data during site creation

If a value must exist when a new site first starts, supply it through the [Create Site endpoint](https://wp.cloud/docs/api/#tag/sites/POST/create-site/{client}) using `persist_data`:

```bash
--data-urlencode 'persist_data[HOST_PLAN]=business'
```

For a complete site-creation request, use the [WP Cloud API quick start](/docs/api-automation/api-quick-start/#create-a-site). Do not call a site-scoped Persistent Data operation until provisioning has finished.

## Set or remove data after a site is provisioned

Use the [Persistent Data endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-persist-data/{site}) after the site exists. This request sets `HOST_PLAN` and removes `PLAN_EXPIRATION` in one operation:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'data[HOST_PLAN][value]=business' \
  --data-urlencode 'data[PLAN_EXPIRATION][delete]=1' \
  "https://atomic-api.wordpress.com/api/v1.0/site-persist-data/${WP_CLOUD_SITE_ID}"
```

A successful response returns the current data and a response ticket ID. Follow the ticket with the [Get Response Ticket Summary endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/summary) or [Get Response Ticket Details endpoint](https://wp.cloud/docs/api/#tag/response-tickets/POST/response-ticket/get/full) until it reaches a terminal state. The returned `job_id` field is deprecated and is not a reliable success signal.

If the endpoint returns HTTP 429, wait for the number of seconds in the `Retry-After` header before trying again. That response means WP Cloud could not acquire the site's data lock.

## Read data in WordPress

WP Cloud encrypts Persistent Data before storing it in the platform database. The site receives an encrypted file at `/tmp/.at-persistent-data`. Read values through the platform class, normally from a partner plugin or mu-plugin:

```php
$persistent_data = new Atomic_Persistent_Data();
$host_plan = $persistent_data->HOST_PLAN;
```

Check that your code handles a missing or expired value safely. A missing plan value should not silently grant a paid feature.

After the response ticket completes, read the value through `Atomic_Persistent_Data` on a non-production site or exercise the partner feature that consumes it. This checks the value that site code receives, rather than only the value accepted by the API.
