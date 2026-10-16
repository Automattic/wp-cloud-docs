# WooCommerce cart caching

WooCommerce cart caching lets visitors with items in their WooCommerce cart receive eligible pages from [Edge Cache](/docs/performance/cache/edge-cache/). WooCommerce then loads the visitor's cart details dynamically.

**Closed beta:** This feature is available only to enabled WP Cloud partner accounts. Partners without access can contact [WP Cloud Support](/docs/getting-started/get-support/) to express interest in exploring or testing it.

## How cart caching works

Shopping cart cookies normally cause requests to bypass Edge Cache. With WooCommerce cart caching enabled, visitors with cart cookies can receive the cached, empty-cart version of an eligible page. WooCommerce's JavaScript then updates the cart elements for that visitor. The cart may appear empty briefly while the page loads.

Cart details remain specific to each visitor. Requests with cart cookies can read cached pages, but their responses are never written into Edge Cache. The feature does not turn the cart or checkout into shared cached pages. Logged-in WordPress sessions still bypass Edge Cache.

Classic themes rely on WooCommerce cart fragments to refresh cart elements. Block themes use the WooCommerce Store API. Incompatible themes or plugins may display empty cart elements even when the visitor has items in the cart.

Test each site's theme and plugins before enabling this feature for all visitors. Do not use the [Page Cache cookie bypass settings](/docs/performance/cache/page-cache/) to ignore cart or authentication cookies as a substitute.

## Test in one browser

Use this browser-only test before enabling cart caching for the site. Your partner account must have access to the closed beta.

1. Open the store in a private browsing window while logged out of WordPress.
2. Open the browser's developer console on the store's domain and set the test cookie:

   ```javascript
   document.cookie='a8c_edge_enable_woocommerce_cart_caching=1; path=/;'
   ```

3. Add items to the cart and browse product and other cacheable pages. Inspect the `x-ac` response header for [Edge Cache results](/docs/performance/cache/edge-cache/#verify-edge-cache).
4. Confirm that cart icons, counts, mini-carts, and totals update after each page loads. Test quantity changes, removing items, and the cart and checkout flow.
5. Check a separate private browser session to confirm that each visitor sees their own cart details.

If cart elements remain empty or incorrect, resolve the theme or plugin integration before enabling the feature for the site.

Set the cookie only in your own browser for testing. Do not add site code that sets it for visitors. For permanent enablement, use the site-level API control below.

To remove the test cookie, run this in the same browser on the store's domain:

```javascript
document.cookie='a8c_edge_enable_woocommerce_cart_caching=; Max-Age=0; path=/;'
```

Removing the cookie ends the browser-only opt-in. If cart caching is enabled through the API, use the API to disable it.

## Enable or disable cart caching

After testing compatibility, your partner's authenticated [WP Cloud API integration](/docs/api-automation/api-quick-start/) can enable the feature for the site. Replace `<site-id>` with its Atomic Site ID. These beta endpoints are not yet listed in the public API reference.

Send this request with an `application/x-www-form-urlencoded` body. Use `enable=1` to enable cart caching, or `enable=0` to disable it:

```text
POST /edge-cache/<site-id>/woo_cart_cache
```

Omitting the POST body also enables the feature. Check whether it is enabled with:

```text
GET /edge-cache/<site-id>/woo_cart_cache
```

Both requests return the setting in `data.enabled`. Without a domain in the path, the requests use the site's primary domain. To control or check another domain on the site, replace `<domain>` with that domain:

```text
POST /edge-cache/<site-id>/woo_cart_cache/<domain>
GET /edge-cache/<site-id>/woo_cart_cache/<domain>
```

The POST request uses the same `enable` field. The GET request reads the setting for the specified domain.

After enabling the feature, repeat your browser checks without the test cookie. If the site shows incorrect cart elements, disable the feature while you investigate compatibility.
