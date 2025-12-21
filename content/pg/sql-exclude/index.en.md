---
title: "Implementing Mutual Exclusion Constraints with Exclude"
date: 2018-04-06
author: "vonng"
summary: >
  Exclude constraint is a PostgreSQL extension that can implement more advanced and sophisticated database constraints.
tags: [PostgreSQL, PG-Development, SQL]
---

Exclude constraint is a PostgreSQL extension that can implement more advanced and sophisticated database constraints.

-----------

## Introduction

Data integrity is extremely important, but data integrity guaranteed by applications isn't always reliable: humans make mistakes, programs have bugs. If data integrity can be enforced through database constraints, that would be ideal: backend programmers don't need to worry about subtle errors caused by race conditions, and data analysts can be confident in data quality without needing validation and cleaning.

Relational databases typically provide `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK` constraints, but not all business constraints can be expressed with these few constraint types. Some constraints are slightly more complex, such as ensuring IP network segments in an IP range table don't overlap, ensuring the same conference room doesn't have overlapping reservation times, ensuring geographical boundaries of different cities in an administrative division table don't overlap. Traditionally implementing such guarantees is quite difficult: for instance, `UNIQUE` constraints cannot express this semantic, while `CHECK` with stored procedures or triggers can implement such checks but are quite tricky. PostgreSQL's `EXCLUDE` constraint can elegantly solve this class of problems.

-----------

## Exclude Constraint Syntax

```sql
 EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
 
exclude_element in an EXCLUDE constraint is:
{ column_name | ( expression ) } [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]
```

The `EXCLUDE` clause defines an exclusion constraint, which guarantees that if any two rows are compared on the specified columns or expressions using the specified operators, not all comparisons will return `TRUE`. If all specified operators test for equality, this is equivalent to a `UNIQUE` constraint, although a normal unique constraint would be faster. However, exclusion constraints can specify more general constraints than simple equality. For example, you can use the `&&` operator to specify a constraint requiring no two rows in the table contain overlapping circles (see [Section 8.8](http://www.postgres.cn/docs/11/datatype-geometric.html)).

Exclusion constraints are implemented using an index, so each specified operator must be associated with an appropriate operator class (see [Section 11.9](http://www.postgres.cn/docs/11/indexes-opclass.html)) for the index access method *index_method*. The operators are required to be commutative. Each *exclude_element* can optionally specify an operator class or ordering options, which are fully described in [???](http://www.postgres.cn/docs/11/SQL-CREATETABLE.html).

The access method must support `amgettuple` (see [Chapter 61](http://www.postgres.cn/docs/11/indexam.html)), which currently means GIN cannot be used. Although allowed, using B-tree or hash indexes in an exclusion constraint makes no sense, as they cannot do better than a normal unique index. Therefore in practice, the access method will always be GiST or SP-GiST.

The *predicate* allows you to specify an exclusion constraint on a subset of the table. Internally this creates a partial index. Note that surrounding parentheses are required for this.

-------------

## Use Case: Conference Room Reservation

Suppose we want to design a conference room reservation system and ensure at the database level that no conflicting room reservations occur: that is, for the same conference room, we don't allow two reservation records with overlapping time ranges to exist simultaneously. The database table can be designed like this:

```sql
-- Built-in PostgreSQL extension, adds GIST index operator support for common types
CREATE EXTENSION btree_gist;

-- Conference room reservation table
CREATE TABLE meeting_room
(
    id      SERIAL PRIMARY KEY,
    user_id INTEGER,
    room_id INTEGER,
    range   tsrange,
    EXCLUDE USING GIST(room_id WITH = , range WITH &&)
);
```

Here `EXCLUDE USING GIST(room_id WITH = , range WITH &&)` specifies an exclusion constraint: not allowing multiple records where `room_id` is equal and `range` overlaps.

```sql
-- User 1 reserves room 101, from 10 AM to 6 PM
INSERT INTO meeting_room(user_id, room_id, range) 
VALUES (1,101, tsrange('2019-01-01 10:00', '2019-01-01 18:00'));

-- User 2 also tries to reserve room 101, from 4 PM to 6 PM
INSERT INTO meeting_room(user_id, room_id, range) 
VALUES (2,101, tsrange('2019-01-01 16:00', '2019-01-01 18:00'));

-- User 2's reservation errors, violating the exclusion constraint
ERROR:  conflicting key value violates exclusion constraint "meeting_room_room_id_range_excl"
DETAIL:  Key (room_id, range)=(101, ["2019-01-01 16:00:00","2019-01-01 18:00:00")) conflicts with existing key (room_id, range)=(101, ["2019-01-01 10:00:00","2019-01-01 18:00:00")).
```

The `EXCLUDE` constraint automatically creates a corresponding GIST index:

```sql
"meeting_room_room_id_range_excl" EXCLUDE USING gist (room_id WITH =, range WITH &&)
```

------------

## Use Case: Ensuring IP Network Segments Don't Overlap

Some constraints are quite complex, such as ensuring IP ranges in a table don't overlap, similarly ensuring geographical boundaries of different cities in an administrative division table don't overlap. Traditionally implementing such guarantees is quite difficult: for instance, `UNIQUE` constraints cannot express this semantic, while `CHECK` with stored procedures or triggers can implement such checks but are quite tricky. PostgreSQL's `EXCLUDE` constraint can elegantly solve this problem. Modify our `geoips` table:

```sql
create table geoips
(
  ips          inetrange,
  geo          geometry(Point),
  country_code text,
  region_code  text,
  city_name    text,
  ad_code      text,
  postal_code  text,
  EXCLUDE USING gist (ips WITH &&) DEFERRABLE INITIALLY DEFERRED 
);
```

Here `EXCLUDE USING gist (ips WITH &&)` means the `ips` field doesn't allow overlapping ranges, i.e., newly inserted fields cannot overlap with any existing ranges (where `&&` returns true). `DEFERRABLE INITIALLY DEFERRED` means check constraints on all rows when the statement ends. Creating this constraint automatically creates a GIST index on the `ips` field, so manual creation is not needed.