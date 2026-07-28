# WP Cloud partner tiers and platform options

WP Cloud offers Self-Service and Managed partnership models for host partners.
Both include support for account, billing, documentation, and WP Cloud
platform issues. The models differ in onboarding, day-to-day collaboration,
implementation help, available resources, and eligibility for tailored
platform configuration.

The services and platform options available to a specific partner depend on
its partnership agreement and current account configuration.

## Compare partner tiers

| Area | Self-Service partners | Managed partners |
| --- | --- | --- |
| Support model | Documentation and support requests for WP Cloud platform issues. | A managed relationship that may include a named contact or account manager. |
| Onboarding | Standard onboarding resources and documentation. | Onboarding tailored to the partner's product, configuration, and workflow. |
| Implementation | The partner's team designs, builds, and troubleshoots its integration using WP Cloud documentation and the API reference. | The WP Cloud team may provide hands-on guidance for setup, optimization, and integrations. |
| Communication | Support requests submitted through the WP Cloud Partner Portal. | Communication methods, check-ins, and reviews arranged with the partner team. |
| Platform configuration | Standard platform features and configuration. Custom chroots are not available. | Approved account-level platform options and configuration based on the partnership agreement. Custom chroots are available only to Managed partners and require WP Cloud configuration. |

Managed services are not identical for every partner. The partner's agreement
and account configuration determine its contacts, communication methods,
platform options, and other services.

## Understand platform configuration availability

Self-Service partners use WP Cloud's standard platform configuration. They can
deploy their own software through SSH automation or install supported packages
on individual sites with the [Manage Site Software
endpoint](https://wp.cloud/docs/api/#tag/sites/POST/site-manage-software/{type}/{site}).

Custom chroots for managed software are available only to Managed partners.
They support client-level managed plugins, themes, mu-plugins, executable
tools, and external repositories across sites. A Managed partnership does not
automatically include a custom chroot; WP Cloud must approve and configure it
for the client account. [Symlinks and managed
software](/docs/wordpress/software-versions/managed-software/) explains the
chroot, repository, deployment, and rollback model.

Other account-level options have their own eligibility and configuration
requirements. [Advanced Cron
scheduling](/docs/wordpress/cron-scheduling/) is reserved for approved Managed
partners. Partners can discuss different [on-demand backup
limits](/docs/backups-restores/on-demand-backups/) with WP Cloud, but should not
assume that every account-configured option requires a Managed partnership.

## Support available to every partner

WP Cloud Support helps both Self-Service and Managed partners with:

- partner account access and permissions;
- billing, invoices, payments, and reporting discrepancies;
- suspected WP Cloud platform incidents, bugs, and behavior that differs from
  the public documentation;
- compliance, policy, and data-handling questions;
- missing, incorrect, or unclear documentation; and
- WP Cloud questions or problems that are not covered by the available
  resources.

WP Cloud supports the platform, while host partners support their hosting
products, customers, sites, custom code, and integrations. [Get
support](/docs/getting-started/get-support/) explains the complete scope
and the information to include with a support request.

## Use Self-Service resources

Self-Service partners use the same public platform information and account
tools available throughout the partner lifecycle:

- Use the [WP Cloud platform
  overview](/docs/getting-started/platform-overview/) and the rest of the WP
  Cloud documentation for platform behavior, recommended workflows, and
  troubleshooting.
- Use the [WP Cloud API reference](https://wp.cloud/docs/api/) for endpoint
  methods, fields, and response schemas.
- Use the [WP Cloud Partner
  Portal](/docs/getting-started/partner-portal/) for account information,
  Inventory, Insights, API keys, billing, team management, accepted documents,
  and support requests, subject to the user's access.
- Use the [PanelAlpha integration](/docs/integrations/panelalpha/) or
  [EasyEngine integration](/docs/integrations/easyengine/) documentation when
  the partner's hosting product uses one of those control panels.

If the documentation does not answer a platform question, or a documented
feature does not behave as described, submit a support request through the WP
Cloud Partner Portal.

## Managed partner services

A Managed partnership may add services such as:

- a named contact or account manager;
- onboarding tailored to the partner's hosting product;
- hands-on guidance for setup, optimization, and integrations;
- regular check-ins or strategic reviews;
- communication methods arranged with the partner team; and
- approved platform options or configuration for the partner's needs.

## Discuss a Managed partnership

A Self-Service partner that needs a custom chroot, recurring hands-on
onboarding, integration guidance, or other tailored platform configuration can
ask WP Cloud about a Managed partnership. Eligibility, commercial terms,
platform options, and included services are determined for the specific
partnership.

Open the [WP Cloud Partner Portal](/docs/getting-started/partner-portal/) and
select **Support request**. Do not send account or commercial details through
a public documentation comment.
