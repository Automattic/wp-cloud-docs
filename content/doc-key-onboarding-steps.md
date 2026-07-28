# Onboard and launch with WP Cloud

New WP Cloud partners can generally launch within one to two months. Most of the work is WP Cloud orientation, choosing and setting up a control panel, building and testing the integration, and preparing the pricing, marketing, and support material for the new hosting product.

## Evaluate WP Cloud

Review the [WP Cloud platform overview](/docs/getting-started/platform-overview/), [case studies](https://wp.cloud/case-studies/), [performance benchmarks](https://wp.cloud/2026-wordpress-hosting-benchmarks/), and [WP Cloud API reference](https://wp.cloud/docs/api/). Compare the platform with the requirements of the hosting product you intend to offer.

## Choose a control panel

Decide how your team will manage sites. You can build your own control panel or integrate a supported third-party panel such as [PanelAlpha](/docs/integrations/panelalpha/) or [EasyEngine](/docs/integrations/easyengine/). The choice affects the API work, customer interface, and operating procedures your team must build.

## Create a partner account

Create or access your account in the [WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud). Complete the account and onboarding items shown there.

Choose portal users carefully. The portal can contain account, site, billing, API-access, and support information.

## Obtain API access

Request the developer and platform credentials your team needs. WP Cloud API keys are restricted to allowed IP addresses, so identify the static office, VPN, bastion, or automation addresses that will make requests.

Use a developer key for individual development and testing. Keep the platform key in your production service rather than distributing it to developers. The [WP Cloud API quick start](/docs/api-automation/api-quick-start/) covers the first test workflow.

## Test the platform

Create test sites and exercise the operations your product will depend on. At minimum, test:

- site creation and job-status handling;
- domain assignment and certificate provisioning;
- site access through SSH, SFTP, and phpMyAdmin;
- backups, restores, software management, and deletion;
- site resource and billing metadata used by your plans.

Use non-production domains and data during integration testing. Record the site ID returned by each create operation because it remains a stable identifier when a site's primary domain changes.

## Review getting support

Review [Get support](/docs/getting-started/get-support/) for general support information and the division of responsibility between WP Cloud and the partner.

Document how your team will provision sites, manage credentials, monitor failures, restore data, and respond to customer issues. Train partner support teams to collect site IDs, timestamps with time zones, URLs, errors, logs, and completed troubleshooting before asking WP Cloud to investigate a platform issue.

## Configure site metadata and billing

Review and configure [site metadata](/docs/sites/site-meta/) before creating production sites. These settings control the resource allocation, site type, and billing information used by the partner's plans.

WP Cloud bills partners automatically. Invoices are available in the billing section of the [WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud). Test the complete provisioning and billing workflow with representative plans instead of relying on platform defaults.

## Develop the go-to-market plan

Develop and implement a go-to-market plan that covers pricing, marketing pages, customer onboarding, migrations, documentation, and the support section for the new product. For examples of how WP Cloud partners present their hosting products, review [WordPress.com](https://wordpress.com/hosting/), [Bluehost Cloud](https://www.bluehost.com/cloud-hosting), [Convesio](https://convesio.com/), and [Ivapix](https://ivapix.com/).

Set prices that cover WP Cloud charges and the cost of operating and supporting the product.

## Complete a launch test

Run the customer journey from purchase through site creation, domain setup, management, support, billing, and cancellation. Verify that your panel handles asynchronous API jobs and failed operations without reporting success too early.

The launch test passes when the product can create and manage a site, record the expected usage in its billing workflow, and give the people supporting customers a repeatable operating procedure. Delete test customer data and any test sites that no longer serve an ongoing integration check.

## Launch and operate the product

After the launch test passes, complete the remaining WP Cloud Partner Portal checklist, launch and promote the product, and support its customers. Continue checking invoices, platform operations, and customer-facing workflows after launch.
