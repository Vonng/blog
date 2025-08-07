---
title: "PostgreSQL Trigger Usage Considerations"
date: 2018-07-07
author: "vonng"
summary: >
  Detailed understanding of trigger management and usage in PostgreSQL
tags: [PostgreSQL, PG Development, Triggers]
---

## Overview

* Trigger behavior overview
* Trigger classification
* Trigger functionality
* Trigger types
* Trigger firing
* Trigger creation
* Trigger modification
* Trigger queries
* Trigger performance

## Trigger Overview

Trigger behavior overview: [English](https://www.postgresql.org/docs/11/trigger-definition.html), [Chinese](http://www.postgres.cn/docs/11/trigger-definition.html)

## Trigger Classification

Trigger timing: `BEFORE`, `AFTER`, `INSTEAD`

Trigger events: `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`

Trigger scope: Statement-level, row-level

Internal creation: Constraint triggers, user-defined triggers

Trigger modes: `origin|local(O)`, `replica(R)`, `disable(D)`

## Trigger Operations

Trigger operations are performed through SQL DDL statements, including `CREATE|ALTER|DROP TRIGGER`, and `ALTER TABLE ENABLE|DISABLE TRIGGER`. Note that PostgreSQL's internal constraints are implemented through triggers.

#### Creation

[`CREATE TRIGGER`](https://www.postgresql.org/docs/current/sql-createtrigger.html) can be used to create triggers.

```sql
CREATE [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    [ FROM referenced_table_name ]
    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
    [ REFERENCING { { OLD | NEW } TABLE [ AS ] transition_relation_name } [ ... ] ]
    [ FOR [ EACH ] { ROW | STATEMENT } ]
    [ WHEN ( condition ) ]
    EXECUTE { FUNCTION | PROCEDURE } function_name ( arguments )

event includes:
    INSERT
    UPDATE [ OF column_name [, ... ] ]
    DELETE
    TRUNCATE
```

#### Deletion

[`DROP TRIGGER`](https://www.postgresql.org/docs/current/sql-droptrigger.html) is used to remove triggers.

```sql
DROP TRIGGER [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

#### Modification

[`ALTER TRIGGER`](https://www.postgresql.org/docs/current/sql-altertrigger.html) is used to modify trigger definitions. Note that this can only modify trigger names and their dependent extensions.

```sql
ALTER TRIGGER name ON table_name RENAME TO new_name
ALTER TRIGGER name ON table_name DEPENDS ON EXTENSION extension_name
```

Enabling/disabling triggers and modifying trigger modes is implemented through [`ALTER TABLE`](https://www.postgresql.org/docs/11/sql-altertable.html) clauses.

[`ALTER TABLE`](https://www.postgresql.org/docs/11/sql-altertable.html) contains a series of trigger modification clauses:

```sql
ALTER TABLE tbl ENABLE TRIGGER tgname; -- Set trigger mode to O (local connection writes trigger, default)
ALTER TABLE tbl ENABLE REPLICA TRIGGER tgname; -- Set trigger mode to R (replica connection writes trigger)
ALTER TABLE tbl ENABLE ALWAYS TRIGGER tgname; -- Set trigger mode to A (always trigger)
ALTER TABLE tbl DISABLE TRIGGER tgname; -- Set trigger mode to D (disabled)
```

Note that when `ENABLE` and `DISABLE` triggers, you can specify `USER` to replace specific trigger names, which allows disabling only user-explicitly-created triggers without disabling system triggers used to maintain constraints.

```sql
ALTER TABLE tbl_name DISABLE TRIGGER USER; -- Disable all user-defined triggers, system triggers unchanged  
ALTER TABLE tbl_name DISABLE TRIGGER ALL;  -- Disable all triggers
ALTER TABLE tbl_name ENABLE TRIGGER USER;  -- Enable all user-defined triggers
ALTER TABLE tbl_name ENABLE TRIGGER ALL;   -- Enable all triggers
```

#### Queries

**Getting table triggers**

The simplest way is psql's `\d+ tablename`. But this method only lists user-created triggers, not triggers associated with table constraints. Query system catalog `pg_trigger` directly and filter by table name through `tgrelid`:

```sql
SELECT * FROM pg_trigger WHERE tgrelid = 'tbl_name'::RegClass;
```

**Getting trigger definitions**

The `pg_get_triggerdef(trigger_oid oid)` function can provide trigger definitions.

This function takes trigger OID as input parameter and returns the SQL DDL statement that creates the trigger.

```sql
SELECT pg_get_triggerdef(oid) FROM pg_trigger; -- WHERE xxx
```

## Trigger Views

[`pg_trigger`](https://www.postgresql.org/docs/current/catalog-pg-trigger.html) ([Chinese](http://www.postgres.cn/docs/11/catalog-pg-trigger.html)) provides the catalog of triggers in the system.

| Name             | Type           | Reference             | Description                                        |
| ---------------- | -------------- | --------------------- | -------------------------------------------------- |
| `oid`            | `oid`          |                       | Trigger object identifier, system hidden column   |
| `tgrelid`        | `oid`          | `pg_class.oid`        | OID of the table the trigger is on                |
| `tgname`         | `name`         |                       | Trigger name, unique within table-level namespace |
| `tgfoid`         | `oid`          | `pg_proc.oid`         | Function called by the trigger                     |
| `tgtype`         | `int2`         |                       | Trigger type, trigger conditions, see comments    |
| `tgenabled`      | `char`         |                       | Trigger mode, see below. `O|R|A|D`                |
| `tgisinternal`   | `bool`         |                       | True if internal trigger for constraints          |
| `tgconstrrelid`  | `oid`          | `pg_class.oid`        | Referenced table in referential integrity constraint, 0 if none |
| `tgconstrindid`  | `oid`          | `pg_class.oid`        | Related index supporting constraint, 0 if none    |
| `tgconstraint`   | `oid`          | `pg_constraint.oid`   | **Constraint** object related to trigger          |
| `tgdeferrable`   | `bool`         |                       | True if `DEFERRED`                                |
| `tginitdeferred` | `bool`         |                       | True if `INITIALLY DEFERRED`                      |
| `tgnargs`        | `int2`         |                       | Number of string arguments passed to trigger function |
| `tgattr`         | `int2vector`   | `pg_attribute.attnum` | Column numbers for column-level update triggers, empty array otherwise |
| `tgargs`         | `bytea`        |                       | Argument strings passed to trigger, C-style null-terminated strings |
| `tgqual`         | `pg_node_tree` |                       | Internal representation of trigger `WHEN` condition |
| `tgoldtable`     | `name`         |                       | `REFERENCING` column name for `OLD TABLE`, empty if none |
| `tgnewtable`     | `name`         |                       | `REFERENCING` column name for `NEW TABLE`, empty if none |

## Trigger Types

Trigger type `tgtype` contains trigger condition information: `BEFORE|AFTER|INSTEAD OF`, `INSERT|UPDATE|DELETE|TRUNCATE`

```c
TRIGGER_TYPE_ROW         (1 << 0)  // [0] 0:statement-level 	1:row-level
TRIGGER_TYPE_BEFORE      (1 << 1)  // [1] 0:AFTER 	1:BEFORE
TRIGGER_TYPE_INSERT      (1 << 2)  // [2] 1: INSERT
TRIGGER_TYPE_DELETE      (1 << 3)  // [3] 1: DELETE
TRIGGER_TYPE_UPDATE      (1 << 4)  // [4] 1: UPDATE
TRIGGER_TYPE_TRUNCATE    (1 << 5)  // [5] 1: TRUNCATE
TRIGGER_TYPE_INSTEAD     (1 << 6)  // [6] 1: INSTEAD OF 
```

## Trigger Modes

The trigger `tgenabled` field controls the trigger's working mode. Parameter [`session_replication_role`](http://www.postgres.cn/docs/11/runtime-config-client.html#GUC-SESSION-REPLICATION-ROLE) can be used to configure trigger firing modes. This parameter can be changed at session level, possible values include: `origin(default)`, `replica`, `local`.

`(D)isable` triggers are never fired, `(A)lways` triggers fire in any situation, `(O)rigin` triggers fire in `origin|local` mode (default), while `(R)eplica` triggers fire in `replica` mode. R triggers are mainly used for logical replication, for example `pglogical` replication connections set session parameter `session_replication_role` to `replica`, and R triggers only fire on changes made by that connection.

```sql
ALTER TABLE tbl ENABLE TRIGGER tgname; -- Set trigger mode to O (local connection writes trigger, default)
ALTER TABLE tbl ENABLE REPLICA TRIGGER tgname; -- Set trigger mode to R (replica connection writes trigger)
ALTER TABLE tbl ENABLE ALWAYS TRIGGER tgname; -- Set trigger mode to A (always trigger)
ALTER TABLE tbl DISABLE TRIGGER tgname; -- Set trigger mode to D (disabled)
```

In `information_schema` there are two more trigger-related views: `information_schema.triggers`, `information_schema.triggered_update_columns`, but they're not discussed here.

## Trigger FAQ

### What types of tables can triggers be created on?

Regular tables (partitioned table parent tables, partitioned table partitions, inheritance table parent tables, inheritance table child tables), views, foreign tables.

### Trigger type restrictions

* Views don't allow `BEFORE` and `AFTER` triggers (whether row-level or statement-level)
* Views can only have `INSTEAD OF` triggers built, `INSTEAD OF` triggers can only be built on views, and only row-level, no statement-level `INSTEAD OF` triggers exist.
* `INSTEAD OF` triggers can only be defined on views and must use row-level triggers, not statement-level triggers.

### Triggers and locks

Creating triggers on tables first attempts to acquire table-level `Share Row Exclusive Lock`. This lock blocks data changes to the underlying table and is self-exclusive. Therefore creating triggers blocks writes to the table.

### Triggers and COPY relationship

COPY only eliminates the overhead of data parsing and packaging. When actually writing to the table, it still fires triggers, just like INSERT.