---
title: "Online Primary Key Column Type Change"
linkTitle: "Online Primary Key Column Type Change"
date: 2021-01-15
author: vonng
summary: >
  How to change column types online, such as upgrading from INT to BIGINT?
tags: [PostgreSQL,PG Administration]
---

> Author: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))

How to change primary key column types online, such as upgrading from `INT` to `BIGINT`, without affecting business operations?

Suppose you have a table in PostgreSQL where you initially chose an INT primary key without much thought, but now your business is thriving and you're running out of sequence numbers, so you want to upgrade to BIGINT type. What should you do?

The obvious approach would be to directly use DDL to modify the type:

```sql
ALTER TABLE pgbench_accounts ALTER COLUMN aid SET DATA TYPE BIGINT;
```

But this approach is not feasible for frequently accessed large production tables.

------------------

## TL;DR

Let's use pgbench's built-in scenario as an example:

```sql
-- Goal: upgrade pgbench_accounts table regular column abalance type: INT -> BIGINT

-- Add new column: abalance_tmp BIGINT
ALTER TABLE pgbench_accounts ADD COLUMN abalance_tmp BIGINT;

-- Create trigger function: keep new column data synchronized with old column
CREATE OR REPLACE FUNCTION public.sync_pgbench_accounts_abalance() RETURNS TRIGGER AS $$
BEGIN NEW.abalance_tmp = NEW.abalance; RETURN NEW;END;
$$ LANGUAGE 'plpgsql';

-- Complete full table update, see batch update method below
UPDATE pgbench_accounts SET abalance_tmp = abalance; -- don't run this on large tables

-- Create trigger
CREATE TRIGGER tg_sync_pgbench_accounts_abalance BEFORE INSERT OR UPDATE ON pgbench_accounts
    FOR EACH ROW EXECUTE FUNCTION sync_pgbench_accounts_abalance();

-- Complete column switch, data sync direction changes - old column data syncs with new column
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

------------------

## Foreign Keys

```sql
alter table my_table add column new_id bigint;

begin; update my_table set new_id = id where id between 0 and 100000; commit;
begin; update my_table set new_id = id where id between 100001 and 200000; commit;
begin; update my_table set new_id = id where id between 200001 and 300000; commit;
begin; update my_table set new_id = id where id between 300001 and 400000; commit;
...

create unique index my_table_pk_idx on my_table(new_id);

begin;
alter table my_table drop constraint my_table_pk;
alter table my_table alter column new_id set default nextval('my_table_id_seq'::regclass);
update my_table set new_id = id where new_id is null;
alter table my_table add constraint my_table_pk primary key using index my_table_pk_idx;
alter table my_table drop column id;
alter table my_table rename column new_id to id;
commit;
```

------------------

## Using pgbench as Example

```sql
vonng=# \d pgbench_accounts
              Table "public.pgbench_accounts"
  Column  |     Type      | Collation | Nullable | Default
----------+---------------+-----------+----------+---------
 aid      | integer       |           | not null |
 bid      | integer       |           |          |
 abalance | integer       |           |          |
 filler   | character(84) |           |          |
Indexes:
    "pgbench_accounts_pkey" PRIMARY KEY, btree (aid)
```

Upgrading the `abalance` column to BIGINT.

This will lock the table and can be used when table size is very small and access volume is very low.

```sql
ALTER TABLE pgbench_accounts ALTER COLUMN abalance SET DATA TYPE bigint;
```

------------------

## Online Upgrade Process

1. Add new column
2. Update data
3. Create related indexes on new column (optional for single column, can speed up step 4)
4. Execute switch **transaction**
   1. Exclusive table lock
   2. UPDATE empty columns (can also use triggers)
   3. Drop old column
   4. Rename new column

```sql
-- Step 1: Create new column
ALTER TABLE pgbench_accounts ADD COLUMN abalance_new BIGINT;

-- Step 2: Update data, can batch update, batch update method detailed below
UPDATE pgbench_accounts SET abalance_new = abalance;

-- Step 3: Optional (create index on new column)
CREATE INDEX CONCURRENTLY ON public.pgbench_accounts (abalance_new);
UPDATE pgbench_accounts SET abalance_new = abalance WHERE ;

-- Step 3:

-- Step 4:
```

```sql
-- Sync update corresponding column
CREATE OR REPLACE FUNCTION public.sync_abalance() RETURNS TRIGGER AS $$
BEGIN NEW.abalance_new = OLD.abalance; RETURN NEW;END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER pgbench_accounts_sync_abalance BEFORE INSERT OR UPDATE ON pgbench_accounts EXECUTE FUNCTION sync_abalance();
```

```sql
alter table my_table add column new_id bigint;

begin; update my_table set new_id = id where id between 0 and 100000; commit;
begin; update my_table set new_id = id where id between 100001 and 200000; commit;
begin; update my_table set new_id = id where id between 200001 and 300000; commit;
begin; update my_table set new_id = id where id between 300001 and 400000; commit;
...

create unique index my_table_pk_idx on my_table(new_id);

begin;
alter table my_table drop constraint my_table_pk;
alter table my_table alter column new_id set default nextval('my_table_id_seq'::regclass);
update my_table set new_id = id where new_id is null;
alter table my_table add constraint my_table_pk primary key using index my_table_pk_idx;
alter table my_table drop column id;
alter table my_table rename column new_id to id;
commit;
```

------------------

## Batch Update Logic

Sometimes you need to add a non-null column with default values to large tables. Therefore, you need to perform a full table update once, which can be done using the method below to split one huge update into 100 or more smaller updates.

Get primary key bucket information from statistics:

```sql
SELECT unnest(histogram_bounds::TEXT::BIGINT[]) FROM pg_stats WHERE tablename = 'signup_users' and attname = 'id';
```

Generate SQL statements directly from statistical bucket information - change the SQL here to the update statement needed:

```bash
SELECT 'UPDATE signup_users SET app_type = '''' WHERE id BETWEEN ' || lo::TEXT || ' AND ' || hi::TEXT || ';'
FROM (
         SELECT lo, lead(lo) OVER (ORDER BY lo) as hi
         FROM (
                  SELECT unnest(histogram_bounds::TEXT::BIGINT[]) lo
                  FROM pg_stats
                  WHERE tablename = 'signup_users'
                    and attname = 'id'
                  ORDER BY 1
              ) t1
     ) t2;
```

Use shell script to print update statements directly:

```bash
DATNAME=""
RELNAME="pgbench_accounts"
IDENTITY="aid"
UPDATE_CLAUSE="abalance_new = abalance"

SQL=$(cat <<-EOF
SELECT 'UPDATE ${RELNAME} SET ${UPDATE_CLAUSE} WHERE ${IDENTITY} BETWEEN ' || lo::TEXT || ' AND ' || hi::TEXT || ';'
FROM (
		SELECT lo, lead(lo) OVER (ORDER BY lo) as hi
		FROM (
				SELECT unnest(histogram_bounds::TEXT::BIGINT[]) lo
				FROM pg_stats
				WHERE tablename = '${RELNAME}'
					and attname = '${IDENTITY}'
				ORDER BY 1
			) t1
	) t2;
EOF
)

# echo $SQL

psql ${DATNAME} -qAXwtc "ANALYZE ${RELNAME};"
psql ${DATNAME} -qAXwtc "${SQL}"
```

Handle boundary cases:

```bash
 UPDATE signup_users SET app_type = '' WHERE app_type != '';
```

------------------

## Optimization and Improvement

Can also add transaction statements and sleep intervals:

```sql
DATNAME="test"
RELNAME="pgbench_accounts"
COLNAME="aid"
UPDATE_CLAUSE="abalance_tmp = abalance"
SLEEP_INTERVAL=0.1

SQL=$(cat <<-EOF
SELECT 'BEGIN;UPDATE ${RELNAME} SET ${UPDATE_CLAUSE} WHERE ${COLNAME} BETWEEN ' || lo::TEXT || ' AND ' || hi::TEXT || ';COMMIT;SELECT pg_sleep(${SLEEP_INTERVAL});VACUUM ${RELNAME};'
FROM (
		SELECT lo, lead(lo) OVER (ORDER BY lo) as hi
		FROM (
				SELECT unnest(histogram_bounds::TEXT::BIGINT[]) lo
				FROM pg_stats
				WHERE tablename = '${RELNAME}'
					and attname = '${COLNAME}'
				ORDER BY 1
			) t1
	) t2;
EOF
)
# echo $SQL
psql ${DATNAME} -qAXwtc "ANALYZE ${RELNAME};"
psql ${DATNAME} -qAXwtc "${SQL}"
```

```sql
BEGIN;UPDATE pgbench_accounts SET abalance_new = abalance WHERE aid BETWEEN 397 AND 103196;COMMIT;SELECT pg_sleep(0.5);VACUUM pgbench_accounts;
BEGIN;UPDATE pgbench_accounts SET abalance_new = abalance WHERE aid BETWEEN 103196 AND 213490;COMMIT;SELECT pg_sleep(0.5);VACUUM pgbench_accounts;
BEGIN;UPDATE pgbench_accounts SET abalance_new = abalance WHERE aid BETWEEN 213490 AND 301811;COMMIT;SELECT pg_sleep(0.5);VACUUM pgbench_accounts;
BEGIN;UPDATE pgbench_accounts SET abalance_new = abalance WHERE aid BETWEEN 301811 AND 400003;COMMIT;SELECT pg_sleep(0.5);VACUUM pgbench_accounts;
BEGIN;UPDATE pgbench_accounts SET abalance_new = abalance WHERE aid BETWEEN 400003 AND 511931;COMMIT;SELECT pg_sleep(0.5);VACUUM pgbench_accounts;
BEGIN;UPDATE pgbench_accounts SET abalance_new = abalance WHERE aid BETWEEN 511931 AND 613890;COMMIT;SELECT pg_sleep(0.5);VACUUM pgbench_accounts;
```