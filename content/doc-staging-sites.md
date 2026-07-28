# Staging sites

A staging site is a separate, non-production WP Cloud site that a partner's customer or end user can use to build a new site, test changes, or prepare updates before releasing them. The host partner provides the staging experience and its controls through its own hosting product.

The WP Cloud platform does not differentiate between production and staging sites at the infrastructure level. Both have the same platform capabilities and configuration options. The `staging` site type identifies a site's billing and inventory status; it does not create a different kind of WP Cloud site.

## Billing and eligibility

A partner may provide one non-billable staging site for each billable site. Additional staging sites are billable. A staging site must not be used as a customer's production site.

Classify an eligible staging site with the `staging` site type in `_data`. The [site-meta article](/docs/sites/site-meta/#set-the-site-type-and-billing-classification) explains the required JSON and billing behavior.

## Provide a staging site

A partner can provide a new site for early site creation and testing or create a staging copy of an existing production site. A common cloning workflow is:

1. [Clone the production site](/docs/sites/cloning/) with the Create Site operation's `clone_from` field.
2. Wait for the provisioning job to report `success`.
3. Set the destination site's `_data` value to `site_type: staging`.
4. Record the production and staging relationship in your hosting product.
5. Apply any staging-specific domain, access, email, indexing, or integration controls owned by your product.

The `staging` site type is a billing and inventory classification. It does not suspend the site or change how WordPress identifies its environment. Configure those behaviors separately when your staging product requires them.

Before making the staging site available, confirm that it loads at its staging domain, its `_data` value contains `site_type: staging`, and the partner's inventory associates it with the intended billable site. Test any customer-facing staging controls supplied by the partner's hosting product.

## Offer an optional staging-to-production workflow

Because production and staging sites have the same WP Cloud capabilities, promotion is a partner-owned workflow. A partner's hosting product might offer an option that replaces the existing production site with the prepared staging site.

That workflow can include:

- moving the primary and alias domains from the existing production site to the prepared staging site using the [domain operations in the WP Cloud API quick start](/docs/api-automation/api-quick-start/#work-with-domains);
- synchronizing site-meta values and other configuration that cloning did not copy or that changed after the staging site was created;
- updating the production and staging relationship in the partner's inventory; and
- updating each site's billing classification so the site serving production traffic is billable and any retained staging site follows the one-per-billable-site rule.

The partner should define how its workflow handles changes made to the production or staging site after the clone. Moving domains does not synchronize later content or configuration changes between the two sites.
