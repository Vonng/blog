---
title: "Finding Unused Indexes"
date: 2018-02-04
author: vonng
summary: >
  Indexes are useful, but they're not free. Unused indexes are a waste. Use these methods to identify unused indexes.
tags: [PostgreSQL, PG Admin]
---

> Author: [Vonng](https://vonng.com/en/)

Indexes are useful, but they're not free. Unused indexes are a waste. Use the following SQL to identify unused indexes:

* First, exclude indexes used to implement constraints (can't be dropped)
* Expression indexes (containing field 0 in `pg_index.indkey`)
* Then find indexes with zero index scans (you can also use a more lenient condition, such as fewer than 1000 scans)


---------------

## Finding Unused Indexes

- View name: `monitor.v_bloat_indexes`
- Calculation time: 1 second, suitable for daily/manual checks, not suitable for frequent polling
- Verified versions: 9.3 ~ 10
- Function: Shows current database index bloat situation

Works well on versions 9.3 and 10.4. View definition:

```sql
-- CREATE SCHEMA IF NOT EXISTS monitor;
-- DROP VIEW IF EXISTS monitor.pg_stat_dummy_indexes;

CREATE OR REPLACE VIEW monitor.pg_stat_dummy_indexes AS
SELECT s.schemaname,
       s.relname AS tablename,
       s.indexrelname AS indexname,
       pg_relation_size(s.indexrelid) AS index_size
FROM pg_catalog.pg_stat_user_indexes s
   JOIN pg_catalog.pg_index i ON s.indexrelid = i.indexrelid
WHERE s.idx_scan = 0      -- has never been scanned
  AND 0 <>ALL (i.indkey)  -- no index column is an expression
  AND NOT EXISTS          -- does not enforce a constraint
         (SELECT 1 FROM pg_catalog.pg_constraint c
          WHERE c.conindid = s.indexrelid)
ORDER BY pg_relation_size(s.indexrelid) DESC;

COMMENT ON VIEW monitor.pg_stat_dummy_indexes IS 'monitor unused indexes'
```

```sql
-- Human-readable manual query
SELECT s.schemaname,
       s.relname AS tablename,
       s.indexrelname AS indexname,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS index_size
FROM pg_catalog.pg_stat_user_indexes s
   JOIN pg_catalog.pg_index i ON s.indexrelid = i.indexrelid
WHERE s.idx_scan = 0      -- has never been scanned
  AND 0 <>ALL (i.indkey)  -- no index column is an expression
  AND NOT EXISTS          -- does not enforce a constraint
         (SELECT 1 FROM pg_catalog.pg_constraint c
          WHERE c.conindid = s.indexrelid)
ORDER BY pg_relation_size(s.indexrelid) DESC;
```



---------------

### Batch Generate Index Drop Commands

```sql
SELECT 'DROP INDEX CONCURRENTLY IF EXISTS "' 
	|| s.schemaname || '"."' || s.indexrelname || '";'
FROM pg_catalog.pg_stat_user_indexes s
   JOIN pg_catalog.pg_index i ON s.indexrelid = i.indexrelid
WHERE s.idx_scan = 0      -- has never been scanned
  AND 0 <>ALL (i.indkey)  -- no index column is an expression
  AND NOT EXISTS          -- does not enforce a constraint
         (SELECT 1 FROM pg_catalog.pg_constraint c
          WHERE c.conindid = s.indexrelid)
ORDER BY pg_relation_size(s.indexrelid) DESC;
```




---------------

## Finding Duplicate Indexes

Check if there are indexes working on the same columns of the same table, but be careful with partial indexes.

```sql
SELECT
  indrelid :: regclass              AS table_name,
  array_agg(indexrelid :: regclass) AS indexes
FROM pg_index
GROUP BY
  indrelid, indkey
HAVING COUNT(*) > 1;
```