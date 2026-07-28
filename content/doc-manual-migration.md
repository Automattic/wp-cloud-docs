# Manually migrate a site

WP Cloud includes native [migration tooling](/docs/migrations/migrate-site/) for live source sites that can be reached over SSH. Use this manual workflow when you only have filesystem and database archives, or when the source site cannot use WP Cloud migration tooling or a migration plugin.

Perform the work on a fresh or staging destination when possible because importing files and a database can overwrite working data.

You need a compressed archive containing the source site's `wp-content` directory and a database export in SQL format. You also need SSH or [User SSH and SFTP access](/docs/site-access/ssh-sftp/user-ssh-sftp/) to the destination.

## Place the archives in the temporary directory

Keep migration files in the destination site's `/tmp` directory while you inspect and extract them. Files there are not publicly accessible, and working in `/tmp` avoids changing the served site until the import begins.

Upload the archives through SFTP, or download them over SSH from direct URLs that return the files themselves. A browser share page is not a direct download URL. When using a direct URL, change to `/tmp` and download each archive:

```bash
cd /tmp
wget 'https://downloads.example.com/wp-content-file-name.zip'
wget 'https://downloads.example.com/database-file-name.gz'
```

Confirm that each download is an archive rather than an HTML sign-in or error page. Check the apparent size of the uncompressed database file:

```bash
du --apparent-size -sh database.sql
```

A database larger than 10 GB may import slowly or fail. Before continuing, ask the site owner whether unnecessary files or directories can be removed from a very large `wp-content` archive.

Remove WordPress core files from the supplied archive. WP Cloud provides and maintains WordPress core; the migration normally needs `wp-content`, the database export, and any additional non-core files that the site owner specifically identifies.

## Preserve the current destination

**Warning:** The file sync and database import can be destructive and difficult to undo. Confirm the destination site and preserve its current state before replacing data.

If the destination already contains a site, export its database to `/tmp`:

```bash
wp db export /tmp/pre-migration-database.sql
```

Keep that export and any existing files whose purpose is unclear until the migrated site has been reviewed and accepted.

## Prepare the source files

Extract each archive in `/tmp` with the command that matches its format:

```bash
unzip file-name.zip
tar -xvf file-name.bz2
gunzip file-name.gz
```

Locate the extracted `wp-content` directory and move it to `/tmp`. For example:

```bash
cd /tmp/htdocs
mv wp-content /tmp
mv database.sql /tmp
```

Move any other approved non-core files to `/tmp` so you can place them deliberately during the import.

## Import the files and database

Sync the source `wp-content` directory into the destination document root:

```bash
rsync -zavh /tmp/wp-content /htdocs
```

Before importing the database, inspect its table names and compare their prefix with `$table_prefix` in `/htdocs/wp-config.php`. New WP Cloud sites default to `wp_`, but imported databases can use another prefix. A mismatch can prevent WordPress from finding its tables.

Update only the prefix value when the imported tables use a different valid prefix:

```php
/**
 * WordPress database table prefix.
 *
 * Use only numbers, letters, and underscores.
 */
$table_prefix = 'wp_';
```

Import the SQL file:

```bash
wp db import /tmp/database.sql
```

Move any other approved files to their intended locations, then load the site and check its public pages, WordPress administration area, plugins, theme, media, and forms. The expected result is a destination that loads the source content with the intended WordPress configuration. Ask the site owner to review the migrated site before removing the source archives or the pre-migration database export.

## Handle database import errors

An export created with incompatible permissions or database definitions can fail during import. Retain the complete error output and request a new database export from the source host when the SQL cannot be imported safely. Use [phpMyAdmin](/docs/site-access/database-access/phpmyadmin/) only when its import or export controls are appropriate for the database size and the required settings are known.

## Remove temporary files

**Warning:** `rm` and `rm -rf` permanently delete the selected paths. Run `pwd` and list the intended files before removal. Do not delete files that were present before the migration if their purpose is unclear.

After the site owner accepts the migration and no rollback files are needed, remove only the known temporary archives, extracted directory, and database files:

```bash
cd /tmp
rm database.sql
rm wp-content-file-name.zip
rm -rf wp-content
```

The migration is complete when the destination loads with the expected content and configuration, the site owner has accepted it, and temporary source files have been handled according to the partner's retention policy.
