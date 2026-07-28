# EasyEngine integration

[EasyEngine](https://easyengine.io/features/wpcloud-sites/) is an optional
third-party dashboard that connects to a host partner's WP Cloud account with
its own API key. The integration can create and manage WP Cloud sites while
EasyEngine supplies the dashboard, team access, and customer-facing workflow.
WP Cloud continues to operate and bill for the hosting infrastructure.

EasyEngine is not required to use WP Cloud. A partner can build its own panel,
use another integration, or manage the platform directly through the API and
Partner Portal.

## How the integration works

EasyEngine uses a bring-your-own-key connection. The host client owns the WP
Cloud account and supplies a restricted API key to EasyEngine. Actions taken in
the dashboard are sent to WP Cloud under that client's identity and limits.
There is no transfer of site ownership to EasyEngine.

The two products remain separate services. WP Cloud operates the WordPress
runtime, network, caching, backups, and platform APIs. EasyEngine operates its
dashboard, team roles, automation, plans, and any billing or customer workflow
built around those APIs.

## What the integration provides

Current EasyEngine features include site provisioning, domains, resource and
PHP settings, Edge Cache, backups, logs, site access, activity history, and
performance views. EasyEngine also supports role-based team access and can
manage sites from more than one hosting provider.

The exact dashboard features and plans are controlled by EasyEngine and can
change separately from WP Cloud. Review the [EasyEngine WP Cloud feature
page](https://easyengine.io/features/wpcloud-sites/) and [EasyEngine
documentation](https://easyengine.io/docs/) for the current interface.

EasyEngine can organize sites across projects and hosting providers, expose
common site actions without requiring command-line access, and provide
role-based access for a partner's team. Its current roles and permissions must
be checked in EasyEngine before the partner relies on them for production
separation; they are not WP Cloud API roles.

## Who should use EasyEngine

The integration can suit agencies, freelancers, and hosting teams that want a
ready-made management interface instead of building a panel directly against
the WP Cloud API. It can also be useful for a team that manages WP Cloud sites
alongside sites on other providers.

A partner with an established customer portal or specialized provisioning
workflow may prefer a direct API integration. Evaluate which system owns site
inventory, customer access, plan configuration, and billing before connecting
production sites so the same action is not managed in conflicting places.

## Connect a WP Cloud account

1. Create a dedicated key in [Manage and secure API
   keys](/docs/api-automation/api-access/). Use a descriptive name and restrict
   its endpoints to the operations EasyEngine needs.
2. Add the EasyEngine service's static egress address to the key's allowed IP
   ranges. Changes to a key can affect every application using it, so do not
   reuse a production automation key.
3. In EasyEngine, open its WP Cloud integration settings, enter the WP Cloud
   client identifier and API key, and test the connection.
4. Create a test site before connecting customer workflows. Choose its domain,
   data center, storage, PHP version, memory, and worker configuration.
5. Confirm the new Atomic Site ID and settings in the [Partner
   Portal](https://hosts.automattic.com/wpcloud) as well as EasyEngine.

The API key gives EasyEngine the ability to act on the host client's WP Cloud
sites within its allowed endpoints. Store it as a secret, limit who can see or
replace it, and revoke it when the integration is no longer used. Existing WP
Cloud sites remain on WP Cloud if the key is disconnected, but EasyEngine can
no longer manage them through that connection.

## Create and manage sites

Inside EasyEngine, choose **Add New Site**, select WP Cloud, and enter the
domain and requested site configuration. EasyEngine sends the provisioning
request to WP Cloud and presents the resulting site in its dashboard. WP Cloud
provides the WordPress runtime, TLS, cache, backups, and platform security;
EasyEngine provides its interface and automation around those APIs.

Use [site meta](/docs/sites/site-meta/) and [WP Cloud
billing](/docs/partner-resources/wp-cloud-billing/) as the authority for
resource and billing behavior even when the values are selected in EasyEngine.
Use [Staging sites](/docs/sites/staging-sites/) for the one-non-billable-staging-site
rule.

EasyEngine and WP Cloud bill separately. WP Cloud invoices the host client for
WP Cloud sites and their configured resources. EasyEngine controls and bills
for its own dashboard plan. Ending or changing an EasyEngine plan does not
cancel a WP Cloud site or change its WP Cloud billing state.

Existing sites can be managed from another authorized integration after the
EasyEngine key is removed. Before disconnecting it, make sure the partner has a
current inventory of Atomic Site IDs and another way to perform the site
actions its support team needs.

If a request fails, read the API response in EasyEngine's logs. Confirm that
the API key is active, its IP range and endpoint scope allow the request, the
host account has capacity, the domain is not assigned elsewhere, and the PHP
version is supported. For a dashboard, billing-plan, or EasyEngine workflow
problem, use EasyEngine's support and documentation. WP Cloud documentation
controls the underlying platform behavior.

When the connection test succeeds, create one test site and confirm that its
Atomic Site ID, domain, resources, and status agree in EasyEngine and the
Partner Portal. This result shows that authentication and provisioning work;
it does not by itself test every backup, access, or lifecycle operation the
partner plans to expose.
