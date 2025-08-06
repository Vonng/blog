---
title: PostgreSQL 17 Beta1 Released!
date: 2024-05-24
author: |
  [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat](https://mp.weixin.qq.com/s/3EBoAHWEI6zZ-T0nNQsk4Q)
summary: >
  The PostgreSQL Global Development Group announces PostgreSQL 17's first Beta version is now available. This time, PostgreSQL has truly burst the toothpaste tube!
tags: [PostgreSQL]
---


The PostgreSQL Global Development Group announces that PostgreSQL 17's first Beta version is now available for [download](https://www.postgresql.org/download/).
This version includes a preview of all features that will be available when PostgreSQL 17 is officially released, though some details may be adjusted during the Beta testing period.

You can find information about all features and changes in PostgreSQL 17 in the [release notes](https://www.postgresql.org/docs/17/release-17.html):

https://www.postgresql.org/docs/17/release-17.html

In keeping with the PostgreSQL open-source community spirit, we strongly encourage you to test PostgreSQL 17's new features on your systems, helping us discover and fix potential bugs or other issues.
While we don't recommend running PostgreSQL 17 Beta 1 in production environments, we hope you'll run this Beta version in test environments and simulate your actual workloads as closely as possible.

The community will continue to ensure PostgreSQL 17's stability and reliability as the world's most advanced open-source relational database, but this depends on your testing and feedback.
For details, please refer to our [Beta testing process](https://www.postgresql.org/developer/beta/) and how you can contribute: https://www.postgresql.org/developer/beta/

------

## PostgreSQL 17 Highlight Features

### Query and Write Performance Improvements

PostgreSQL 17's recent builds continue the commitment to overall system performance optimization. PostgreSQL's [Vacuum](https://www.postgresql.org/docs/17/routine-vacuuming.html) process, responsible for reclaiming storage space, uses new internal data structures that reduce memory usage by up to 20x while decreasing execution time.
Additionally, the Vacuum process is no longer limited to `1GB` memory usage, but is controlled by [`maintenance_work_mem`](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM), meaning you can allocate more resources to the Vacuum process.

This version introduces a streaming I/O interface that improves performance for sequential scans and running [`ANALYZE`](https://www.postgresql.org/docs/17/sql-analyze.html).
PostgreSQL 17 also adds configuration parameters to control the size of [transaction, subtransaction, and multixact buffers](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-MULTIXACT-MEMBER-BUFFERS).

PostgreSQL 17 can now leverage both planner statistics and the sort order in [Common Table Expression (CTE)](https://www.postgresql.org/docs/17/queries-with.html) results (i.e., [`WITH` queries](https://www.postgresql.org/docs/17/queries-with.html)) to further optimize these queries' speed.
Additionally, this version significantly improves query execution time for queries with `IN` clauses when using [B-tree indexes](https://www.postgresql.org/docs/17/indexes-types.html#INDEXES-TYPES-BTREE).
Starting with this version, for columns with `NOT NULL` constraints, PostgreSQL will directly optimize out redundant `IS NOT NULL` statements in queries. Similarly, queries with `IS NULL` will also be directly optimized. PostgreSQL 17 also supports parallel construction of [BRIN](https://www.postgresql.org/docs/17/brin.html) indexes.

High-concurrency write workloads can significantly benefit from PostgreSQL 17's write-ahead log ([WAL](https://www.postgresql.org/docs/17/wal-intro.html)) lock management improvements, with tests showing performance improvements **up to two times higher**.

Finally, PostgreSQL 17 adds more explicit SIMD instructions, such as enabling AVX-512 instruction support for the [`bit_count`](https://www.postgresql.org/docs/17/functions-bitstring.html) function.

------

### Partitioning and Distributed Workload Enhancements

PostgreSQL 17's partition management is more flexible, adding the ability to **split** and **merge** partitions, and allowing partitioned tables to use **identity columns** and **exclusion constraints**.
Additionally, [PostgreSQL foreign data wrapper](https://www.postgresql.org/docs/17/postgres-fdw.html) ([`postgres_fdw`](https://www.postgresql.org/docs/17/postgres-fdw.html)) can now push down `EXISTS` and `IN` subqueries to remote servers, improving performance.

PostgreSQL 17 adds new functionality to logical replication, making it more usable in high-availability architectures and major version upgrades.
When upgrading from PostgreSQL 17 to higher versions using [`pg_upgrade`](https://www.postgresql.org/docs/17/pgupgrade.html), you no longer need to drop [logical replication slots](https://www.postgresql.org/docs/17/logical-replication-subscription.html#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT), avoiding the hassle of re-synchronizing data after upgrades.
Additionally, you can control the failover process of logical replication, providing better controllability for managing PostgreSQL in high-availability architectures. PostgreSQL 17 also allows logical replication subscribers to use `hash` indexes for lookups and introduces the `pg_createsubscriber` command-line tool for creating logical replication on physical replication standby servers.

------

### Developer Experience

PostgreSQL 17 continues to deepen support for the SQL/JSON standard, adding the `JSON_TABLE` feature that converts JSON to standard PostgreSQL tables, as well as SQL/JSON constructor functions (`JSON`, `JSON_SCALAR`, `JSON_SERIALIZE`) and query functions (`JSON_EXISTS`, `JSON_QUERY`, `JSON_VALUE`).
Notably, these features were originally planned for release in PostgreSQL 15 but were withdrawn during the Beta period due to design trade-off considerations — this is one reason we hope you'll help test new features during the Beta period! Additionally, PostgreSQL 17 adds more functionality to `jsonpath` implementation, including the ability to convert JSON-typed values to various specific data types.

The [`MERGE`](https://www.postgresql.org/docs/17/sql-merge.html) command now supports the `RETURNING` clause, allowing you to further process modified rows in the same command.
You can also use the new `merge_action` function to see which part of the `MERGE` command was modified.
PostgreSQL 17 also allows using the `MERGE` command to update views and adds the `WHEN NOT MATCHED BY SOURCE` clause, allowing users to specify what actions to take when rows in the source have no matches.

The [`COPY`](https://www.postgresql.org/docs/17/sql-copy.html) command is used for efficiently bulk loading and exporting data from PostgreSQL. In PostgreSQL 17, **performance when exporting large rows can be improved by up to two times**.
Additionally, `COPY` performance is improved when source and target encodings match. COPY adds an `ON_ERROR` option that allows continuation even when insertion errors occur.
Additionally, in PostgreSQL 17, drivers can leverage the libpq API to use [asynchronous and safer query cancellation methods](https://www.postgresql.org/docs/17/libpq-cancel.html).

PostgreSQL 17 introduces a built-in collation provider that provides sorting semantics similar to the `C` collation but encoded as `UTF-8` rather than `SQL_ASCII`. This new collation provider provides immutability guarantees, ensuring your sorting results won't change across different systems.

------

### Security Features

PostgreSQL 17 adds a new connection parameter `sslnegotiation` that allows PostgreSQL to perform direct TLS handshakes when using [ALPN](https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation), reducing one network round trip. PostgreSQL registers as `postgresql` in the ALPN directory.

This version introduces new EventTrigger events — triggered when user authentication occurs. It also provides a new API called `PQchangePassword` in libpq that can automatically hash passwords on the client side to prevent accidentally logging plaintext passwords on the server.

PostgreSQL 17 adds a new [predefined role](https://www.postgresql.org/docs/17/predefined-roles.html) called `pg_maintain`, granting users permission to execute `VACUUM`, `ANALYZE`, `CLUSTER`, `REFRESH MATERIALIZED VIEW`, `REINDEX`, and `LOCK TABLE`,
and ensures `search_path` is safe for maintenance operations like `VACUUM`, `ANALYZE`, `CLUSTER`, `REFRESH MATERIALIZED VIEW`, and `INDEX`.
Finally, users can now use `ALTER SYSTEM` to set undefined configuration parameters that the system doesn't recognize.

------

### Backup and Export Management

PostgreSQL 17 can perform incremental backups using [`pg_basebackup`](https://www.postgresql.org/docs/17/app-pgbasebackup.html) and adds a new utility [`pg_combinebackup`](https://www.postgresql.org/docs/17/app-pgcombinebackup.html) for combining backups during the recovery process.
This version adds a `--filter` parameter to [`pg_dump`](https://www.postgresql.org/docs/17/app-pgdump.html), allowing you to specify a file to further specify which objects to include or exclude during the dump process.

------

### Monitoring

The [`EXPLAIN`](https://www.postgresql.org/docs/17/sql-explain.html) command provides information about query plans and execution details. It now adds two options: `SERIALIZE` shows time spent serializing data for network transmission; `MEMORY` reports optimizer memory usage. Additionally, `EXPLAIN` can now show time spent on I/O block reads and writes.

PostgreSQL 17 standardizes `CALL` parameters in [`pg_stat_statements`](https://www.postgresql.org/docs/17/pgstatstatements.html), reducing the number of records generated by frequently called stored procedures.
Additionally, [`VACUUM` progress reporting](https://www.postgresql.org/docs/devel/progress-reporting.html#VACUUM-PROGRESS-REPORTING) now shows index garbage collection progress.
PostgreSQL 17 also introduces a new view, [`pg_wait_events`](https://www.postgresql.org/docs/17/view-pg-wait-events.html), providing descriptions of wait events that can be used with `pg_stat_activity` to gain deeper insights into why active sessions are waiting.
Additionally, some information from the [`pg_stat_bgwriter`](https://www.postgresql.org/docs/17/monitoring-stats.html#MONITORING-PG-STAT-BGWRITER-VIEW) view has now been split into the new [`pg_stat_checkpointer`](https://www.postgresql.org/docs/17/monitoring-stats.html#MONITORING-PG-STAT-CHECKPOINTER-VIEW) view.



------

## Other Features

PostgreSQL 17 has many other new features and improvements, many of which may benefit your use cases. Please refer to the [release notes](https://www.postgresql.org/docs/17/release-17.html) for a complete list of new features and changes:

https://www.postgresql.org/docs/17/release-17.html



------

## Bug and Compatibility Testing

The stability of each PostgreSQL version largely depends on PostgreSQL community users like you, who can test upcoming versions with your workloads and testing tools to discover bugs and complete regression testing before PostgreSQL 17's official release. Since this is a Beta version, small changes to database behavior, feature details, and APIs may still occur. Your feedback and testing will help adjust and finalize these new features, so please test in the near future. The quality of user testing helps us determine when we can make the final release.

The PostgreSQL wiki publicly provides an [open issues](https://wiki.postgresql.org/wiki/PostgreSQL_17_Open_Items) list. You can [report bugs](https://www.postgresql.org/account/submitbug/) using this form on the PostgreSQL website:

https://www.postgresql.org/account/submitbug/



------

## Beta Timeline

This is the first Beta version of PostgreSQL 17. The PostgreSQL project will release more Beta versions as needed for testing, followed by one or more RC versions, with the final version expected around September or October 2024. For details, please refer to the [Beta testing](https://www.postgresql.org/developer/beta/) page.


------

## Links

- [Download](https://www.postgresql.org/download/)
- [Beta Testing Information](https://www.postgresql.org/developer/beta/)
- [PostgreSQL 17 Beta Release Notes](https://www.postgresql.org/docs/17/release-17.html)
- [PostgreSQL 17 Open Issues](https://wiki.postgresql.org/wiki/PostgreSQL_17_Open_Items)
- [Feature Matrix](https://www.postgresql.org/about/featurematrix/)
- [Submit Bugs](https://www.postgresql.org/account/submitbug/)
- [Follow @postgresql on X/Twitter](https://twitter.com/postgresql)
- [Donate](https://www.postgresql.org/about/donate/)