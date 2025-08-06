---
title: "Relation Bloat Monitoring and Management"
linkTitle: "Relation Bloat Monitoring and Management"
date: 2018-10-06
author: vonng
summary: >
  PostgreSQL uses MVCC as its primary concurrency control technology. While it has many benefits, it also brings other effects, such as relation bloat.
tags: [PostgreSQL,PG Administration]
---

> Author: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))

PostgreSQL uses MVCC as its primary concurrency control technology. While it has many benefits, it also brings other effects, such as relation bloat. Relation bloat (table and index) negatively impacts database performance and wastes disk space. To keep PostgreSQL always at optimal performance, it's necessary to perform timely garbage collection on bloated relations and regularly rebuild excessively bloated relations.

In actual operations, garbage collection isn't that simple. Here are a series of issues:

* What causes relation bloat?
* How to measure relation bloat?
* How to monitor relation bloat?
* How to handle relation bloat?

This article will explain these issues in detail.

---------------------

## Relation Bloat Overview

Suppose a relation actually occupies 100G of storage, but much space is wasted by dead tuples, fragments, and free areas. If it were compressed into a new relation, it would occupy 60G, then we can approximately consider this relation has a bloat rate of (100 - 60) / 100 = 40%.

Regular `VACUUM` cannot solve table bloat issues. Dead tuples themselves can be reclaimed by concurrent `VACUUM` mechanisms, but the fragments and holes they create cannot. For example, even after deleting many dead tuples, the table size cannot be reduced. Over time, relation files become filled with many holes, wasting substantial disk space.

The `VACUUM FULL` command can reclaim this space by copying live tuples from the old table file to a new table, compacting the table by rewriting the entire table. However, in actual production, this operation holds an `AccessExclusiveLock` on the table, blocking normal business access, making it unsuitable for non-stop services. `pg_repack` is a practical third-party plugin that can perform lock-free `VACUUM FULL` while online business continues normally.

Unfortunately, there's no best practice for when to perform `VACUUM FULL` to handle bloat. DBAs need to formulate cleanup strategies for their specific business scenarios. However, regardless of the strategy adopted, the mechanisms for implementing these strategies are similar:

* Monitor, detect, and measure relation bloat levels
* Handle relation bloat based on bloat level, timing, and other factors

Here are some key questions: first, how to define relation bloat rate?

---------------------

## Measuring Relation Bloat

To measure relation bloat levels, we first need to define a metric: **bloat rate**.

The calculation idea for bloat rate is: estimate the space that would be occupied if the target table were in a **compact** state through statistical information, and the proportion of actual used space exceeding this compact space is the bloat rate. Therefore, bloat rate can be defined as 1 - (total bytes occupied by live tuples / total bytes occupied by relation).

For example, if a table actually occupies 100G of storage, but much space is wasted by dead tuples, fragments, and free areas, and if compressed into a new table it would occupy 60G, then the bloat rate is 1 - 60/100 = 40%.

Getting relation size is relatively simple and can be obtained directly from system catalogs. So the key issue is how to obtain **total bytes of live tuples**.

### Precise Calculation of Bloat Rate

PostgreSQL comes with the `pgstattuple` module, which can be used to precisely calculate table bloat rates. For example, the `tuple_percent` field here is the percentage of actual tuple bytes to total relation size. Subtracting this value from 1 gives the bloat rate.

```sql
vonng@[local]:5432/bench# select *,
                          1.0 - tuple_len::numeric / table_len as bloat 
                          from pgstattuple('pgbench_accounts');
┌─[ RECORD 1 ]───────┬────────────────────────┐
│ table_len          │ 136642560              │
│ tuple_count        │ 1000000                │
│ tuple_len          │ 121000000              │
│ tuple_percent      │ 88.55                  │
│ dead_tuple_count   │ 16418                  │
│ dead_tuple_len     │ 1986578                │
│ dead_tuple_percent │ 1.45                   │
│ free_space         │ 1674768                │
│ free_percent       │ 1.23                   │
│ bloat              │ 0.11447794889088729017 │
└────────────────────┴────────────────────────┘
```

`pgstattuple` is very useful for precisely determining table and index bloat. For specific details, refer to the official documentation: https://www.postgresql.org/docs/current/static/pgstattuple.html.

Additionally, PostgreSQL provides two built-in extensions, `pg_freespacemap` and `pageinspect`. The former can be used to examine the free space size in each page, while the latter can precisely show the physical storage content within each data page in relations. If you want to examine the internal state of relations, these two plugins are very practical. Detailed usage can be found in the official documentation:

https://www.postgresql.org/docs/current/static/pgfreespacemap.html

https://www.postgresql.org/docs/current/static/pageinspect.html

However, in most cases, we don't care too much about the precision of bloat rates. In actual production, the requirements for bloat rates aren't high: having the first significant digit accurate is generally sufficient. On the other hand, to know precisely the total bytes occupied by live tuples, a full scan of the entire relation is needed, which puts pressure on the online system's I/O. If you want to monitor bloat rates for all tables, this approach isn't suitable.

For example, a 200G relation would take approximately 5 minutes to perform precise bloat rate estimation using the `pgstattuple` plugin. In version 9.5 and later, the `pgstattuple` plugin also provides the `pgstattuple_approx` function, trading precision for speed. But even with estimation, it still takes seconds.

For monitoring bloat rates, the most important requirement is fast speed and low impact. Therefore, when we need to monitor many tables across many databases simultaneously, we need to perform **fast estimation** of bloat rates to avoid impacting business operations.

---------------------

## Estimating Bloat Rate

PostgreSQL maintains many statistical information for each relation. Using statistical information, we can quickly and efficiently estimate bloat rates for all tables in the database. Estimating bloat rates requires using statistical information on tables and columns. Three directly used statistical metrics are:

* Average tuple width `avgwidth`: calculated from column-level statistical data, used to estimate space occupied in compact state
* Tuple count: `pg_class.reltuples`: used to estimate space occupied in compact state
* Page count: `pg_class.relpages`: used to measure actually used space

The calculation formula is also simple:

```c
1 - (reltuples * avgwidth) / (block_size - pageheader) / relpages 
```

Here `block_size` is page size, default 8182, `pageheader` is header overhead, default 24 bytes. Page size minus header size gives actual space available for tuple storage. Therefore, `(reltuples * avgwidth)` gives estimated total tuple size, and dividing by the former gives expected pages needed to compactly store all tuples. Finally, expected page count divided by actual page count gives **utilization rate**, and 1 minus utilization rate gives bloat rate.

### Difficulties

The key here is how to use statistical information to estimate average tuple length. To achieve this, we need to overcome three difficulties:

* When tuples contain null values, headers will have null bitmaps
* There's padding between headers and data sections, requiring boundary alignment consideration
* Some field types also have alignment requirements

Fortunately, bloat rate itself is an estimation, so being roughly correct is sufficient.

### Calculating Average Tuple Length

To understand the estimation process, we first need to understand PostgreSQL's internal layout of data pages and tuples.

First, let's look at tuple **average length**. The tuple layout in PostgreSQL is shown in the diagram below.

![](page-tuple.png)

Space occupied by a tuple can be divided into three parts:

* Fixed-length line pointer (4 bytes, strictly speaking this isn't part of the tuple, but it corresponds one-to-one with tuples)
* Variable-length header
  * Fixed-length part 23 bytes
  * When tuples contain null values, a null bitmap appears, with each field occupying one bit, so its length is the number of fields divided by 8
  * After the null bitmap, padding is needed to `MAXALIGN`, usually 8
  * If the table has the `WITH OIDS` option enabled, tuples also have a 4-byte OID, but we don't consider this case here
* Data section

Therefore, a tuple's average length (including corresponding line pointer) can be calculated as:

```c
avg_size_tuple = 4 + avg_size_hdr + avg_size_data
```

The key is finding **average header length** and **average data section length**.

### Calculating Average Header Length

The main variables in average header length are **null bitmap** and **padding alignment**. To estimate average tuple header length, we need several parameters:

* Average header length without null bitmap (with padding): `normhdr`
* Average header length with null bitmap (with padding): `nullhdr`
* Proportion of tuples with null values: `nullfrac`

The formula for estimating average header length is also very simple:

```python
avg_size_hdr =  nullhdr * nullfrac + normhdr * (1 - nullfrac)
```

Since headers without null bitmaps are 23 bytes long, aligned to 8-byte boundaries gives 24 bytes, the above formula becomes:

```python
avg_size_hdr =  nullhdr * nullfrac +  24 * (1 - nullfrac)
```

To calculate the length of a value padded to 8-byte boundaries, use this formula for efficient computation:

```python
padding = lambda x : x + 7 >> 3 << 3
```

### Calculating Average Data Section Length

Average data section length mainly depends on each field's average width and null rate, plus trailing alignment.

The following SQL can calculate average tuple data section width for all tables using statistical information:

```sql
SELECT schemaname, tablename, sum((1 - null_frac) * avg_width)
FROM pg_stats GROUP BY (schemaname, tablename);
```

For example, this SQL can get average tuple length for table `app.apple` from the `pg_stats` system statistics view:

```sql
SELECT
  count(*),                        -- number of fields
  ceil(count(*) / 8.0),            -- bytes occupied by null bitmap
  max(null_frac),                  -- maximum null rate
  sum((1 - null_frac) * avg_width) -- average width of data section
FROM pg_stats
where schemaname = 'app' and tablename = 'apple';

-[ RECORD 1 ]-----------
count | 47
ceil  | 6
max   | 1
sum   | 1733.76873471724
```

### Integration

Integrating the logic from the above three sections, we get the following stored procedure that returns bloat rate for a given table:

```sql
CREATE OR REPLACE FUNCTION public.pg_table_bloat(relation regclass)
 RETURNS double precision
 LANGUAGE plpgsql
AS $function$
DECLARE
  _schemaname text;
  tuples      BIGINT := 0;
  pages       INTEGER := 0;
  nullheader  INTEGER:= 0;
  nullfrac    FLOAT := 0;
  datawidth   INTEGER :=0;
  avgtuplelen FLOAT :=24;
BEGIN
  SELECT
    relnamespace :: RegNamespace,
    reltuples,
    relpages
  into _schemaname, tuples, pages
  FROM pg_class
  Where oid = relation;

  SELECT
    23 + ceil(count(*) >> 3),
    max(null_frac),
    ceil(sum((1 - null_frac) * avg_width))
  into nullheader, nullfrac, datawidth
  FROM pg_stats
  where schemaname = _schemaname and tablename = relation :: text;

  SELECT (datawidth + 8 - (CASE WHEN datawidth%8=0 THEN 8 ELSE datawidth%8 END)) -- avg data len
    + (1 - nullfrac) * 24 + nullfrac * (nullheader + 8 - (CASE WHEN nullheader%8=0 THEN 8 ELSE nullheader%8 END))
    INTO avgtuplelen;

  raise notice '% %', nullfrac, datawidth;

  RETURN 1 - (ceil(tuples * avgtuplelen / 8168)) / pages;
END;
$function$
```

### Batch Calculation

For monitoring, we often care about not just one table, but all tables in the database. Therefore, the above bloat rate calculation logic can be rewritten as a batch calculation query and defined as a view for easy use:

```sql
DROP VIEW IF EXISTS monitor.pg_bloat_indexes CASCADE;
CREATE OR REPLACE VIEW monitor.pg_bloat_indexes AS
  WITH btree_index_atts AS (
      SELECT
        pg_namespace.nspname,
        indexclass.relname                                                          AS index_name,
        indexclass.reltuples,
        indexclass.relpages,
        pg_index.indrelid,
        pg_index.indexrelid,
        indexclass.relam,
        tableclass.relname                                                          AS tablename,
        (regexp_split_to_table((pg_index.indkey) :: TEXT, ' ' :: TEXT)) :: SMALLINT AS attnum,
        pg_index.indexrelid                                                         AS index_oid
      FROM ((((pg_index
        JOIN pg_class indexclass ON ((pg_index.indexrelid = indexclass.oid)))
        JOIN pg_class tableclass ON ((pg_index.indrelid = tableclass.oid)))
        JOIN pg_namespace ON ((pg_namespace.oid = indexclass.relnamespace)))
        JOIN pg_am ON ((indexclass.relam = pg_am.oid)))
      WHERE ((pg_am.amname = 'btree' :: NAME) AND (indexclass.relpages > 0))
  ), index_item_sizes AS (
      SELECT
        ind_atts.nspname,
        ind_atts.index_name,
        ind_atts.reltuples,
        ind_atts.relpages,
        ind_atts.relam,
        ind_atts.indrelid                                    AS table_oid,
        ind_atts.index_oid,
        (current_setting('block_size' :: TEXT)) :: NUMERIC   AS bs,
        8                                                    AS maxalign,
        24                                                   AS pagehdr,
        CASE
        WHEN (max(COALESCE(pg_stats.null_frac, (0) :: REAL)) = (0) :: FLOAT)
          THEN 2
        ELSE 6
        END                                                  AS index_tuple_hdr,
        sum((((1) :: FLOAT - COALESCE(pg_stats.null_frac, (0) :: REAL)) *
             (COALESCE(pg_stats.avg_width, 1024)) :: FLOAT)) AS nulldatawidth
      FROM ((pg_attribute
        JOIN btree_index_atts ind_atts
          ON (((pg_attribute.attrelid = ind_atts.indexrelid) AND (pg_attribute.attnum = ind_atts.attnum))))
        JOIN pg_stats ON (((pg_stats.schemaname = ind_atts.nspname) AND (((pg_stats.tablename = ind_atts.tablename) AND
                                                                          ((pg_stats.attname) :: TEXT =
                                                                           pg_get_indexdef(pg_attribute.attrelid,
                                                                                           (pg_attribute.attnum) :: INTEGER,
                                                                                           TRUE))) OR
                                                                         ((pg_stats.tablename = ind_atts.index_name) AND
                                                                          (pg_stats.attname = pg_attribute.attname))))))
      WHERE (pg_attribute.attnum > 0)
      GROUP BY ind_atts.nspname, ind_atts.index_name, ind_atts.reltuples, ind_atts.relpages, ind_atts.relam,
        ind_atts.indrelid, ind_atts.index_oid, (current_setting('block_size' :: TEXT)) :: NUMERIC, 8 :: INTEGER
  ), index_aligned_est AS (
      SELECT
        index_item_sizes.maxalign,
        index_item_sizes.bs,
        index_item_sizes.nspname,
        index_item_sizes.index_name,
        index_item_sizes.reltuples,
        index_item_sizes.relpages,
        index_item_sizes.relam,
        index_item_sizes.table_oid,
        index_item_sizes.index_oid,
        COALESCE(ceil((((index_item_sizes.reltuples * ((((((((6 + index_item_sizes.maxalign) -
                                                             CASE
                                                             WHEN ((index_item_sizes.index_tuple_hdr %
                                                                    index_item_sizes.maxalign) = 0)
                                                               THEN index_item_sizes.maxalign
                                                             ELSE (index_item_sizes.index_tuple_hdr %
                                                                   index_item_sizes.maxalign)
                                                             END)) :: FLOAT + index_item_sizes.nulldatawidth)
                                                          + (index_item_sizes.maxalign) :: FLOAT) - (
                                                           CASE
                                                           WHEN (((index_item_sizes.nulldatawidth) :: INTEGER %
                                                                  index_item_sizes.maxalign) = 0)
                                                             THEN index_item_sizes.maxalign
                                                           ELSE ((index_item_sizes.nulldatawidth) :: INTEGER %
                                                                 index_item_sizes.maxalign)
                                                           END) :: FLOAT)) :: NUMERIC) :: FLOAT) /
                        ((index_item_sizes.bs - (index_item_sizes.pagehdr) :: NUMERIC)) :: FLOAT) +
                       (1) :: FLOAT)), (0) :: FLOAT) AS expected
      FROM index_item_sizes
  ), raw_bloat AS (
      SELECT
        current_database()                                                           AS dbname,
        index_aligned_est.nspname,
        pg_class.relname                                                             AS table_name,
        index_aligned_est.index_name,
        (index_aligned_est.bs * ((index_aligned_est.relpages) :: BIGINT) :: NUMERIC) AS totalbytes,
        index_aligned_est.expected,
        CASE
        WHEN ((index_aligned_est.relpages) :: FLOAT <= index_aligned_est.expected)
          THEN (0) :: NUMERIC
        ELSE (index_aligned_est.bs *
              ((((index_aligned_est.relpages) :: FLOAT - index_aligned_est.expected)) :: BIGINT) :: NUMERIC)
        END                                                                          AS wastedbytes,
        CASE
        WHEN ((index_aligned_est.relpages) :: FLOAT <= index_aligned_est.expected)
          THEN (0) :: NUMERIC
        ELSE (((index_aligned_est.bs * ((((index_aligned_est.relpages) :: FLOAT -
                                          index_aligned_est.expected)) :: BIGINT) :: NUMERIC) * (100) :: NUMERIC) /
              (index_aligned_est.bs * ((index_aligned_est.relpages) :: BIGINT) :: NUMERIC))
        END                                                                          AS realbloat,
        pg_relation_size((index_aligned_est.table_oid) :: REGCLASS)                  AS table_bytes,
        stat.idx_scan                                                                AS index_scans
      FROM ((index_aligned_est
        JOIN pg_class ON ((pg_class.oid = index_aligned_est.table_oid)))
        JOIN pg_stat_user_indexes stat ON ((index_aligned_est.index_oid = stat.indexrelid)))
  ), format_bloat AS (
      SELECT
        raw_bloat.dbname                                             AS database_name,
        raw_bloat.nspname                                            AS schema_name,
        raw_bloat.table_name,
        raw_bloat.index_name,
        round(
            raw_bloat.realbloat)                                     AS bloat_pct,
        round((raw_bloat.wastedbytes / (((1024) :: FLOAT ^
                                         (2) :: FLOAT)) :: NUMERIC)) AS bloat_mb,
        round((raw_bloat.totalbytes / (((1024) :: FLOAT ^ (2) :: FLOAT)) :: NUMERIC),
              3)                                                     AS index_mb,
        round(
            ((raw_bloat.table_bytes) :: NUMERIC / (((1024) :: FLOAT ^ (2) :: FLOAT)) :: NUMERIC),
            3)                                                       AS table_mb,
        raw_bloat.index_scans
      FROM raw_bloat
  )
  SELECT
    format_bloat.database_name                    as datname,
    format_bloat.schema_name                      as nspname,
    format_bloat.table_name                       as relname,
    format_bloat.index_name                       as idxname,
    format_bloat.index_scans                      as idx_scans,
    format_bloat.bloat_pct                        as bloat_pct,
    format_bloat.table_mb,
    format_bloat.index_mb - format_bloat.bloat_mb as actual_mb,
    format_bloat.bloat_mb,
    format_bloat.index_mb                         as total_mb
  FROM format_bloat
  ORDER BY format_bloat.bloat_mb DESC;


COMMENT ON VIEW monitor.pg_bloat_indexes IS 'index bloat monitor';
```

Although it looks long, querying this view to get bloat rates for all tables in the entire database (3TB) takes only 50ms of computation. And it only needs to access statistical data, not the relations themselves, consuming no instance I/O.

---------------------

## Handling Table Bloat

If it's just a toy database, or the business allows long daily downtime for maintenance, then simply executing `VACUUM FULL` in the database would suffice. But `VACUUM FULL` requires exclusive read-write locks on tables. For databases that need to run continuously, we need to use `pg_repack` to handle table bloat.

* Homepage: http://reorg.github.io/pg_repack/

`pg_repack` is included in PostgreSQL's official yum repository, so it can be installed directly via `yum install pg_repack`.

```bash
yum install pg_repack10
```

---------------------

### Using `pg_repack`

Like most PostgreSQL client programs, `pg_repack` also connects to PostgreSQL servers through similar parameters.

Before using `pg_repack`, you need to create the `pg_repack` extension in the database to be reorganized:

```sql
CREATE EXTENSION pg_repack
```

Then you can use it normally. Several typical usage patterns:

```bash
# Complete cleanup of entire database, 5 concurrent tasks, 10 second timeout
pg_repack -d <database> -j 5 -T 10

# Clean specific table mytable in mydb, 10 second timeout
pg_repack mydb -t public.mytable -T 10

# Clean specific index myschema.myindex, must use full name with schema
pg_repack mydb -i myschema.myindex
```

Detailed usage can be found in the official documentation.

---------------------

### `pg_repack` Strategy

Usually, if business has peak and valley cycles, you can choose to perform reorganization during business valleys. `pg_repack` executes quickly but is resource-intensive. Running during peak periods might affect overall database performance and could cause replication lag.

For example, you can use the bloat rate monitoring views provided in the above two sections to daily select the most severely bloated tables and indexes for automatic reorganization.

```bash
#--------------------------------------------------------------#
# Name: repack_tables
# Desc: repack table via fullname
# Arg1: database_name
# Argv: list of table full name
# Deps: psql
#--------------------------------------------------------------#
# repack single table
function repack_tables(){
    local db=$1
    shift

    log_info "repack ${db} tables begin"
    log_info "repack table list: $@"

    for relname in $@
    do
        old_size=$(psql ${db} -Atqc "SELECT pg_size_pretty(pg_relation_size('${relname}'));")
        # kill_queries ${db}
        log_info "repack table ${relname} begin, old size: ${old_size}"
        pg_repack ${db} -T 10 -t ${relname}
        new_size=$(psql ${db} -Atqc "SELECT pg_size_pretty(pg_relation_size('${relname}'));")
        log_info "repack table ${relname} done , new size: ${old_size} -> ${new_size}"
    done

    log_info "repack ${db} tables done"
}

#--------------------------------------------------------------#
# Name: get_bloat_tables
# Desc: find bloat tables in given database match some condition
# Arg1: database_name
# Echo: list of full table name
# Deps: psql, monitor.pg_bloat_tables
#--------------------------------------------------------------#
function get_bloat_tables(){
    echo $(psql ${1} -Atq <<-'EOF'
    WITH bloat_tables AS (
        SELECT
          nspname || '.' || relname as relname,
          actual_mb,
          bloat_pct
        FROM monitor.pg_bloat_tables
        WHERE nspname NOT IN ('dba', 'monitor', 'trash')
        ORDER BY 2 DESC,3 DESC
    )
    -- 64 small + 16 medium + 4 large
    (SELECT relname FROM bloat_tables WHERE actual_mb < 256 AND bloat_pct > 40 ORDER BY bloat_pct DESC LIMIT 64) UNION
    (SELECT relname FROM bloat_tables WHERE actual_mb BETWEEN 256 AND 1024  AND bloat_pct > 30 ORDER BY bloat_pct DESC LIMIT 16) UNION
    (SELECT relname FROM bloat_tables WHERE actual_mb BETWEEN 1024 AND 4096  AND bloat_pct > 20 ORDER BY bloat_pct DESC  LIMIT 4);
EOF
)
}
```

Here, three rules are set:

* From small tables < 256MB with bloat rate > 40%, select TOP64
* From medium tables 256MB to 1GB with bloat rate > 40%, select TOP16  
* From large tables 1GB to 4GB with bloat rate > 20%, select TOP4

Select these tables for automatic reorganization during early morning valleys. Tables over 4GB are handled manually.

But when to perform reorganization still depends on specific business patterns.

---------------------

### `pg_repack` Principles

`pg_repack`'s principle is quite simple. It creates a copy for the table to be rebuilt. First, it takes a full snapshot, writes all live tuples to the new table, and synchronizes all changes to the original table to the new table through triggers. Finally, it replaces the old table with the new compact copy through renaming. For indexes, this is accomplished through PostgreSQL's `CREATE(DROP) INDEX CONCURRENTLY`.

**Reorganizing Tables**

1. Create an empty table with the same schema as the original table but without indexes
2. Create a log table corresponding to the original table to record changes that occur on that table during `pg_repack` operation
3. Add a row trigger to the original table to record all `INSERT`, `DELETE`, `UPDATE` operations in the corresponding log table
4. Copy data from the old table to the new empty table
5. Create the same indexes on the new table
6. Apply incremental changes from the log table to the new table
7. Switch new and old tables through renaming
8. Drop the old, renamed table

**Reorganizing Indexes**

1. Use `CREATE INDEX CONCURRENTLY` to create a new index on the original table, maintaining the same definition as the old index
2. `Analyze` the new index, set the old index as invalid, and swap new and old indexes in the data directory
3. Delete the old index

---------------------

### `pg_repack` Considerations

- Before starting reorganization, it's best to cancel all ongoing `Vacuum` tasks
- Before reorganizing indexes, it's best to manually clean up queries that might be using those indexes

- If abnormal situations occur (like forced exit midway), garbage might be left behind that needs manual cleanup. This might include:
  - Temporary tables and temporary indexes built in the same schema as the original table/index
  - Temporary table names: `${schema_name}.table_${table_oid}`
  - Temporary index names: `${schema_name}.index_${table_oid}}`
  - Related triggers might remain on the original table and need manual cleanup
- When reorganizing particularly large tables, reserve at least the same amount of disk space as the table and its indexes, requiring special care and manual checking
- When completing reorganization and performing renaming replacement, massive amounts of WAL will be generated, possibly causing replication delay that cannot be canceled