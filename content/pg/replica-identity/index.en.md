---
title: "PG Replica Identity Explained"
linkTitle: "PG Replica Identity Explained"
date: 2021-03-03
author: |
  [Vonng](https://vonng.com)（[@Vonng](https://vonng.com/en/)）
summary: >
  Replica identity is important - it determines the success or failure of logical replication
---




## Introduction: DIY Logical Replication

The concept of replica identity serves [**logical replication**](/pg/logical-replication/).

The basic working principle of logical replication is to decode **row-level INSERT/UPDATE/DELETE** events from logical publication-related tables and replicate them for execution on logical subscribers.

Logical replication works somewhat like row-level triggers, firing on changed tuples row by row after transaction execution.

Suppose you need to implement logical replication yourself through triggers, replicating changes from table A to another table B. Typically, this trigger function logic would look like this:

```sql
-- Notification trigger
CREATE OR REPLACE FUNCTION replicate_change() RETURNS TRIGGER AS $$
BEGIN
  IF    (TG_OP = 'INSERT') THEN 
  -- INSERT INTO tbl_b VALUES (NEW.col);
  ELSIF (TG_OP = 'DELETE') THEN 
	-- DELETE tbl_b WHERE id = OLD.id;
  ELSIF (TG_OP = 'UPDATE') THEN 
	-- UPDATE tbl_b SET col = NEW.col,... WHERE id = OLD.id;
  END IF;
END; $$ LANGUAGE plpgsql;
```

The trigger contains two variables `OLD` and `NEW`, containing the old and new values of changed records respectively.

* `INSERT` operations only have the `NEW` variable because it's newly inserted, so we directly insert it into another table.
* `DELETE` operations only have the `OLD` variable because it only deletes existing records. We delete **by ID** in target table B.
* `UPDATE` operations have both `OLD` and `NEW` variables. We need to locate the record in target table B through `OLD.id` and update it to new values `NEW`.

Such trigger-based "logical replication" can perfectly achieve our purpose. In logical replication, table A has a primary key field `id`. So when we delete records from table A, for example: deleting the record with `id = 1`, we only need to tell the subscriber `id = 1`, rather than passing the entire deleted tuple to the subscriber. Here, the primary key column `id` is the **replica identity** for logical replication.

But the example above implies a working assumption: table A and table B have the same schema with a primary key named `id`.

For production-grade logical replication solutions, namely PostgreSQL's logical replication provided after version 10.0, **such working assumptions are unreasonable**. Because the system cannot require users to always create tables with primary keys, nor can it require primary keys to always be named `id`.

Thus, the concept of **Replica Identity** emerged. Replica identity is a further generalization and abstraction of the working assumption like `OLD.id`, used to tell the logical replication system **which information can be used to uniquely locate a record in a table**.




## Replica Identity

For logical replication, `INSERT` events don't need special handling, but to replicate `DELETE|UPDATE` to subscribers, a way to identify rows must be provided, namely **Replica Identity**. Replica identity is a **set of columns** that can uniquely identify a record. In concept, this definition is essentially **the set of columns forming a primary key**. Of course, non-null unique index columns (**candidate keys**) can also serve the same purpose.

A table included in a logical replication **publication** must be configured with **Replica Identity** to locate rows that need updating on the **subscriber** side, completing `UPDATE` and `DELETE` operation replication. By default, **Primary Key** and **UNIQUE NOT NULL indexes** can serve as replica identity.

Note that **replica identity** is not the same as primary keys or non-null unique indexes on tables. Replica identity is an **attribute** of the table that specifies which information will be used as identity locator identifiers written into logical replication records for subscribers to locate and execute changes.

As described in PostgreSQL 13 [official documentation](https://www.postgresql.org/docs/13/sql-altertable.html#replica_identity), tables have 4 configuration modes for **replica identity**:

* Default mode (default): Default mode for non-system tables. If there's a primary key, use primary key columns as identity; otherwise use full mode.
* Index mode (index): Use columns from a qualifying index as identity
* Full mode (full): Use all columns in the entire row as replica identity (like all columns in the table forming a primary key together)
* Nothing mode (nothing): No replica identity recorded, meaning `UPDATE|DELETE` operations cannot be replicated to subscribers.

### Querying Replica Identity

Table **replica identity** can be obtained by checking `pg_class.relreplident`.

This is a character-type "enum" identifying columns used to assemble "replica identity": `d` = default, `f` = all columns, `i` = use specific index, `n` = no replica identity.

Whether a table has index constraints available as replica identity can be obtained through this query:

```sql
SELECT quote_ident(nspname) || '.' || quote_ident(relname) AS name, con.ri AS keys,
       CASE relreplident WHEN 'd' THEN 'default' WHEN 'n' THEN 'nothing' WHEN 'f' THEN 'full' WHEN 'i' THEN 'index' END AS replica_identity
FROM pg_class c JOIN pg_namespace n ON c.relnamespace = n.oid, LATERAL (SELECT array_agg(contype) AS ri FROM pg_constraint WHERE conrelid = c.oid) con
WHERE relkind = 'r' AND nspname NOT IN ('pg_catalog', 'information_schema', 'monitor', 'repack', 'pg_toast')
ORDER BY 2,3;
```

### Configuring Replica Identity

Table replica identity can be modified through `ALTER TABLE`.

```sql
ALTER TABLE tbl REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING };
-- Specifically four forms
ALTER TABLE t_normal REPLICA IDENTITY DEFAULT;                    -- Use primary key, FULL if no primary key
ALTER TABLE t_normal REPLICA IDENTITY FULL;                       -- Use entire row as identity
ALTER TABLE t_normal REPLICA IDENTITY USING INDEX t_normal_v_key; -- Use unique index
ALTER TABLE t_normal REPLICA IDENTITY NOTHING;                    -- Don't set replica identity
```



## Replica Identity Examples

Here's a concrete example illustrating replica identity effects:

```sql
CREATE TABLE test(k text primary key, v int not null unique);
```

Now we have table `test` with two columns `k` and `v`.

```sql
INSERT INTO test VALUES('Alice', '1'), ('Bob', '2');
UPDATE test SET v = '3' WHERE k = 'Alice';    -- update Alice value to 3
UPDATE test SET k = 'Oscar' WHERE k = 'Bob';  -- rename Bob to Oscar
DELETE FROM test WHERE k = 'Alice';           -- delete Alice
```

In this example, we performed INSERT/UPDATE/DELETE operations on table `test`. The corresponding logical decoding results are:

```ini
table public.test: INSERT: k[text]:'Alice' v[integer]:1
table public.test: INSERT: k[text]:'Bob' v[integer]:2
table public.test: UPDATE: k[text]:'Alice' v[integer]:3
table public.test: UPDATE: old-key: k[text]:'Bob' new-tuple: k[text]:'Oscar' v[integer]:2
table public.test: DELETE: k[text]:'Alice'
```

By default, PostgreSQL uses the table's primary key as **replica identity**. Therefore, in `UPDATE|DELETE` operations, column `k` is used to locate records needing modification.

If we manually modify the table's replica identity to use non-null unique column `v` as replica identity, that's also possible:

```sql
ALTER TABLE test REPLICA IDENTITY USING INDEX test_v_key; -- Replica identity based on UNIQUE index
```

The same changes now produce the following logical decoding results, where `v` appears as identity in all `UPDATE|DELETE` events.

```ini
table public.test: INSERT: k[text]:'Alice' v[integer]:1
table public.test: INSERT: k[text]:'Bob' v[integer]:2
table public.test: UPDATE: old-key: v[integer]:1 new-tuple: k[text]:'Alice' v[integer]:3
table public.test: UPDATE: k[text]:'Oscar' v[integer]:2
table public.test: DELETE: v[integer]:3
```

If using **full identity mode (full)**

```sql
ALTER TABLE test REPLICA IDENTITY FULL; -- Table test now uses all columns as replica identity
```

Here, both `k` and `v` serve as identity, recorded in `UPDATE|DELETE` logs. For tables without primary keys, this is a fallback solution.

```ini
table public.test: INSERT: k[text]:'Alice' v[integer]:1
table public.test: INSERT: k[text]:'Bob' v[integer]:2
table public.test: UPDATE: old-key: k[text]:'Alice' v[integer]:1 new-tuple: k[text]:'Alice' v[integer]:3
table public.test: UPDATE: old-key: k[text]:'Bob' v[integer]:2 new-tuple: k[text]:'Oscar' v[integer]:2
table public.test: DELETE: k[text]:'Alice' v[integer]:3
```

If using **nothing mode (nothing)**

```sql
ALTER TABLE test REPLICA IDENTITY NOTHING; -- Table test now has no replica identity
```

Then logical decoding records only contain new records in `UPDATE` operations without old record unique identity, while `DELETE` operations contain no information at all.

```ini
table public.test: INSERT: k[text]:'Alice' v[integer]:1
table public.test: INSERT: k[text]:'Bob' v[integer]:2
table public.test: UPDATE: k[text]:'Alice' v[integer]:3
table public.test: UPDATE: k[text]:'Oscar' v[integer]:2
table public.test: DELETE: (no-tuple-data)
```

Such logical change logs are completely useless for subscribers. In actual usage, executing `DELETE|UPDATE` on tables without replica identity in logical replication will directly error.



## Replica Identity Details

Table replica identity configuration and whether the table has indexes are relatively orthogonal factors.

Although various combinations are possible, only three situations are feasible in actual usage:

* Table has primary key, uses default `default` replica identity
* Table has no primary key but has non-null unique index, explicitly configure `index` replica identity
* Table has neither primary key nor non-null unique index, explicitly configure `full` replica identity (very inefficient, only as fallback)
* All other situations cannot complete logical replication functionality properly

| Replica Identity\Table Constraints | Primary Key(p) | Non-null Unique Index(u) | Neither(n) |
| :---------------------------------: | :------------: | :----------------------: | :--------: |
|          **d**efault                |   **Valid**    |            x             |     x      |
|           **i**ndex                 |       x        |        **Valid**         |     x      |
|           **f**ull                  |  **Low Eff**   |       **Low Eff**        | **Low Eff** |
|          **n**othing                |       x        |            x             |     x      |

Below, we'll consider some edge cases.

### Rebuilding Primary Key

Suppose due to index bloat, we want to rebuild the primary key index on the table to reclaim space.

```sql
CREATE TABLE test(k text primary key, v int);
CREATE UNIQUE INDEX test_pkey2 ON test(k);
BEGIN;
ALTER TABLE test DROP CONSTRAINT test_pkey;
ALTER TABLE test ADD PRIMARY KEY USING INDEX test_pkey2;
COMMIT;
```

In `default` mode, rebuilding and replacing primary key constraints and indexes **will not** affect replica identity.

### Rebuilding Unique Index

Suppose due to index bloat, we want to rebuild the non-null unique index on the table to reclaim space.

```sql
CREATE TABLE test(k text, v int not null unique);
ALTER TABLE test REPLICA IDENTITY USING INDEX test_v_key;
CREATE UNIQUE INDEX test_v_key2 ON test(v);
-- Replace old Unique index with new test_v_key2 index
BEGIN;
ALTER TABLE test ADD UNIQUE USING INDEX test_v_key2;
ALTER TABLE test DROP CONSTRAINT test_v_key;
COMMIT;
```

Unlike `default` mode, in `index` mode, replica identity is bound to a **specific** index:

```sql
                                    Table "public.test"
 Column |  Type   | Collation | Nullable | Default | Storage  | Stats target | Description
--------+---------+-----------+----------+---------+----------+--------------+-------------
 k      | text    |           |          |         | extended |              |
 v      | integer |           | not null |         | plain    |              |
Indexes:
    "test_v_key" UNIQUE CONSTRAINT, btree (v) REPLICA IDENTITY
    "test_v_key2" UNIQUE CONSTRAINT, btree (v)
```

This means replacing UNIQUE indexes with sleight of hand will cause replica identity loss.

There are two solutions:

1. Use `REINDEX INDEX (CONCURRENTLY)` to rebuild the index, which won't lose replica identity information.
2. When replacing the index, also refresh the table's default replica identity:

```sql
BEGIN;
ALTER TABLE test ADD UNIQUE USING INDEX test_v_key2;
ALTER TABLE test REPLICA IDENTITY USING INDEX test_v_key2;
ALTER TABLE test DROP CONSTRAINT test_v_key;
COMMIT;
```

Incidentally, removing an index serving as identity makes it equivalent to `nothing` mode despite table configuration still showing `index` mode. So don't casually mess with indexes serving as identity.

### Using Unqualified Index as Replica Identity

Replica identity requires a unique, non-deferrable, table-wide index built on non-null column sets.

The most classic example is primary key indexes and single-column non-null indexes declared through `col type NOT NULL UNIQUE`.

The requirement for NOT NULL is because NULL values cannot be compared for equality, so tables allow multiple records with `NULL` values in UNIQUE columns. Allowing null values means this column cannot uniquely identify records. Attempting to use a regular `UNIQUE` index (columns without non-null constraints) as replica identity will error.

```ini
[42809] ERROR: index "t_normal_v_key" cannot be used as replica identity because column "v" is nullable
```



### Using FULL Replica Identity

If there's no replica identity available, you can set replica identity to `FULL`, treating the entire row as replica identity.

Using `FULL` mode replica identity is very inefficient, so this configuration can only be a fallback solution or used for very small tables. Because every row modification requires a **full table scan** on subscribers, which **can easily drag down subscribers**.

#### FULL Mode Limitations

Using `FULL` mode replica identity has one limitation: columns contained in subscriber-side table replica identity must either match the publisher or be fewer than the publisher, otherwise correctness cannot be guaranteed. Here's a specific example.

Suppose both publisher and subscriber tables use `FULL` replica identity, but the subscriber-side table has one more column than the publisher (yes, logical replication allows subscriber tables to have columns that publisher tables don't have). In this case, subscriber-side table replica identity contains more columns than publisher-side. Suppose deleting record `(f1=a, f2=a)` on publisher would cause deletion of two records meeting identity equivalence conditions on subscriber.

```
     (Publication)       ------>           (Subscription)
|--- f1 ---|--- f2 ---|          |--- f1 ---|--- f2 ---|--- f3 ---|
|    a     |     a    |          |    a     |     a    |     b    |
                                 |    a     |     a    |     c    |
```

#### How FULL Mode Handles Duplicate Row Issues

PostgreSQL's logical replication can "correctly" handle scenarios with identical rows in `FULL` mode. Suppose there's such a poorly designed table with multiple identical records.

```sql
CREATE TABLE shitty_table(
	 f1  TEXT,
	 f2  TEXT,
	 f3  TEXT
);
INSERT INTO shitty_table VALUES ('a', 'a', 'a'), ('a', 'a', 'a'), ('a', 'a', 'a');
```

In FULL mode, the entire row serves as replica identity. Suppose we cheat using ctid scan and delete one of the three identical records.

```sql
# SELECT ctid,* FROM shitty_table;
 ctid  | a | b | c
-------+---+---+---
 (0,1) | a | a | a
 (0,2) | a | a | a
 (0,3) | a | a | a

# DELETE FROM shitty_table WHERE ctid = '(0,1)';
DELETE 1

# SELECT ctid,* FROM shitty_table;
 ctid  | a | b | c
-------+---+---+---
 (0,2) | a | a | a
 (0,3) | a | a | a
```

Logically, using the entire row as identity means subscribers would execute the following logic, causing all 3 records to be deleted.

```sql
DELETE FROM shitty_table WHERE f1 = 'a' AND f2 = 'a' AND f3 = 'a'
```

But in reality, because PostgreSQL's change records are tuple-based, this change only affects the **first matching** record, so subscriber-side behavior is also deleting 1 out of 3 rows. This is logically equivalent to the publisher.