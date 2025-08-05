---
title: PostgreSQL Convention 2024
date: 2023-11-27
hero: /hero/pg-convention.jpg
author: |
  [Ruohang Feng](https://vonng.com/en/) ([@Vonng](https://vonng.com/en/)) | [Wechat Column](https://mp.weixin.qq.com/s/W1hwbl3qmjC4Dcmadc8uSg)
summary: >
  No rules, no standards. Some developer conventions for PostgreSQL 16.
tags: [PostgreSQL,Develop]
---

![](/img/blog/hero/pg-convention.jpg)

- [Background](#background)
- [0x01 Naming Convention](#0x01-naming-convention)
- [0x01 Design Convention](#0x02-design-convention)
- [0x01 Query Convention](#0x03-query-convention)
- [0x01 Admin Convention](#0x04-administration-convention)

> Roughly translated from [PostgreSQL Convention 2024](/pg/pg-convention/) with Google.

---------

## 0x00 Background

> No Rules, No Lines

The functions of PostgreSQL are very powerful, but to use PostgreSQL well requires the cooperation of backend, operation and maintenance, and DBA.

This article has compiled a development/operation and maintenance protocol based on the principles and characteristics of the PostgreSQL database, hoping to reduce the confusion you encounter when using the PostgreSQL database: hello, me, everyone.

The first version of this article is mainly for PostgreSQL 9.4 - PostgreSQL 10. The latest version has been updated and adjusted for PostgreSQL 15/16.


------------

## 0x01 naming convention

> There are only two hard problems in computer science: cache invalidation and **naming** .

**Generic naming rules** (Generic)

- This rule applies to all objects **in the database** , including: library names, table names, index names, column names, function names, view names, serial number names, aliases, etc.
- The object name must use only lowercase letters, underscores, and numbers, and the first letter must be a lowercase letter.
- The length of the object name must not exceed 63 characters, and the naming `snake_case`style must be uniform.
- The use of SQL reserved words is prohibited, use `select pg_get_keywords();`to obtain a list of reserved keywords.
- Dollar signs are prohibited `$`, Chinese characters are prohibited, and do not `pg`begin with .
- Improve your wording taste and be honest and elegant; do not use pinyin, do not use uncommon words, and do not use niche abbreviations.

**Cluster naming rules** (Cluster)

- The name of the PostgreSQL cluster will be used as the namespace of the cluster resource and must be a valid DNS domain name without any dots or underscores.
- The cluster name should start with a lowercase letter, contain only lowercase letters, numbers, and minus signs, and conform to the regular expression: `[a-z][a-z0-9-]*`.
- PostgreSQL database cluster naming usually follows a three-part structure: `pg-<biz>-<tld>`. Database type/business name/business line or environment
- `biz`The English words that best represent the characteristics of the business should only consist of lowercase letters and numbers, and should not contain hyphens `-`.
- When using a backup cluster to build a delayed slave database of an existing cluster, `biz`the name should be `<biz>delay`, for example `pg-testdelay`.
- When branching an existing cluster, you can `biz`add a number at the end of : for example, `pg-user1`you can branch from `pg-user2`, `pg-user3`etc.
- For horizontally sharded clusters, `biz`the name should include `shard`and be preceded by the shard number, for example `pg-testshard1`, `pg-testshard2`,...
- `<tld>`It is the top-level business line and can also be used to distinguish different environments: for example `-tt`, `-dev`, `-uat`, `-prod`etc. It can be omitted if not required.

**Service naming rules** (Service)

- Each PostgreSQL cluster will provide 2 to 6 types of external services, which use fixed naming rules by default.
- The service name is prefixed with the cluster name and the service type is suffixed, for example `pg-test-primary`, `pg-test-replica`.
- Read-write services are uniformly `primary`named with the suffix, and read-only services are uniformly `replica`named with the suffix. These two services are required.
- ETL pull/individual user query is `offline`named with the suffix, and direct connection to the main database/ETL write is `default`named with the suffix, which is an optional service.
- The synchronous read service is `standby`named with the suffix, and the delayed slave library service is `delayed`named with the suffix. A small number of core libraries can provide this service.

**Instance naming rules** (Instance)

- A PostgreSQL cluster consists of at least one instance, and each instance has a unique instance number assigned from zero or one within the cluster.
- **The instance name**`-` is composed of the cluster name + instance number with hyphens , for example: `pg-test-1`, `pg-test-2`.
- Once assigned, the instance number cannot be modified until the instance is offline and destroyed, and cannot be reassigned for use.
- The instance name will be used as a label for monitoring system data `ins`and will be attached to all data of this instance.
- If you are using a host/database 1:1 exclusive deployment, the node Hostname can use the database instance name.

**Database naming rules** (Database)

- The database name should be consistent with the cluster and application, and must be a highly distinguishable English word.
- The naming is `<tld>_<biz>`constructed in the form of , `<tld>`which is the top-level business line. It can also be used to distinguish different environments and can be omitted if not used.
- `<biz>`For a specific business name, for example, `pg-test-tt`the cluster can use the library name `tt_test`or `test`. This is not mandatory, i.e. it is allowed to create `<biz>`other databases with different cluster names.
- For sharded libraries, `<biz>`the section must `shard`end with but **should not** contain the shard number, for example `pg-testshard1`, `pg-testshard2`both `testshard`should be used.
- Multiple parts use `-`joins. For example: `<biz>-chat-shard`, `<biz>-payment`etc., no more than three paragraphs in total.

**Role naming convention** (Role/User)

- `dbsu`There is only one database super user : `postgres`, the user used for streaming replication is named `replicator`.
- The users used for monitoring are uniformly named `dbuser_monitor`, and the super users used for daily management are: `dbuser_dba`.
- The business user used by the program/service defaults to using `dbuser_<biz>`as the username, for example `dbuser_test`. Access from different services should be differentiated using separate business users.
- The database user applied for by the individual user agrees to use `dbp_<name>`, where is `name`the standard user name in LDAP.
- The default permission group naming is fixed as: `dbrole_readonly`, `dbrole_readwrite`, `dbrole_admin`, `dbrole_offline`.

**Schema naming rules** (Schema)

- The business uniformly uses a global `<prefix>`as the schema name, as short as possible, and is set to `search_path`the first element by default.
- `<prefix>`You must not use `public`, `monitor`, and must not conflict with any schema name used by PostgreSQL extensions, such as: `timescaledb`, `citus`, `repack`, `graphql`, `net`, `cron`,... It is not appropriate to use special names: `dba`, `trash`.
- Sharding mode naming rules adopt: `rel_<partition_total_num>_<partition_index>`. The middle is the total number of shards, which is currently fixed at 8192. The suffix is the shard number, counting from 0. Such as `rel_8192_0`,...,,, `rel_8192_11`etc.
- Creating additional schemas, or using `<prefix>`schema names other than , will require R&D to explain their necessity.

**Relationship naming rules** (Relation)

- The first priority for relationship naming is to have clear meaning. Do not use ambiguous abbreviations or be too lengthy. Follow general naming rules.
- Table names should use **plural nouns** and be consistent with historical conventions. Words with irregular plural forms should be avoided as much as possible.
- Views use `v_`as the naming prefix, materialized views use `mv_`as the naming prefix, temporary tables use `tmp_`as the naming prefix.
- Inherited or partitioned tables should be prefixed by the parent table name and suffixed by the child table attributes (rules, shard ranges, etc.).
- The time range partition uses the starting interval as the naming suffix. If the first partition has no upper bound, the R&D will specify a far enough time point: grade partition: `tbl_2023`, month-level partition `tbl_202304`, day-level partition `tbl_20230405`, hour-level partition `tbl_2023040518`. The default partition `_default`ends with .
- The hash partition is named with the remainder as the suffix of the partition table name, and the list partition is manually specified by the R&D team with a reasonable partition table name corresponding to the list item.

**Index naming rules** (Index)

- When creating an index, the index name should be **specified explicitly** and consistent with the PostgreSQL default naming rules.
- Index names are prefixed with the table name, primary key indexes `_pkey`end with , unique indexes `_key`end with , ordinary indexes end `_idx`with , and indexes used for `EXCLUDED`constraints `_excl`end with .
- When using conditional index/function index, the function and condition content used should be reflected in the index name. For example `tbl_md5_title_idx`, `tbl_ts_ge_2023_idx`, but the length limit cannot be exceeded.

**Field naming rules** (Attribute)

- It is prohibited to use system column reserved field names: `oid`, `xmin`, `xmax`, `cmin`, `cmax`, `ctid`.
- Primary key columns are usually named with `id`or as `id`a suffix.
- The conventional name is the creation time field `created_time`, and the conventional name is the last modification time field.`updated_time`
- `is_`It is recommended to use , etc. as the prefix for Boolean fields `has_`.
- Additional flexible JSONB fields are fixed using `extra`as column names.
- The remaining field names must be consistent with existing table naming conventions, and any field naming that breaks conventions should be accompanied by written design instructions and explanations.

**Enumeration item naming** (Enum)

- Enumeration items should be used by default `camelCase`, but other styles are allowed.

**Function naming rules** (Function)

- Function names start with verbs: `select`, `insert`, `delete`, `update`, `upsert`, `create`,….
- Important parameters can be reflected in the function name through `_by_ids`the `_by_user_ids`suffix of.
- Avoid function overloading and try to keep only one function with the same name.
- `BIGINT/INTEGER/SMALLINT`It is forbidden to overload function signatures through integer types such as , which may cause ambiguity when calling.
- Use named parameters for variables in stored procedures and functions, and avoid positional parameters ( `$1`, `$2`,...).
- If the parameter name conflicts with the object name, add before the parameter `_`, for example `_user_id`.

**Comment specifications** (Comment)

- Try your best to provide comments ( `COMMENT`) for various objects. Comments should be in English, concise and concise, and one line should be used.
- When the object's schema or content semantics change, be sure to update the annotations to keep them in sync with the actual situation.









------

## 0x02 Design Convention

> To each his own

**Things to note when creating a table**

- The DDL statement for creating a table needs to use the standard format, with SQL keywords in uppercase letters and other words in lowercase letters.
- Use lowercase letters uniformly in field names/table names/aliases, and try not to be case-sensitive. If you encounter a mixed case, or a name that conflicts with SQL keywords, you need to use double quotation marks for quoting.
- Use specialized type (NUMERIC, ENUM, INET, MONEY, JSON, UUID, ...) if applicable, and avoid using `TEXT` type as much as possible. The `TEXT` type is not conducive to the database's understanding of the data. Use these types to improve data storage, query, indexing, and calculation efficiency, and improve maintainability.
- Optimizing column layout and alignment types can have additional performance/storage gains.
- Unique constraints must be guaranteed by the database, and any unique column must have a corresponding unique constraint. `EXCLUDE`Constraints are generalized unique constraints that can be used to ensure data integrity in low-frequency update scenarios.

**Partition table considerations**

- If a single table exceeds hundreds of TB, or the monthly incremental data exceeds more than ten GB, you can consider table partitioning.
- A guideline for partitioning is to keep the size of each partition within the comfortable range of 1GB to 64GB.
- Tables that are conditionally partitioned by time range are first partitioned by time range. Commonly used granularities include: decade, year, month, day, and hour. The partitions required in the future should be created at least three months in advance.
- For extremely skewed data distributions, different time granularities can be combined, for example: 1900 - 2000 as one large partition, 2000 - 2020 as year partitions, and after 2020 as month partitions. When using time partitioning, the table name uses the value of the lower limit of the partition (if infinity, use a value that is far enough back).

**Notes on wide tables**

- Wide tables (for example, tables with dozens of fields) can be considered for vertical splitting, with mutual references to the main table through the same primary key.
- Because of the PostgreSQL MVCC mechanism, the write amplification phenomenon of wide tables is more obvious, reducing frequent updates to wide tables.
- In Internet scenarios, it is allowed to appropriately lower the normalization level and reduce multi-table connections to improve performance.

**Primary key considerations**

- Every table **must** have **an identity column** , and in principle it must have a primary key. The minimum requirement is to have **a non-null unique constraint** .
- The identity column is used to uniquely identify any tuple in the table, and logical replication and many third-party tools depend on it.
- If the primary key contains multiple columns, it should be specified using a single column after creating the field list of the table DDL `PRIMARY KEY(a,b,...)`.
- In principle, it is recommended to use integer `UUID`types for primary keys, which can be used with caution and text types with limited length. Using other types requires explicit explanation and evaluation.
- The primary key usually uses a single integer column. In principle, it is recommended to use it `BIGINT`. Use it with caution `INTEGER`and it is not allowed `SMALLINT`.
- The primary key should be used to `GENERATED ALWAYS AS IDENTITY`generate a unique primary key; `SERIAL`, `BIGSERIAL`which is only allowed when compatibility with PG versions below 10 is required.
- The primary key can use `UUID`the type as the primary key, and it is recommended to use UUID v1/v7; use UUIDv4 as the primary key with caution, as random UUID has poor locality and has a collision probability.
- When using a string column as a primary key, you should add a length limit. Generally used `VARCHAR(64)`, use of longer strings should be explained and evaluated.
- `INSERT/UPDATE`In principle, it is forbidden to modify the value of the primary key column, and `INSERT RETURNING` it can be used to return the automatically generated primary key value.

**Foreign key considerations**

- When defining a foreign key, the reference must explicitly set the corresponding action: `SET NULL`, `SET DEFAULT`, `CASCADE`, and use cascading operations with caution.
- The columns referenced by foreign keys need to be primary key columns in other tables/this table.
- Internet businesses, especially partition tables and horizontal shard libraries, use foreign keys with caution and can be solved at the application layer.

**Null/Default Value Considerations**

- If there is no distinction between zero and null values in the field semantics, null values are not allowed and `NOT NULL`constraints must be configured for the column.
- If a field has a default value semantically, `DEFAULT`the default value should be configured.

**Numeric type considerations**

- Used for regular numeric fields `INTEGER`. Used for numeric columns whose capacity is uncertain `BIGINT`.
- Don't use it without special reasons `SMALLINT`. The performance and storage improvements are very small, but there will be many additional problems.
- Note that the SQL standard does not provide unsigned integers, and values exceeding `INTMAX`but not exceeding `UINTMAX`need to be upgraded and stored. Do not store more `INT64MAX`values in `BIGINT`the column as it will overflow into negative numbers.
- `REAL`Represents a 4-byte floating point number, `FLOAT`represents an 8-byte floating point number. Floating point numbers can only be used in scenarios where the final precision doesn't matter, such as geographic coordinates. **Remember not to use equality judgment on floating point numbers, except for zero values** .
- Use exact numeric types `NUMERIC`. If possible, use `NUMERIC(p)`and `NUMERIC(p,s)`to set the number of significant digits and the number of significant digits in the decimal part. For example, the temperature in Celsius ( `37.0`) can `NUMERIC(3,1)`be stored with 3 significant digits and 1 decimal place using type.
- Currency value type is used `MONEY`.

**Text type considerations**

- PostgreSQL text types include `char(n)`, `varchar(n)`, `text`. By default, `text`the type can be used, which does not limit the string length, but is limited by the maximum field length of 1GB.
- If conditions permit, it is preferable to use `varchar(n)`the type to set a maximum string length. This will introduce minimal additional checking overhead, but can avoid some dirty data and corner cases.
- Avoid use `char(n)`, this type has unintuitive behavior (padding spaces and truncation) and has no storage or performance advantages in order to be compatible with the SQL standard.

**Time type considerations**

- There are only two ways to store time: with time zone `TIMESTAMPTZ`and without time zone `TIMESTAMP`.
- It is recommended to use one with time zone `TIMESTAMPTZ`. If you use `TIMESTAMP`storage, you must use 0 time zone standard time.
- Please use it to generate 0 time zone time `now() AT TIME ZONE 'UTC'`. You cannot truncate the time zone directly `now()::TIMESTAMP`.
- Uniformly use ISO-8601 format input and output time type: `2006-01-02 15:04:05`to avoid DMY and MDY problems.
- Users in China can use `Asia/Hong_Kong`the +8 time zone uniformly because the Shanghai time zone abbreviation `CST`is ambiguous.

**Notes on enumeration types**

- Fields that are more stable and have a small value space (within tens to hundreds) should use enumeration types instead of integers and strings.
- Enumerations are internally implemented using dynamic integers, which have readability advantages over integers and performance, storage, and maintainability advantages over strings.
- Enumeration items can only be added, not deleted, but existing enumeration values can be renamed. `ALTER TYPE <enum_name>`Used to modify enumerations.

**UUID type considerations**

- Please note that the fully random UUIDv4 has poor locality when used as a primary key. Consider using UUIDv1/v7 instead if possible.
- Some UUID generation/processing functions require additional extension plug-ins, such as `uuid-ossp`, `pg_uuidv7` etc. If you have this requirement, please specify it during configuration.

**JSON type considerations**

- Unless there is a special reason, always use the binary storage `JSONB`type and related functions instead of the text version `JSON`.
- Note the subtle differences between atomic types in JSON and their PostgreSQL counterparts: the zero character `text`is not allowed in the type corresponding to a JSON string `\u0000`, and the and `numeric`is not allowed in the type corresponding to a JSON numeric type . Boolean values only accept lowercase and literal values.`NaN``infinity``true``false`
- Please note that objects in the JSON standard `null`and null values in the SQL standard `NULL` are not the same concept.

**Array type considerations**

- When storing a small number of elements, array fields can be used instead of individually.
- Suitable for storing data with a relatively small number of elements and infrequent changes. If the number of elements in the array is very large or changes frequently, consider using a separate table to store the data and using foreign key associations.
- For high-dimensional floating-point arrays, consider using `pgvector`the dedicated data types provided by the extension.

**GIS type considerations**

- The GIS type uses the srid=4326 reference coordinate system by default.
- Longitude and latitude coordinate points should use the Geography type without explicitly specifying the reference system coordinates 4326

**Trigger considerations**

- Triggers will increase the complexity and maintenance cost of the database system, and their use is discouraged in principle. The use of rule systems is prohibited and such requirements should be replaced by triggers.
- Typical scenarios for triggers are to automatically modify a row to the current timestamp after modifying it `updated_time`, or to record additions, deletions, and modifications of a table to another log table, or to maintain business consistency between the two tables.
- Operations in triggers are transactional, meaning if the trigger or operations in the trigger fail, the entire transaction is rolled back, so test and prove the correctness of your triggers thoroughly. Special attention needs to be paid to recursive calls, deadlocks in complex query execution, and the execution sequence of multiple triggers.

**Stored procedure/function considerations**

- Functions/stored procedures are suitable for encapsulating transactions, reducing concurrency conflicts, reducing network round-trips, reducing the amount of returned data, and executing **a small amount** of custom logic.

- Stored procedures **are not suitable** for complex calculations, and are not suitable for trivial/frequent type conversion and packaging. In critical high-load systems, **unnecessary** computationally intensive logic in the database should be removed, such as using SQL in the database to convert WGS84 to other coordinate systems. Calculation logic closely related to data acquisition and filtering can use functions/stored procedures: for example, geometric relationship judgment in PostGIS.

- Replaced functions and stored procedures that are no longer in use should be taken offline in a timely manner to avoid conflicts with future functions.

- Use a unified syntax format for function creation. The signature occupies a separate line (function name and parameters), the return value starts on a separate line, and the language is the first label. Be sure to mark the function volatility level: `IMMUTABLE`, `STABLE`, `VOLATILE`. Add attribute tags, such as: `RETURNS NULL ON NULL INPUT`, `PARALLEL SAFE`, `ROWS 1`etc.

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

**Use sensible Locale options**

- Used by default `en_US.UTF8`and cannot be changed without special reasons.
- The default `collate`rule must be `C`, to avoid string indexing problems.
- https://mp.weixin.qq.com/s/SEXcyRFmdXNI7rpPUB3Zew

**Use reasonable character encoding and localization configuration**

- Character encoding must be used `UTF8`, any other character encoding is strictly prohibited.
- Must be used `C`as `LC_COLLATE`the default collation, any special requirements must be explicitly specified in the DDL/query clause to implement.
- Character set `LC_CTYPE`is used by default `en_US.UTF8`, some extensions rely on character set information to work properly, such as `pg_trgm`.

**Notes on indexing**

- All online queries must design corresponding indexes according to their access patterns, and full table scans are not allowed except for very small tables.
- Indexes have a price, and it is not allowed to create unused indexes. Indexes that are no longer used should be cleaned up in time.
- When building a joint index, columns with high differentiation and selectivity should be placed first, such as ID, timestamp, etc.
- GiST index can be used to solve the nearest neighbor query problem, and traditional B-tree index cannot provide good support for KNN problem.
- For data whose values are linearly related to the storage order of the heap table, if the usual query is a range query, it is recommended to use the BRIN index. The most typical scenario is to only append written time series data. BRIN index is more efficient than Btree.
- When retrieving against JSONB/array fields, you can use GIN indexes to speed up queries.

**Clarify the order of null values in B-tree indexes**

- `NULLS FIRST`If there is a sorting requirement on a nullable column, it needs to be explicitly specified in the query and index `NULLS LAST`.
- Note that `DESC`the default rule for sorting is `NULLS FIRST`that null values appear first in the sort, which is generally not desired behavior.
- The sorting conditions of the index must match the query, such as:`CREATE INDEX ON tbl (id DESC NULLS LAST);`

**Disable indexing on large fields**

- The size of the indexed field cannot exceed 2KB (1/3 of the page capacity). You need to be careful when creating indexes on text types. The text to be indexed should use `varchar(n)`types with length constraints.
- When a text type is used as a primary key, a maximum length must be set. In principle, the length should not exceed 64 characters. In special cases, the evaluation needs to be explicitly stated.
- If there is a need for large field indexing, you can consider hashing the large field and establishing a function index. Or use another type of index (GIN).

**Make the most of functional indexes**

- Any redundant fields that can be inferred from other fields in the same row can be replaced using functional indexes.
- For statements that often use expressions as query conditions, you can use expression or function indexes to speed up queries.
- Typical scenario: Establish a hash function index on a large field, and establish a `reverse`function index for text columns that require left fuzzy query.

**Take advantage of partial indexes**

- For the part of the query where the query conditions are fixed, partial indexes can be used to reduce the index size and improve query efficiency.
- If a field to be indexed in a query has only a limited number of values, several corresponding partial indexes can also be established.
- If the columns in some indexes are frequently updated, please pay attention to the expansion of these indexes.







------

## 0x03 Query Convention

> The limits of my language mean the limits of my world.
>
> —Ludwig Wittgenstein

**Use service access**

- Access to the production database must be through domain name access [services](https://doc.pigsty.cc/#/zh/PGSQL-SVC) , and direct connection using IP addresses is strictly prohibited.
- VIP is used for services and access, LVS/HAProxy shields the role changes of cluster instance members, and master-slave switching does not require application restart.

**Read and write separation**

- Internet business scenario: Write requests must go through the main library and be accessed through the Primary service.
- In principle, read requests go from the slave library and are accessed through the Replica service.
- Exceptions: If you need "Read Your Write" consistency guarantees, and significant replication delays are detected, read requests can access the main library; or apply to the DBA to provide Standby services.


**Separation of speed and slowness**

- Queries within 1 millisecond in production are called fast queries, and queries that exceed 1 second in production are called slow queries.
- Slow queries must go to the offline slave database - Offline service/instance, and a timeout should be set during execution.
- In principle, the execution time of online general queries in production should be controlled within 1ms.
- If the execution time of an online general query in production exceeds 10ms, the technical solution needs to be modified and optimized before going online.
- Online queries should be configured with a Timeout of the order of 10ms or faster to avoid avalanches caused by accumulation.
- ETL data from the primary is prohibited, and the offline service should be used to retrieve data from a dedicated instance.

**Use connection pool**

- Production applications must access the database through a connection pool and the PostgreSQL database through a 1:1 deployed Pgbouncer proxy. Offline service, individual users are strictly prohibited from using the connection pool directly.
- Pgbouncer connection pool uses Transaction Pooling mode by default. Some session-level functions may not be available (such as Notify/Listen), so special attention is required. Pre-1.21 Pgbouncer does not support the use of Prepared Statements in this mode. In special scenarios, you can use Session Pooling or bypass the connection pool to directly access the database, which requires special DBA review and approval.
- When using a connection pool, it is prohibited to modify the connection status, including modifying connection parameters, modifying search paths, changing roles, and changing databases. The connection must be completely destroyed after modification as a last resort. Putting the changed connection back into the connection pool will lead to the spread of contamination. Use of pg_dump to dump data via Pgbouncer is strictly prohibited.

**Configure active timeout for query statements**

- Applications should configure active timeouts for all statements and proactively cancel requests after timeout to avoid avalanches. (Go context)
- Statements that are executed periodically must be configured with a timeout smaller than the execution period to avoid avalanches.
- HAProxy is configured with a default connection timeout of 24 hours for rolling expired long connections. Please do not run SQL that takes more than 1 day to execute on offline instances. This requirement will be specially adjusted by the DBA.

**Pay attention to replication latency**

- Applications must be aware of synchronization delays between masters and slaves and properly handle situations where replication delays exceed reasonable limits.
- Under normal circumstances, replication delays are on the order of 100µs/tens of KB, but in extreme cases, slave libraries may experience replication delays of minutes/hours. Applications should be aware of this phenomenon and have corresponding degradation plans - Select Read from the main library and try again later, or report an error directly.

**Retry failed transactions**

- **Queries** may be killed due to concurrency contention, administrator commands, etc. Applications need to be aware of this and retry if necessary.
- When the application reports a large number of errors in the database, it can trigger the circuit breaker to avoid an avalanche. But be careful to distinguish the type and nature of errors.

**Disconnected and reconnected**

- The database **connection** may be terminated for various reasons, and the application **must** have a disconnection reconnection mechanism.
- It can be used `SELECT 1`as a heartbeat packet query to detect the presence of messages on the connection and keep it alive periodically.

**Online service application code prohibits execution of DDL**

- It is strictly forbidden to execute DDL in production applications and do not make big news in the application code.
- Exception scenario: Creating new time partitions for partitioned tables can be carefully managed by the application.
- Special exception: Databases used by office systems, such as Gitlab/Jira/Confluence, etc., can grant application DDL permissions.

**SELECT statement explicitly specifies column names**

- Avoid using it `SELECT *`, or `RETURNING`use it in a clause `*`. Please use a specific field list and do not return unused fields. When the table structure changes (for example, a new value column), queries that use column wildcards are likely to encounter column mismatch errors.
- After the fields of some tables are maintained, the order will change. For example: after `id`upgrading the INTEGER primary key to `BIGINT`, `id`the column order will be the last column. This problem can only be fixed during maintenance and migration. R&D developers should resist the compulsion to adjust the column order and explicitly specify the column order in the SELECT statement.
- Exception: Wildcards are allowed when a stored procedure returns a specific table row type.

**Disable online query full table scan**

- Exceptions: constant minimal table, extremely low-frequency operations, table/return result set is very small (within 100 records/100 KB).
- Using negative operators such as on the first-level filter condition will result in a full table scan and must be `!=`avoided .`<>`

**Disallow long waits in transactions**

- Transactions must be committed or rolled back as soon as possible after being started. Transactions that exceed 10 minutes `IDEL IN Transaction`will be forcibly killed.
- Applications should enable AutoCommit to avoid `BEGIN`unpaired `ROLLBACK`or unpaired applications later `COMMIT`.
- Try to use the transaction infrastructure provided by the standard library, and do not control transactions manually unless absolutely necessary.

**Things to note when using count**

- `count(*)`It is the standard syntax for **counting rows** and has nothing to do with null values.
- `count(col)`The count is **the number of non-null records**`col` in the column . NULL values in this column will not be counted.
- `count(distinct col)`When `col`deduplicating columns and counting them, null values are also ignored, that is, only the number of non-null distinct values is counted.
- `count((col1, col2))`When counting multiple columns, even if the columns to be counted are all empty, they will still be counted. `(NULL,NULL)`This is valid.
- `a(distinct (col1, col2))`For multi-column deduplication counting, even if the columns to be counted are all empty, they will be counted, `(NULL,NULL)`which is effective.

**Things to note when using aggregate functions**

- All `count`aggregate functions except `NULL`But `count(col)`in this case it will be returned `0`as an exception.
- If returning null from an aggregate function is not expected, use `coalesce`to set a default value.

**Handle null values with caution**

- Clearly distinguish between zero values and null values. Use null values `IS NULL`for equivalence judgment, and use regular `=`operators for zero values for equivalence judgment.
- When a null value is used as a function input parameter, it should have a type modifier, otherwise the overloaded function will not be able to identify which one to use.
- Pay attention to the null value comparison logic: the result of any comparison operation involving null values is `unknown`  you need to pay attention to `null` the logic involved in Boolean operations:
  - `and`: `TRUE or NULL`Will return due to logical short circuit `TRUE`.
  - `or`: `FALSE and NULL`Will return due to logical short circuit`FALSE`
  - In other cases, as long as the operand appears `NULL`, the result is`NULL`

- The result of logical judgment between null value and **any value** is null value, for example, `NULL=NULL`the return result is `NULL`not `TRUE/FALSE`.

- For equality comparisons involving null values and non-null values, please use ``IS DISTINCT FROM ` `for comparison to ensure that the comparison result is not null.

- NULL values and aggregate functions: When **all** input values are NULL, the aggregate function returns NULL.

**Note that the serial number is empty**

- When using `Serial`types, `INSERT`, `UPSERT`and other operations will consume sequence numbers, and this consumption will not be rolled back when the transaction fails.
- When using an integer `INTEGER`as the primary key and the table has frequent insertion conflicts, you need to pay attention to the problem of integer overflow.

**The cursor must be closed promptly after use**

**Repeated queries using prepared statements**

- **Prepared Statements** should be used for repeated queries to eliminate the CPU overhead of database hard parsing. Pgbouncer versions earlier than 1.21 cannot support this feature in transaction pooling mode, please pay special attention.
- Prepared statements will modify the connection status. Please pay attention to the impact of the connection pool on prepared statements.

**Choose the appropriate transaction isolation level**

- The default isolation level is **read committed** , which is suitable for most simple read and write transactions. For ordinary transactions, choose the lowest isolation level that meets the requirements.
- For write transactions that require transaction-level consistent snapshots, use the **Repeatable Read** isolation level.
- For write transactions that have strict requirements on correctness (such as money-related), use the **serializable** isolation level.
- When a concurrency conflict occurs between the RR and SR isolation levels, the application should actively retry depending on the error type.

rh 09 **Do not use count when judging the existence of a result.**

- It is faster than Count to `SELECT 1 FROM tbl WHERE xxx LIMIT 1`judge whether there are columns that meet the conditions.
- `SELECT exists(SELECT * FROM tbl WHERE xxx LIMIT 1)`The existence result can be converted to a Boolean value using .

**Use the RETURNING clause to retrieve the modified results in one go**

- `RETURNING`The clause can be used after the `INSERT`, `UPDATE`, `DELETE`statement to effectively reduce the number of database interactions.

**Use UPSERT to simplify logic**

- When the business has an insert-failure-update sequence of operations, consider using `UPSERT`substitution.

**Use advisory locks to deal with hotspot concurrency** .

- For extremely high-frequency concurrent writes (spike) of single-row records, advisory locks should be used to lock the record ID.
- If high concurrency contention can be resolved at the application level, don't do it at the database level.

**Optimize IN operator**

- Use `EXISTS`clause instead of `IN`operator for better performance.
- Use `=ANY(ARRAY[1,2,3,4])`instead `IN (1,2,3,4)`for better results.
- Control the size of the parameter list. In principle, it should not exceed 10,000. If it exceeds, you can consider batch processing.

**It is not recommended to use left fuzzy search**

- Left fuzzy search `WHERE col LIKE '%xxx'`cannot make full use of B-tree index. If necessary, `reverse`expression function index can be used.

**Use arrays instead of temporary tables**

- Consider using an array instead of a temporary table, for example when obtaining corresponding records for a series of IDs. `=ANY(ARRAY[1,2,3])`Better than temporary table JOIN.












------

## 0x04 Administration Convention

**Use Pigsty to build PostgreSQL cluster and infrastructure**

- The production environment uses the Pigsty trunk version uniformly, and deploys the database on x86_64 machines and CentOS 7.9 / RockyLinux 8.8 operating systems.
- `pigsty.yml`Configuration files usually contain highly sensitive and important confidential information. Git should be used for version management and access permissions should be strictly controlled.
- `files/pki`The CA private key and other certificates generated within the system should be properly kept, regularly backed up to a secure area for storage and archiving, and access permissions should be strictly controlled.
- All passwords are not allowed to use default values, and make sure they have been changed to new passwords with sufficient strength.
- Strictly control access rights to management nodes and configuration code warehouses, and only allow DBA login and access.

**Monitoring system is a must**

- Any deployment must have a monitoring system, and the production environment uses at least two sets of Infra nodes to provide redundancy.

**Properly plan the cluster architecture according to needs**

- Any production database cluster managed by a DBA must have at least one online slave database for online failover.
- The template is used by default `oltp`, the analytical database uses `olap`the template, the financial database uses `crit`the template, and the micro virtual machine (within four cores) uses `tiny`the template.
- For businesses whose annual data volume exceeds 1TB, or for clusters whose write TPS exceeds 30,000 to 50,000, you can consider building a horizontal sharding cluster.

**Configure cluster high availability using Patroni and Etcd**

- The production database cluster uses Patroni as the high-availability component and etcd as the DCS.
- `etcd`Use a dedicated virtual machine cluster, with 3 to 5 nodes, strictly scattered and distributed on different cabinets.
- Patroni Failsafe mode must be turned on to ensure that the cluster main library can continue to work when etcd fails.

**Configure cluster PITR using pgBackRest and MinIO**

- The production database cluster uses pgBackRest as the backup recovery/PITR solution and MinIO as the backup storage warehouse.
- MinIO uses a multi-node multi-disk cluster, and can also use S3/OSS/COS services instead. Password encryption must be set for cold backup.
- All database clusters perform a local full backup every day, retain the backup and WAL of the last week, and save a full backup every other month.
- When a WAL archiving error occurs, you should check the backup warehouse and troubleshoot the problem in time.

**Core business database configuration considerations**

- The core business cluster needs to configure at least two online slave libraries, one of which is a dedicated offline query instance.
- The core business cluster needs to build a delayed slave cluster with a 24-hour delay for emergency data recovery.
- Core business clusters usually use asynchronous submission, while those related to money use synchronous submission.

**Financial database configuration considerations**

- The financial database cluster requires at least two online slave databases, one of which is a dedicated synchronization Standby instance, and Standby service access is enabled.
- Money-related libraries must use `crit`templates with RPO = 0, enable synchronous submission to ensure zero data loss, and enable Watchdog as appropriate.
- Money-related libraries must be forced to turn on data checksums and, if appropriate, turn on full DML logs.

**Use reasonable character encoding and localization configuration**

- Character encoding must be used `UTF8`, any other character encoding is strictly prohibited.
- Must be used `C`as `LC_COLLATE`the default collation, any special requirements must be explicitly specified in the DDL/query clause to implement.
- Character set `LC_CTYPE`is used by default `en_US.UTF8`, some extensions rely on character set information to work properly, such as `pg_trgm`.

**Business database management considerations**

- Multiple different databases are allowed to be created in the same cluster, and Ansible scripts must be used to create new business databases.
- All business databases must exist synchronously in the Pgbouncer connection pool.

**Business user management considerations**

- Different businesses/services must use different database users, and Ansible scripts must be used to create new business users.
- All production business users must be synchronized in the user list file of the Pgbouncer connection pool.
- Individual users should set a password with a default validity period of 90 days and change it regularly.
- Individual users are only allowed to access authorized cluster offline instances or slave `pg_offline_query`libraries with from the springboard machine.

**Notes on extension management**

- `yum/apt`When installing a new extension, you must first install the corresponding major version of the extension binary package in all instances of the cluster .
- Before enabling the extension, you need to confirm whether the extension needs to be added `shared_preload_libraries`. If necessary, a rolling restart should be arranged.
- Note that `shared_preload_libraries`in order of priority, `citus`, `timescaledb`, `pgml`are usually placed first.
- `pg_stat_statements`and `auto_explain`are required plugins and must be enabled in all clusters.
- Install extensions uniformly using , and create them `dbsu`in the business database .`CREATE EXTENSION`

**Database XID and age considerations**

- Pay attention to the age of the database and tables to avoid running out of XID transaction numbers. If the usage exceeds 20%, you should pay attention; if it exceeds 50%, you should intervene immediately.
- When processing XID, execute the table one by one in order of age from largest to smallest `VACUUM FREEZE`.

**Database table and index expansion considerations**

- Pay attention to the expansion rate of tables and indexes to avoid index performance degradation, and use `pg_repack`online processing to handle table/index expansion problems.
- Generally speaking, indexes and tables whose expansion rate exceeds 50% can be considered for reorganization.
- When dealing with table expansion exceeding 100GB, you should pay special attention and choose business low times.

**Database restart considerations**

- Before restarting the database, execute it `CHECKPOINT`twice to force dirty pages to be flushed, which can speed up the restart process.
- Before restarting the database, perform `pg_ctl reload`reload configuration to confirm that the configuration file is available normally.
- To restart the database, use `pg_ctl restart`patronictl or patronictl to restart the entire cluster at the same time.
- Use `kill -9`to shut down any database process is strictly prohibited.

**Replication latency considerations**

- Monitor replication latency, especially when using replication slots.

**New slave database data warm-up**

- When adding a new slave database instance to a high-load business cluster, the new database instance should be warmed up, and the HAProxy instance weight should be gradually adjusted and applied in gradients: 4, 8, 16, 32, 64, and 100. `pg_prewarm`Hot data can be loaded into memory using .

**Database publishing process**

- Online database release requires several evaluation stages: R&D self-test, supervisor review, QA review (optional), and DBA review.
- During the R&D self-test phase, R&D should ensure that changes are executed correctly in the development and pre-release environments.
  - If a new table is created, the record order magnitude, daily data increment estimate, and read and write throughput magnitude estimate should be given.
  - If it is a new function, the average execution time and extreme case descriptions should be given.
  - If it is a mode change, all upstream and downstream dependencies must be sorted out.
  - If it is a data change and record revision, a rollback SQL must be given.
- The R&D Team Leader needs to evaluate and review changes and be responsible for the content of the changes.
- The DBA evaluates and reviews the form and impact of the release, puts forward review opinions, and calls back or implements them uniformly.

**Data work order format**

- Database changes are made through the platform, with one work order for each change.
- The title is clear: A certain business needs `xx`to perform an action in the database `yy`.
- The goal is clear: what operations need to be performed on which instances in each step, and how to verify the results.
- Rollback plan: Any changes need to provide a rollback plan, and new ones also need to provide a cleanup script.
- Any changes need to be recorded and archived, and have complete approval records. They are first approved by the R&D superior TL Review and then approved by the DBA.

**Database change release considerations**

- Using a unified release window, changes of the day will be collected uniformly at 16:00 every day and executed sequentially; requirements confirmed by TL after 16:00 will be postponed to the next day. Database release is not allowed after 19:00. For emergency releases, please ask TL to make special instructions and send a copy to the CTO for approval before execution.
- Database DDL changes and DML changes are uniformly `dbuser_dba`executed remotely using the administrator user to ensure that the default permissions work properly.
- When the business administrator executes DDL by himself, **he must**`SET ROLE dbrole_admin` first execute the release to ensure the default permissions.
- Any changes require a rollback plan before they can be executed, and very few operations that cannot be rolled back need to be handled with special caution (such as enumeration of value additions)
- Database changes use `psql`command line tools, connect to the cluster main database to execute, use `\i`execution scripts or `\e`manual execution in batches.

**Things to note when deleting tables**

- The production data table `DROP`should be renamed first and allowed to cool for 1 to 3 days to ensure that it is not accessed before being removed.
- When cleaning the table, you must sort out all dependencies, including directly and indirectly dependent objects: triggers, foreign key references, etc.
- The temporary table to be deleted is usually placed in `trash`Schema and `ALTER TABLE SET SCHEMA`the schema name is modified.
- In high-load business clusters, when removing particularly large tables (> 100G), select business valleys to avoid preempting I/O.

**Things to note when creating and deleting indexes**

- You must use `CREATE INDEX CONCURRENTLY`concurrent index creation and `DROP INDEX CONCURRENTLY`concurrent index removal.
- When rebuilding an index, always create a new index first, then remove the old index, and modify the new index name to be consistent with the old index.
- After index creation fails, you should remove `INVALID`the index in time. After modifying the index, use `analyze`to re-collect statistical data on the table.
- When the business is idle, you can enable parallel index creation and set it `maintenance_work_mem`to a larger value to speed up index creation.

**Make schema changes carefully**

- Try to avoid full table rewrite changes as much as possible. Full table rewrite is allowed for tables within 1GB. The DBA should notify all relevant business parties when the changes are made.
- When adding new columns to an existing table, you should avoid using functions in default values `VOLATILE`to avoid a full table rewrite.
- When changing a column type, all functions and views that depend on that type should be rebuilt if necessary, and `ANALYZE`statistics should be refreshed.

**Control the batch size of data writing**

- Large batch write operations should be divided into small batches to avoid generating a large amount of WAL or occupying I/O at one time.
- After a large batch `UPDATE`is executed, `VACUUM`the space occupied by dead tuples is reclaimed.
- The essence of executing DDL statements is to modify the system directory, and it is also necessary to control the number of DDL statements in a batch.

**Data loading considerations**

- Use `COPY`load data, which can be executed in parallel if necessary.
- You can temporarily shut down before loading data `autovacuum`, disable triggers as needed, and create constraints and indexes after loading.
- Turn it up `maintenance_work_mem`, increase it `max_wal_size`.
- Executed after loading is complete `vacuum verbose analyze table`.

**Notes on database migration and major version upgrades**

- The production environment uniformly uses standard migration to build script logic, and realizes requirements such as non-stop cluster migration and major version upgrades through blue-green deployment.
- For clusters that do not require downtime, you can use `pg_dump | psql`logical export and import to stop and upgrade.

**Data Accidental Deletion/Accidental Update Process**

- After an accident occurs, immediately assess whether it is necessary to stop the operation to stop bleeding, assess the scale of the impact, and decide on treatment methods.
- If there is a way to recover on the R&D side, priority will be given to the R&D team to make corrections through SQL publishing; otherwise, use `pageinspect`and `pg_dirtyread`to rescue data from the bad table.
- If there is a delayed slave library, extract data from the delayed slave library for repair. First, confirm the time point of accidental deletion, and advance the delay to extract data from the database to the XID.
- A large area was accidentally deleted and written. After communicating with the business and agreeing, perform an in-place PITR rollback to a specific time.

**Data corruption processing process**

- Confirm whether the slave database data can be used for recovery. If the slave database data is intact, you can switchover to the slave database first.
- Temporarily shut down `auto_vacuum`, locate the root cause of the error, replace the failed disk and add a new slave database.
- If the system directory is damaged, or use to `pg_filedump`recover data from table binaries.
- If the CLOG is damaged, use `dd`to generate a fake submission record.

**Things to note when the database connection is full**

- When the connection is full (avalanche), immediately use the kill connection query to cure the symptoms and stop the loss: `pg_cancel_backend`or `pg_terminate_backend`.
- Use to `pg_terminate_backend`abort all normal backend processes, `psql` `\watch 1`starting with once per second ( ). And confirm the connection status from the monitoring system. If the accumulation continues, continue to increase the execution frequency of the connection killing query, for example, once every 0.1 seconds until there is no more accumulation.
- After confirming that the bleeding has stopped from the monitoring system, try to stop the killing connection. If the accumulation reappears, immediately resume the killing connection. Immediately analyze the root cause and perform corresponding processing (upgrade, limit current, add index, etc.)