# WP Cloud documentation terminology

Created: 2026-07-15
Updated: 2026-07-28

Use this glossary when writing or reviewing WP Cloud documentation. Write to publishable standards. When current product behavior or an approved interface conflicts with this file, verify the behavior and update this file before applying the new term across articles.

## Terminology and ownership

Throughout WP Cloud documentation, `WP Cloud partner`, `partner`, `host partner`, `client`, `client host`, `host client`, `partner client`, and `partner host` refer to the same organization: a hosting provider that uses WP Cloud. As a host provider using WP Cloud, you are both a WP Cloud partner and a client host. Managed partners and self-serve hosts remain partners and client hosts; those labels describe a service or account model, not a different place in the ownership model.

Prefer `WP Cloud partner` or `partner` in general prose. Use another partner, client, or host variant when it matches an API field, account boundary, feature, interface, or source term, or when it helps readers recognize terminology they encounter elsewhere. When an article uses more than one variant, establish their equivalence on the first useful mention. Do not alternate among the terms merely for variety. Within WP Cloud documentation, `client` means the partner organization, not its downstream customer. Qualify bare `client` when it could mean an HTTP or API client.

WP Cloud is a cloud infrastructure platform specialized in WordPress hosting. It provides WordPress-as-a-Service and is designed for client-host-level operations. The WP Cloud API operates at client-account scope: subject to the endpoint and network restrictions configured for an API key, the key can operate on sites in its client account. WP Cloud models sites and the partner or client host whose account contains them. It does not model the partner's end customers.

End customers are not represented in the WP Cloud API and do not have direct access to it. An end customer may initiate an action through a partner-owned panel or workflow, but the partner's system makes the WP Cloud API request. Customer identity, customer-to-site ownership mapping, downstream access control, and downstream billing belong to the partner and are handled through the partner's systems, panels, and workflows.

## Product and audience names

| Use | Meaning and guidance | Avoid |
| --- | --- | --- |
| **WP Cloud** | Automattic's cloud infrastructure platform specialized in WordPress hosting. It provides WordPress-as-a-Service for partners or client hosts. Use on first mention and throughout public documentation. | `WPCloud`, `WP cloud`, or bare `Cloud`. |
| **WP Cloud platform** | Use when distinguishing the platform from a partner's hosting product, dashboard, customer relationship, or support process. | `Atomic` as a public synonym for the platform. |
| **WP Cloud API** | Preferred public prose name for the API. `WP Cloud API`, `WP Cloud Atomic API`, and `Atomic API` refer to the same API. Link endpoint details to the generated WP Cloud API reference. | Treating these names as separate interfaces, account scopes, or authentication systems. |
| **WP Cloud Atomic API** or **Atomic API** | Alternate names for the WP Cloud API. Use when defining the equivalence, matching a current interface, or helping readers recognize the name. Prefer `WP Cloud API` in general prose. | Using `Atomic` alone as a synonym for the WP Cloud platform. |
| **WP Cloud API reference** | The generated endpoint reference at `wp.cloud/docs/api/`. | `API docs` when the distinction from contextual documentation matters. |
| **WP Cloud documentation** | Contextual product documentation maintained as Markdown in this repository and, when published, at `wp.cloud/docs`. | `Field Guide` for the maintained documentation set. |
| **WP Cloud partner**, **partner**, or **host partner** | The preferred general-prose names for the organization that uses WP Cloud to provide a hosting product. It is the same actor as the client or client host. | Treating a partner and client host as separate organizations. |
| **client**, **client host**, **host client**, **partner client**, or **partner host** | Equivalent names for the WP Cloud partner. Use the variant shown by the API, account boundary, feature, interface, or relevant source. Qualify `client` when software could be the intended meaning. | Treating a variant as a separate role or using bare `client` when it could mean an HTTP or API client. |
| **managed partner** or **self-serve host** | A WP Cloud partner or client host under a particular service or account model. Use the exact current model name only when the distinction affects access, support, billing, or available features. | Treating these as different actors in the account and customer ownership model. |
| **partner developer**, **partner engineer**, **partner support team** | Roles within the partner or client-host organization. Use when access, responsibility, or prerequisites differ by role. | Separate documentation trees by role unless the workflow truly differs. |
| **end customer** or **customer** | The partner's downstream hosting customer. Use `end customer` when contrasting the customer with the partner or WP Cloud; use `customer` after the relationship is clear. The customer has no WP Cloud API identity or direct API access. | `WP Cloud customer` when the person or organization is actually the partner's customer, or implying that WP Cloud manages the customer relationship. |
| **end user** | A person who uses the partner's hosting product or a WP Cloud site. An end user may be the partner's customer, that customer's user, a student, a staff member, or another downstream user. Use `the partner's end user` when `customer` would be too narrow. | Bare `user` when the role changes responsibility or the recommended action. |
| **site owner** | Use only when downstream or business ownership of a WordPress site is relevant. WP Cloud's platform-level association is between the site and the partner's client account; the partner maintains any customer-to-site ownership mapping. | Using `site owner` as if it were a WP Cloud API identity, or using `user` as a catch-all for every participant. |
| **WP Cloud Support** | The platform support function or escalation destination confirmed by current public guidance. It works with the partner or client host, not directly with the partner's end customers. | Internal channel names or team aliases. |

## WordPress product boundaries

| Term | Guidance |
| --- | --- |
| **WordPress** | The open source software or behavior shared across WordPress installations. Do not use `WordPress.org` as a synonym for the software. |
| **WordPress user** or **WordPress account** | An application account stored in a WordPress installation. `Local WordPress user account` and `local user` are alternate names when distinguishing it from a platform, hosting, SSH, or partner customer account. Do not imply that a WordPress user is a WP Cloud API identity. |
| **WordPress.org** | The website and services at `wordpress.org`. Use only when referring to that site, its directories, or its community resources. |
| **WordPress.com** | Automattic's WordPress hosting product. It is one product that can run on WP Cloud. Do not transfer its plans, dashboards, support paths, or custom behavior into generic WP Cloud documentation. |
| **WordPress.com on WP Cloud** | Use only when an article explicitly discusses that client implementation. Do not use internal abbreviations in public WP Cloud docs. |
| **Automattic** | The company. Spell it with two t's after the `ma`. Do not use `A8C` or `a8c` in public prose. |

## Platform and site terms

| Use | Guidance | Avoid or qualify |
| --- | --- | --- |
| **site** | A WordPress site hosted on WP Cloud. | `blog` unless the subject is specifically a blog. |
| **Atomic Site ID** | The persistent identifier assigned to a WP Cloud site. It does not change when the site's domains change. Track it throughout the site lifecycle and use it for operations where a domain could be reassigned, including deletion. | Treating a domain as the site's permanent identifier. |
| **staging site** | A non-production site used to test changes. State whether a workflow creates a separate site or changes an existing site's state. | `staging environment` when the API and UI call it a site. |
| **production site** | A site serving live traffic. Use only when the distinction matters. | `live site` if the source or interface uses `production site`. |
| **environment** | A broader runtime or client-host environment. Define which environment the article means. | Using it as a loose synonym for site. |
| **partner dashboard** or **client-host dashboard** | A dashboard owned or supplied by the partner. Name the product if the workflow depends on a specific dashboard. | Inventing WP Cloud UI labels for partner-owned interfaces. |
| **WP Cloud Partner Portal** | The current authenticated account area for WP Cloud partners and client hosts at `https://hosts.automattic.com/wpcloud`. This is a fixed product name; use the full name on first mention. | `Partner Portal` without context on first mention, or renaming it to match another equivalent audience term. |
| **origin server** | The server that runs WordPress and produces uncached responses. Define on first use in general-audience articles. | Assuming readers know how origin differs from edge. |
| **edge server** | A server in the edge network that handles traffic near the requester. Define on first use when relevant. | `CDN server` when the distinction matters. |
| **Automated failover** | The WP Cloud platform capability that redirects traffic between synchronized primary and secondary origin servers. Use this name for the feature and canonical article. | `Automatic Failover` or `automatic failover` as the feature name. |
| **chroot** | A site filesystem environment. Use only when the concept is required and explain the practical boundary. | Treating internal directory layouts as a stable public contract. |

## Cache and performance terms

| Use | Meaning |
| --- | --- |
| **cache** | Stored data or output reused to avoid repeated work. Name the cache layer instead of using `cache` alone when behavior differs by layer. |
| **Edge Cache** | WP Cloud's cache at the network edge. Capitalize when naming the platform feature or canonical article. |
| **Page Cache** | Full-page response caching on the WordPress origin. Capitalize when naming the platform feature or canonical article. Introduce Batcache only where implementation details matter. |
| **Object Cache** | Persistent caching for WordPress objects and query results. Capitalize when naming the platform feature or canonical article. |
| **cache purge** | Removal or invalidation of cached content. Use the verb shown by the API or interface, such as `purge` or `clear`, and do not swap them casually. |
| **cache bypass** | A request or configuration that prevents use of a cache layer. State which layer and whether the bypass is temporary or configured. |
| **autoloaded options** | WordPress options loaded on most requests. Use lowercase in prose unless it starts a title. |

## Metrics and operational interfaces

| Use | Guidance | Avoid |
| --- | --- | --- |
| **Metrics** | WP Cloud time-series telemetry. Link contextual guidance to the Metrics article and endpoint fields to the generated WP Cloud API reference. | Treating origin web server logs as the source for requests served entirely at the edge. |
| **Insights** | The current WP Cloud Partner Portal section for account-wide and site-specific metrics and statistics. Name the specific chart, site, or task when possible. | Calling this section `WP Cloud Insights`, or linking to the former WP Cloud Insights article, interface, or URL. |
| **Time Series Metrics endpoint** | The current API operation under `/metrics/{type}/{key}`. | The deprecated Site Metrics endpoint under `/site-metrics/{site}`. |

## Security and access terms

| Use | Guidance |
| --- | --- |
| **Defensive Mode** | The current feature name used for challenge-based traffic protection. Verify activation, status, and scope claims before publication. |
| **distributed denial-of-service**, then **DDoS** | Expand on first use in mixed-audience content. `DDoS` is acceptable without expansion in narrow technical references. |
| **rate limit** | A boundary on requests or operations over time. State the actor, resource, interval, and response when verified. |
| **web application firewall**, then **WAF** | Expand on first use unless the article defines the term in its title. |
| **SSH** | Secure Shell access. State whether the article means client-host-level or site-user access. Partner-level and client-level describe the same account-side actor. |
| **SFTP** | SSH File Transfer Protocol. Do not call it FTP. |
| **Client SSH** | The official WP Cloud feature name for client-host-level shell and SFTP access used by partner developers, engineers, support teams, panels, and automation. Introduce the account-wide credential boundary before using `partner-level access` or `client-level access` as a shorter explanation. |
| **User SSH and SFTP access** | Site-scoped access created by a partner or client host for its customer, developer, or support staff. Use `site user` after the full name is clear. Do not call this Client SSH. |
| **WP-CLI** | The WordPress command-line interface. Keep the hyphen and capitalization. |
| **API key** | A credential scoped to one WP Cloud client account and used by the partner's integrations to authenticate API requests. Subject to the key's endpoint and network restrictions, it can operate on sites in that account. It does not represent an end customer. Never include a real value. |
| **credential** | A secret or identity material such as an API key, password, or private key. Do not publish real credentials, hashes, or credential-shaped values from source material. |
| **allowlist** and **blocklist** | Preferred terms for explicitly permitted or denied values. Use a current interface label verbatim when it differs. |

## API and operation terms

| Use | Guidance |
| --- | --- |
| **endpoint** | A specific API method and path. Link definitions, fields, and response schemas to the generated reference. |
| **API integration** or **requesting application** | Software that calls the WP Cloud API for the partner. Prefer one of these when `API client` could be confused with the partner or client host. |
| **request** and **response** | Identify the method, path, content type, authentication, and relevant fields in tested examples. |
| **job** | An asynchronous unit of work returned by the API. Do not imply the requested operation has finished when the API has only accepted a job. |
| **webhook** | An event notification sent to a configured destination. Name the event and delivery expectation when known. |
| **payload** | Request or response body data. Prefer `request body` or `response body` when that is clearer. |
| **fleet operation** | An action applied across several sites. Use only when the operation is truly multi-site. |
| **bulk operation** | The current taxonomy label. Do not replace it with `fleet operation` across navigation until the taxonomy decision is approved. |

## Mechanics

- Use American English.
- Use the serial comma.
- Use sentence case for titles and headings.
- Spell out zero through nine. Use numerals for 10 and above, except for commands, code, versions, status codes, measurements, and interface values.
- Put a space between a number and a unit, such as `50 GB`.
- Use `log in` and `set up` as verbs. Use `login` and `setup` as nouns or adjectives.
- Define an acronym on first use unless the article title defines it or the intended reader can reasonably be expected to know it.
- Preserve exact capitalization and punctuation in code, commands, API fields, response values, filenames, and UI labels.

## Phrases to rewrite

| Avoid | Prefer |
| --- | --- |
| `in order to` | `to` |
| `utilize` or `leverage` | `use` |
| `at this time` | `now`, or remove the phrase |
| `you are able to` | `you can` |
| `allows you to` | Make the reader the subject and name the action. |
| `simple`, `easy`, `just`, `obviously` | State the action or requirement without judging its difficulty. |
| `powerful`, `robust`, `seamless`, `best-in-class` | Name the behavior, limit, or measured result. |
| `new`, `recently`, `now available` | Give a version, release date, or current behavior when time matters. |
| `click here`, `learn more`, `read this` | Name the destination or task in the link text. |
| `support path`, `authorized path`, or `escalation path` | Name the support destination or access rule and link its canonical article. |
| `resource pressure` or `reduce pressure` | Name the measured resource and the change, such as reducing PHP connection use or uncached requests. |

## Internal terms and source residue

Do not publish the following unless the article explicitly explains a public, verified term:

- Internal team, P2, Slack, project, or channel names.
- Internal hostnames, dashboards, tooling paths, or private repository links.
- `Atomic` as an unexplained synonym for WP Cloud.
- Internal abbreviations for WordPress.com client implementations.
- Partner- or client-specific customizations presented as platform defaults.
- Prerelease code names or unsupported roadmap claims.

When source text contains one of these terms, flag it for owner review. Do not silently replace it with a plausible public term.
