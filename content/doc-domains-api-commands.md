# Domain Services API command reference


The Domain Services API (DSAPI) accepts commands as JSON payloads. Each command
follows this structure:

```json
{
  "command": "Domain\\Register",
  "params": {
    "domain": "example.com",
    "contacts": { ... }
  },
  "client_txn_id": "unique-correlation-id"
}
```

- `command`: The fully qualified command name (e.g., `Domain\Register`).
- `params`: An object containing the command parameters.
- `client_txn_id`: An optional correlation ID you provide to match async events back to the originating command.

All responses share a common envelope (`status`, `success`, `client_txn_id`,
`data`, `errors`, and other fields) described in the [Domain Services API
overview](/docs/api-automation/domain-registration-api/overview/#response-envelope). The **Response**
sections below describe the command-specific payload under the envelope's
`data` key.

Treat authorization codes and domain contact information as sensitive. Do not
write them to application logs or expose them to an end customer who does not
control the domain.

## Synchronous and asynchronous commands

Commands are either **synchronous** or **asynchronous**:

- **Sync** commands return their result directly in the HTTP response.
- **Async** commands return HTTP `202 Accepted` immediately. The actual result is delivered later as an event. Use the Event commands to poll for and acknowledge these results. The `client_txn_id` you provide in the request will appear in the corresponding event, allowing you to correlate responses.

Async commands: `Domain\Register`, `Domain\Transfer`, `Domain\Renew`, `Domain\Restore`, `Domain\Delete`.

---

## Domain commands

### `Domain\Check`

Check the availability of a domain name.

> **Note:** The `domains` parameter is an array for future compatibility, but currently it must contain exactly one domain name. Requests with more than one domain are rejected with an invalid value error.

| Parameter | Type  | Required | Description                                             |
|-----------|-------|----------|---------------------------------------------------------|
| `domains` | array | Yes      | Array containing the domain name to check (exactly one). |

**Response:** Sync. Returns a `domains` object keyed by domain name. Each entry contains:

| Field                | Type        | Description                                                       |
|----------------------|-------------|-------------------------------------------------------------------|
| `available`          | bool        | Whether the domain is available for registration.                 |
| `zone_is_active`     | bool        | Whether the TLD is active for your account.                       |
| `tld_in_maintenance` | bool        | Whether the TLD is currently in maintenance.                      |
| `fee_class`          | string      | Fee class of the domain (e.g., standard or premium).              |
| `fee_amount`         | float\|null | Fee for premium domains. `null` for standard-priced domains.      |

Premium domains may additionally include `fee_amount_new`, `fee_amount_renewal`, and `fee_amount_transfer`.

---

### `Domain\Register`

Register a new domain name.

> **Note:** Registration of [premium domains](/docs/api-automation/domain-registration-api/overview/#premium-domains) is not currently supported.

| Parameter         | Type           | Required | Description                                                                 |
|-------------------|----------------|----------|-----------------------------------------------------------------------------|
| `domain`          | string         | Yes      | The domain name to register.                                                |
| `contacts`        | object         | Yes      | Contact information (owner, admin, tech, billing).                          |
| `period`          | int            | No       | Registration period in years. Default: `1`.                                 |
| `nameservers`     | array          | No       | Nameservers to set. Default: `ns1.wordpress.com`, `ns2.wordpress.com`, `ns3.wordpress.com`. |
| `dns_records`     | array          | No       | DNS records to set after registration.                                      |
| `privacy_setting` | string         | No       | WHOIS privacy setting. Default: privacy service enabled.                    |
| `price`           | int or null    | No       | Reserved for premium domain pricing, which is not currently supported. Omit or pass `null`. |

> **`contacts` object:** Contains up to 4 contact types: `owner`, `admin`, `tech`, `billing`. Each contact has fields: `first_name`, `last_name`, `organization`, `address_1`, `address_2`, `city`, `state`, `postal_code`, `country_code`, `email`, `phone`, `fax`.

> **`dns_records` array:** Each element is a record object with `type` (A, AAAA, CNAME, MX, TXT, etc.), `name`, and `data` fields.

**Response:** Async (HTTP 202)

---

### `Domain\Transfer`

Transfer a domain in from another registrar.

> **Note:** Transfer of [premium domains](/docs/api-automation/domain-registration-api/overview/#premium-domains) is not currently supported.

| Parameter     | Type   | Required | Description                                            |
|---------------|--------|----------|--------------------------------------------------------|
| `domain`      | string | Yes      | The domain name to transfer.                           |
| `auth_code`   | string | Yes      | The authorization/EPP code from the current registrar. |
| `contacts`    | object | Yes      | Contact information (owner, admin, tech, billing).     |
| `nameservers` | array  | No       | Nameservers to set after transfer completes.           |
| `dns_records` | array  | No       | DNS records to set after transfer completes.           |

**Response:** Async (HTTP 202)

---

### `Domain\Transferable`

Check whether a domain can be transferred to DSAPI.

| Parameter   | Type   | Required | Description                                            |
|-------------|--------|----------|--------------------------------------------------------|
| `domain`    | string | Yes      | The domain name to check.                              |
| `auth_code` | string | Yes      | The authorization/EPP code from the current registrar. |

**Response:** Sync

---

### `Domain\Renew`

Renew an existing domain registration.

| Parameter                | Type          | Required | Description                                                        |
|--------------------------|---------------|----------|--------------------------------------------------------------------|
| `domain`                 | string        | Yes      | The domain name to renew.                                          |
| `current_expiration_year`| int           | Yes      | The domain's current expiration year (used to prevent double renewals). |
| `period`                 | int           | No       | Number of years to renew. Default: `1`.                            |
| `fee_amount`             | float or null | No       | Renewal fee for premium domains. Omit or pass `null` for standard-priced domains. |

**Response:** Async (HTTP 202)

---

### `Domain\Restore`

Restore a domain that is in the redemption period.

| Parameter | Type   | Required | Description                  |
|-----------|--------|----------|------------------------------|
| `domain`  | string | Yes      | The domain name to restore.  |

**Response:** Async (HTTP 202)

---

### `Domain\Delete`

Delete a domain registration.

> **Warning:** A deletion can move a domain to Pending Delete when its TLD does
> not support redemption. Confirm the domain and its recovery rules before
> sending this command.

| Parameter | Type   | Required | Description                 |
|-----------|--------|----------|-----------------------------|
| `domain`  | string | Yes      | The domain name to delete.  |

**Response:** Async (HTTP 202)

---

### `Domain\Info`

Retrieve detailed information about a domain.

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| `domain`  | string | Yes      | The domain name to query.           |

**Response:** Sync. Returns the domain's registration data:

| Field                                | Type   | Description                                                    |
|--------------------------------------|--------|----------------------------------------------------------------|
| `created_date`                       | string | Date the domain was registered.                                |
| `expiration_date`                    | string | Domain expiration date.                                        |
| `renewable_until`                    | string | Last date the domain can be renewed.                           |
| `paid_until`                         | string | Date the registration is paid up to.                           |
| `updated_date`                       | string | Date the domain record was last updated.                       |
| `auth_code`                          | string | The domain's authorization (EPP/transfer) code.                |
| `nameservers`                        | array  | Nameservers currently set on the domain.                       |
| `contacts`                           | object | Contact information (owner, admin, tech, billing).             |
| `domain_status`                      | array  | EPP status codes for the domain.                               |
| `transferlock`                       | bool   | Whether the transfer lock is enabled.                          |
| `privacy_setting`                    | string | Current WHOIS privacy setting.                                 |
| `rgp_status`                         | string | Registry grace period status, if applicable.                   |
| `dnssec`                             | string | DNSSEC status.                                                 |
| `unverified_contact_suspension_date` | string | Date by which contacts must be verified to avoid suspension.   |

> **Note:** If the domain is not registered with the partner account,
> `Domain\Info` returns the same availability information as `Domain\Check`.

---

### `Domain\Suggestions`

Get domain name suggestions based on a search query.

| Parameter     | Type          | Required | Description                                              |
|---------------|---------------|----------|----------------------------------------------------------|
| `query`       | string        | Yes      | The search term to base suggestions on.                  |
| `quantity`    | int           | Yes      | Number of suggestions to return.                         |
| `tlds`        | array or null | No       | Restrict suggestions to these TLDs. `null` for no restriction. |
| `exact_match` | bool          | No       | Only return exact matches. Default: `false`.             |

**Response:** Sync. Returns a list of suggested domain names.

---

### `Domain\Get\Contacts`

Retrieve the contact information for a domain.

| Parameter | Type   | Required | Description                |
|-----------|--------|----------|----------------------------|
| `domain`  | string | Yes      | The domain name to query.  |

**Response:** Sync. Returns contact information (owner, admin, tech, billing).

---

### `Domain\Set\Contacts`

Update the contact information for a domain.

| Parameter             | Type   | Required | Description                                                                  |
|-----------------------|--------|----------|------------------------------------------------------------------------------|
| `domain`              | string | Yes      | The domain name to update.                                                   |
| `contacts`            | object | Yes      | New contact information (owner, admin, tech, billing).                       |
| `transferlock_opt_out`| bool   | No       | Set to `true` to prevent the 60-day transfer lock. Default: `false`.         |

**Response:** Sync

> **Note:** Updating contacts can trigger the [60-day transfer lock](/docs/api-automation/domain-registration-api/overview/#the-60-day-transfer-lock) per ICANN policy. Set `transferlock_opt_out` to `true` to opt out of this lock.

---

### `Domain\Set\Nameservers`

Set the nameservers for a domain.

| Parameter     | Type   | Required | Description                          |
|---------------|--------|----------|--------------------------------------|
| `domain`      | string | Yes      | The domain name to update.           |
| `nameservers` | array  | Yes      | Array of nameserver hostnames to set.|

**Response:** Sync

---

### `Domain\Set\Privacy`

Set the WHOIS privacy setting for a domain.

| Parameter         | Type   | Required | Description                         |
|-------------------|--------|----------|-------------------------------------|
| `domain`          | string | Yes      | The domain name to update.          |
| `privacy_setting` | string | Yes      | The privacy setting to apply.       |

> **Valid `privacy_setting` values:**
> - `enable_privacy_service`: Enable WHOIS privacy protection
> - `redact_contact_info`: Redact contact information from WHOIS
> - `disclose_contact_info`: Show full contact information in WHOIS

**Response:** Sync

---

### `Domain\Set\Transferlock`

Enable or disable the transfer lock on a domain.

| Parameter      | Type   | Required | Description                                          |
|----------------|--------|----------|------------------------------------------------------|
| `domain`       | string | Yes      | The domain name to update.                           |
| `transferlock` | bool   | Yes      | `true` to lock the domain, `false` to unlock it.    |

**Response:** Sync

---

## DNS commands

DNS commands manage records for domains using the WordPress.com nameservers.
See [Nameservers and DNS](/docs/api-automation/domain-registration-api/overview/#nameservers-and-dns).

> **Note:** DNS record management is not available in OTE, since OTE domains are not actually registered.

### `Dns\Get`

Retrieve all DNS records for a domain.

| Parameter | Type   | Required | Description                |
|-----------|--------|----------|----------------------------|
| `domain`  | string | Yes      | The domain name to query.  |

**Response:** Sync. Returns an array of DNS records for the domain.

---

### `Dns\Set`

Set DNS records for a domain. This replaces all existing records.

> **Warning:** Include every record that must remain. Omitting a record removes
> it and can interrupt the domain's website, email, or other services.

| Parameter     | Type   | Required | Description                              |
|---------------|--------|----------|------------------------------------------|
| `domain`      | string | Yes      | The domain name to update.               |
| `dns_records` | array  | Yes      | Array of DNS record objects to set.      |

**Response:** Sync

---

## Event commands

Events are the mechanism for receiving results from async commands and domain lifecycle notifications. Each event has a unique ID and must be acknowledged after processing to prevent it from being returned again. See the [Events Reference](/docs/api-automation/domain-registration-api/events/) for the polling flow and all event types.

### `Event\Enumerate`

List unacknowledged events.

| Parameter | Type | Required | Description                                   |
|-----------|------|----------|-----------------------------------------------|
| `limit`   | int  | No       | Maximum number of events to return. Default: `50`. Max: `50` (higher values are rejected). |

**Response:** Sync. Returns:

| Field         | Type   | Description                                                                  |
|---------------|--------|------------------------------------------------------------------------------|
| `events`      | array  | Unacknowledged events (up to `limit`), full payloads included. See [Event Structure](/docs/api-automation/domain-registration-api/events/#event-structure). |
| `total_count` | int    | Total number of unacknowledged events, which may exceed the number returned. |

---

### `Event\Details`

Get a single event by ID. Useful for re-fetching a specific event; `Event\Enumerate` already returns full event payloads.

| Parameter  | Type | Required | Description                  |
|------------|------|----------|------------------------------|
| `event_id` | int  | Yes      | The ID of the event to retrieve. |

**Response:** Sync. Returns the event object under the `event` key. See [Event Structure](/docs/api-automation/domain-registration-api/events/#event-structure).

---

### `Event\Ack`

Acknowledge an event, marking it as processed. Acknowledged events will no longer appear in `Event\Enumerate` results.

| Parameter  | Type | Required | Description                       |
|------------|------|----------|-----------------------------------|
| `event_id` | int  | Yes      | The ID of the event to acknowledge. |

**Response:** Sync

---

## Email commands

### `Email\Send\Auth_Code`

Send the domain's authorization (EPP/transfer) code to the domain owner's email address.

| Parameter | Type   | Required | Description                            |
|-----------|--------|----------|----------------------------------------|
| `domain`  | string | Yes      | The domain whose auth code to send.    |

**Response:** Sync

---

### `Email\Send\Verification`

Send a contact verification email to the specified address.

| Parameter | Type   | Required | Description                            |
|-----------|--------|----------|----------------------------------------|
| `email`   | string | Yes      | The email address to send verification to. |

**Response:** Sync
