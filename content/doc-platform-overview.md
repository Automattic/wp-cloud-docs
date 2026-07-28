# WP Cloud platform overview

The WP Cloud hosting platform was built from the ground up to serve Automattic's most demanding customers. The goal was to build a secure, performant, and flexible multi-tenant WordPress hosting platform without giving up SFTP, SSH, phpMyAdmin, or the ability to install the plugins and themes that customers expect.

Automattic built WP Cloud from what it learned running hundreds of millions of sites on WordPress.com, some of the world's highest-traffic WordPress sites through WordPress VIP, and performance-focused, full-service hosting through Pressable.

Partners keep control of their product, customer experience, pricing, and support. WP Cloud runs the hosting platform beneath that product.

## How WP Cloud hosts sites

WP Cloud runs WordPress sites on a multi-tenant platform. Linux kernel namespaces, control groups, and a site filesystem environment isolate site processes and resources. WP Cloud does not host sites in Docker containers or provision a virtual private server for each site. It does use Docker containers for specific features, including [SSH access](/docs/site-access/ssh-sftp/), to limit the effects of malicious actions and mistakes.

A custom scheduler limits the effect of unusually high resource use by one site while allowing a site to use available capacity when the pool can support it.

Each site belongs to a server pool with primary and secondary copies in different geographic locations. The two copies run the same managed software and continuously replicate site data. If the primary server or its data center becomes unavailable, WP Cloud can [fail over to the secondary copy](/docs/infrastructure/automated-failover/).

WP Cloud engineers can relocate a site between server pools without downtime. A move may place the site on a different server, in a different data center, or in a different country. WP Cloud uses these moves to replace hardware, balance resource use across pools, and improve performance for one site or a group of sites. Partners should not treat a specific origin server or data center as a permanent property of a site.

## How requests reach a site

Requests first enter WP Cloud through its edge network. When [Edge Cache](/docs/performance/cache/edge-cache/) has a usable response, an edge server can return it without contacting the site's origin server. Other requests continue to an origin data center and then to the site's primary server.

Traffic remains encrypted with Transport Layer Security between the edge network and the site. WP Cloud's origin routing also supports automated failover when the primary copy cannot serve traffic.

WP Cloud origin servers are self-sufficient. Everything needed to serve a site assigned to the server runs there, including [NGINX](/docs/infrastructure/server-specs-settings/), PHP, the site's document root and files, MariaDB, the site's database, and [Memcached](/docs/performance/cache/). Keeping these services together avoids adding a remote service call to every uncached WordPress request.

## Managed cache layers

WP Cloud sites use several cache layers:

- [Edge Cache](/docs/performance/cache/edge-cache/) stores eligible responses near visitors when the feature is enabled.
- [Page Cache](/docs/performance/cache/page-cache/) stores complete WordPress responses at the origin.
- [Object Cache](/docs/performance/cache/object-cache/) keeps WordPress objects and query results in persistent Memcached storage.
- PHP OPcache stores compiled PHP bytecode.

Each layer caches different data and has different bypass and purge behavior. A site can use Page Cache and Object Cache even when Edge Cache is disabled.

## Performance and traffic capacity

The isolation model, custom scheduler, self-sufficient origin servers, and cache layers are designed to support thousands of active users on a site, absorb large traffic bursts, and run demanding ecommerce sites.

Every WP Cloud-powered host that entered the independent 2026 WP Hosting Benchmarks earned Top Tier recognition across the tiers tested. The benchmark covered load testing, uptime, global page speed, and WordPress performance. Review the [2026 WordPress hosting benchmark results](https://wp.cloud/2026-wordpress-hosting-benchmarks/) for measurements and methodology.

## Managed WordPress software

WP Cloud maintains WordPress core and selected platform software as read-only, shared files. Shared software makes it possible to deploy platform-managed updates consistently and improves OPcache use across sites.

Partners can still install and manage ordinary plugins and themes. Read-only managed files must be changed through the supported software controls instead of editing their symlinked copies on a site.

WP Cloud also supplies WP-CLI, SFTP, SSH, phpMyAdmin, backups, and several supported PHP and WordPress release tracks. Availability and management details belong to the focused article for each feature because versions and controls change independently.

## How partners manage WP Cloud

Partners manage sites through the [WP Cloud API reference](https://wp.cloud/docs/api/). The API includes operations for:

- creating, cloning, inspecting, and deleting sites;
- managing domains, PHP and WordPress versions, software, access, and site settings;
- retrieving backup information and requesting platform operations;
- managing SSH and SFTP users and generating phpMyAdmin access URLs.

The [WP Cloud Partner Portal](/docs/getting-started/partner-portal/) provides account and site information alongside support and API-access resources. A partner may call the API from its own control panel or use a supported integration.

## Responsibilities

WP Cloud operates the hosting platform and its managed features. Partners operate the hosting product they provide to customers. This normally includes the partner's dashboard, plans, billing, customer support, site configuration, and any software the partner or customer installs.

Partner-owned code and custom workflows can change how a site behaves. WP Cloud documentation describes the platform's standard behavior, not custom software deployed by an individual partner.
