# SSH and SFTP access models

WP Cloud provides two ways to connect to a site's files and command line. Client SSH is for a host partner's developers, support teams, panels, and automation. User SSH and SFTP access is for a person or service that should have credentials for one site.

The two services use different hostnames and credentials. A Client SSH key cannot authenticate as a site user, and a site-user credential cannot authenticate through Client SSH.

## Choose the right access model

### Client SSH

Use [Client SSH](/docs/site-access/ssh-sftp/client-ssh/) for partner developers, engineers, support teams, panels, and automation. It uses public-key authentication and provides full shell and SFTP access to the selected partner site:

```text
<site-id>@client-ssh.atomicsites.net
```

It is a high-privilege service: a Client SSH credential may be authorized for sites across the partner account, although the site ID in the connection selects the site reached by that session.

### User SSH and SFTP access

Use [User SSH and SFTP access](/docs/site-access/ssh-sftp/user-ssh-sftp/) for customers, site developers, and other users whose credential should apply to one site. Site users can use a public key or password. They receive SFTP-only access by default, or a full shell when it is enabled for the site:

```text
<username>@ssh.atomicsites.net
```

Site users are created and removed separately for each site.

## How connections reach a site

WP Cloud sites can move between servers and data centers for maintenance, load balancing, and failover. The stable SSH hostnames route a connection to the site's current server, so users and integrations do not need to track the origin server's address.

WP Cloud reads the connection username to identify the site. For Client SSH, the username is the WP Cloud site ID. For user access, WP Cloud looks up the site assigned to that username. The connection is then routed through an SSH proxy to an isolated container for the selected site.

This routing also avoids a DNS problem. A hostname that pointed directly to an origin server could remain cached after a site moved, and a public record for every site would disclose infrastructure details that are not needed for access.

Direct origin connections would also leave partners to track changing server addresses and manage separate `authorized_keys` files on each server. The proxy keeps authentication and routing at one stable entry point while allowing WP Cloud to move a site without changing the connection details given to users or automation. Key management remains independent of the pool server currently hosting the site.

After authentication, WP Cloud opens the requested SFTP, shell, or direct-command channel in a Docker container for that connection. The container limits what the session can see and do outside the selected site, protecting other sites on the same server from mistakes or malicious commands.

## Filesystem locations

An SFTP session begins in the site's web root:

```text
/srv/htdocs
```

An interactive shell or a command run directly through SSH begins in `/home/<site-id>`. This directory is the session's `$HOME` directory. It is private to SSH sessions: files placed there are not served by the web server and are not available to PHP code handling a web request.

Put WordPress files and anything the site must serve or load in `/srv/htdocs`. Use `$HOME` for shell configuration and private working files. Use `/tmp` for temporary work that does not need to persist.

## Run a command through SSH

When a remote command contains quotes of its own, wrap the complete command in double quotes and escape inner double quotes. For example:

```bash
ssh <user>@<host> "wp eval 'echo \"hello world\\n\";'"
```

Without the outer quotes, part of the command may run in the local shell instead of on the WP Cloud site.

## Session limits

SSH and SFTP sessions have the following limits:

- A session can run for up to eight hours.
- All processes in a session can use up to 1 GB of memory in total.
- A session can create up to 25 processes. The shell and every command in a pipeline count toward this limit.
- Background processes stop when the session disconnects, including processes started with `nohup`.
- A site can have up to 10 concurrent site-user connections.

The 10-connection limit is shared by every site-user credential for the site. Ten connections from one username consume the same capacity as one connection from each of 10 usernames. SSH and SFTP connections both count.

Client SSH connections **do not** count toward the site's 10 concurrent site-user connections. They are intended for interactive work and bounded automation, not permanent workers or daemons.

Process counts can be higher than they first appear. A shell script that runs `wp command | grep something | cut -f1 | sort | uniq` uses a process for the login shell, the script, `wp`, and each command in the pipeline. Break large jobs into restartable stages instead of trying to keep one session open indefinitely.

## Check access

Test a new credential on a non-production site. Confirm that it uses the intended hostname, reaches the expected site, starts in the expected directory, and receives SFTP-only or full-shell access as configured. The [Client SSH](/docs/site-access/ssh-sftp/client-ssh/) and [User SSH and SFTP access](/docs/site-access/ssh-sftp/user-ssh-sftp/) articles include the checks specific to each access model.
