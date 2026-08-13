# Domain Services API overview

## How the Domain Services API works

The Domain Services API (DSAPI) lets WP Cloud partners register and manage domains
for their end customers, with Automattic as the registrar. Partners can manage
transfers, renewals, Domain Name System (DNS) records, and contact information.
Partner integrations poll asynchronous events to track operation results and
domain lifecycle changes.

## Terminology

The domain industry assigns a specific role to each party involved in a registration:

- **Registry**: The organization that operates a top-level domain (TLD) and
  maintains its authoritative database of registered domains. For example,
  Verisign operates `.com`.
- **Registrar**: An organization accredited to register domains with
  registries. Automattic is the registrar for the DSAPI.
- **Reseller**: An intermediary that offers domain registration to its own
  customers through a registrar. WP Cloud partners are the resellers.
- **Registrant**: The partner's end customer who holds the registration and the
  right to use the domain. The registrant is listed as the owner contact.

## Premium domains

Premium domains are domain names that the registry prices individually, usually because of their perceived value (short, generic, or highly brandable names). Their fees can be much higher than the standard price for the TLD, and they may also carry premium renewal fees.

`Domain\Check` identifies premium domains: the `fee_class` field marks the domain's pricing class, and the fee fields report the actual amounts.

> **Note:** Registration and transfer of premium domains are not currently supported.

## Nameservers and DNS

By default, domains are registered with the WordPress.com nameservers (`ns1.wordpress.com`, `ns2.wordpress.com`, `ns3.wordpress.com`). Domains using these nameservers get DNS hosting on Automattic's DNS infrastructure (powered by PowerDNS) for free, and their records are managed through the `Dns\Get` and `Dns\Set` commands.

Alternatively, a domain can use custom nameservers, set at registration or later via `Domain\Set\Nameservers`. In that case DNS is managed wherever those nameservers point, and the DSAPI DNS commands do not apply.

## The 60-day transfer lock

Internet Corporation for Assigned Names and Numbers (ICANN) policy requires a
60-day lock during which a domain cannot be transferred to another registrar.
The lock is applied after:

- the initial registration,
- an inbound transfer completes,
- a change to the registrant contact information (this one can be avoided by setting `transferlock_opt_out` in `Domain\Set\Contacts`).

When a lock is applied, the `transferlocked_until_date` field in the related events reports when it expires.

This lock is separate from the regular registrar transfer lock, which can be toggled at any time with `Domain\Set\Transferlock` and should stay enabled except when intentionally transferring the domain out.

## Emails to registrants

As the registrar, Automattic sends operational and ICANN-mandated emails
directly to registrants. These emails require no action from the partner.

| Email | When it is sent |
|-------|-----------------|
| Contact verification | On registration, inbound transfer, or registrant email change, when the address is not already verified. Contains the verification link. See [Registrant contact verification](/docs/api-automation/domain-registration-api/domain-lifecycle/#registrant-contact-verification). |
| Contact verified | When the registrant completes the verification. |
| Domain suspended | When a domain is suspended because its registrant email was not verified in time. |
| Renewal reminders | 30 days and 5 days before expiration, and 3 days after expiration, per the ICANN expiration policy. |
| Registrant change complete | When the registrant contact information has been changed. |
| Transfer-away confirmation | When an outbound transfer is requested, asking the registrant to confirm it. |
| Authorization code | When requested via the `Email\Send\Auth_Code` command. |

## Architecture

Partners use the DSAPI for domain operations handled by
Automattic as the registrar. Commands are processed synchronously when
possible. Operations that depend on registry workflows produce asynchronous
events that the partner's integration must poll for.

## Environments

DSAPI operates in two environments:

- **OTE** (Operational Test Environment): for integration testing. Commands run against a test system: registrations are not real, and no real charges apply.
- **LIVE**: production. Commands affect real domains.

Both environments expose the same command surface, so an integration built against OTE works unchanged against LIVE. Each environment has its own separate account: domains registered and events queued in OTE are not visible in LIVE, and vice versa.

Each request is mapped to the partner's account in the selected environment.
Commands can only view and manage domains that belong to that account in that
environment.

> **Note:** DNS record management is not available in OTE, since OTE domains are not actually registered.

### Select the environment

The environment is selected per request with the `live` flag, sent alongside the command:

```json
{
  "command": "Domain\\Check",
  "params": {
    "domains": [ "example.com" ]
  },
  "live": false
}
```

- `"live": false`, or omitting the flag entirely, runs the command against **OTE**. Anything other than an explicit true value also stays on OTE, so a malformed flag fails toward the test environment.
- `"live": true` runs the command against **LIVE**.

Develop and test your integration against OTE first, then switch to LIVE by sending `"live": true`.

## Quick start

### Command structure

All commands are sent as JSON with this structure:

```json
{
  "command": "Domain\\Register",
  "params": {
    "domain": "example.com",
    "period": 1
  },
  "client_txn_id": "your-unique-correlation-id"
}
```

The `client_txn_id` is a correlation ID that you provide; if you omit it, one is generated automatically. It is echoed back in the command's response and in any async events produced by the command, so you can match results to the original request.

### Synchronous and asynchronous responses

Most commands return status `200` with immediate results in the response body. Commands that trigger long-running registrar operations instead return status `202` (accepted) and deliver their outcome later as an event:

- **Async commands:** `Domain\Register`, `Domain\Transfer`, `Domain\Renew`, `Domain\Restore`, `Domain\Delete`
- **Sync commands:** everything else (availability checks, DNS updates, contact info, event operations, etc.)

### Poll for events

To receive results from async commands and domain lifecycle notifications:

1. Call `Event\Enumerate` to fetch unacknowledged events (up to 50 per call, full payloads included).
2. Process each event in your system.
3. Call `Event\Ack` for each processed event so it is not returned again.

See the [Events Reference](/docs/api-automation/domain-registration-api/events/) for the full polling flow and all event types.

### Date format

All dates in DSAPI are formatted as `YYYY-MM-DD HH:MM:SS` in UTC.

## Responses

### Response envelope

Every response (success or failure, sync or async) carries the same envelope fields:

| Field                | Type   | Description                                                        |
|----------------------|--------|--------------------------------------------------------------------|
| `status`             | int    | Status code (`200` success, `202` accepted, `5xx`/`6xx` error).    |
| `status_description` | string | Human-readable description of the status code.                     |
| `success`            | bool   | Whether the command succeeded.                                     |
| `client_txn_id`      | string | The correlation ID you sent with the command.                      |
| `server_txn_id`      | string | Server-generated transaction ID. Useful when reporting issues.     |
| `timestamp`          | int    | Unix timestamp of when the request was processed.                  |
| `runtime`            | float  | Server processing time in seconds.                                 |
| `data`               | object | Command-specific result payload (present on sync successes).       |
| `errors`             | array  | Error details (present on failures). See below.                    |

A successful sync response looks like this:

```json
{
  "status": 200,
  "status_description": "Command completed successfully",
  "success": true,
  "client_txn_id": "your-unique-correlation-id",
  "server_txn_id": "63.146622342506884399164123",
  "timestamp": 1755084000,
  "runtime": 0.1204,
  "data": {
    "domains": {
      "example.com": {
        "available": true,
        "zone_is_active": true,
        "tld_in_maintenance": false,
        "fee_class": "standard",
        "fee_amount": null
      }
    }
  }
}
```

### Error responses

When a command fails, `success` is `false`, `status` holds an error code, and `errors` contains one or more error objects:

```json
{
  "status": 504,
  "status_description": "Missing required attribute",
  "success": false,
  "client_txn_id": "your-unique-correlation-id",
  "server_txn_id": "63.146622342506884399164124",
  "timestamp": 1755084000,
  "runtime": 0.0312,
  "errors": [
    {
      "description": "Domain name is required",
      "extra": {}
    }
  ]
}
```

- `description`: human-readable error message.
- `extra`: additional structured error data, when available.

### Error codes

| Code | Description |
|------|-------------|
| 200  | Command completed successfully |
| 202  | Request has been accepted for processing |
| 500  | Invalid command name |
| 501  | Invalid command option |
| 502  | Invalid entity value |
| 503  | Invalid attribute name |
| 504  | Missing required attribute |
| 505  | Invalid attribute value syntax |
| 506  | Invalid option value |
| 507  | Invalid command format |
| 508  | Missing required entity |
| 509  | Missing command option |
| 520  | Server closing connection |
| 521  | Too many sessions open |
| 530  | Authentication failed |
| 531  | Authorization failed |
| 541  | Invalid attribute value |
| 545  | Entity not found |
| 549  | Command failed |
| 554  | Domain already registered |
| 599  | Domain TLD currently in maintenance |
| 600  | Invalid event data |
| 601  | Invalid event name |
| 602  | Invalid verification data |
| 603  | Contact handle not linked with a domain |
| 604  | Domain transfer cannot be initiated |
| 999  | Unknown error |
