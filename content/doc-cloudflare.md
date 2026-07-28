# Cloudflare and WP Cloud

WP Cloud host partners should advise their end users to avoid proxying WP Cloud
site traffic through Cloudflare unless a required Cloudflare feature depends
on the proxy. Like Cloudflare, WP Cloud operates an Anycast network. WP Cloud
receives inbound traffic and routes requests through regional edge load
balancers and services, protecting the origin server and its IP address.

WP Cloud applies traffic classification, rate limiting, and distributed
denial-of-service (DDoS) mitigation at its edge and load balancers. [Edge
Cache](/docs/performance/cache/edge-cache/) can also serve eligible responses
without sending the request to the origin. An additional Cloudflare proxy is
therefore unnecessary for many WP Cloud sites and can interfere with WP Cloud
caching and traffic protection.

Cloudflare can still provide DNS without proxying site traffic. Host partners
can use the guidance below in their own documentation and support responses.
If an end user's site must use the Cloudflare proxy, review both the proxy and
TLS settings below.

## Avoid Cloudflare proxying when possible

Advise end users to configure the site's A and CNAME records as **DNS only** in
Cloudflare unless a required Cloudflare feature depends on proxied records.
This is commonly called disabling the proxy or orange cloud. Visitors then
connect to WP Cloud's Anycast edge network instead of passing through an
additional proxy.

When Cloudflare proxies a request, WP Cloud receives the connection from
Cloudflare instead of directly from the visitor. This can hide connection
signals that WP Cloud uses to classify requests and apply traffic protection.
If Cloudflare does not stop an attack, the changed request information can
contribute to unexpected rate limiting or increased use of PHP and other site
resources.

Some Cloudflare features require proxied records. If an end user chooses one of
those features, the host partner should treat proxying as an intentional
tradeoff and test the site's cache behavior, legitimate automated clients, and
traffic protections after the change.

## Prevent HTTPS conflicts

When a proxied site has redirect loops or other HTTPS problems, check the
Cloudflare SSL/TLS settings before changing the WP Cloud certificate or domain
configuration.

- Set the Cloudflare SSL/TLS encryption mode to
  [`Full`](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full/).
  Do not use a mode that sends unencrypted HTTP requests from Cloudflare to WP
  Cloud.
- If the site enters a redirect loop, disable [**Always Use
  HTTPS**](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/always-use-https/)
  under **SSL/TLS > Edge Certificates** and let WP Cloud handle the HTTPS
  redirect.
- If Cloudflare rewrites links or resources unexpectedly, disable [**Automatic
  HTTPS
  Rewrites**](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/automatic-https-rewrites/)
  under **SSL/TLS > Edge Certificates**.

Change only the setting related to the observed conflict. Cloudflare changes
can affect customer traffic immediately, so confirm that the primary domain,
aliases, WordPress administration, and important automated requests still load
afterward.

With DNS-only records, visitors connect directly to WP Cloud. When proxying is
required, the expected result is a site that loads over HTTPS without a
redirect loop or rewritten resources. Proxying still changes the connection
information that reaches WP Cloud; these TLS settings do not make proxied
traffic equivalent to a direct connection.
