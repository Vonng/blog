---
title: "Transaction Isolation Level Considerations"
date: 2019-11-12
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  PostgreSQL actually has only two transaction isolation levels: **Read Committed** and **Serializable**
tags: [PostgreSQL,PG Development]
---


PostgreSQL actually has only two transaction isolation levels: **Read Committed** and **Serializable**

---------------------

## Basics

The SQL standard defines four isolation levels, but PostgreSQL actually has only two transaction isolation levels: **Read Committed** and **Serializable**

The SQL standard defines four isolation levels, but actually this is a rather crude classification. For details, please refer to [Concurrency Anomalies](/db/concurrent-control/).



## Viewing/Setting Transaction Isolation Levels

You can view the current transaction isolation level by executing: `SELECT current_setting('transaction_isolation');`

Set the transaction isolation level by executing `SET TRANSACTION ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }` at the top of a transaction block.

Or set the transaction isolation level for the current session lifetime:

`SET SESSION CHARACTERISTICS AS TRANSACTION transaction_mode`



| Actual isolation level     | P4 | G-single | G2-item | G2 |
|----------------------------|----|----------|---------|----|
| RC（monotonic atomic views） | -  | -        | -       | -  |
| RR（snapshot isolation）     | ✓  | ✓        | -       | -  |
| Serializable               | ✓  | ✓        | ✓       | ✓  |


## Isolation Levels and Concurrency Issues

Create test table `t` and insert two rows of test data.

```sql
CREATE TABLE t (k INTEGER PRIMARY KEY, v int);
TRUNCATE t; INSERT INTO t VALUES (1,10), (2,20);
```



## Lost Update (P4)

PostgreSQL's **Read Committed (RC)** isolation level cannot prevent lost update problems, but the repeatable read isolation level can.

Lost update, as the name suggests, is when one transaction's write overwrites another transaction's write result.

Under the read committed isolation level, lost update problems cannot be prevented. Consider a counter concurrent update example where two transactions simultaneously read a value from the counter, add 1, and write back to the original table.

|                 T1                  |                 T2                  | Comment  |
|:-----------------------------------:|:-----------------------------------:|:--------:|
|             ` begin; `              |                                     |          |
|                                     |              ` begin;`              |          |
|    `SELECT v FROM t WHERE k = 1`    |                                     |   T1 reads    |
|                                     |    `SELECT v FROM t WHERE k = 1`    |   T2 reads    |
| `update t set v = 11 where k = 1; ` |                                     |   T1 writes    |
|                                     | ` update t set v = 11 where k = 1;` | T2 blocked by T1  |
|              `COMMIT`               |                                     | T2 resumes, writes  |
|                                     |              `COMMIT`               | T2 write overwrites T1 |

There are two ways to solve this problem: use atomic operations, or execute transactions at the repeatable read isolation level.

Using atomic operations:

|                  T1                  |                   T2                   | Comment  |
|:------------------------------------:|:--------------------------------------:|:--------:|
|              ` begin; `              |                                        |          |
|                                      |               ` begin;`                |          |
| `update t set v = v+1 where k = 1; ` |                                        |   T1 writes    |
|                                      | ` update t set v = v + 1 where k = 1;` | T2 blocked by T1  |
|               `COMMIT`               |                                        | T2 resumes, writes  |
|                                      |                `COMMIT`                | T2 write overwrites T1 |

There are two ways to solve this problem: use atomic operations, or execute transactions at the repeatable read isolation level.

At the repeatable read isolation level




## Read Committed (RC)

```sql
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2

update t set v = 11 where k = 1; -- T1
update t set v = 12 where k = 1; -- T2, BLOCKS
update t set v = 21 where k = 2; -- T1

commit; -- T1. This unblocks T2
select * from t; -- T1. Shows 1 => 11, 2 => 21
update t set v = 22 where k = 2; -- T2


commit; -- T2
select * from test; -- either. Shows 1 => 12, 2 => 22
```



|                            T1                             |                            T2                             |     Comment     |
|:---------------------------------------------------------:|:---------------------------------------------------------:|:---------------:|
| ` begin; set transaction isolation level read committed;` |                                                           |                 |
|                                                           | ` begin; set transaction isolation level read committed;` |                 |
|            `update t set v = 11 where k = 1; `            |                                                           |                 |
|                                                           |            ` update t set v = 12 where k = 1;`            |   T2 waits for T1's lock   |
|                     `SELECT * FROM t`                     |                                                           |   2:20, 1:11    |
|          ` update pair set v = 21 where k = 2;`           |                                                           |                 |
|                        ` commit;`                         |                                                           |      T2 unlocks       |
|                                                           |                  ` select * from pair;`                   | T2 sees T1's results and its own changes |
|                                                           |            ` update t set v = 22 where k = 2`             |                 |
|                                                           |                         `commit`                          |                 |

Result after commit



1

```bash
 relname | locktype | virtualtransaction |  pid  |       mode       | granted | fastpath
---------+----------+--------------------+-------+------------------+---------+----------
 t_pkey  | relation | 4/578              | 37670 | RowExclusiveLock | t       | t
 t       | relation | 4/578              | 37670 | RowExclusiveLock | t       | t
```

```bash
 relname | locktype | virtualtransaction |  pid  |       mode       | granted | fastpath
---------+----------+--------------------+-------+------------------+---------+----------
 t_pkey  | relation | 4/578              | 37670 | RowExclusiveLock | t       | t
 t       | relation | 4/578              | 37670 | RowExclusiveLock | t       | t
 t_pkey  | relation | 6/494              | 37672 | RowExclusiveLock | t       | t
 t       | relation | 6/494              | 37672 | RowExclusiveLock | t       | t
 t       | tuple    | 6/494              | 37672 | ExclusiveLock    | t       | f
```

```bash
 relname | locktype | virtualtransaction |  pid  |       mode       | granted | fastpath
---------+----------+--------------------+-------+------------------+---------+----------
 t_pkey  | relation | 4/578              | 37670 | RowExclusiveLock | t       | t
 t       | relation | 4/578              | 37670 | RowExclusiveLock | t       | t
 t_pkey  | relation | 6/494              | 37672 | RowExclusiveLock | t       | t
 t       | relation | 6/494              | 37672 | RowExclusiveLock | t       | t
 t       | tuple    | 6/494              | 37672 | ExclusiveLock    | t       | f
```




# Testing PostgreSQL transaction isolation levels

These tests were run with Postgres 9.3.5.

Setup (before every test case):

```
create table test (id int primary key, value int);
insert into test (id, value) values (1, 10), (2, 20);
```

To see the current isolation level:

```
select current_setting('transaction_isolation');
```

## Read Committed basic requirements (G0, G1a, G1b, G1c)

Postgres "read committed" prevents Write Cycles (G0) by locking updated rows:

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
update test set value = 11 where id = 1; -- T1
update test set value = 12 where id = 1; -- T2, BLOCKS
update test set value = 21 where id = 2; -- T1
commit; -- T1. This unblocks T2
select * from test; -- T1. Shows 1 => 11, 2 => 21
update test set value = 22 where id = 2; -- T2
commit; -- T2
select * from test; -- either. Shows 1 => 12, 2 => 22
```

Postgres "read committed" prevents Aborted Reads (G1a):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
update test set value = 101 where id = 1; -- T1
select * from test; -- T2. Still shows 1 => 10
abort;  -- T1
select * from test; -- T2. Still shows 1 => 10
commit; -- T2
```

Postgres "read committed" prevents Intermediate Reads (G1b):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
update test set value = 101 where id = 1; -- T1
select * from test; -- T2. Still shows 1 => 10
update test set value = 11 where id = 1; -- T1
commit; -- T1
select * from test; -- T2. Now shows 1 => 11
commit; -- T2
```

Postgres "read committed" prevents Circular Information Flow (G1c):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
update test set value = 11 where id = 1; -- T1
update test set value = 22 where id = 2; -- T2
select * from test where id = 2; -- T1. Still shows 2 => 20
select * from test where id = 1; -- T2. Still shows 1 => 10
commit; -- T1
commit; -- T2
```

## Observed Transaction Vanishes (OTV)

Postgres "read committed" prevents Observed Transaction Vanishes (OTV):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
begin; set transaction isolation level read committed; -- T3
update test set value = 11 where id = 1; -- T1
update test set value = 19 where id = 2; -- T1
update test set value = 12 where id = 1; -- T2. BLOCKS
commit; -- T1. This unblocks T2
select * from test where id = 1; -- T3. Shows 1 => 11
update test set value = 18 where id = 2; -- T2
select * from test where id = 2; -- T3. Shows 2 => 19
commit; -- T2
select * from test where id = 2; -- T3. Shows 2 => 18
select * from test where id = 1; -- T3. Shows 1 => 12
commit; -- T3
```

## Predicate-Many-Preceders (PMP)

Postgres "read committed" does not prevent Predicate-Many-Preceders (PMP):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
select * from test where value = 30; -- T1. Returns nothing
insert into test (id, value) values(3, 30); -- T2
commit; -- T2
select * from test where value % 3 = 0; -- T1. Returns the newly inserted row
commit; -- T1
```

Postgres "repeatable read" prevents Predicate-Many-Preceders (PMP):

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where value = 30; -- T1. Returns nothing
insert into test (id, value) values(3, 30); -- T2
commit; -- T2
select * from test where value % 3 = 0; -- T1. Still returns nothing
commit; -- T1
```

Postgres "read committed" does not prevent Predicate-Many-Preceders (PMP) for write predicates -- example from Postgres documentation:

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
update test set value = value + 10; -- T1
delete from test where value = 20;  -- T2, BLOCKS
commit; -- T1. This unblocks T2
select * from test where value = 20; -- T2, returns 1 => 20 (despite ostensibly having been deleted)
commit; -- T2
```

Postgres "repeatable read" prevents Predicate-Many-Preceders (PMP) for write predicates -- example from Postgres documentation:

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
update test set value = value + 10; -- T1
delete from test where value = 20;  -- T2, BLOCKS
commit; -- T1. T2 now prints out "ERROR: could not serialize access due to concurrent update"
abort;  -- T2. There's nothing else we can do, this transaction has failed
```

## Lost Update (P4)

Postgres "read committed" does not prevent Lost Update (P4):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
select * from test where id = 1; -- T1
select * from test where id = 1; -- T2
update test set value = 11 where id = 1; -- T1
update test set value = 11 where id = 1; -- T2, BLOCKS
commit; -- T1. This unblocks T2, so T1's update is overwritten
commit; -- T2
```

Postgres "repeatable read" prevents Lost Update (P4):

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where id = 1; -- T1
select * from test where id = 1; -- T2
update test set value = 11 where id = 1; -- T1
update test set value = 11 where id = 1; -- T2, BLOCKS
commit; -- T1. T2 now prints out "ERROR: could not serialize access due to concurrent update"
abort;  -- T2. There's nothing else we can do, this transaction has failed
```

## Read Skew (G-single)

Postgres "read committed" does not prevent Read Skew (G-single):

```
begin; set transaction isolation level read committed; -- T1
begin; set transaction isolation level read committed; -- T2
select * from test where id = 1; -- T1. Shows 1 => 10
select * from test where id = 1; -- T2
select * from test where id = 2; -- T2
update test set value = 12 where id = 1; -- T2
update test set value = 18 where id = 2; -- T2
commit; -- T2
select * from test where id = 2; -- T1. Shows 2 => 18
commit; -- T1
```

Postgres "repeatable read" prevents Read Skew (G-single):

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where id = 1; -- T1. Shows 1 => 10
select * from test where id = 1; -- T2
select * from test where id = 2; -- T2
update test set value = 12 where id = 1; -- T2
update test set value = 18 where id = 2; -- T2
commit; -- T2
select * from test where id = 2; -- T1. Shows 2 => 20
commit; -- T1
```

Postgres "repeatable read" prevents Read Skew (G-single) -- test using predicate dependencies:

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where value % 5 = 0; -- T1
update test set value = 12 where value = 10; -- T2
commit; -- T2
select * from test where value % 3 = 0; -- T1. Returns nothing
commit; -- T1
```

Postgres "repeatable read" prevents Read Skew (G-single) -- test using write predicate:

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where id = 1; -- T1. Shows 1 => 10
select * from test; -- T2
update test set value = 12 where id = 1; -- T2
update test set value = 18 where id = 2; -- T2
commit; -- T2
delete from test where value = 20; -- T1. Prints "ERROR: could not serialize access due to concurrent update"
abort; -- T1. There's nothing else we can do, this transaction has failed
```

## Write Skew (G2-item)

Postgres "repeatable read" does not prevent Write Skew (G2-item):

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where id in (1,2); -- T1
select * from test where id in (1,2); -- T2
update test set value = 11 where id = 1; -- T1
update test set value = 21 where id = 2; -- T2
commit; -- T1
commit; -- T2
```

Postgres "serializable" prevents Write Skew (G2-item):

```
begin; set transaction isolation level serializable; -- T1
begin; set transaction isolation level serializable; -- T2
select * from test where id in (1,2); -- T1
select * from test where id in (1,2); -- T2
update test set value = 11 where id = 1; -- T1
update test set value = 21 where id = 2; -- T2
commit; -- T1
commit; -- T2. Prints out "ERROR: could not serialize access due to read/write dependencies among transactions"
```

## Anti-Dependency Cycles (G2)

Postgres "repeatable read" does not prevent Anti-Dependency Cycles (G2):

```
begin; set transaction isolation level repeatable read; -- T1
begin; set transaction isolation level repeatable read; -- T2
select * from test where value % 3 = 0; -- T1
select * from test where value % 3 = 0; -- T2
insert into test (id, value) values(3, 30); -- T1
insert into test (id, value) values(4, 42); -- T2
commit; -- T1
commit; -- T2
select * from test where value % 3 = 0; -- Either. Returns 3 => 30, 4 => 42
```

Postgres "serializable" prevents Anti-Dependency Cycles (G2):

```
begin; set transaction isolation level serializable; -- T1
begin; set transaction isolation level serializable; -- T2
select * from test where value % 3 = 0; -- T1
select * from test where value % 3 = 0; -- T2
insert into test (id, value) values(3, 30); -- T1
insert into test (id, value) values(4, 42); -- T2
commit; -- T1
commit; -- T2. Prints out "ERROR: could not serialize access due to read/write dependencies among transactions"
```

Postgres "serializable" prevents Anti-Dependency Cycles (G2) -- Fekete et al's example with two anti-dependency edges:

```
begin; set transaction isolation level serializable; -- T1
select * from test; -- T1. Shows 1 => 10, 2 => 20
begin; set transaction isolation level serializable; -- T2
update test set value = value + 5 where id = 2; -- T2
commit; -- T2
begin; set transaction isolation level serializable; -- T3
select * from test; -- T3. Shows 1 => 10, 2 => 25
commit; -- T3
update test set value = 0 where id = 1; -- T1. Prints out "ERROR: could not serialize access due to read/write dependencies among transactions"
abort; -- T1. There's nothing else we can do, this transaction has failed
```