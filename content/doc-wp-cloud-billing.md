# WP Cloud billing

WP Cloud bills the host partner for the resources assigned to its sites. The
partner decides how to package and price those resources for end users. Before
launching billable sites, add a valid payment method in the [Partner
Portal](https://hosts.automattic.com/wpcloud).

## Monthly billing

At the end of each month, WP Cloud records the partner's billable sites and
their assigned resources. The payment method is charged at the beginning of
the following month. Billing is based on allocated resources, not the fraction
of those resources a site happened to consume during the period.

WP Cloud does not add page-view or visitor overage charges. Host partners can
still define their own product limits, plans, and overage policies.

For example, a customer can move to a larger partner plan without replacing
its Atomic Site ID. The partner updates that site's allowed resource values and
its own billing record in place.

## Keep billing data accurate

Review the Partner Portal inventory regularly and make sure each site has the
intended resource configuration. [Site meta](/docs/sites/site-meta/) controls
billable storage, PHP resources, memory, and site type.

WP Cloud permits one non-billable staging site per billable site. A site with
no site-type value is billable by default, and additional staging sites can be
billed when staging sites outnumber billable sites. See [Staging
sites](/docs/sites/staging-sites/) for the complete rules.

When a customer changes plans, update the existing site's resource values. A
site does not need to be reprovisioned. Storage cannot be reduced below the
space already in use, and resource values must remain within the current
limits documented in [Configure resources, site type, and billing with site
meta](/docs/sites/site-meta/).

## Payment problems

If a partner's credit card is declined and payment remains overdue, WP Cloud
applies progressive restrictions:

| Payment status | Account effect |
| --- | --- |
| 30 days late | Site configuration changes are restricted, and new site creation is suspended. |
| 60 days late | All sites are temporarily suspended. |
| 90 days late | Complete account deletion. |

The governing partner agreement and current billing notices provide the
current payment terms and restriction dates. Regular billing verification
helps maintain uninterrupted service and prevents unexpected charges. Keep the
payment method and billing contacts current, and address a failed charge
promptly.

Use the Partner Portal Billing section to review invoices and payment details.
If a billing status or notice does not match the account, submit a request from
the portal before the next restriction date.
