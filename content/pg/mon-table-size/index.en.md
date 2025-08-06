---
title: "Monitoring Table Size in PostgreSQL"
date: 2018-05-14
author: "vonng"
summary: "Tables in PostgreSQL correspond to many physical files. This article explains how to calculate the actual size of a table in PostgreSQL."
tags: ["PostgreSQL","PG Management","Monitoring"]
---

### Table Space Layout

In the broad sense, a **Table** includes two parts: the **main table** and **TOAST table**:

* Main table: stores the relation's own data, i.e., the narrow sense relation, `relkind='r'`.
* TOAST table: corresponds one-to-one with the main table, stores oversized fields, `relkind='t'`.

Each table consists of **main body** and **indexes** - two **Relations** (for main tables, index relations may not exist):

* Main relation: stores tuples.
* Index relation: stores index tuples.

Each **relation** may have **four forks**:

* main: the relation's main file, numbered 0

* fsm: stores information about free space in the main fork, numbered 1
* vm: stores information about visibility in the main fork, numbered 2
* init: used for unlogged tables and indexes, a rare special fork, numbered 3

Each fork is stored as one or more files on disk: files larger than 1GB are split into multiple segments of maximum 1GB each.

In summary, a table is not as simple as it appears - it consists of several relations:

* Main table's main relation (single)
* Main table's indexes (multiple)
* TOAST table's main relation (single)
* TOAST table's index (single)

Each relation may actually contain 1-3 forks: `main` (always exists), `fsm`, `vm`.

### Getting Table's Associated Relations

Use the following query to list all fork oids:

```sql
select
  nsp.nspname,
  rel.relname,
  rel.relnamespace    as nspid,
  rel.oid             as relid,
  rel.reltoastrelid   as toastid,
  toastind.indexrelid as toastindexid,
  ind.indexes
from
  pg_namespace nsp
  join pg_class rel on nsp.oid = rel.relnamespace
  , LATERAL ( select array_agg(indexrelid) as indexes from pg_index where indrelid = rel.oid) ind
  , LATERAL ( select indexrelid from pg_index where indrelid = rel.reltoastrelid) toastind
where nspname not in ('pg_catalog', 'information_schema') and rel.relkind = 'r';
```

```
 nspname |  relname   |  nspid  |  relid  | toastid | toastindexid |      indexes
---------+------------+---------+---------+---------+--------------+--------------------
 public  | aoi        | 4310872 | 4320271 | 4320274 |      4320276 | {4325606,4325605}
 public  | poi        | 4310872 | 4332324 | 4332327 |      4332329 | {4368886}
```

### Statistical Functions

PostgreSQL provides a series of functions to determine the space occupied by various parts.

| Function                        | Statistical Scope                                        |
| ------------------------------- | -------------------------------------------------------- |
| `pg_total_relation_size(oid) `  | Entire relation, including table, indexes, TOAST, etc.  |
| `pg_indexes_size(oid) `         | Space occupied by relation's index portion              |
| `pg_table_size(oid)`            | Space occupied by relation excluding indexes            |
| `pg_relation_size(oid) `        | Get size of a relation's main file part (main fork)    |
| `pg_relation_size(oid, 'main')` | Get relation's `main` fork size                         |
| `pg_relation_size(oid, 'fsm')`  | Get relation's `fsm` fork size                          |
| `pg_relation_size(oid, 'vm')`   | Get relation's `vm` fork size                           |
| `pg_relation_size(oid, 'init')` | Get relation's `init` fork size                         |

Although physically a table consists of so many files, logically we usually only care about the size of two things: table and indexes. Therefore, the main functions used here are `pg_indexes_size` and `pg_table_size`, whose sum equals `pg_total_relation_size` for regular tables.

The table size portion can typically be calculated as:

```sql
 pg_table_size(relid)
 	= pg_relation_size(relid, 'main') 
 	+ pg_relation_size(relid, 'fsm') 
 	+ pg_relation_size(relid, 'vm') 
 	+ pg_total_relation_size(reltoastrelid)
 	
 pg_indexes_size(relid)
 	= (select sum(pg_total_relation_size(indexrelid)) where indrelid = relid)
```

Note that TOAST tables also have their own indexes, but there is only one, so using `pg_total_relation_size(reltoastrelid)` can calculate the overall size of the TOAST table.

### Example: Statistics for a Specific Table and Related Relations UDTF

```sql
SELECT
  oid,
  relname,
  relnamespace::RegNamespace::Text               as nspname,
  relkind                                        as relkind,
  reltuples                                      as tuples,
  relpages                                       as pages,
  pg_total_relation_size(oid)                    as size
  FROM pg_class
WHERE oid = ANY(array(SELECT 16418 as id -- main
UNION ALL SELECT indexrelid FROM pg_index WHERE indrelid = 16418 -- index
UNION ALL SELECT reltoastrelid FROM pg_class WHERE oid = 16418)); -- toast
```

This can be wrapped as a UDTF: `pg_table_size_detail`, for convenient use:

```sql
CREATE OR REPLACE FUNCTION pg_table_size_detail(relation RegClass)
  RETURNS TABLE(
    id      oid,
    pid     oid,
    relname name,
    nspname text,
    relkind "char",
    tuples  bigint,
    pages   integer,
    size    bigint
  )
AS $$
BEGIN
  RETURN QUERY
  SELECT
    rel.oid,
    relation::oid,
    rel.relname,
    rel.relnamespace :: RegNamespace :: Text as nspname,
    rel.relkind                              as relkind,
    rel.reltuples::bigint                    as tuples,
    rel.relpages                             as pages,
    pg_total_relation_size(oid)              as size
  FROM pg_class rel
  WHERE oid = ANY (array(
      SELECT relation as id -- main
      UNION ALL SELECT indexrelid FROM pg_index WHERE indrelid = relation -- index
      UNION ALL SELECT reltoastrelid FROM pg_class WHERE oid = relation)); -- toast
END;
$$
LANGUAGE PlPgSQL;

SELECT * FROM pg_table_size_detail(16418);
```

Sample return result:

```
geo=# select * from  pg_table_size_detail(4325625);
   id    |   pid   |        relname        | nspname  | relkind |  tuples  |  pages  |    size
---------+---------+-----------------------+----------+---------+----------+---------+-------------
 4325628 | 4325625 | pg_toast_4325625      | pg_toast | t       |   154336 |   23012 |   192077824
 4419940 | 4325625 | idx_poi_adcode_btree  | gaode    | i       | 62685464 |  172058 |  1409499136
 4419941 | 4325625 | idx_poi_cate_id_btree | gaode    | i       | 62685464 |  172318 |  1411629056
 4419942 | 4325625 | idx_poi_lat_btree     | gaode    | i       | 62685464 |  172058 |  1409499136
 4419943 | 4325625 | idx_poi_lon_btree     | gaode    | i       | 62685464 |  172058 |  1409499136
 4419944 | 4325625 | idx_poi_name_btree    | gaode    | i       | 62685464 |  335624 |  2749431808
 4325625 | 4325625 | gaode_poi             | gaode    | r       | 62685464 | 2441923 | 33714962432
 4420005 | 4325625 | idx_poi_position_gist | gaode    | i       | 62685464 |  453374 |  3714039808
 4420044 | 4325625 | poi_position_geohash6 | gaode    | i       | 62685464 |  172058 |  1409499136
```

### Example: Relation Size Details Summary

```sql
select
  nsp.nspname,
  rel.relname,
  rel.relnamespace    as nspid,
  rel.oid             as relid,
  rel.reltoastrelid   as toastid,
  toastind.indexrelid as toastindexid,
  pg_total_relation_size(rel.oid)  as size,
  pg_relation_size(rel.oid) + pg_relation_size(rel.oid,'fsm') 
  + pg_relation_size(rel.oid,'vm') as relsize,
  pg_indexes_size(rel.oid)         as indexsize,
  pg_total_relation_size(reltoastrelid) as toastsize,
  ind.indexids,
  ind.indexnames,
  ind.indexsizes
from pg_namespace nsp
  join pg_class rel on nsp.oid = rel.relnamespace
  ,LATERAL ( select indexrelid from pg_index where indrelid = rel.reltoastrelid) toastind
  , LATERAL ( select  array_agg(indexrelid) as indexids,
                      array_agg(indexrelid::RegClass) as indexnames,
                      array_agg(pg_total_relation_size(indexrelid)) as indexsizes
              from pg_index where indrelid = rel.oid) ind
where nspname not in ('pg_catalog', 'information_schema') and rel.relkind = 'r';
```