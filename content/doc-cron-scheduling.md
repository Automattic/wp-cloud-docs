# Cron scheduling

WP Cloud provides platform cron for commands that need to run on a schedule. It runs independently of visits to the site and is separate from [WordPress pseudo-cron](https://developer.wordpress.org/plugins/cron/), which checks for due WordPress events when the site receives a request.

## Choose a scheduling method

Use the method that matches the work:

| Method | Use it for |
| --- | --- |
| WordPress pseudo-cron | Events registered through the WordPress Cron API and managed by WordPress. |
| WP Cloud standard schedules | WP-CLI commands or scripts that should run at a named or shorthand cadence, such as hourly, daily, `2h`, or `3w`. WP Cloud distributes these jobs within the requested cadence, so a standard schedule does not promise an exact wall-clock minute. |
| WP Cloud advanced schedules | A full crontab expression, such as `*/5 * * * *`, for approved managed partners whose host client and site have advanced cron enabled. |
| An external scheduler | A workflow owned by another system. Requests it sends to the site are handled as normal web traffic. |

Standard schedules accept `hourly`, `daily`, `twicedaily`, and `weekly`.
Shorthand schedules include `2h` for twice per hour, `6d` for six times per
day, and `3w` for three times per week. WP Cloud chooses the exact run times
within a standard cadence, so two daily entries are unlikely to run at the same
time.

Advanced cron is reserved for approved WP Cloud managed partners. Confirm that
the feature is enabled for the host client and site before accepting a full
crontab expression. Advanced schedules run at more exact times, so account for
the site's concurrency limit when several entries may start together.

Avoid using platform cron for long sleeps, repeated self-requests, or cache warming. These patterns keep a worker occupied and can create overlapping work. Use a suitable queue, batch operation, or application-level schedule instead.

## Add a cron entry

The [Add Cron Entry endpoint](https://wp.cloud/docs/api/#tag/cron/POST/crontab/{site}/add) requires both a `schedule` and a `command`. Commands run in an environment similar to an SSH session and can use WP-CLI or site scripts.

This example adds a harmless command that reads the site's home URL once per day:

```bash
export WP_CLOUD_SITE='site-id-or-domain'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Auth: ${WP_CLOUD_API_KEY}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'schedule=daily' \
  --data-urlencode 'command=wp option get home' \
  "https://atomic-api.wordpress.com/api/v1.0/crontab/${WP_CLOUD_SITE}/add"
```

A successful response returns a `cron_id`. It confirms that WP Cloud accepted the configuration, not that the command has already run:

```json
{
  "message": "OK",
  "data": {
    "cron_id": 96
  }
}
```

## List, change, or remove entries

Use the [List Cron Entries endpoint](https://wp.cloud/docs/api/#tag/cron/GET/crontab/{site}/list) to retrieve each entry's ID, requested schedule, resulting schedule, and command.

For example, a shorthand request can appear with both its requested value and
the resulting crontab schedule:

```json
{
  "message": "OK",
  "data": [
    {
      "cron_id": 94,
      "schedule": "1 4,16 * * *",
      "requested_schedule": "2h",
      "command": "wp custom sync-products"
    }
  ]
}
```

The [Update Cron Entry endpoint](https://wp.cloud/docs/api/#tag/cron/POST/crontab/{site}/update/{cron_id}) changes the command only. To change a schedule, remove the existing entry and add a new one. This avoids leaving duplicate jobs behind.

Use the [Remove Cron Entry endpoint](https://wp.cloud/docs/api/#tag/cron/POST/crontab/{site}/remove) when the job is no longer needed. Removing a running entry prevents future runs but does not interrupt the current run.

A successful removal returns an empty `data` array:

```json
{
  "message": "OK",
  "data": []
}
```

## Run commands and scripts

Cron commands run in an environment similar to an SSH session. WP-CLI finds
the correct WordPress installation and can be used directly in the command.

The working directory is the user's home directory. Run an executable shell
script with a dot-relative path such as `./script.sh`, or invoke it with
`bash script.sh` or `sh script.sh`.

You can append command output to a file with `>>`, but WP Cloud does not rotate
or delete these files automatically. Log files count toward the site's
filesystem quota, so monitor their size or arrange for their removal.

## Understand runtime limits

- A cron command can run for up to eight hours.
- WP Cloud skips a scheduled run when the previous run of that entry has not finished.
- A site can have up to three cron commands running at once. Additional work is postponed.
- Cron execution can be delayed in rare cases. Missed runs eventually catch
  up, but WP Cloud runs the entry only once during the catch-up period rather
  than once for every missed interval.
- Duplicate entries can run the same command more than once. List the site's entries before adding or replacing a schedule.

Test new commands on a non-production site before scheduling them. Start with a read-only command, list the entry to confirm its stored schedule and command, and remove the test entry when the check is complete.

## Monitor cron results

Configure [Webhooks](/docs/api-automation/webhooks/) to receive `site-cron-results` events for failed commands and concurrency failures. Store the cron ID, site ID, exit status, output, and event time so the host partner can connect a result to the configured entry.

An accepted API request and a listed cron entry show that the schedule is configured. They do not show that every scheduled run completed successfully.
