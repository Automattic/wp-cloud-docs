# IP ranges

WP Cloud uses different addresses for inbound site traffic and outbound
connections from origin servers. Partners should use the WP Cloud API for a
domain's recommended inbound addresses and should not treat a site's outbound
address as permanent. Each range below identifies its purpose and whether it
can be safely used as a site-specific identifier.

## Inbound addresses

WP Cloud routes inbound traffic through an Anycast network. A visitor connects
to a nearby edge location even when the site's origin server is in another
region. The DNS addresses supplied to a partner's customers are load-balancer
addresses, not the addresses of individual origin server pools.

Inbound addresses can differ by host client, and a host client can use its own
CIDR allocation. Retrieve the approved addresses for a domain with the [Get Client IP Addresses endpoint](https://wp.cloud/docs/api/#tag/sites/GET/get-ips/{client}/{domain}). Use the API's `suggested` addresses for production DNS unless the partner's WP Cloud configuration specifies otherwise.

The default WP Cloud inbound load-balancer range is:

```text
192.0.79.128/26
```

Any address in that range can route to a WP Cloud site. When an integration
must choose addresses without using the API's suggestions, it can use a stable
domain-based selection from each half of the range:

```php
if ( ! empty( $domain ) ) {
    srand( crc32( $domain ) );
    $ip1 = '192.0.79.' . mt_rand( 128, 159 );
    $ip2 = '192.0.79.' . mt_rand( 160, 191 );
    srand();
    $rval['suggested'] = [ $ip1, $ip2 ];
}
```

Prefer the API because a host client's approved addresses can differ from the
default range.

## Shared outbound pool ranges

Origin server pool addresses can change. Allowlisting complete WP Cloud
outbound ranges is not recommended because other WP Cloud sites can make
connections from the same ranges. Partners whose external integration requires
the current ranges may request them from WP Cloud Support.

## Site outbound address

A site's outbound address depends on its current origin server pool. It can
change when WP Cloud moves a site for platform health or performance, when
[automated failover](/docs/infrastructure/automated-failover/) changes the
active server, or when a clone replaces the original site. A clone is a
separate site and is not guaranteed to use the same server pool.

From an SSH session on the site, request an external address service to see the
public address used for that connection:

```bash
curl https://whatismyip.akamai.com; echo
```
