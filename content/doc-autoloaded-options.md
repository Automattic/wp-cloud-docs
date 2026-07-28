# Audit autoloaded options

Use WP-CLI to measure the WordPress options loaded on most requests and find
the largest entries without displaying their values. This read-only audit can
show whether autoloaded options deserve closer investigation; it does not prove
that one option causes a performance problem.

Autoloaded options are loaded early in a WordPress request. WP Cloud's
persistent Object Cache can keep that data in memory between requests, so an
unusually large autoloaded set can also contribute to a large object cache and
longer request or query times.

## Requirements

- WP-CLI access to the site.
- Permission to inspect WordPress option names.
- A secure place for the command output. Option names can reveal installed
  plugins, themes, or business context even when values are omitted.

The commands in this article read the set returned by
`wp_load_alloptions()`. They do not update or delete an option.

## Measure the total serialized size

Run this command to print the combined serialized size of the options
WordPress currently autoloads:

```bash
wp eval 'echo strlen(serialize(wp_load_alloptions())) . PHP_EOL;'
```

The command returns one integer in bytes. Record the result with the time of
the audit so you can compare it with a later measurement.

WordPress Site Health uses a filterable default warning threshold of 800,000
bytes for the combined autoloaded set. Use that value as a reason to inspect
the data, not as a universal performance limit. Request time, query time,
traffic, object-cache behavior, and the contents of individual options all
affect the practical impact.

## Find the largest entries

Run this command to return the 20 largest option names and their estimated
serialized sizes:

```bash
wp eval '$alloptions = wp_load_alloptions(); $rows = array(); foreach ($alloptions as $name => $value) { $rows[] = array("option_name" => $name, "serialized_bytes" => strlen(serialize($value))); } usort($rows, static fn($a, $b) => $b["serialized_bytes"] <=> $a["serialized_bytes"]); fputcsv(STDOUT, array("option_name", "serialized_bytes")); foreach (array_slice($rows, 0, 20) as $row) { fputcsv(STDOUT, $row); }'
```

The first line is the CSV header:

```text
option_name,serialized_bytes
```

Each following row contains an option name and a byte estimate. The command
does not print option values.

## Interpret the results

Start with the largest entries, but do not treat size alone as proof that an
option is faulty. For each entry:

1. Identify the plugin, theme, or WordPress component that owns the option.
2. Confirm whether the component still uses it on normal requests.
3. Compare the total autoloaded size with page-generation time, query time,
   and Object Cache observations from the same period.
4. Look for a pattern, such as stale data left by a removed plugin, a growing
   cache stored in an option, or many entries owned by the same component.

A large Memcached total can be a useful symptom, but it is not an autoloaded
options threshold. The Object Cache stores more than the autoloaded option set,
and a single debug-bar measurement does not establish the cause of a slow
request.

## Choose the next safe action

Do not delete an option or change its autoload behavior until you know what
owns it and when it is read. Removing required data can break a plugin, theme,
or site feature; disabling autoload for data used on most requests can replace
one performance problem with repeated database queries.

Prefer the owning component's documented cleanup or repair method. Test a
manual database change on a staging site, take a current backup, and define how
you will restore the original value and autoload setting before changing a
production site.

## Verify the audit

The audit is complete when you have:

- A timestamped total in bytes.
- A ranked list of option names and byte estimates.
- The likely owner of each entry you intend to investigate.
- Related request-time, query-time, or Object Cache observations.
- A documented and reversible next step for any proposed change.

Redact option names before sharing results with anyone who does not need access
to inspect the site. Rerun both commands after an approved cleanup to confirm
that the intended entries and total changed.

## WordPress references

- [`wp eval`](https://developer.wordpress.org/cli/commands/eval/) runs PHP code
  after WordPress loads.
- [`wp_load_alloptions()`](https://developer.wordpress.org/reference/functions/wp_load_alloptions/)
  returns the options WordPress loads automatically.
- [`WP_Site_Health::get_test_autoloaded_options()`](https://developer.wordpress.org/reference/classes/wp_site_health/get_test_autoloaded_options/)
  defines the current Site Health test and its filterable threshold.
