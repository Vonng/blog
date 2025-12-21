---
title: "Incident: PostgreSQL Extension Installation Causes Connection Failure"
linkTitle: "Incident: Extension Causes Connection Denial"
date: 2019-06-13
author: vonng
summary: >
  Today encountered an interesting case where a customer reported database connection issues caused by extensions.
tags: [PostgreSQL, PG-Admin, Extension, Incident-Report]
---

> Author: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))

Today encountered an interesting case where a customer reported database connection issues. The error was:

```bash
psql: FATAL:  could not load library "/export/servers/pgsql/lib/pg_hint_plan.so": /export/servers/pgsql/lib/pg_hint_plan.so: undefined symbol: RINFO_IS_PUSHED_DOWN
```

Obviously, this error shows the plugin wasn't compiled properly, reporting symbol not found. Therefore, database backend processes crashed with FATAL error and exited directly when attempting to load the `pg_hint_plan` plugin during startup.

Usually this problem is relatively easy to solve. Such additional extensions are typically specified in `shared_preload_libraries` - just remove this extension name.

## But then...

The customer said they enabled the extension via `ALTER ROLE|DATABASE SET session_preload_libraries = pg_hint_plan`.

These two commands override system default parameters when using specific users or connecting to specific databases to load the `pg_hint_plan` plugin.

```psql
ALTER DATABASE postgres SET session_preload_libraries = pg_hint_plan;
ALTER ROLE postgres SET session_preload_libraries = pg_hint_plan;
```

If this is the case, it's still solvable. Usually as long as other users or databases can log in normally, you can remove these two configuration lines via `ALTER TABLE` statements.

But the bad thing was, all users and databases had this parameter configured, so no connection could connect to the database.

In this situation, the database became vegetative - postmaster was still alive, but any newly created backend server processes would commit suicide due to failed extensions... Even external binary commands like `dropdb` couldn't work.

## So then...

Unable to establish database connections, conventional methods all failed... only dirty hacks remained.

If we could erase user and database level configuration items at binary level, then we could connect to the database and clean up the extensions.

DB and Role level configurations are stored in system catalog `pg_db_role_setting`, which has fixed OID = 2964, stored in `global/2964` under the data directory. Shut down the database, open the `pg_db_role_setting` file with binary editor:

```bash
# Open with vim, use :%!xxd to edit binary
# After editing use :%!xxd -r to convert back to binary, then :wq to save
vi ${PGDATA}/global/2964
```

![](pit-extension.png)

Here, replace all `pg_hint_plan` strings with equal-length `^@` binary zero characters. Of course, if you don't care about original configurations, the simpler approach is directly truncating this file to zero length.

Restart database, finally could connect again.

## Reproduction

This problem is very simple to reproduce. Initialize a new database instance:

```bash
initdb -D /pg/test -U postgres && pg_ctl -D /pg/test start
```

Then execute the following statement to experience this sourness:

```sql
psql postgres postgres -c 'ALTER ROLE postgres SET session_preload_libraries = pg_hint_plan;'
```

## Lessons...

1. After installing extensions, always verify the extension works properly before **enabling** it
2. Always leave a way out: an emergency clean superuser or a pollution-free connectable database would avoid such troubles