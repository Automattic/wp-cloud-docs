# Run bulk tasks across sites

Use the Tasks API to run one operation across many sites in a WP Cloud client account. A task can search site files, run a WP-CLI command, change plugins or themes, or run a supported WP Cloud scan.

## Use tasks safely

**Warning:** The Tasks API can execute a WP-CLI command on every WP Cloud site in a host client's account.

When developing a new WP-CLI command for a task:

- Build a dry-run mode into the command.
- Test the command through [Client SSH](/docs/site-access/ssh-sftp/client-ssh/) on a variety of sites.
- Use `site_count_limit` to run the command on a limited number of sites before running it across every site in the account.

Use `site_run_list` instead when you need to target a known set of specific site IDs.

## Choose a task type

The [Create Task endpoint](https://wp.cloud/docs/api/#tag/tasks/POST/task-create/{client}/{type}) accepts these task types:

- `site-find-files` searches full filesystem paths for a pattern. `*` expands to `(.*)`, and `?` expands to `(.)`.
- `run-wp-cli-command` runs a WP-CLI command with a limit of five minutes and 1,200 MB of memory per site.
- `software` installs, activates, deactivates, or removes plugins and themes.
- `wpcloud-scan` runs a supported `pnt-versions` or `wpscan` scan.

Use `site_run_list` to target an array of up to 200 site IDs. Invalid IDs in that list fail silently and do not produce webhook events. Use `site_count_limit` with an integer or percentage to run against only part of the client account before expanding the task.

## Create a task

Search for sites containing `sample.php`:

```bash
export WP_CLOUD_CLIENT='client-name'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'pattern=sample.php' \
  --data-urlencode 'site_count_limit=10' \
  "https://atomic-api.wordpress.com/api/v1.0/task-create/${WP_CLOUD_CLIENT}/site-find-files"
```

Run `wp db size` against a limited set of sites:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'args[]=db' \
  --data-urlencode 'args[]=size' \
  --data-urlencode 'site_run_list[]=123456' \
  --data-urlencode 'site_run_list[]=123457' \
  "https://atomic-api.wordpress.com/api/v1.0/task-create/${WP_CLOUD_CLIENT}/run-wp-cli-command"
```

A successful response includes the `task_id` used to retrieve or interrupt the task. A `400` response means the client, task type, or task parameters are invalid. A `409` response means another task is already in progress for the client.

## Process task webhooks

By default, WP Cloud sends a `task_progress` event after each site finishes and a `task_complete` event after all selected sites finish. Use `send_webhook_for` with `all`, `success`, `failure`, or `none` to control which per-site results produce webhooks.

Example `task_progress` payload:

```json
{
  "event": "task_progress",
  "timestamp": 1728057609,
  "atomic_site_id": 1000000,
  "data": {
    "task_id": "74",
    "task_type": "software",
    "status": "0",
    "stdout": "Installing Variations (4.3.2)",
    "stderr": "",
    "took": "12"
  }
}
```

`status` is the command's exit status, where `0` means success and a nonzero value means failure. `took` is measured in milliseconds. `stdout` and `stderr` are each limited to 40 KB.

## Retrieve task results

Send the task ID to the [Get Task Details endpoint](https://wp.cloud/docs/api/#tag/tasks/POST/task-get/{atomic_task_id}):

```bash
export WP_CLOUD_TASK_ID='88'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/task-get/${WP_CLOUD_TASK_ID}"
```

Example response, shortened to the fields used for review:

```json
{
  "message": "OK",
  "data": {
    "task_id": "88",
    "type": "site-find-files",
    "created": "2024-12-13 15:43:17",
    "complete": "2024-12-13 15:44:27",
    "meta": {
      "failure_count": "96",
      "success_count": "4",
      "site_count_limit": "100",
      "site_list": "123456555,123456554,123456553",
      "took": "2844"
    }
  }
}
```

`meta.site_list` is populated only when `site_count_limit` was used to create the task. It contains the full list of Atomic Site IDs selected for that run, so partners can identify exactly which sites received the operation. Per-site webhooks provide the corresponding command output, and the task details summarize successes, failures, and timing.

## Interrupt an incomplete task

Send a `POST` request to the [Interrupt Task endpoint](https://wp.cloud/docs/api/#tag/tasks/POST/task-interrupt/{task_id}) with the task ID. The endpoint returns `400` if the ID is invalid or the task already completed.

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Auth: API_AUTH_TOKEN' \
  "https://atomic-api.wordpress.com/api/v1.0/task-interrupt/${WP_CLOUD_TASK_ID}"
```

The task is complete when the `task_complete` event arrives or the task details contain a completion time. Review `success_count`, `failure_count`, and the per-site output before expanding a limited task to more sites.
