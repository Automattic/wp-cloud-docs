# Troubleshoot site performance

WP Cloud provides a highly performant, scalable, and resilient hosting
platform. Built-in features include [Page Cache](/docs/performance/cache/page-cache/),
[Edge Cache](/docs/performance/cache/edge-cache/), persistent [Object
Cache](/docs/performance/cache/object-cache/), [separate handling for static
files](/docs/performance/lightweight-404s-static-files/), [dynamic image
resizing and transformation](/docs/performance/image-optimization/image-transformation/),
[image subsize offloading](/docs/performance/image-optimization/offload-image-sub-sizes/),
automatic scaling of PHP workers, and more. Together, these features help
WordPress sites remain fast and scale as traffic changes.

A site's code and functionality can still limit performance. Slow database queries, inefficient plugin or theme code, external requests, and uncached traffic can increase response times and use available PHP or database capacity. Investigating and fixing these performance issues helps the site make the most of WP Cloud's reliability and performance capabilities.

Use WP Cloud Metrics, origin logs, [application performance monitoring (APM)](/docs/monitoring-logs/apm/), WordPress debugging tools, and WP-CLI profiling to investigate a performance issue. Start with two questions: how much eligible traffic is served from Page Cache or Edge Cache, and how long uncached origin requests take to finish.

A site can appear fast during normal traffic while one slow uncached request leaves less capacity for traffic increases. Review performance after significant code or plugin changes and before a planned traffic event, not only after visitors report a problem.

If visitors receive HTTP 429 responses or the logs contain 599 records, use [Troubleshoot HTTP 429 and 599 errors](/docs/troubleshooting/429-599-errors/) for the status-code-specific diagnosis. The steps below apply to slow or resource-heavy requests with or without those status codes.

## Define the slow request

Record the affected site, URL or WordPress action, time and time zone, user state, and the behavior the customer observed. Note whether the request is consistently slow or only slows during traffic increases.

Common sources of high PHP or database use include:

- excessive uncached requests;
- slow database queries or PHP functions;
- slow external HTTP requests;
- frequent `admin-ajax.php` or WooCommerce `wc-ajax` requests;
- plugins or custom code that keep PHP workers occupied;
- full WordPress loads for missing static files; and
- repeated cache purges or code that prevents responses from being cached.

Use a short, known time range instead of starting with an account-wide search. A narrow window makes it possible to compare Metrics, logs, and an APM trace without mixing unrelated traffic.

## Check Insights and Metrics

The [Insights section in the WP Cloud Partner Portal](https://hosts.automattic.com/wpcloud) provides account-wide and site-specific metrics and statistics. For the same time range, compare request volume, response time, and Edge Cache hits and misses. Then check whether PHP or MySQL use changed with them.

Use the [Time Series Metrics endpoint](https://wp.cloud/docs/api/#tag/metrics/POST/metrics/{type}/{key}[/summarize]) when you need exact values or dimensions for a dashboard or investigation. Useful measurements include:

- `requests` and `response_time_average` for request volume and response time;
- `php_cpu_time`, `php_response_time`, and `php_workers_max` for PHP work;
- `php_request_burst_percentage`, `php_request_limited_percentage`, and `php_request_normal_percentage` for PHP connection behavior;
- `mysql_cpu_time`, connection, row, and command metrics for database activity; and
- `edge_cache_hit_percentage` and `edge_cache_miss_percentage` for edge caching.

Use dimensions such as `path`, `http_status`, `page_renderer`, `page_is_cached`, `wp_admin_ajax_action`, `http_user_agent`, `visitor_is_crawler`, `is_rate_limited`, and `rate_limit_reason` to narrow the measurement. Metrics served from the edge are not fully represented in origin web server logs.

Account-wide averages can hide one slow site or path. Narrow the results by site and request dimensions before deciding that a change in the overall average explains the reported problem.

## Compare web and error logs

[Web server logs](/docs/monitoring-logs/logs/web-server-logs/) identify the origin requests made during the affected period. Compare request URLs, methods, statuses, renderers, cache state, request times, user agents, and visitor addresses.

Look for:

- the slowest request paths and actions;
- one slow path requested many times;
- query-string variations associated with slow or uncached requests;
- crawlers repeatedly requesting archive, search, or missing URLs;
- missing pages and static assets that produce a full WordPress 404 response;
- repeated `admin-ajax.php`, `wc-ajax`, REST API, or cron requests; and
- HTTP 4xx and 5xx responses during the same period.

Start with patterns that combine high request volume and long request time. One unusually slow request may matter, but a moderately slow request repeated thousands of times can use more PHP and database capacity.

[Error logs](/docs/monitoring-logs/logs/error-logs/) can reveal PHP warnings, deprecations, and fatal errors associated with the same request. An error can explain a failure or repeated work, but the absence of an error does not mean the request is efficient.

## Capture an APM trace

WP Cloud application performance monitoring (APM) shows how one captured request spends its time. Enable APM for a short window, reproduce the exact page or action, and inspect the matching trace. For an intermittent problem, reproduce the same user state, inputs, and cache state that appeared in the logs.

Use the trace to find slow WordPress hooks, database queries, plugin code, theme code, or external HTTP requests. Then compare that request with Metrics and logs to determine whether it is an isolated trace or a repeated source of site load.

## Inspect WordPress execution

Use [Query Monitor](https://wordpress.org/plugins/query-monitor/) to inspect the page-generation time, peak memory use, database query count and time, PHP errors, hooks, and external HTTP requests for one page load. Filter database queries by component and caller to find the plugin, theme, function, or WordPress code responsible for slow, duplicate, or erroneous queries. Review external HTTP requests for slow or failed dependencies.

Use [Debug Bar](https://wordpress.org/plugins/debug-bar/) when you need a simpler view of page-generation time, database queries, and Object Cache activity. Some Debug Bar details require WordPress debugging constants such as `SAVEQUERIES`; enable additional debugging only for a controlled investigation and do not enable WordPress core debug logging as a substitute for [WP Cloud error logs](/docs/monitoring-logs/logs/error-logs/).

Use these plugins on a staging site or during a controlled investigation. Debugging plugins add work to the request and can expose implementation details to users with access to their panels.

Both plugins describe the request you loaded. Compare their findings with Metrics, logs, or APM before treating one page load as representative of the site.

If the investigation points to repeated database work or cache behavior, see [Object Cache](/docs/performance/cache/object-cache/).

For command-line profiling, use the [WP-CLI profile command](https://developer.wordpress.org/cli/commands/profile/) through [Client SSH](/docs/site-access/ssh-sftp/client-ssh/) to identify slow stages, hooks, and callbacks. Run profiling against the same action seen in Metrics or logs rather than profiling an unrelated page.

## Fix the performance issue

Make the change that addresses the performance issue you identified:

- Improve [Page Cache](/docs/performance/cache/page-cache/) and [Edge Cache](/docs/performance/cache/edge-cache/) coverage for eligible public responses. If a public URL continues to miss or bypass either layer, use [Troubleshoot Page and Edge Cache](/docs/troubleshooting/page-edge-cache/) to inspect response headers, cookies, and explicit bypasses. Avoid frequent broad purges.
- Optimize the underlying slow database query or PHP function before relying on Object Cache to hide its cost. Cached values can expire or be evicted, and the site must still generate the value after a cache miss.
- Cache external API responses when the data can be reused. When the page does not require current data, retrieve it with a scheduled task instead of making the visitor wait. Set an appropriate timeout and failure behavior for requests that must run while the page loads.
- Optimize, replace, or remove the plugin or theme code identified by APM, Query Monitor, or profiling.
- Reduce repeated logged-out `admin-ajax.php` or `wc-ajax` requests, which load WordPress and cannot use full-page cache.
- Fix missing static assets. The default WordPress 404 response loads PHP; [static files and lightweight 404s](/docs/performance/lightweight-404s-static-files/) can reduce that work for eligible requests.
- Avoid proxying a WP Cloud domain when possible. A proxy can replace or obscure connection signals that WP Cloud uses to classify traffic. If a site requires another proxy, follow [Configure Cloudflare with WP Cloud](/docs/sites/domains/cloudflare/).

Deactivate or replace a component only after the measurements point to it. Test production-impacting changes on a staging site when possible and keep a rollback method.

## Compare before and after

Repeat the same URL or action and compare the same Metrics, log fields, Query Monitor measurements, or APM trace. Confirm that response time or PHP and database work improved without breaking logged-in, checkout, account, API, or other intentionally uncached requests.

Allow enough normal traffic to pass before evaluating aggregate cache ratios or request distributions. A single fast request does not prove that a recurring performance issue is resolved.

Keep a timestamped record of normal cache ratios, origin response times, and PHP and MySQL use after a significant release. That baseline makes a later regression or traffic-event review easier to interpret.
