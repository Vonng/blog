---
title: "The Versatile file_fdw — Reading System Information from Your Database"
linkTitle: "FileFDW Use Case: Reading OS Info"
date: 2017-12-01
author: vonng
summary: >
  With `file_fdw`, you can easily view operating system information, fetch network data, and feed various data sources into your database for unified viewing and management.
tags: [PostgreSQL, PG-Admin, Extension]
---

> Author: [Vonng](https://vonng.com/en/)

PostgreSQL is the most advanced open-source database, and one of its killer features is FDW: Foreign Data Wrapper. Through FDW, users can access various external data sources from Postgres in a unified manner. `file_fdw` is one of the two FDWs that come bundled with the database. With the update to PostgreSQL 10, `file_fdw` has gained an awesome new capability: reading from program output.

This little powerhouse has endless possibilities. Through `file_fdw`, we can easily view operating system information, fetch network data, and feed various data sources into the database for unified viewing and management.



---------------

## Installation and Configuration

`file_fdw` is a built-in PostgreSQL component that doesn't require any special configuration. You can enable `file_fdw` in your database with a single command:

```plsql
CREATE EXTENSION file_fdw;
```

After enabling the FDW extension, you need to create an instance. This is also done with a single SQL statement. Let's create an FDW Server instance named `fs`:

```plsql
CREATE SERVER fs FOREIGN DATA WRAPPER file_fdw;
```


---------------

## Creating Foreign Tables

For example, if I want to read information about running processes on the operating system from within the database, how would I do that?

The most typical and commonly used external data format is CSV. However, the output from system commands isn't always well-formatted:

```bash
>>> ps ux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
vonng     2658  0.0  0.2 148428  2620 ?        S    11:51   0:00 sshd: vonng@pts/0,pts/2
vonng     2659  0.0  0.2 115648  2312 pts/0    Ss+  11:51   0:00 -bash
vonng     4854  0.0  0.2 115648  2272 pts/2    Ss   15:46   0:00 -bash
vonng     5176  0.0  0.1 150940  1828 pts/2    R+   16:06   0:00 ps -ux
vonng    26460  0.0  1.2 271808 13060 ?        S    Oct26   0:22 /usr/local/pgsql/bin/postgres
vonng    26462  0.0  0.2 271960  2640 ?        Ss   Oct26   0:00 postgres: checkpointer process
vonng    26463  0.0  0.2 271808  2148 ?        Ss   Oct26   0:25 postgres: writer process
vonng    26464  0.0  0.5 271808  5300 ?        Ss   Oct26   0:27 postgres: wal writer process
vonng    26465  0.0  0.2 272216  2096 ?        Ss   Oct26   0:31 postgres: autovacuum launcher process
vonng    26466  0.0  0.1 126896  1104 ?        Ss   Oct26   0:54 postgres: stats collector process
vonng    26467  0.0  0.1 272100  1588 ?        Ss   Oct26   0:01 postgres: bgworker: logical replication launcher

```

We can use `awk` to format the `ps` command output into CSV format with `\x1F` as the delimiter:

```
ps aux | awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,substr($0,index($0,$11))}' OFS='\037'
```

Now for the main event! Create a foreign table definition with the following DDL:

```plsql
CREATE FOREIGN TABLE process_status (
  username TEXT,
  pid      INTEGER,
  cpu      NUMERIC,
  mem      NUMERIC,
  vsz      BIGINT,
  rss      BIGINT,
  tty      TEXT,
  stat     TEXT,
  start    TEXT,
  time     TEXT,
  command  TEXT
) SERVER fs OPTIONS (
PROGRAM $$ps aux | awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,substr($0,index($0,$11))}' OFS='\037'$$,
FORMAT 'csv', DELIMITER E'\037', HEADER 'TRUE');
```

The key here is providing the appropriate parameters through `OPTIONS` in `CREATE FOREIGN TABLE OPTIONS (xxxx)`. By specifying the command in the `PROGRAM` parameter, PostgreSQL will automatically execute this command when querying this table and read its output. The `FORMAT` parameter is set to `CSV`, the `DELIMITER` parameter is set to the previously used `\x1F`, and we ignore the first line of the CSV with `HEADER 'TRUE'`.

So what's the result?

![](file_fdw.png)





---------------

## What's It Good For?

In the simplest scenario, system metric monitoring that previously required writing various monitoring scripts deployed in random places, then regularly executing them to pull metrics and store them in a database — now through file_fdw, you can directly import the metrics of interest into database tables in one step. It's easier to maintain, simpler to deploy, and more reliable. By adding views on top of foreign tables and regularly pulling aggregations, you can accomplish in the database what would normally require an entire monitoring system.

Since it can read output from programs, file_fdw can work with various powerful command-line tools in the Linux ecosystem, unleashing tremendous power.


---------------

## More Examples

Along these lines, I later discovered that Facebook apparently has a similar product called OSQuery, which does pretty much the same thing — querying operating system metrics through SQL. But clearly the PostgreSQL approach is the most straightforward and efficient. Just define the table structure and command data source, and you can easily interface with metric data. You can build something with similar functionality in less than a day.

DDL for reading the system user list:

```plsql
CREATE FOREIGN TABLE etc_password (
  username  TEXT,
  password  TEXT,
  user_id   INTEGER,
  group_id  INTEGER,
  user_info TEXT,
  home_dir  TEXT,
  shell     TEXT
) SERVER fs OPTIONS (
  PROGRAM $$awk -F: 'NF && !/^[:space:]*#/ {print $1,$2,$3,$4,$5,$6,$7}' OFS='\037' /etc/passwd$$, 
  FORMAT 'csv', DELIMITER E'\037'
);
```

DDL for reading disk usage:

```plsql
CREATE FOREIGN TABLE disk_free (
  file_system TEXT,
  blocks_1m   BIGINT,
  used_1m     BIGINT,
  avail_1m    BIGINT,
  capacity    TEXT,
  iused       BIGINT,
  ifree       BIGINT,
  iused_pct   TEXT,
  mounted_on  TEXT
) SERVER fs OPTIONS (PROGRAM $$df -ml| awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9}' OFS='\037'$$, FORMAT 'csv', HEADER 'TRUE', DELIMITER E'\037'
);
```

Of course, file_fdw is just a very basic FDW — for example, it's read-only, you can't modify data through it.

Writing your own FDW to implement CRUD logic is also quite simple. For example, Multicorn is a project for writing FDWs in Python.

SQL over everything — making the world simpler!