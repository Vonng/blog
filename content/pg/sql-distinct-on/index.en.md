---
title: "Distinct On: Remove Duplicate Data"
date: 2018-04-06
author: "vonng"
summary: >
  Use Distinct On extension clause to quickly find records with maximum/minimum values within groups
tags: [PostgreSQL, PG-Development, SQL]
---

Distinct On is a unique syntax provided by PostgreSQL that can efficiently solve typical query problems, for example, quickly finding records with maximum/minimum values within groups.

## Introduction

Finding records with maximum/minimum values within groups is a very common requirement. Traditional SQL certainly has ways to solve this, but they're not elegant enough. PostgreSQL's SQL extension syntax Distinct ON can solve this type of problem in one step.

## DISTINCT ON Syntax

```sql
SELECT DISTINCT ON (expression [, expression ...]) select_list ...
```

Here *expression* is an arbitrary value expression that is evaluated for all rows. A set of rows for which all the expressions are equal are considered duplicates, and only the first row of the set is kept in the output. Note that the "first row" of a set is unpredictable unless the query is sorted on enough columns to guarantee a unique ordering of the rows arriving at the `DISTINCT` filter. (`DISTINCT ON` processing occurs after `ORDER BY` sorting.)

## Distinct On Use Cases

For example, find the latest log for each machine in the log table, extracting log records grouped by machine node_id with the maximum timestamp `ts`.

```sql
CREATE TABLE nodes(node_id INTEGER, ts TIMESTAMP);

INSERT INTO test_data
SELECT (random() * 10)::INTEGER as node_id, t
FROM generate_series('2019-01-01'::TIMESTAMP, '2019-05-01'::TIMESTAMP, '1h'::INTERVAL) AS t;
```

Here we can create some random data:

```
5	2019-01-01 00:00:00.000000
0	2019-01-01 01:00:00.000000
9	2019-01-01 02:00:00.000000
1	2019-01-01 03:00:00.000000
7	2019-01-01 04:00:00.000000
2	2019-01-01 05:00:00.000000
8	2019-01-01 06:00:00.000000
3	2019-01-01 07:00:00.000000
1	2019-01-01 08:00:00.000000
4	2019-01-01 09:00:00.000000
9	2019-01-01 10:00:00.000000
0	2019-01-01 11:00:00.000000
3	2019-01-01 12:00:00.000000
6	2019-01-01 13:00:00.000000
9	2019-01-01 14:00:00.000000
1	2019-01-01 15:00:00.000000
7	2019-01-01 16:00:00.000000
8	2019-01-01 17:00:00.000000
9	2019-01-01 18:00:00.000000
10	2019-01-01 19:00:00.000000
5	2019-01-01 20:00:00.000000
4	2019-01-01 21:00:00.000000
```

Now using DistinctON, the parentheses after Distinct On represent which key records should be deduplicated by. Records with the same values in the expression list within parentheses will keep only one record. (Of course, which one is kept is random, because which record in the group returns first is uncertain)

```sql
SELECT DISTINCT ON (node_id) * FROM test_data

0	2019-04-30 17:00:00.000000
1	2019-04-30 22:00:00.000000
2	2019-04-30 23:00:00.000000
3	2019-04-30 13:00:00.000000
4	2019-05-01 00:00:00.000000
5	2019-04-30 20:00:00.000000
6	2019-04-30 11:00:00.000000
7	2019-04-30 15:00:00.000000
8	2019-04-30 16:00:00.000000
9	2019-04-30 21:00:00.000000
10	2019-04-29 18:00:00.000000
```

DistinctON has a supporting ORDER BY clause to specify which record within the group will be kept. The first sorted record will remain, so if we want the latest log for each machine, we can write it like this:

```sql
SELECT DISTINCT ON (node_id) * FROM test_data ORDER BY node_id, ts DESC NULLS LAST

0	2019-04-30 17:00:00.000000
1	2019-04-30 22:00:00.000000
2	2019-04-30 23:00:00.000000
3	2019-04-30 13:00:00.000000
4	2019-05-01 00:00:00.000000
5	2019-04-30 20:00:00.000000
6	2019-04-30 11:00:00.000000
7	2019-04-30 15:00:00.000000
8	2019-04-30 16:00:00.000000
9	2019-04-30 21:00:00.000000
10	2019-04-29 18:00:00.000000
```

## Using Indexes to Accelerate Distinct On Queries

Distinct On queries can certainly be accelerated by indexes. For example, the following index can make the above query use an index:

```sql
CREATE INDEX ON test_data USING btree(node_id, ts DESC NULLS LAST);

set enable_seqscan = off;
explain SELECT DISTINCT ON (node_id) * FROM test_data ORDER BY node_id, ts DESC NULLS LAST;
Unique  (cost=0.28..170.43 rows=11 width=12)
  ->  Index Only Scan using test_data_node_id_ts_idx on test_data  (cost=0.28..163.23 rows=2881 width=12)
```

Note: When sorting, make sure NULLS FIRST|LAST matches the rules actually used in the query. Otherwise, the index might not be used.