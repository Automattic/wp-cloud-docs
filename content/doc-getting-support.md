# Get support from WP Cloud

WP Cloud Support works with WP Cloud host partners, also known as host clients, on onboarding, account and API access, billing, platform behavior, and confirmed platform problems. Host partners support the hosting products and client sites they manage.

## Check service status

Check [Automattic Status](https://automatticstatus.com/) for current WP Cloud API and infrastructure incidents before opening a request. Include the incident name in your request when it matches the problem you see.

If the status page reports the same problem, follow that incident for updates and avoid sending duplicate reports unless your evidence shows a different failure. A normal status page means only that no broad incident is posted. Continue the site or API investigation before concluding that the platform is healthy.

## Include useful evidence

Give the support team enough information to identify the request and reproduce the problem:

- Give the exact timestamp for each issue, or the full time range when it occurred. Always include the time zone; Coordinated Universal Time (UTC) is preferred. For an intermittent issue, include the first and most recent occurrences.
- Describe what happened, what you expected, and the customer or operational effect.
- Explain what the issue prevents you or your customer from doing.
- List the exact steps needed to reproduce it.
- Provide the affected site IDs and domains. Prefer the site ID because it does not change when the primary domain changes.
- Include relevant URLs, HTTP methods, status codes, error messages, request IDs, logs, and Metrics results.
- Describe the troubleshooting already completed and the result of each check.
- Attach a screenshot when it shows an important interface state or error that text does not capture.
- Provide a non-production example site when the issue is complex and can be reproduced safely there.

For a domain or network problem, check DNS propagation and include relevant `curl`, `ping`, or `traceroute` results. Remove credentials, API keys, customer data, and other secrets from every attachment and code sample.

## Support scope

WP Cloud provides platform support to host partners, not direct support to their customers. Host partners are expected to have moderate to advanced technical capabilities and to identify and resolve issues with the client sites they manage.

### What WP Cloud Support covers

WP Cloud Support can help with:

- partner onboarding and WP Cloud integration questions;
- partner account, billing, and API-access problems;
- billing, account, or reporting data that appears incorrect;
- platform operations and behavior that differs from the public documentation;
- suspected WP Cloud API, infrastructure, or managed-software defects;
- platform incidents affecting partner sites;
- policy, compliance, and documentation questions, including gaps or unclear instructions; and
- high-level WordPress questions when they help distinguish a platform problem from a site-specific problem;
- sales and marketing questions related to the WP Cloud partnership.

Some account and site operations require identity or access verification. WP Cloud shares information only with authorized partner contacts and does not disclose information about another partner or its sites.

### What host partners support

Host partners support the hosting products they provide to customers. This includes general customer support and site-specific work that is not caused by the WP Cloud platform.

Examples outside the scope of WP Cloud Support include:

- customer domain and Domain Name System (DNS) problems unrelated to WP Cloud;
- general WordPress use, site design, and development;
- plugin and theme conflicts unrelated to WP Cloud-managed software or platform configuration;
- site code, database, and performance optimization;
- manual site migrations;
- in-depth remediation of compromised sites;
- partner dashboards, custom integrations, and automation; and
- customer communication, billing, and account support.

WP Cloud may help a host partner use platform tools, documentation, logs, or Metrics to determine whether a problem involves the platform. Host partners remain responsible for maintaining, debugging, and optimizing their sites and custom code.

## Report a security vulnerability

Do not send exploit payloads, credentials, or sensitive reproduction data through a normal support request. Report a suspected vulnerability in an Automattic service through [Automattic's HackerOne program](https://hackerone.com/automattic) and select the WP Cloud scope. Follow the program instructions for securely providing technical details.

## Send a support request

Submit WP Cloud questions and platform issues through the [Partner Portal support form](https://hosts.automattic.com/wpcloud/support-request). Continue using another contact method only when a WP Cloud representative has arranged it with your team.

WP Cloud monitors incoming support messages around the clock. General requests normally receive a response within 24 hours. Reports of broad platform failures and emergency API-key problems receive urgent review.
