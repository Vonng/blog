---
title: "Online PostgreSQL Column Type Migration"
date: 2020-01-30
author: "vonng"
summary: "How to modify PostgreSQL column types online? A general approach"
tags: ["PostgreSQL","PG Management","Migration"]
---

## Scenario

In the lifecycle of a database, there's a common type of requirement: modifying column types. For example:

* Using `INT` as a primary key, only to discover that business is booming and the 2.1 billion limit of INT32 isn't enough, wanting to upgrade to `BIGINT`
* Using `BIGINT` to store ID numbers, only to discover there's an `X` in them requiring change to `TEXT` type
* Using `FLOAT` to store currency, discovering precision loss and wanting to change to Decimal
* Using `TEXT` to store JSON fields, wanting to use PostgreSQL's JSON features and change to JSONB type

So how do we handle this kind of requirement?

## Conventional Approach

Typically, `ALTER TABLE` can be used to modify column types.

```sql
ALTER TABLE tbl_name ALTER col_name TYPE new_type USING expression;
```

Modifying column types usually **rewrites** the entire table. As a special case, if the modified type is [binary compatible](https://www.postgresql.org/docs/13/sql-createcast.html) with the previous type, the **table rewrite** process can be skipped, but if there are indexes on the column, **indexes still need to be rebuilt**. Binary compatible conversions can be listed with the following query:

```sql
SELECT t1.typname AS from, t2.typname AS To
FROM pg_cast c
         join pg_type t1 on c.castsource = t1.oid
         join pg_type t2 on c.casttarget = t2.oid
where c.castmethod = 'b';
```

Excluding PostgreSQL internal types, binary compatible type conversions are as follows:

```
text     → varchar 
xml      → varchar 
xml      → text    
cidr     → inet    
varchar  → text    
bit      → varbit  
varbit   → bit     
```

Common binary compatible type conversions are basically these two types:

* varchar(n1) →  varchar(n2)  (n2 ≥ n1) (quite common, expanding length constraints won't rewrite, shrinking will rewrite)

* varchar ↔  text (synonymous conversion, basically useless)

This means all other type conversions involve table **rewriting**. Large table rewrites are slow, potentially taking minutes to tens of hours. Once **rewriting** occurs, the table will have `AccessExclusiveLock`, blocking all concurrent access.

If it's a toy database, or the business hasn't gone live yet, or the business doesn't care about downtime duration, then the full table rewrite approach is certainly fine. But most of the time, business simply cannot accept such downtime. Therefore, we need an online upgrade method. Complete column type transformation without **downtime**.

## Basic Approach

The basic principle of online column modification is as follows:

* Create a new temporary column with the new type

* Synchronize data from old column to new temporary column

  * Stock synchronization: batch updates
  * Incremental synchronization: update triggers

* Handle column dependencies: indexes

* Execute the switch

  * Handle column dependencies: constraints, default values, partitions, inheritance, triggers

  * Complete old/new column switching through column renaming

Online transformation addresses **lock granularity splitting**, equivalently replacing one **long-term heavy lock** operation with multiple **instantaneous light lock** operations.

The original `ALTER TYPE` rewrite process would acquire `AccessExclusiveLock`, blocking all concurrent access for minutes to days.

* Add new column: instant completion: `AccessExclusiveLock`
* Sync new column-incremental: create trigger, instant completion, low lock level
* Sync new column-stock: batch UPDATE, small amounts frequently, each can **complete quickly**, low lock level
* Old/new switching: lock table, instant completion

Let's use `pgbench`'s default use case to illustrate the basic principle of online column modification. Suppose we want to modify the `abalance` field type from `INT` to `BIGINT` in `pgbench_accounts` while it's being accessed, how should we handle this?

1. First, create a new column named `abalance_tmp` with type `BIGINT` for `pgbench_accounts`.
2. Write and create column synchronization trigger, which will sync from old column `abalance` to

Details are as follows:

```sql
-- Target operation: upgrade pgbench_accounts table regular column abalance type: INT -> BIGINT

-- Add new column: abalance_tmp BIGINT
ALTER TABLE pgbench_accounts ADD COLUMN abalance_tmp BIGINT;

-- Create trigger function: keep new column data synchronized with old column
CREATE OR REPLACE FUNCTION public.sync_pgbench_accounts_abalance() RETURNS TRIGGER AS $$
BEGIN NEW.abalance_tmp = NEW.abalance; RETURN NEW;END;
$$ LANGUAGE 'plpgsql';

-- Complete full table update, see below for batch update method
UPDATE pgbench_accounts SET abalance_tmp = abalance; -- Don't run this on large tables

-- Create trigger
CREATE TRIGGER tg_sync_pgbench_accounts_abalance BEFORE INSERT OR UPDATE ON pgbench_accounts
    FOR EACH ROW EXECUTE FUNCTION sync_pgbench_accounts_abalance();

-- Complete old/new column switching, at this point data sync direction changes - old column data stays in sync with new column
BEGIN;
LOCK TABLE pgbench_accounts IN EXCLUSIVE MODE;
ALTER TABLE pgbench_accounts DISABLE TRIGGER tg_sync_pgbench_accounts_abalance;
ALTER TABLE pgbench_accounts RENAME COLUMN abalance TO abalance_old;
ALTER TABLE pgbench_accounts RENAME COLUMN abalance_tmp TO abalance;
ALTER TABLE pgbench_accounts RENAME COLUMN abalance_old TO abalance_tmp;
ALTER TABLE pgbench_accounts ENABLE TRIGGER tg_sync_pgbench_accounts_abalance;
COMMIT;

-- Verify data integrity
SELECT count(*) FROM pgbench_accounts WHERE abalance_new != abalance;

-- Clean up trigger and function
DROP FUNCTION IF EXISTS sync_pgbench_accounts_abalance();
DROP TRIGGER tg_sync_pgbench_accounts_abalance ON pgbench_accounts;
```

## Considerations

1. MVCC safety of ALTER TABLE
2. What if there are constraints on the column? (PrimaryKey, ForeignKey, Unique, NotNULL)
3. What if there are indexes on the column?
4. Primary-replica replication lag caused by ALTER TABLE