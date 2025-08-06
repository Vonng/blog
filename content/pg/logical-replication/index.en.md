---
title: "PostgreSQL Logical Replication Deep Dive"
date: 2021-03-03
author: |
  [Vonng](https://vonng.com)（[@Vonng](https://vonng.com/en/)）
summary: >
  This article introduces the principles and best practices of logical replication in PostgreSQL 13.
tags: [PostgreSQL,PG Administration]
---

------

## Logical Replication

**Logical Replication** is a method of replicating data objects and their changes based on their [**replica identity**](/pg/replica-identity/) (usually the primary key).

The term **logical replication** contrasts with **physical replication**. Physical replication uses exact block addresses and byte-for-byte copying, while logical replication allows fine-grained control over the replication process.

Logical replication is based on a **publication** and **subscription** model:

* A **publisher** can have multiple **publications**, and a **subscriber** can have multiple **subscriptions**.
* A publication can be subscribed to by multiple subscribers, but a subscription can only subscribe to one **publisher**, though it can subscribe to multiple different publications from the same publisher.

Logical replication for a table typically works as follows: the subscriber gets a snapshot of the publisher database and copies the existing data in the table. Once data copying is complete, **changes** (insert, update, delete, truncate) from the publisher are sent to the subscriber in real-time. The subscriber applies these changes in the same order, ensuring transactional consistency for logical replication. This method is sometimes called **transactional replication**.

Typical uses of logical replication include:

* Migration across PostgreSQL major versions and operating system platforms.
* CDC (Change Data Capture) to collect incremental changes from a database (or subset), triggering custom logic on the subscriber side.
* Splitting: integrating multiple databases into one, or splitting one database into multiple, with fine-grained splitting, integration, and access control.

A logical subscriber behaves like a normal PostgreSQL instance (primary), and can also create its own publications and have its own subscribers.

If the logical subscriber is read-only, there will be no **conflicts**. If there are writes to the logical subscriber's subscription set, conflicts may occur.

------

## Publication

A **publication** can be defined on a physical replication **primary**. The node that creates a publication is called a **publisher**.

A **publication** is **a change set composed of a group of tables**. It can also be viewed as a **change set** or **replication set**. Each publication can only exist in one **database**.

Publications are different from **schemas** and don't affect how tables are accessed. (Whether a table is included in a publication doesn't affect its own access.)

Publications currently can only contain **tables** (i.e., indexes, sequences, materialized views are not published). Each table can be added to multiple publications.

Unless a publication is created for `ALL TABLES`, objects (tables) in a publication can only be **explicitly added** (via `ALTER PUBLICATION ADD TABLE`).

Publications can filter the types of changes needed: any combination of `INSERT`, `UPDATE`, `DELETE`, and `TRUNCATE`, similar to trigger events. By default, all changes are published.

### Replica Identity

> [Replica Identity](/pg/replica-identity)

A table included in a publication must have a **replica identity** so that rows needing updates can be located on the subscriber side to complete `UPDATE` and `DELETE` operation replication.

By default, the **primary key** is the table's replica identity. **Unique indexes on non-null columns** can also be used as replica identity.

If there's no replica identity, you can set the replica identity to `FULL`, meaning the entire row serves as the replica identity. (An interesting case: multiple completely identical records in a table can be handled correctly, see subsequent examples.) Using `FULL` mode replica identity is inefficient (because every row modification requires a full table scan on the subscriber, easily overwhelming the subscriber), so this configuration can only be a fallback. Using `FULL` mode replica identity has another limitation: columns included in the replica identity on the subscriber side must either match the publisher or be fewer than the publisher.

`INSERT` operations can always proceed regardless of replica identity (because inserting a new record doesn't require locating any existing records on the subscriber; while delete and update operations need the **replica identity** to locate records to operate on). If a table without replica identity is added to a publication with `UPDATE` and `DELETE`, subsequent `UPDATE` and `DELETE` operations will cause errors on the publisher.

The table's replica identity mode can be queried from `pg_class.relreplident` and modified via `ALTER TABLE`.

```sql
ALTER TABLE tbl REPLICA IDENTITY 
{ DEFAULT | USING INDEX index_name | FULL | NOTHING };
```

Although various combinations are possible, in practice, only three situations are feasible:

* Table has primary key, use default `default` replica identity
* Table has no primary key but has non-null unique index, explicitly configure `index` replica identity  
* Table has neither primary key nor non-null unique index, explicitly configure `full` replica identity (very inefficient, only as fallback)
* All other situations cannot complete logical replication functionality normally. Insufficient output information may cause errors or may not.
* Special note: if a table with `nothing` replica identity is included in logical replication, delete/update operations will cause publisher errors!

| Replica Identity Mode\Table Constraints | Primary Key (p) | Non-null Unique Index (u) | Neither (n) |
|:------------:|:------:|:---------:|:-------:|
| **d**efault  | **Valid** |     x     |    x    |
|  **i**ndex   |   x    |  **Valid**   |    x    |
|   **f**ull   | **Inefficient** |  **Inefficient**   | **Inefficient**  |
| **n**othing  |  xxxx  |   xxxx    |  xxxx   |

### Managing Publications

`CREATE PUBLICATION` creates publications, `DROP PUBLICATION` removes publications, `ALTER PUBLICATION` modifies publications.

After publication creation, tables can be dynamically added or removed from publications via `ALTER PUBLICATION`. These operations are transactional.

```sql
CREATE PUBLICATION name
    [ FOR TABLE [ ONLY ] table_name [ * ] [, ...]
      | FOR ALL TABLES ]
    [ WITH ( publication_parameter [= value] [, ... ] ) ]

ALTER PUBLICATION name ADD TABLE [ ONLY ] table_name [ * ] [, ...]
ALTER PUBLICATION name SET TABLE [ ONLY ] table_name [ * ] [, ...]
ALTER PUBLICATION name DROP TABLE [ ONLY ] table_name [ * ] [, ...]
ALTER PUBLICATION name SET ( publication_parameter [= value] [, ... ] )
ALTER PUBLICATION name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER PUBLICATION name RENAME TO new_name

DROP PUBLICATION [ IF EXISTS ] name [, ...];
```

`publication_parameter` mainly includes two options:

* `publish`: Defines types of change operations to publish, comma-separated string, defaults to `insert, update, delete, truncate`.
* `publish_via_partition_root`: New option in v13+, if true, partitioned tables will use the root partition's replica identity for logical replication.

### Querying Publications

Publications can be queried using the psql meta-command `\dRp`.

```bash
# \dRp
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Via root
----------+------------+---------+---------+---------+-----------+----------
 postgres | t          | t       | t       | t       | t         | f
```

###  `pg_publication` Publication Definition Table

`pg_publication` contains raw publication definitions, with each record corresponding to one publication.

```sql
# table pg_publication;
oid          | 20453
pubname      | pg_meta_pub
pubowner     | 10
puballtables | t
pubinsert    | t
pubupdate    | t
pubdelete    | t
pubtruncate  | t
pubviaroot   | f
```

* `puballtables`: Whether to include all tables
* `pubinsert|update|delete|truncate`: Whether to publish these operations
* `pubviaroot`: If set, any partitioned table (leaf table) will use the topmost (partitioned) table's **replica identity**. So the entire partitioned table can be treated as one table rather than a series of tables for publication.

###  `pg_publication_tables` Publication Content Table

`pg_publication_tables` is a view composed of `pg_publication`, `pg_class`, and `pg_namespace`, recording table information included in publications.

```bash
postgres@meta:5432/meta=# table pg_publication_tables;
   pubname   | schemaname |    tablename
-------------+------------+-----------------
 pg_meta_pub | public     | spatial_ref_sys
 pg_meta_pub | public     | t_normal
 pg_meta_pub | public     | t_unique
 pg_meta_pub | public     | t_tricky
```

Using `pg_get_publication_tables` can get subscription table OIDs based on subscription name:

```sql
SELECT * FROM pg_get_publication_tables('pg_meta_pub');
SELECT p.pubname,
       n.nspname AS schemaname,
       c.relname AS tablename
FROM pg_publication p,
     LATERAL pg_get_publication_tables(p.pubname::text) gpt(relid),
     pg_class c
         JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.oid = gpt.relid;
```

Additionally, `pg_publication_rel` provides similar information but from a many-to-many OID perspective, containing raw data.

```
  oid  | prpubid | prrelid
-------+---------+---------
 20414 |   20413 |   20397
 20415 |   20413 |   20400
 20416 |   20413 |   20391
 20417 |   20413 |   20394
```

The difference between these two is particularly noteworthy: when publishing for `ALL TABLES`, `pg_publication_rel` won't have specific table OIDs, but `pg_publication_tables` can query the actual table list included in logical replication. So `pg_publication_tables` should usually be the reference.

When creating subscriptions, the database first modifies the `pg_publication` catalog, then fills publication table information into `pg_publication_rel`.

------

## Subscription

A **subscription** is the downstream of logical replication. The node that defines a subscription is called a **subscriber**.

A subscription defines how to **connect** to another database and which **publications** on the target publisher to subscribe to.

A logical subscriber behaves like a normal PostgreSQL instance (primary). Logical subscribers can also create their own publications and have their own subscribers.

Each subscriber receives changes through a **replication slot**. During initial data replication, additional temporary replication slots may be needed.

Logical replication subscriptions can serve as synchronous replication standby servers. The standby server name is the subscription name by default, but you can use a different name by setting `application_name` in the connection information.

Only superusers can dump subscription definitions with `pg_dump`, as only superusers can access the `pg_subscription` view. Regular users will skip and print warnings when attempting to dump.

Logical replication doesn't replicate DDL changes, so tables in the publication set must **already exist** on the subscriber side. Only changes on **regular tables** are replicated; views, materialized views, sequences, indexes are not replicated.

Tables on the publisher and subscriber sides are matched by fully qualified names (like `public.table`). Replicating changes to tables with different names is not supported.

Columns in tables on publisher and subscriber sides are also matched by **name**. Column order doesn't matter, and data types don't need to be identical, as long as the **text representation** of the two columns is compatible, meaning the data's text representation can be converted to the target column type. Subscriber tables can contain columns that don't exist on the publisher; these new columns will be filled with default values.

### Managing Subscriptions

`CREATE SUBSCRIPTION` creates subscriptions, `DROP SUBSCRIPTION` removes subscriptions, `ALTER SUBSCRIPTION` modifies subscriptions.

After subscription creation, subscriptions can be **paused** and **resumed** anytime via `ALTER SUBSCRIPTION`.

Removing and recreating subscriptions will cause **synchronization information loss**, meaning related data needs to be re-synchronized.

```sql
CREATE SUBSCRIPTION subscription_name
    CONNECTION 'conninfo'
    PUBLICATION publication_name [, ...]
    [ WITH ( subscription_parameter [= value] [, ... ] ) ]

ALTER SUBSCRIPTION name CONNECTION 'conninfo'
ALTER SUBSCRIPTION name SET PUBLICATION publication_name [, ...] [ WITH ( set_publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name REFRESH PUBLICATION [ WITH ( refresh_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ENABLE
ALTER SUBSCRIPTION name DISABLE
ALTER SUBSCRIPTION name SET ( subscription_parameter [= value] [, ... ] )
ALTER SUBSCRIPTION name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER SUBSCRIPTION name RENAME TO new_name

DROP SUBSCRIPTION [ IF EXISTS ] name;
```

`subscription_parameter` defines subscription options, including:

* `copy_data(bool)`: Whether to copy data after replication starts, defaults to true
* `create_slot(bool)`: Whether to create replication slot on publisher, defaults to true
* `enabled(bool)`: Whether to enable this subscription, defaults to true
* `connect(bool)`: Whether to attempt connection to publisher, defaults to true. Setting to false forces the above options to false.
* `synchronous_commit(bool)`: Whether to enable synchronous commit, reporting progress to the primary.
* `slot_name`: Replication slot name associated with subscription. Setting to empty disassociates subscription from replication slot.

### Managing Replication Slots

Each active subscription receives changes from remote publishers through **replication slots**.

Usually these remote **replication slots** are automatically managed, created automatically during `CREATE SUBSCRIPTION` and deleted automatically during `DROP SUBSCRIPTION`.

In specific scenarios, you might need to operate subscriptions and underlying replication slots separately:

* When creating subscriptions, if the required replication slot already exists, you can associate with existing replication slots via `create_slot = false`.

* When creating subscriptions, if the remote is unreachable or status is unclear, you can use `connect = false` to not access remote hosts. This is what `pg_dump` does. In this case, you must manually create replication slots on the remote before enabling the subscription locally.

* When removing subscriptions, if you need to preserve replication slots. This usually occurs when the subscriber is moving to another machine and wants to resume subscription there. In this case, you need to first disassociate the subscription from the replication slot via `ALTER SUBSCRIPTION`.

* When removing subscriptions, if the remote is unreachable. In this case, you need to disassociate the replication slot from the subscription using `ALTER SUBSCRIPTION` before deleting the subscription.

  If the remote instance is no longer used, that's fine. However, if the remote instance is only temporarily unreachable, you should manually delete the replication slot on it; otherwise it will continue retaining WAL and may cause disk space issues.

### Querying Subscriptions

Subscriptions can be queried using the psql meta-command `\dRs`.

```bash
# \dRs
     Name     |  Owner   | Enabled |  Publication
--------------+----------+---------+----------------
 pg_bench_sub | postgres | t       | {pg_bench_pub}
```

###  `pg_subscription` Subscription Definition Table

Each logical subscription has one record. Note this view spans database clusters; each database can see subscription information for the entire cluster.

Only superusers can access this view because it contains plaintext passwords (connection information).

```sql
oid             | 20421
subdbid         | 19356
subname         | pg_test_sub
subowner        | 10
subenabled      | t
subconninfo     | host=10.10.10.10 user=replicator password=DBUser.Replicator dbname=meta
subslotname     | pg_test_sub
subsynccommit   | off
subpublications | {pg_meta_pub}
```

* `subenabled`: Whether subscription is enabled
* `subconninfo`: Hidden from regular users due to sensitive information.
* `subslotname`: Replication slot name used by subscription, also used as logical replication **origin name** for deduplication.
* `subpublications`: List of subscribed publication names.
* Other status information: whether synchronous commit is enabled, etc.

### `pg_subscription_rel` Subscription Content Table

`pg_subscription_rel` records information about each table in subscriptions, including status and progress.

* `srrelid`: OID of relations in subscription
* `srsubstate`: State of relations in subscription: `i` initializing, `d` copying data, `s` synchronization complete, `r` normal replication.
* `srsublsn`: Empty when in `i|d` state, remote LSN position when in `s|r` state.

### During Subscription Creation

When a new subscription is created, the following operations are executed in sequence:

* Store publication information in `pg_subscription` catalog, including connection info, replication slot, publication names, configuration options, etc.
* Connect to publisher, check replication permissions (note this **doesn't check if corresponding publications exist**).
* Create logical replication slot: `pg_create_logical_replication_slot(name, 'pgoutput')`
* Register tables in replication set to subscriber's `pg_subscription_rel` catalog.
* Perform initial snapshot synchronization. Note that existing data in subscriber tables won't be deleted.

------

## Replication Conflicts

Logical replication behaves like normal DML operations, updating data even if it has changed locally on the user node. If replicated data violates any constraints, replication will stop. This phenomenon is called **conflict**.

When replicating `UPDATE` or `DELETE` operations, missing data (i.e., data to be updated/deleted no longer exists) doesn't cause conflicts; such operations are simply skipped.

Conflicts cause errors and abort logical replication. The logical replication management process will retry continuously at 5-second intervals. Conflicts don't block SQL on subscription-side tables in the replication set. Conflict details can be found in the user's server logs. **Conflicts must be manually resolved by users**.

### Conflicts That May Appear in Logs

|          Conflict Mode          | Replication Process | Log Output |
| :------------------------: | :------: | :------: |
|   Missing UPDATE/DELETE objects    |   Continue   |  No output  |
|        Table/row lock wait         |   Wait   |  No output  |
|  Violate primary key/unique/check constraints   | **Abort** |   Output   |
| Target table/column doesn't exist  | **Abort** |   Output   |
| Cannot convert data to target column type | **Abort** |   Output   |

Methods to resolve conflicts can be changing data on the subscription side so it doesn't conflict with incoming changes, or skipping transactions that conflict with existing data.

Use the function `pg_replication_origin_advance()` with the subscription's corresponding `node_name` and LSN position to skip transactions. Current ORIGIN positions can be seen in the `pg_replication_origin_status` system view.

------

## Limitations

Logical replication currently has the following limitations or missing functionality. These issues may be resolved in future versions.

**Database schemas and DDL commands are not replicated**. Existing schemas can be manually replicated via `pg_dump --schema-only`. Incremental schema changes need to be manually kept in sync (publisher and subscriber schemas don't need to be absolutely identical). Logical replication is still reliable for online DDL changes: after executing DDL changes in the publication database, replicated data arrives at the subscriber but replication stops due to schema mismatches. After updating the subscriber's schema, replication continues. In many cases, executing changes on the subscriber first can avoid intermediate errors.

**Sequence data is not replicated**. Data in identity columns and `SERIAL` types served by **sequences** will of course be replicated as part of the table, but the sequences themselves remain at initial values on the subscriber. If the subscriber is used as a read-only database, this is usually fine. However, if you plan some form of switchover or failover to the subscriber database, you need to update sequences to latest values, either by copying current data from the publisher (perhaps using `pg_dump -t *seq*`) or determining a sufficiently high value from the table data content itself (e.g., `max(id)+1000000`). Otherwise, when executing operations that get sequences as identities on the new database, conflicts are likely to occur.

**Logical replication supports replicating `TRUNCATE` commands**, but special care is needed when `TRUNCATE` involves a group of tables connected by foreign keys. When executing `TRUNCATE` operations, the group of tables associated with it on the publisher (through explicit listing or cascade relationships) will all be `TRUNCATE`d, but on the subscriber, tables not in the subscription set won't be `TRUNCATE`d. This operation is logically reasonable because logical replication shouldn't affect tables outside the replication set. But if some tables not in the subscription set reference tables in the subscription set that are being `TRUNCATE`d through foreign keys, the `TRUNCATE` operation will fail.

**Large objects are not replicated**

**Only tables can be replicated (including partitioned tables)**. Attempting to replicate other table types will cause errors (views, materialized views, foreign tables, unlogged tables). Specifically, only tables with `pg_class.relkind = 'r'` can participate in logical replication.

**When replicating partitioned tables, replication is done by sub-table by default**. By default, changes are triggered by leaf partitions of partitioned tables, meaning each partition sub-table in the publication needs to exist on the subscription side (of course, this partition sub-table on the subscriber doesn't necessarily have to be a partition sub-table; it could be a partition parent table or a regular table). Publications can declare whether to use replica identity on partition root tables instead of partition leaf tables. This is a new feature in PG13, specified via the `publish_via_partition_root` option when creating publications.

**Trigger behavior differs**. **Row-level triggers** will fire, but `UPDATE OF cols` type triggers won't fire. Statement-level triggers only fire during initial data copying.

**Logging behavior differs**. Even with `log_statement = 'all'` set, SQL statements generated by replication won't be recorded in logs.

**Bidirectional replication requires extreme care**: mutual publication and subscription is feasible as long as table sets on both sides don't intersect. But once table intersections appear, infinite WAL loops will occur.

**Replication within the same instance**: Logical replication within the same instance requires special care. You must **manually create logical replication slots** and use existing logical replication slots when creating subscriptions, otherwise deadlock will occur.

**Can only be performed on primary**: Currently, logical decoding from physical replication standby servers is not supported, and replication slots cannot be created on standby servers, so standby servers cannot serve as publishers. But this issue may be resolved in the future.

------

## Architecture

Logical replication begins by taking a snapshot of the publisher database and copying existing data in tables based on this snapshot. Once copying is complete, **changes** (insert, update, delete, etc.) from the publisher are sent to the subscriber in real-time.

Logical replication uses an architecture similar to physical replication, implemented through `walsender` and `apply` processes. The publisher's `walsender` process loads logical decoding plugins (`pgoutput`) and begins logical decoding of WAL logs. **Logical decoding plugins** read changes from WAL, filter changes according to **publication** definitions, transform changes into specific forms, and transmit them via logical replication protocol. Data is transmitted to the subscriber's `apply` process via streaming replication protocol. This process maps changes to local tables upon receiving them and reapplies these changes in transaction order.

### Initial Snapshot

Subscriber tables during initialization and data copying are handled by a special `apply` process. This process creates its own **temporary replication slot** and copies existing data in tables.

Once data copying is complete, the table enters synchronization mode (`pg_subscription_rel.srsubstate = 's'`). Synchronization mode ensures the **main apply process** can apply changes that occurred during data copying using standard logical replication methods. Once synchronization is complete, table replication control is transferred back to the **main apply process**, resuming normal replication mode.

### Process Structure

The logical replication publisher creates a corresponding `walsender` process for each connection from subscribers, sending decoded WAL logs. On the subscriber side...

### Replication Slots

When creating subscriptions...

One logical replication...

### Logical Decoding

### Synchronous Commit

Synchronous commit for logical replication is accomplished through SIGUSR1 communication between Backend and Walsender.

### Temporary Data

Temporary data from logical decoding is written to disk as local log snapshots. When walsender receives SIGUSR1 signals from walwriter, it reads WAL logs and generates corresponding logical decoding snapshots. These snapshots are deleted when transmission ends.

File location: `$PGDATA/pg_logical/snapshots/{LSN Upper}-{LSN Lower}.snap`

------

## Monitoring

Logical replication uses an architecture similar to physical streaming replication, so monitoring a logical replication **publisher node** is not much different from monitoring a physical replication primary.

Subscriber monitoring information can be obtained through the `pg_stat_subscription` view.

###  `pg_stat_subscription` Subscription Statistics Table

Each **active subscription** has **at least one** record in this view, i.e., the Main Worker (responsible for applying logical logs).

The Main Worker has `relid = NULL`. If there are processes responsible for initial data copying, they will also have records here, with `relid` being the table responsible for copying data.

```bash
subid                 | 20421
subname               | pg_test_sub
pid                   | 5261
relid                 | NULL
received_lsn          | 0/2A4F6B8
last_msg_send_time    | 2021-02-22 17:05:06.578574+08
last_msg_receipt_time | 2021-02-22 17:05:06.583326+08
latest_end_lsn        | 0/2A4F6B8
latest_end_time       | 2021-02-22 17:05:06.578574+08
```

* `received_lsn`: Most recently **received** log position.
* `latest_end_lsn`: Last LSN position reported to walsender, i.e., `confirmed_flush_lsn` on the primary. However, this value doesn't update very frequently.

Usually, an active subscription has one apply process running. Disabled or crashed subscriptions have no records in this view. During initial synchronization, synchronized tables will have additional worker process records.

###  `pg_replication_slot` Replication Slots

```bash
postgres@meta:5432/meta=# table pg_replication_slots ;
-[ RECORD 1 ]-------+------------
slot_name           | pg_test_sub
plugin              | pgoutput
slot_type           | logical
datoid              | 19355
database            | meta
temporary           | f
active              | t
active_pid          | 89367
xmin                | NULL
catalog_xmin        | 1524
restart_lsn         | 0/2A08D40
confirmed_flush_lsn | 0/2A097F8
wal_status          | reserved
safe_wal_size       | NULL
```

The replication slot view contains both logical and physical replication slots. Main characteristics of logical replication slots:

* `plugin` field is not empty, identifying the logical decoding plugin used. Logical replication uses the `pgoutput` plugin by default.
* `slot_type = logical`, physical replication slot type is `physical`.
* `datoid` and `database` fields are not empty, because physical replication is associated with clusters while logical replication is associated with databases.

Logical subscribers also appear as standard **replication standby servers** in the `pg_stat_replication` view.

### `pg_replication_origin` Replication Origins

Replication origins...

```sql
table pg_replication_origin_status;
-[ RECORD 1 ]-----------
local_id    | 1
external_id | pg_19378
remote_lsn  | 0/0
local_lsn   | 0/6BB53640
```

* `local_id`: Local ID of replication origin, efficient 2-byte representation.
* `external_id`: ID of replication origin, can be referenced across nodes.
* `remote_lsn`: Most recent **commit position** from source.
* `local_lsn`: LSN of locally persisted commit records

### Detecting Replication Conflicts

The most reliable detection method is always from logs on both publisher and subscriber sides. When replication conflicts occur, disconnected replication connections can be seen on the publisher side:

```yaml
LOG:  terminating walsender process due to replication timeout
LOG:  starting logical decoding for slot "pg_test_sub"
DETAIL:  streaming transactions committing after 0/xxxxx, reading WAL from 0/xxxx
```

On the subscriber side, you can see specific reasons for replication conflicts, such as:

```csv
logical replication worker PID 4585 exited with exit code 1
ERROR: duplicate key value violates unique constraint "pgbench_tellers_pkey","Key (tid)=(9) already exists.",,,,"COPY pgbench_tellers, line 31",,,,"","logical replication worker"
```

Additionally, some monitoring metrics can reflect logical replication status:

For example: `pg_replication_slots.confirmed_flush_lsn` lagging behind `pg_current_wal_lsn` for extended periods, or significant increases in `pg_stat_replication.flush_lag/write_lag`.

------

## Security

For tables participating in subscriptions, ownership and trigger permissions must be controlled by roles trusted by superusers (otherwise modifying these tables may cause logical replication interruption).

On publisher nodes, if untrusted users have table creation privileges, publications should explicitly specify table names rather than using the wildcard `ALL TABLES`. That is, `FOR ALL TABLES` should only be used when superusers trust all users who can have table creation privileges (non-temporary tables) on either publisher or subscriber sides.

Users for replication connections must have `REPLICATION` privileges (or be SUPERUSER). If the role lacks `SUPERUSER` and `BYPASSRLS`, row security policies on the publisher may be executed. If the table owner sets row-level security policies after replication starts, this configuration may cause replication to abort directly rather than policies taking effect. The user must have LOGIN privileges, and HBA rules must allow access.

To replicate initial table data, the role used for replication connections must have `SELECT` privileges on published tables (or be superuser).

Creating publications requires `CREATE` privileges in the database. Creating a `FOR ALL TABLES` publication requires superuser privileges.

Adding tables to publications requires **ownership** privileges on the tables.

Creating subscriptions requires superuser privileges because subscription apply processes run with superuser privileges in the local database.

**Privileges are only checked when establishing replication connections**, not when reading each change record on the publisher side, nor when applying each record on the subscriber side.

## Configuration Options

Logical replication requires some configuration options to work properly.

On the publisher side, `wal_level` must be set to `logical`. `max_replication_slots` needs to be set to at least the number of subscriptions + number used for table data synchronization. `max_wal_senders` needs to be set to at least `max_replication_slots` + number reserved for physical replication.

On the subscriber side, `max_replication_slots` also needs to be set, with `max_replication_slots` needing to be set to at least the number of subscriptions.

`max_logical_replication_workers` needs to be configured to at least the number of subscriptions plus some worker processes for data synchronization.

Additionally, `max_worker_processes` needs to be adjusted accordingly, should be at least `max_logical_replication_worker` + 1. Note that some extension plugins and parallel queries also use worker processes from the pool.

### Configuration Parameter Examples

For 64-core machines with 1-2 publications and subscriptions, up to 6 sync workers, up to 8 physical standby servers, a sample configuration is as follows:

First determine slot count: 2 subscriptions, 6 sync workers, 8 physical standby servers, so configure as 16. Sender = Slot + Physical Replica = 24.

Sync worker limit is 6, 2 subscriptions, so total logical replication workers set to 8.

```ini
wal_level: logical                      # logical	
max_worker_processes: 64                # default 8 -> 64, set to CPU CORE 64
max_parallel_workers: 32                # default 8 -> 32, limit by max_worker_processes
max_parallel_maintenance_workers: 16    # default 2 -> 16, limit by parallel worker
max_parallel_workers_per_gather: 0      # default 2 -> 0,  disable parallel query on OLTP instance
# max_parallel_workers_per_gather: 16   # default 2 -> 16, enable parallel query on OLAP instance

max_wal_senders: 24                     # 10 -> 24
max_replication_slots: 16               # 10 -> 16 
max_logical_replication_workers: 8      # 4 -> 8, 6 sync worker + 1~2 apply worker
max_sync_workers_per_subscription: 6    # 2 -> 6, 6 sync worker
```

------

## Quick Configuration

First set the publisher-side configuration option `wal_level = logical`. This parameter requires a restart to take effect; default values for other parameters don't affect usage.

Then create replication users and add `pg_hba.conf` configuration entries to allow external access. A typical configuration is:

```sql
CREATE USER replicator REPLICATION BYPASSRLS PASSWORD 'DBUser.Replicator';
```

Note: logical replication users need `SELECT` privileges. In Pigsty, `replicator` has been granted the `dbrole_readonly` role.

```ini
host     all          replicator     0.0.0.0/0     md5
host     replicator   replicator     0.0.0.0/0     md5
```

Then execute on the publisher-side database:

```sql
CREATE PUBLICATION mypub FOR TABLE <tablename>;
```

Then execute on the subscriber-side database:

```sql
CREATE SUBSCRIPTION mysub CONNECTION 'dbname=<pub_db> host=<pub_host> user=replicator' PUBLICATION mypub;
```

The above configuration will start replication, first copying initial table data, then synchronizing incremental changes.

### Sandbox Example

Using Pigsty's standard 4-node two-cluster sandbox as an example, with two database clusters `pg-meta` and `pg-test`. Now using `pg-meta-1` as publisher and `pg-test-1` as subscriber.

```bash
PGSRC='postgres://dbuser_admin@meta-1/meta'           # Publisher
PGDST='postgres://dbuser_admin@node-1/test'           # Subscriber
pgbench -is100 ${PGSRC}                               # Initialize Pgbench on publisher
pg_dump -Oscx -t pgbench* -s ${PGSRC} | psql ${PGDST} # Sync table structure on subscriber

# Create **publication** on publisher, add default `pgbench` related tables to publication set.
psql ${PGSRC} -AXwt <<-'EOF'
CREATE PUBLICATION "pg_meta_pub" FOR TABLE
  pgbench_accounts,pgbench_branches,pgbench_history,pgbench_tellers;
EOF

# Create **subscription** on subscriber, subscribe to publication on publisher.
psql ${PGDST} <<-'EOF'
CREATE SUBSCRIPTION pg_test_sub
  CONNECTION 'host=10.10.10.10 dbname=meta user=replicator' 
  PUBLICATION pg_meta_pub;
EOF
```

------

## Replication Flow

After logical replication subscription creation, if everything is normal, logical replication will automatically begin, executing replication state machine logic for **each table in the subscription**.

As shown in the diagram below.

<div class="mermaid">
stateDiagram-v2
    [*] --> init : Table added to subscription set
    init --> data : Begin synchronizing table's initial snapshot
    data --> sync : Existing data synchronization complete
    sync --> ready : Incremental changes during sync applied, enter ready state
</div>

When all tables complete replication and enter `r` (ready) state, the existing data synchronization phase of logical replication is complete, and publisher and subscriber overall enter synchronized state.

Therefore, logically there are two state machines: **table-level replication small state machine** and **global replication large state machine**. Each Sync Worker handles a small state machine on one table, while one Apply Worker handles the large state machine of one logical replication.

------

## Logical Replication State Machine

Logical replication has two types of workers: Sync and Apply.

Therefore, logical replication is logically divided into two parts: **each table replicates independently**, and when replication progress catches up to the latest position...

When creating or refreshing subscriptions, tables are added to the subscription set. Each table in the subscription set has a corresponding record in the `pg_subscription_rel` view, showing the current replication state of that table. Tables just added to the subscription set have initial state `i`, i.e., `initialize`, **initial state**.

If the subscription's `copy_data` option is true (default), and there are idle workers in the worker process pool, PostgreSQL will assign a synchronization worker process to this table to synchronize existing data on the table. At this time, the table's state enters `d`, i.e., **copying data**. Table data synchronization is similar to performing `basebackup` on a database cluster. The Sync Worker creates temporary replication slots on the publisher, gets snapshots on the table, and completes basic data synchronization through COPY.

After basic data copying on the table is complete, the table enters `sync` mode, i.e., **data synchronization**. The synchronization process will catch up on incremental changes that occurred during synchronization. When catch-up is complete, the synchronization process marks this table as `r` (ready) state and transfers it to the main logical replication Apply process for change management, indicating this table is in normal replication.

### 2.4 Waiting for Logical Replication Synchronization

After creating subscriptions, you must first monitor database logs on both **publisher and subscriber sides** to **ensure no errors occur**.

#### 2.4.1 Logical Replication State Machine

#### 2.4.2 Synchronization Progress Tracking

The data synchronization (`d`) phase may take some time, depending on network cards, network, disk, table size and distribution, number of logical replication sync workers, and other factors.

As reference, a 1TB database with 20 tables, including 250GB large tables, dual 10-gigabit network cards, with 6 data sync workers takes approximately 6-8 hours to complete replication.

During data synchronization, each table sync task creates temporary replication slots on the source database. Please ensure not to put unnecessary write pressure on the source primary during logical replication initial synchronization to avoid WAL disk space issues.

Publisher-side `pg_stat_replication`, `pg_replication_slots`, subscriber-side `pg_stat_subscription`, `pg_subscription_rel` provide logical replication status information that needs attention.

```sql
psql ${PGDST} -Xxw <<-'EOF'
    SELECT subname, json_object_agg(srsubstate, cnt) FROM
    pg_subscription s JOIN
      (SELECT srsubid, srsubstate, count(*) AS cnt FROM pg_subscription_rel 
       GROUP BY srsubid, srsubstate) sr
    ON s.oid = sr.srsubid GROUP BY subname;
EOF
```

You can use the following SQL to confirm table states in subscriptions. If all table states show as `r`, it indicates logical replication has been successfully established and the subscriber can be used for switching.

```bash
   subname   | json_object_agg
-------------+-----------------
 pg_test_sub | { "r" : 5 }
```

Of course, the best way is always to track replication status through monitoring systems.

------

## Sandbox Example

Using Pigsty's standard 4-node two-cluster sandbox as an example, with two database clusters `pg-meta` and `pg-test`. Now using `pg-meta-1` as publisher and `pg-test-1` as subscriber.

Usually the prerequisite for logical replication is that the publisher has `wal_level = logical` set and has a replication user that can be accessed normally with correct privileges.

Pigsty's default configuration already meets requirements and comes with a qualified replication user `replicator`. The following commands are all initiated from the meta node as `postgres` user, database user `dbuser_admin`, with `SUPERUSER` privileges.

```bash
PGSRC='postgres://dbuser_admin@meta-1/meta'        # Publisher
PGDST='postgres://dbuser_admin@node-1/test'        # Subscriber
```

### Preparing Logical Replication

Use the `pgbench` tool to initialize table structure in the `meta` database of the `pg-meta` cluster.

```bash
pgbench -is100 ${PGSRC}
```

Use `pg_dump` and `psql` to **synchronize** definitions of `pgbench*` related tables.

```bash
pg_dump -Oscx -t pgbench* -s ${PGSRC} | psql ${PGDST}
```

### Creating Publications and Subscriptions

Create **publication** on publisher, adding default `pgbench` related tables to the publication set.

```bash
psql ${PGSRC} -AXwt <<-'EOF'
CREATE PUBLICATION "pg_meta_pub" FOR TABLE
  pgbench_accounts,pgbench_branches,pgbench_history,pgbench_tellers;
EOF
```

Create **subscription** on subscriber, subscribing to publication on publisher.

```bash
psql ${PGDST} <<-'EOF'
CREATE SUBSCRIPTION pg_test_sub
  CONNECTION 'host=10.10.10.10 dbname=meta user=replicator' 
  PUBLICATION pg_meta_pub;
EOF
```

### Observing Replication Status

When all `pg_subscription_rel.srsubstate` become `r` (ready) state, logical replication is established.

```bash
$ psql ${PGDST} -c 'TABLE pg_subscription_rel;'
 srsubid | srrelid | srsubstate |  srsublsn
---------+---------+------------+------------
   20451 |   20433 | d          | NULL
   20451 |   20442 | r          | 0/4ECCDB78
   20451 |   20436 | r          | 0/4ECCDB78
   20451 |   20439 | r          | 0/4ECCDBB0
```

### Verifying Replicated Data

You can simply compare record counts and maximum/minimum values of replica identity columns on both publisher and subscriber sides to verify complete data replication.

```bash
function compare_relation(){
	local relname=$1
	local identity=${2-'id'}
	psql ${3-${PGPUB}} -AXtwc "SELECT count(*) AS cnt, max($identity) AS max, min($identity) AS min FROM ${relname};"
	psql ${4-${PGSUB}} -AXtwc "SELECT count(*) AS cnt, max($identity) AS max, min($identity) AS min FROM ${relname};"
}
compare_relation pgbench_accounts aid
compare_relation pgbench_branches bid
compare_relation pgbench_history  tid
compare_relation pgbench_tellers  tid
```

Further verification can be done by manually creating a record on the publisher and reading it from the subscriber.

```bash
$ psql ${PGPUB} -AXtwc 'INSERT INTO pgbench_accounts(aid,bid,abalance) VALUES (99999999,1,0);'
INSERT 0 1
$ psql ${PGSUB} -AXtwc 'SELECT * FROM pgbench_accounts WHERE aid = 99999999;'
99999999|1|0|
```

Now you have a working logical replication. Let's master the use and management of logical replication through a series of experiments and explore various potential issues.

------

## Logical Replication Experiments

### Adding Tables to Existing Publications

```sql
CREATE TABLE t_normal(id BIGSERIAL PRIMARY KEY,v  TIMESTAMP); -- Regular table with primary key
ALTER PUBLICATION pg_meta_pub ADD TABLE t_normal; -- Add newly created table to publication
```

If this table already exists on the subscriber side, it can enter normal logical replication flow: `i -> d -> s -> r`.

What if you add a table to publication that doesn't exist on the subscriber side? Then new subscriptions **cannot be created**. **Existing subscriptions cannot be refreshed**, but can maintain original replication.

If the subscription **doesn't exist yet**, creation will fail with an error: table not found on subscriber side. If subscription **already exists**, refresh command cannot be executed:

```sql
ALTER SUBSCRIPTION pg_test_sub REFRESH PUBLICATION;
```

If newly added tables have no writes, existing replication relationships won't change. Once newly added tables have changes, **replication conflicts** will immediately occur.

### Removing Tables from Publications

```sql
ALTER PUBLICATION pg_meta_pub ADD TABLE t_normal;
```

After removing from publication, subscriber side won't be affected. The effect is that changes to this table seem to disappear. After executing subscription refresh, this table will be removed from the subscription set.

Another situation is **renaming** tables in publications/subscriptions. When executing table rename on publisher side, publisher's publication set will immediately update accordingly. Although table names in subscription sets won't update immediately, as long as renamed tables have any changes and subscriber doesn't have corresponding tables, **replication conflicts** will immediately occur.

Similarly, when renaming tables on subscriber side, subscription's relation set will also refresh, but because publisher tables have no corresponding objects, if tables have no changes, everything continues as usual. Once changes occur, **replication conflicts** immediately appear.

Directly `DROP`ping tables on publisher side will also **remove the table from publication** without errors or impacts. But directly `DROP`ping tables on subscriber side may cause **problems**. When `DROP TABLE`, the table is also removed from subscription set. If publisher still has changes on this table, it will cause **replication conflicts**.

**So, table deletion should be done on publisher first, then subscriber.**

### Inconsistent Column Definitions Between Sides

Columns in tables on publisher and subscriber sides are matched by **name**. Column order doesn't matter.

**Subscriber tables having more columns usually has no impact**. Extra columns will be filled with default values (usually `NULL`).

Special note: if you want to add `NOT NULL` constraints to extra columns, you must configure a default value, otherwise constraint violations during changes will cause replication conflicts.

**If subscriber has fewer columns than publisher, replication conflicts will occur**. Adding a new column on publisher won't **immediately** cause replication conflicts; the first subsequent change will cause replication conflicts.

So when executing add column DDL changes, you can execute on subscriber first, then on publisher.

Column **data types don't need to be completely identical**, as long as the **text representation** of the two columns is compatible, meaning data's text representation can be converted to the target column type.

This means any type can be converted to TEXT type. `BIGINT` can also be converted to `INT` as long as no errors occur, but once overflow happens, **replication conflicts** will still occur.

### Correct Configuration of Replica Identity and Indexes

Replica identity configuration on tables and whether tables have indexes are two independent matters. Although various combinations are possible, in practice only three situations are feasible. Other situations cannot normally complete logical replication functionality (if no errors occur, it's usually lucky).

* Table has primary key, use default `default` replica identity, no additional configuration needed.
* Table has no primary key but has non-null unique index, explicitly configure `index` replica identity.
* Table has neither primary key nor non-null unique index, explicitly configure `full` replica identity (low efficiency, only as fallback).

| Replica Identity Mode\Table Constraints | Primary Key (p) | Non-null Unique Index (u) | Neither (n) |
|:------------:|:------:|:---------:|:-------:|
| **d**efault  | **Valid** |     x     |    x    |
|  **i**ndex   |   x    |  **Valid**   |    x    |
|   **f**ull   | **Inefficient** |  **Inefficient**   | **Inefficient**  |
| **n**othing  |   x    |     x     |    x    |

> In all cases, `INSERT` can be replicated normally. `x` represents missing key information needed for `DELETE|UPDATE` to complete normally.

The best approach is of course to fix beforehand, specifying primary keys for all tables. The following query can be used to find tables missing primary keys or non-null unique indexes:

```sql
SELECT quote_ident(nspname) || '.' || quote_ident(relname) AS name, con.ri AS keys,
       CASE relreplident WHEN 'd' THEN 'default' WHEN 'n' THEN 'nothing' WHEN 'f' THEN 'full' WHEN 'i' THEN 'index' END AS replica_identity
FROM pg_class c JOIN pg_namespace n ON c.relnamespace = n.oid, LATERAL (SELECT array_agg(contype) AS ri FROM pg_constraint WHERE conrelid = c.oid) con
WHERE relkind = 'r' AND nspname NOT IN ('pg_catalog', 'information_schema', 'monitor', 'repack', 'pg_toast')
ORDER BY 2,3;
```

Note: tables with `nothing` replica identity can be added to publications, but executing `UPDATE|DELETE` on them on the publisher will directly cause errors.

------

## Other Issues

### Q: Logical Replication Preparation

### Q: What Types of Tables Can Use Logical Replication?

### Q: Monitoring Logical Replication Status

### Q: Adding New Tables to Publications

### Q: Adding Tables Without Primary Keys to Publications?

### Q: How to Handle Tables Without Replica Identity?

### Q: How ALTER PUB Takes Effect

### Q: If Multiple Subscriptions Exist on the Same Publisher-Subscriber Pair with Overlapping Publication Tables?

### Q: What Are the Limitations on Table Definitions Between Subscribers and Publishers?

### Q: How pg_dump Handles Subscriptions

### Q: When Do You Need to Manually Manage Subscription Replication Slots?