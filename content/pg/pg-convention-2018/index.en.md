---
title: "PostgreSQL Development Convention (2018 Edition)"
linkTitle: "PostgreSQL Development Convention 2018 Edition"
date: 2018-06-20
author: "vonng"
summary: "Without rules, there can be no order. This article compiles a development specification for PostgreSQL database principles and features, which can reduce confusion encountered when using PostgreSQL."
tags: ["PostgreSQL","PG Development","Convention"]
---

## 0x00 Background

> Without rules, there can be no order.

PostgreSQL is extremely powerful, but to use PostgreSQL well requires coordinated effort from backend developers, operations teams, and DBAs.

This article compiles a development specification based on PostgreSQL database principles and features, hoping to reduce confusion encountered when using PostgreSQL. Good for you, good for me, good for everyone.

## 0x01 Naming Conventions

> The nameless is the beginning of heaven and earth; the named is the mother of all things.

【Mandatory】 **General Naming Rules**

* This rule applies to all object names, including: database names, table names, column names, function names, view names, sequence names, aliases, etc.
* Object names must only use lowercase letters, underscores, numbers, but must start with a lowercase letter. Regular tables are prohibited from starting with `_`.
* Object names must not exceed 63 characters, naming uniformly adopts `snake_case`.
* Prohibited to use SQL reserved words. Use `select pg_get_keywords();` to get reserved keyword list.
* Prohibited to use dollar signs, Chinese characters, don't start with `pg`.
* Improve vocabulary taste, be clear and elegant; don't use pinyin, don't use obscure words, don't use niche abbreviations.

【Mandatory】 **Database Naming Rules**

* Database names should ideally match the application or service, must be highly distinctive English words.
* Naming must start with `<biz>-`, where `<biz>` is the specific business line name. If it's a shard database, it must end with `-shard`.
* Multiple parts connected with `-`. Examples: `<biz>-chat-shard`, `<biz>-payment`, etc., no more than three segments total.

【Mandatory】 **Role Naming Conventions**

* Database `su` has one and only one: `postgres`. User for streaming replication named `replication`.
* Production users use `<biz>-` as prefix, specific function as suffix.
* All databases have three basic roles by default: `<biz>-read`, `<biz>-write`, `<biz>-usage`, with read-only, write-only, and function execution permissions for all tables respectively.
* Production users, ETL users, and personal users obtain permissions by inheriting corresponding basic roles.
* More fine-grained permission control uses independent roles and users, varies by business.

【Mandatory】 **Schema Naming Rules**

* Business uniformly uses `<*>` as schema name, where `<*>` is business-defined name, must be set as first element of `search_path`.
* `dba`, `monitor`, `trash` are reserved schema names.
* Shard schema naming rule: `rel_<partition_total_num>_<partition_index>`.
* No special reason to create objects in other schemas.

【Recommended】 **Relation Naming Rules**

* Relation naming should prioritize clear meaning, don't use ambiguous abbreviations, shouldn't be overly lengthy, follow general naming rules.
* Table names should use plural nouns, consistent with historical conventions, but avoid words with irregular plural forms.
* Views use `v_` as naming prefix, materialized views use `mv_` as naming prefix, temporary tables use `tmp_` as naming prefix.
* Inherited or partition tables should use parent table name as prefix, with child table characteristics (rules, shard ranges, etc.) as suffix.

【Recommended】 **Index Naming Rules**

* When creating indexes, **if possible** specify index names and maintain consistency with PostgreSQL default naming rules to avoid creating duplicate indexes on repeated execution.
* Indexes for primary keys end with `_pkey`, unique indexes end with `_key`, indexes for `EXCLUDED` constraints end with `_excl`, regular indexes end with `_idx`.

【Recommended】 **Function Naming Rules**

* Start with `select`, `insert`, `delete`, `update`, `upsert` to indicate action type.
* Important parameters can be reflected in function names through suffixes like `_by_ids`, `_by_user_ids`.
* Avoid function overloading, keep only one function with the same name.
* Prohibited to overload through `BIGINT/INTEGER/SMALLINT` integer types, may cause ambiguity when calling.

【Recommended】 **Field Naming Rules**

* Must not use system column reserved field names: `oid`, `xmin`, `xmax`, `cmin`, `cmax`, `ctid`, etc.
* Primary key columns usually named `id`, or use `id` as suffix.
* Creation time usually named `created_time`, modification time usually named `updated_time`.
* Boolean fields suggest using `is_`, `has_` etc. as prefixes.
* Other field names need to maintain consistency with existing table naming conventions.

【Recommended】 **Variable Naming Rules**

* Variables in stored procedures and functions use named parameters, not positional parameters.
* If parameter names conflict with object names, add `_` after parameter, e.g., `user_id_`.

【Recommended】 **Comment Conventions**

* Try to provide comments (`COMMENT`) for objects, comments use English, concise and clear, preferably one line.
* When object schema or content semantics change, must update comments accordingly, keeping in sync with actual situation.

## 0x02 Design Conventions

> Suum cuique

【Mandatory】 **Character encoding must be UTF8**

* Prohibited to use any other character encoding.

【Mandatory】 **Capacity Planning**

- Single table over 100 million records, or exceeding 10GB scale, consider starting table partitioning.
- Single table capacity over 1T, single database capacity over 2T. Need to consider sharding.

【Mandatory】 **Don't abuse stored procedures**

* Stored procedures suitable for encapsulating transactions, reducing concurrency conflicts, reducing network round trips, reducing return data volume, executing **small amounts** of custom logic.
* Stored procedures **not suitable** for complex calculations, not suitable for trivial/frequent type conversions and wrapping.

【Mandatory】 **Storage-compute separation**

* Remove **unnecessary** compute-intensive logic from database, such as using SQL in database for WGS84 to other coordinate system conversions.
* Exception: Computational logic closely related to data retrieval and filtering allowed in database, such as geometric relationship judgments in PostGIS.

【Mandatory】 **Primary keys and identity columns**

* Every table must have **identity column**, in principle must have primary key, minimum requirement is having **non-null unique constraint**.
* Identity column used to uniquely identify any tuple in table, logical replication and many third-party tools depend on this.

【Mandatory】 **Foreign keys**

* Not recommended to use foreign keys, suggest solving at application layer. When using foreign keys, references must set corresponding actions: `SET NULL`, `SET DEFAULT`, `CASCADE`, use cascade operations carefully.

【Mandatory】 **Use wide tables carefully**

* Tables with more than 15 fields considered wide tables, wide tables should consider vertical splitting, referencing each other through same primary key with main table.
* Due to MVCC mechanism, write amplification in wide tables is quite obvious, try to reduce frequent updates to wide tables.

【Mandatory】 **Configure appropriate default values**

* Columns with default values must add `DEFAULT` clause specifying default value.
* Can use functions in default values to dynamically generate default values (e.g., primary key generators).

【Mandatory】 **Properly handle null values**

- Fields with no semantic distinction between zero and null values don't allow null values, must configure `NOT NULL` constraint for columns.

【Mandatory】 **Unique constraints enforced by database**

* Unique constraints must be guaranteed by database, any unique column must have unique constraint.
* `EXCLUDE` constraint is generalized unique constraint, can be used to ensure data integrity in low-frequency update scenarios.

【Mandatory】 **Pay attention to integer overflow risk**

* Note that SQL standard doesn't provide unsigned integer types, values exceeding `INTMAX` but not `UINTMAX` need upgraded storage.
* Don't store values exceeding `INT64MAX` in `BIGINT` columns, will overflow to negative numbers.

【Mandatory】 **Unified timezone**

* Use `TIMESTAMP` to store time, use `utc` timezone.
* Uniformly use ISO-8601 format for inputting/outputting time types: `2006-01-02 15:04:05`, avoid DMY vs MDY issues.
* When using `TIMESTAMPTZ`, use GMT/UTC time, 0 timezone standard time.

【Mandatory】 **Timely cleanup of outdated functions**

- Functions no longer used or replaced should be taken offline promptly to avoid conflicts with future functions.

【Recommended】 **Primary key types**

- Primary keys usually use integer type, recommend using `BIGINT`, allow using strings no longer than 64 bytes.
- Primary keys allow using `Serial` auto-generation, recommend using `Default next_id()` generator functions.

【Recommended】 **Choose appropriate types**

* When specialized types can be used, don't use strings. (Numbers, enums, network addresses, currency, JSON, UUID, etc.)
* Using correct data types can significantly improve data storage, query, index, computation efficiency, and improve maintainability.

【Recommended】 **Use enum types**

* Relatively stable fields with small value space (within a dozen) should use enum types, don't use integers and strings to represent.
* Using enum types has advantages in performance, storage, and maintainability.

【Recommended】 **Choose appropriate text types**

* PostgreSQL text types include `char(n)`, `varchar(n)`, `text`.
* Usually recommend using `varchar` or `text`. Types with `(n)` modifier check string length, causing minor additional overhead. When string length limits are needed, use `varchar(n)` to avoid inserting overly long dirty data.
* Avoid using `char(n)`. For SQL standard compatibility, this type has unintuitive behavior (padding spaces and truncation), and has no storage or performance advantages.

【Recommended】 **Choose appropriate numeric types**

* Regular numeric fields use `INTEGER`. Primary keys, capacity uncertain numeric columns use `BIGINT`.
* Don't use `SMALLINT` without special reason, performance and storage improvements are minimal, will have many additional problems.
* `REAL` represents 4-byte floating point, `FLOAT` represents 8-byte floating point
* Floating point numbers only usable in scenarios where end precision doesn't matter, such as geographic coordinates. Don't use equality comparisons on floating point numbers.
* Exact numeric types use `NUMERIC`, pay attention to precision and decimal place settings.
* Monetary numeric types use `MONEY`.

【Recommended】 **Use unified function creation syntax**

- Signature occupies separate line (function name and parameters), return value starts new line, language as first tag.
- Must annotate function volatility level: `IMMUTABLE`, `STABLE`, `VOLATILE`.
- Add definite attribute tags, such as: `RETURNS NULL ON NULL INPUT`, `PARALLEL SAFE`, `ROWS 1`, pay attention to version compatibility.

```sql
CREATE OR REPLACE FUNCTION
  nspname.myfunc(arg1_ TEXT, arg2_ INTEGER)
  RETURNS VOID
LANGUAGE SQL
STABLE
PARALLEL SAFE
ROWS 1
RETURNS NULL ON NULL INPUT
AS $function$
SELECT 1;
$function$;
```

【Recommended】 **Design for evolvability**

* When designing tables, should fully consider future expansion needs, can appropriately add 1-3 reserved fields when creating tables.
* For variable non-critical fields, can use JSON type.

【Recommended】 **Choose reasonable normalization level**

- Allow appropriately reducing normalization level, reducing multi-table joins to improve performance.

【Recommended】 **Use new versions**

- New versions have cost-free performance improvements, stability improvements, more new features.
- Fully utilize new features, reduce design complexity.

【Recommended】 **Use triggers carefully**

* Triggers increase system complexity and maintenance costs, not encouraged.

## 0x03 Index Conventions

> Wer Ordnung hält, ist nur zu faul zum Suchen.

【Mandatory】 **Online queries must have supporting indexes**

- All online queries must design corresponding indexes for their access patterns, full table scans not allowed except for very few small tables.
- Indexes have costs, not allowed to create unused indexes.

【Mandatory】 **Prohibited to build indexes on large fields**

- Indexed field size cannot exceed 2KB (1/3 page capacity), in principle prohibited to exceed 64 characters.
- If large field indexing needed, consider hashing large fields and building function indexes. Or use other types of indexes (GIN).

【Mandatory】 **Specify null value sorting rules**

* If sorting needed on nullable columns, need to explicitly specify `NULLS FIRST` or `NULLS LAST` in queries and indexes.
* Note that default rule for `DESC` sorting is `NULLS FIRST`, meaning null values appear at the front of sort, usually not desired behavior.
* Index sorting conditions must match query, such as: `create index on tbl (id desc nulls last);`

【Mandatory】 **Use GiST indexes for nearest neighbor queries**

- Traditional B-tree indexes cannot provide good support for KNN problems, should use GiST indexes.

【Recommended】 **Utilize function indexes**

* Any redundant fields that can be inferred from other fields in the same row can use function indexes instead.
* For statements frequently using expressions as query conditions, can use expression or function indexes to accelerate queries.
* Typical scenarios: Build hash function indexes on large fields, build reverse function indexes for text columns needing left fuzzy queries.

【Recommended】 **Utilize partial indexes**

* Fixed parts in query conditions can use partial indexes, reducing index size and improving query efficiency.
* If indexed field in query has only limited few values, can also build several corresponding partial indexes.

【Recommended】 **Utilize range indexes**

* For data where values are linearly correlated with heap table storage order, if usual queries are range queries, recommend using BRIN indexes.
* Most typical scenario is append-only time series data, BRIN indexes more efficient.

【Recommended】 **Pay attention to composite index selectivity**

* Put columns with high selectivity first.

## 0x04 Query Conventions

> The limits of my language mean the limits of my world.
>
> —Ludwig Wittgenstein

【Mandatory】 **Read-write separation**

- In principle, write requests go to primary, read requests go to replica.
- Exception: Need read-your-own-write consistency guarantee, and significant replication lag detected.

【Mandatory】 **Fast-slow separation**

- Queries within 1ms in production called fast queries, queries over 1 second in production called slow queries.
- Slow queries must go to offline replica, must set appropriate timeouts.
- Online regular query execution time in production should in principle be controlled within 1ms.
- Online regular query execution time in production exceeding 10ms needs technical solution modification, optimize to standard before going online.
- Online queries should configure 10ms level or faster timeouts, avoid accumulation causing avalanche.
- Master and Slave roles not allowed to bulk pull data, data warehouse ETL programs should pull data from Offline replicas.

【Mandatory】 **Active timeout**

- Configure active timeout for all statements, actively cancel requests after timeout to avoid avalanche.
- Periodically executed statements must configure timeout smaller than execution period.

【Mandatory】 **Pay attention to replication lag**

- Applications must be aware of sync lag between primary and replica, and properly handle situations where replication lag exceeds reasonable range.
- Usually 0.1ms lag can reach tens of minutes or even hours in extreme cases. Applications can choose to read from primary, retry later, or report error.

【Mandatory】 **Use connection pooling**

- Applications must access database through connection pooling, connect to port 6432's pgbouncer instead of port 5432's postgres.
- Note differences between using connection pooling vs direct database connection, some features may not be available (like Notify/Listen), may also have connection pollution issues.

【Mandatory】 **Prohibited to modify connection state**

- When using public connection pools, prohibited to modify connection state, including modifying connection parameters, changing search path, switching roles, switching databases.
- If absolutely necessary to modify, must completely destroy connection. Returning state-changed connections to connection pool will cause pollution spread.

【Mandatory】 **Retry failed transactions**

- **Queries** may be killed due to concurrency contention, admin commands, etc. Applications need to be aware of this and retry when necessary.
- Applications can trigger circuit breaker when database reports many errors, avoid avalanche. But pay attention to distinguishing error types and nature.

【Mandatory】 **Reconnect on disconnect**

* **Connections** may be terminated for various reasons, applications **must** have disconnect-reconnect mechanism.
* Can use `SELECT 1` as heartbeat query to check connection liveness and keep alive regularly.

【Mandatory】 **Online service application code prohibited from executing DDL**

* Don't make big news in application code.

【Mandatory】 **Explicitly specify column names**

* Avoid using `SELECT *`, or using `*` in `RETURNING` clauses. Please use specific field lists, don't return unused fields. When table structure changes (e.g., new columns), queries using column wildcards may experience column count mismatch errors.
* Exception: When stored procedures return specific table row types, wildcards allowed.

【Mandatory】 **Prohibited full table scans in online queries**

- Exceptions: constant tiny tables, extremely low frequency operations, tables/result sets very small (within hundreds of records/hundreds of KB).
- Using negation operators like `!=`, `<>` in first-level filter conditions causes full table scans, must avoid.

【Mandatory】 **Prohibited long waits in transactions**

* Must commit or rollback promptly after starting transaction, `IDLE IN Transaction` over 10 minutes will be forcibly killed.
* Applications should enable AutoCommit, avoid unpaired `ROLLBACK` or `COMMIT` after `BEGIN`.
* Try to use standard library provided transaction infrastructure, don't manually control transactions unless absolutely necessary.

【Mandatory】 **Must close cursors promptly after use**

【Mandatory】 **Scientific counting**

* `count(*)` is standard syntax for **counting rows**, unrelated to null values.
* `count(col)` counts **non-null records** in `col` column. NULL values in this column not counted.
* `count(distinct col)` distinct count on `col` column, also ignores null values, only counts non-null distinct values.
* `count((col1, col2))` multi-column count, even if counted columns are all null will be counted, `(NULL,NULL)` valid.
* `count(distinct (col1, col2))` multi-column distinct count, even if counted columns all null will be counted, `(NULL,NULL)` valid.

【Mandatory】 **Pay attention to null value issues in aggregate functions**

* All aggregate functions except `count` ignore null value inputs, so when all input values are null, result is `NULL`. But `count(col)` returns 0 in this case, an exception.
* If aggregate function returning null is not desired result, use `coalesce` to set default value.

【Mandatory】**Handle null values carefully**

- Clearly distinguish zero values from null values, null values use `IS NULL` for equality judgment, zero values use regular `=` operator for equality judgment.
- When null values serve as function input parameters, should have type modifiers, otherwise overloaded functions cannot identify which to use.
- Pay attention to null value comparison logic: any comparison operation involving null values results in `unknown`, need to pay attention to `unknown` participating in boolean operations:
  - `and`: `TRUE or UNKNOWN` returns `TRUE` due to logical short-circuit.
  - `or`: `FALSE and UNKNOWN` returns `FALSE` due to logical short-circuit
  - Other cases where operands have `UNKNOWN`, results are all `UNKNOWN`
- Logical judgment between null values and **any value** results in null value, e.g., `NULL=NULL` returns `NULL` not `TRUE/FALSE`.
- For equality comparisons involving null and non-null values, use `IS DISTINCT FROM` for comparison, ensuring non-null comparison results.
- Null values and aggregate functions: aggregate functions return NULL when **all** input values are NULL.

【Mandatory】 **Pay attention to sequence number gaps**

* When using `Serial` type, operations like `INSERT`, `UPSERT` consume sequence numbers, this consumption won't rollback with transaction failure.
* When using integers as primary keys and table has frequent insert conflicts, need to pay attention to integer overflow issues.

【Recommended】 **Use prepared statements for repeated queries**

- Repeated queries should use **prepared statements**, eliminating database hard parsing CPU overhead.
- Prepared statements modify connection state, pay attention to connection pool impact on prepared statements.

【Recommended】 **Choose appropriate transaction isolation level**

- Default isolation level is **read committed**, suitable for most simple read-write transactions, regular transactions choose minimum isolation level meeting requirements.
- Write transactions needing transaction-level consistent snapshots, use **repeatable read** isolation level.
- Write transactions with strict correctness requirements use **serializable** isolation level.
- When concurrency conflicts occur in RR and SR isolation levels, should actively retry based on error type.

【Recommended】 **Don't use count to judge result existence**

* Use `SELECT 1 FROM tbl WHERE xxx LIMIT 1` to judge if records meeting conditions exist, faster than Count.
* Can use `select exists(select * FROM app.sjqq where xxx limit 1)` to convert existence result to boolean value.

【Recommended】 **Use RETURNING clause**

* If users need to immediately get inserted, deleted, or modified data after inserting, before deleting, or after modifying data, recommend using `RETURNING` clause to reduce database interactions.

【Recommended】 **Use UPSERT to simplify logic**

* When business has insert-fail-update operation sequences, consider using `UPSERT` instead.

【Recommended】 **Use advisory locks for hotspot concurrency**

* For extremely high frequency concurrent writes to single records (flash sales), should use advisory locks to lock record IDs.
* If high concurrency contention can be solved at application layer, don't put it at database layer.

【Recommended】**Optimize IN operator**

* Use `EXISTS` clause instead of `IN` operator for better results.
* Use `=ANY(ARRAY[1,2,3,4])` instead of `IN (1,2,3,4)` for better results.

【Recommended】 **Left fuzzy search not recommended**

* Left fuzzy search `WHERE col LIKE '%xxx'` cannot fully utilize B-tree indexes, if needed, can use `reverse` expression function indexes.

【Recommended】 **Use arrays instead of temporary tables**

* Consider using arrays instead of temporary tables, e.g., when getting corresponding records for a series of IDs. `=ANY(ARRAY[1,2,3])` better than temporary table JOIN.

## 0x05 Release Conventions

【Mandatory】 **Release format**

* Currently submit releases via email, send emails to dba@p1.com for archiving and scheduling.
* Clear title: xx project needs to execute xx action in xx database.
* Clear objectives: each step needs to execute what operations on which instances, how to verify results.
* Rollback plan: any changes need to provide rollback plan, new creations also need cleanup scripts.

【Mandatory】**Release evaluation**

- Online database releases need to go through developer self-testing, supervisor review, (optional QA review), DBA review evaluation stages.
- Self-testing stage should ensure changes execute correctly in development and pre-production environments.
  - If creating new tables, should provide record quantity scale, daily data increment estimates, read-write volume estimates.
  - If creating new functions, should provide stress test reports, at least need average execution time.
  - If schema migration, must clearly sort out all upstream and downstream dependencies.
- Team Leader needs to evaluate and review changes, responsible for change content.
- DBA evaluates and reviews release format and impact.

【Mandatory】 **Release window**

* No database releases allowed after 19:00, emergency releases require TL special explanation, copy CTO.
* Requirements confirmed after 16:00 will be postponed to next day. (Based on TL confirmation time)

## 0x06 Management Conventions

【Mandatory】 **Pay attention to backups**

* Daily full backups, continuous archiving of WAL segments

【Mandatory】 **Pay attention to age**

* Pay attention to database and table age, avoid transaction ID wraparound.

【Mandatory】 **Pay attention to aging and bloat**

* Pay attention to table and index bloat rates, avoid performance degradation.

【Mandatory】 **Pay attention to replication lag**

* Monitor replication lag, must pay special attention when using replication slots.

【Mandatory】 **Follow minimum privilege principle**

【Mandatory】**Create and drop indexes concurrently**

* For production tables, must use `CREATE INDEX CONCURRENTLY` to create indexes concurrently.

【Mandatory】 **New replica data prewarming**

* Use `pg_prewarm`, or gradually introduce traffic.

【Mandatory】 **Carefully perform schema changes**

* When adding new columns must use syntax without default values, avoid full table rewrite
* When changing types, must rebuild all functions depending on that type when necessary.

【Recommended】 **Split large batch operations**

* Large batch write operations should be split into small batches, avoid generating large amounts of WAL at once.

【Recommended】 **Accelerate data loading**

* Turn off `autovacuum`, use `COPY` to load data.
* Build constraints and indexes afterwards.
* Increase `maintenance_work_mem`, increase `max_wal_size`.
* Execute `vacuum verbose analyze table` after completion.