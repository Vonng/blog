---
title: "Incident Report: Integer Overflow from Rapid Sequence Number Consumption"
date: 2018-07-20
author: "vonng"
summary: >
  If you use Integer sequences on tables, you should consider potential overflow scenarios.
tags: [PostgreSQL, PG Management, Incident Report]
---

-----------------

## 0x01 Overview

* Incident symptoms:
  * A table using auto-increment columns had sequence numbers reach the integer limit, preventing writes.
  * Discovered large gaps in auto-increment columns, with many sequence numbers consumed without corresponding records.
* Incident impact: Non-critical business table unable to write for about 10 minutes.

* Root cause:
  * Internal: Used INTEGER instead of BIGINT for primary key type.
  * External: Business team didn't understand `SEQUENCE` characteristics, executing many constraint-violating invalid inserts, wasting numerous sequence numbers.

* Fix approach:
  * Emergency operation: Downgrade online insert function to direct return, preventing error escalation.
  * Temporary solution: Create temporary table, generate 50 million temporary IDs from wasted gaps, modify insert function to check before inserting and take IDs from temporary ID table.
  * Long-term solution: Execute schema migration, update all related table primary key and foreign key types to Bigint.

-----------------

## Root Cause Analysis

### Internal Cause: Improper Type Usage

Business used 32-bit integers for primary key auto-increment IDs instead of Bigint.

* Unless there are special reasons, primary keys and auto-increment columns should use BIGINT type.

### External Cause: Unfamiliarity with Sequence Characteristics

- If frequent invalid inserts or frequent UPSERT usage occurs, attention must be paid to Sequence consumption issues.
- Consider using custom ID generation functions (Snowflake-like)

In PostgreSQL, Sequence is a special type. Particularly, sequence numbers consumed in transactions don't rollback. Since sequence numbers can be acquired concurrently, there's no logically reasonable rollback operation.

In production, we encountered this type of failure. A table directly used Serial as primary key:

```sql
CREATE TABLE sample(
	id   	SERIAL PRIMARY KEY,
	name  	TEXT UNIQUE,
    value   INTEGER
);
```

The insert was like this:

```sql
INSERT INTO sample(name, value) VALUES(?,?)
```

Due to the constraint on the `name` column, if duplicate `name` fields are inserted, the transaction will error and rollback. However, the sequence number is already consumed, and even if the transaction rolls back, the sequence number doesn't rollback.

```bash
vonng=# INSERT INTO sample(name, value) VALUES('Alice',1);
INSERT 0 1
vonng=# SELECT currval('sample_id_seq'::RegClass);
 currval
---------
       1
(1 row)

vonng=# INSERT INTO sample(name, value) VALUES('Alice',1);
ERROR:  duplicate key value violates unique constraint "sample_name_key"
DETAIL:  Key (name)=(Alice) already exists.
vonng=# SELECT currval('sample_id_seq'::RegClass);
 currval
---------
       2
(1 row)

vonng=# BEGIN;
BEGIN
vonng=# INSERT INTO sample(name, value) VALUES('Alice',1);
ERROR:  duplicate key value violates unique constraint "sample_name_key"
DETAIL:  Key (name)=(Alice) already exists.
vonng=# ROLLBACK;
ROLLBACK
vonng=# SELECT currval('sample_id_seq'::RegClass);
 currval
---------
       3
```

Therefore, when executed inserts have many duplicates, i.e., many conflicts, it may cause sequence numbers to be consumed very quickly. Large gaps appear!

Another point to note is that UPSERT operations also consume sequence numbers! From the behavior perspective, this means even if the actual operation is UPDATE rather than INSERT, a sequence number is still consumed.

```sql
vonng=# INSERT INTO sample(name, value) VALUES('Alice',3) ON CONFLICT(name) DO UPDATE SET value = EXCLUDED.value;
INSERT 0 1
vonng=# SELECT currval('sample_id_seq'::RegClass);
 currval
---------
       4
(1 row)

vonng=# INSERT INTO sample(name, value) VALUES('Alice',4) ON CONFLICT(name) DO UPDATE SET value = EXCLUDED.value;
INSERT 0 1
vonng=# SELECT currval('sample_id_seq'::RegClass);
 currval
---------
       5
(1 row)
```

-----------------

## Solution

All online queries and inserts use stored procedures. For non-critical business, brief write failures are acceptable. First downgrade insert function to prevent errors from affecting AppServer. Since the table has many dependencies, its type cannot be directly modified, requiring a temporary solution.

Investigation found large gaps in ID columns, with only 1% actually used out of every 10,000 sequence numbers. Therefore, use the following function to generate temporary ID table.

```sql
CREATE TABLE sample_temp_id(id INTEGER PRIMARY KEY);

-- Insert about 50 million temporary IDs, enough for dozens of days.
INSERT INTO sample_temp_id
    SELECT generate_series(2000000000,2100000000) as id EXCEPT SELECT id FROM sample;

-- Modify insert stored procedure to pop ID from temporary table.
DELETE FROM sample_temp_id WHERE id = (SELECT id FROM sample_temp_id FOR UPDATE LIMIT 1) RETURNING id;
```

Modify insert stored procedure to take an ID from temporary ID table each time, explicitly inserting into the table.

-----------------

## Lessons Learned

Use BIGINT when possible instead of INT, and pay special attention when using `UPSERT`.