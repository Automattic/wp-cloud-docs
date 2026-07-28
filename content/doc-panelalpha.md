# PanelAlpha integration

[PanelAlpha](https://www.panelalpha.com/wp-cloud-integration) is an optional,
self-hosted control panel that uses WP Cloud as the WordPress hosting backend.
PanelAlpha supplies white-label customer and team interfaces, hosting plans,
billing integrations, onboarding, and site-management workflows. WP Cloud
supplies and bills the underlying WordPress infrastructure.

The partner maintains accounts with both providers and operates the server
that runs PanelAlpha. A PanelAlpha license change does not delete the WP Cloud
sites, but the partner must use another management interface when PanelAlpha
can no longer access them.

## What the integration provides

PanelAlpha adds the customer-facing and business layer around WP Cloud. Its
current product can provide a white-label control panel, customer and team
accounts, hosting-plan configuration, WHMCS billing integration, onboarding,
site organization, updates, backup controls, DNS workflows, activity logs,
and marketplaces for partner-selected products. Review [PanelAlpha's WP Cloud
integration page](https://www.panelalpha.com/wp-cloud-integration) for the
current feature set.

These are PanelAlpha features, not additional WP Cloud platform guarantees.
The partner decides which actions and plan values to expose to end users. WP
Cloud remains the authority for API behavior, site limits, resource settings,
staging eligibility, and infrastructure billing.

## Who should use PanelAlpha

PanelAlpha can suit hosting providers, domain registrars, agencies, and
multi-site organizations that want a self-hosted, white-label panel instead of
building a customer interface from the WP Cloud API. The partner needs a
server and operational ownership for PanelAlpha itself; WP Cloud hosts the
WordPress sites created through it, not the control panel application.

A team that already has its own portal can integrate with the WP Cloud API
directly. Compare customer management, branding, billing, access controls,
automation, and ongoing PanelAlpha operations before choosing either path.

## Prepare WP Cloud access

1. Create a dedicated key in [Manage and secure API
   keys](/docs/api-automation/api-access/) and restrict it to the endpoints
   PanelAlpha needs. A managed partner without Partner Portal key management
   can request the key and scope through WP Cloud support.
2. Add the PanelAlpha server's static egress address to the key's allowed IP
   ranges.
3. Configure [Client SSH](/docs/site-access/ssh-sftp/client-ssh/) if the
   PanelAlpha workflows will use it. Current PanelAlpha versions can prepare
   and register their Client SSH key through the WP Cloud API, but the host
   client's SSH firewall and allowed source address still need to permit the
   connection.
4. Keep the API key, client identifier, and SSH key restricted to the
   PanelAlpha server. Do not reuse a developer's personal key.

## Add WP Cloud to PanelAlpha

Follow PanelAlpha's current [WP Cloud hosting-server
documentation](https://www.panelalpha.com/documentation/multi-server/hosting-servers/wp-cloud/).
During its installation wizard, add WP Cloud in **Connect Your Server**. In an
existing installation, use **Configuration → Servers → Hosting Servers → Add
Server**. Enter the client identifier and dedicated API key, then test the
connection.

Create a PanelAlpha hosting plan for that server. Its WP Cloud options can
include storage, PHP workers and memory, bursting, data center, and SSH access.
The current limits and billing rules in [Configure resources, site type, and
billing with site meta](/docs/sites/site-meta/) remain authoritative when a
PanelAlpha field or default differs.

PanelAlpha and WP Cloud are separate accounts. WP Cloud bills the host client
for the infrastructure and configured WP Cloud sites. PanelAlpha licenses its
self-hosted control-panel software separately. Keep both accounts and their
operational contacts current while PanelAlpha is the partner's management
interface.

## Test the customer workflow

Create a non-production site through PanelAlpha and confirm:

- the Atomic Site ID and domain appear in the Partner Portal inventory;
- its resource values and site type are correct;
- the intended TLS and DNS records are present;
- SSO, wp-admin, SSH, and SFTP access behave as the plan promises;
- backups, cache controls, and site actions reach the intended WP Cloud site;
  and
- a staging site follows the [WP Cloud staging
  rules](/docs/sites/staging-sites/).

PanelAlpha can also create DNS templates for WP Cloud transactional-email
records. Use [Transactional
email](/docs/wordpress/transactional-email/) as the source for the
current SPF, DKIM, and DMARC guidance.

When this test succeeds, the same Atomic Site ID and intended configuration
should appear in PanelAlpha and the Partner Portal, and each enabled customer
action should affect that site. Test destructive actions, access controls, and
billing-related plan changes separately before offering them to end users.

The expected result is one consistent site record across both systems, with
the customer seeing only the actions and values allowed by the hosting plan.
Resolve any mismatch before using that plan for production provisioning.

## Diagnose integration failures

For an API connection failure, compare the key's allowed IPs with the
PanelAlpha server's actual egress address, confirm its endpoint scope, and
check that the client identifier and key contain no added whitespace. When the
API test succeeds but Client SSH does not, check the Client SSH firewall,
registered key, public-key alias, and source address.

For a provisioning failure, read the returned WP Cloud API error and check
account capacity, domain ownership, supported PHP versions, and plan values.
PanelAlpha controls its user interface, plan configuration, WHMCS integration,
customer management, and licensing; its documentation and support are the
authority for those behaviors.

## Common questions

**Does PanelAlpha host the WordPress sites?** No. PanelAlpha is the management
panel; WP Cloud supplies the WordPress hosting infrastructure.

**Can the service be offered under the partner's brand?** Yes. PanelAlpha is
designed for white-label customer experiences, while WP Cloud operates below
the API layer unless the partner chooses to identify it.

**What happens if PanelAlpha is disconnected?** The WP Cloud sites remain on
WP Cloud and continue to follow their WP Cloud billing and lifecycle settings.
PanelAlpha cannot manage them after its key is revoked, so the partner needs an
alternative interface or direct API process.

**Which limits apply?** WP Cloud account and site limits apply to the hosting
infrastructure. PanelAlpha's license and plan limits apply to the control panel.
Check both before promising a site count or customer feature.
