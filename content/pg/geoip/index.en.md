---
title: "GeoIP Geographic Reverse Lookup Optimization"
date: 2018-07-07
author: "vonng"
summary: >
  A common requirement in application development is GeoIP conversion - converting source IP addresses to geographic coordinates or administrative divisions (country-state-city-county-town-village)
tags: [PostgreSQL, PG-Development, Extension, GIS]
---


> Efficient implementation of IP geolocation lookups

In application development, a 'very common' requirement is GeoIP conversion - converting source IP addresses from requests into corresponding geographic coordinates or administrative divisions (country-state-city-county-town-village). This functionality has many uses, such as analyzing geographic sources of website traffic or doing some shady things. Using PostgreSQL can achieve this requirement elegantly and efficiently with high performance and cost effectiveness.




-------------

## 0x01 Approach and Methods

Usually, IP geographic databases on the internet are in the format: `start_ip, stop_ip, longitude, latitude`, with some additional attribute fields like country codes, city codes, postal codes, etc. It looks roughly like this:

| Column       | Type |
|--------------|------|
| start_ip     | text |
| end_ip       | text |
| longitude    | text |
| latitude     | text |
| country_code | text |
| ……           | text |

Essentially, the core is mapping from **IP address ranges** to **geographic coordinate points**.

A typical query actually provides an IP address and returns the geographic range corresponding to that address. The logic expressed in SQL looks roughly like this:

```sql
SELECT longitude, latitude FROM geoip 
WHERE start_ip <= target_ip AND target_ip <= stop_ip;
```

However, to provide direct service, several issues need to be resolved:

* First issue: Although IPv4 is actually a `uint32`, we're completely accustomed to the textual representation like `123.123.123.123`. This textual representation cannot be compared for size.
* Second issue: The IP range here is represented by two IP boundary fields, so is this range an open or closed interval? Do we need an additional field to represent this?
* Third issue: For efficient querying, how should indexes on two fields be established?
* Fourth issue: We want all IP segments to not overlap with each other, but a simple unique constraint on `(start_ip, stop_ip)` cannot guarantee this - what should we do?

Fortunately, for PostgreSQL, these are not problems. The four issues above can be easily solved using PostgreSQL features.

* Network data types: High-performance, compact, flexible network address representation.
* Range types: Good abstraction for intervals, good support for interval queries and operations.
* GiST indexes: Can be applied to both IP address ranges and geographic location points.
* Exclude constraints: Generalized advanced UNIQUE constraints that fundamentally ensure data integrity.




-------------

## 0x01 Network Address Types

PostgreSQL provides data types for storing IPv4, IPv6, and MAC addresses, including `cidr`, `inet`, and `macaddr`, along with many common operation functions, eliminating the need to implement tedious repetitive functionality in programs.

The most common network address is IPv4 address, corresponding to PostgreSQL's built-in `inet` type. The inet type can store IPv4, IPv6 addresses, or with an optional subnet. Of course, these detailed operations can be [referenced in the documentation](http://www.postgres.cn/docs/9.6/datatype-net-types.html) and won't be detailed here.

One point to note is that although we know IPv4 is essentially an `Unsigned Integer`, storing it as `INTEGER` in the database actually doesn't work because the SQL standard doesn't support `Unsigned` usage, so half of the IP addresses would be interpreted as negative numbers, producing surprising results when comparing sizes. If you really want to store it this way, please use `BIGINT`. Moreover, directly facing a bunch of long integers is quite headache-inducing, so `inet` is the best choice.

If you need to convert between IP addresses (`inet` type) and corresponding integers, just perform addition and subtraction with `0.0.0.0`; you can also use the following functions and create a type conversion to directly convert between `inet` and `bigint`:

```sql
-- inet to bigint
CREATE FUNCTION inet2int(inet) RETURNS bigint AS $$
SELECT $1 - inet '0.0.0.0';
$$ LANGUAGE SQL  IMMUTABLE RETURNS NULL ON NULL INPUT;

-- bigint to inet
CREATE FUNCTION int2inet(bigint) RETURNS inet AS $$
SELECT inet '0.0.0.0' + $1;
$$ LANGUAGE SQL  IMMUTABLE RETURNS NULL ON NULL INPUT;

-- create type conversion
CREATE CAST (inet AS bigint) WITH FUNCTION inet2int(inet);
CREATE CAST (bigint AS inet) WITH FUNCTION int2inet(bigint);

-- test
SELECT 123456::BIGINT::INET;
SELECT '1.2.3.4'::INET::BIGINT;

-- Generate random IP addresses
SELECT (random() * 4294967295)::BIGINT::INET;
```

Size comparison between `inet` values is also quite straightforward - just use size comparison operators directly. The actual comparison is of the underlying integer values. This solves the first problem.




-------------

## 0x02 Range Types

PostgreSQL's Range types are a very practical feature. Like arrays, they belong to a **generic** type. Any data type that can be B-tree indexed (can be compared for size) can serve as the base type for range types. They're particularly suitable for representing intervals: integer intervals, time intervals, IP address ranges, etc. They have relatively detailed consideration for open intervals, closed intervals, and interval indexing issues.

PostgreSQL has built-in predefined `int4range, int8range, numrange, tsrange, tstzrange, daterange` that are ready to use out of the box. But it doesn't provide range types corresponding to network addresses, though creating one yourself is very simple:

```sql
CREATE TYPE inetrange AS RANGE(SUBTYPE = inet)
```

Of course, to efficiently support GiST index queries, you also need to implement a distance metric that tells the index how to calculate the distance between two `inet` values:

```sql
-- Define distance metric between basic types
CREATE FUNCTION inet_diff(x INET, y INET) RETURNS FLOAT AS $$
  SELECT (x - y) :: FLOAT;
$$ LANGUAGE SQL IMMUTABLE STRICT;

-- Recreate inetrange type using the newly defined distance metric
CREATE TYPE inetrange AS RANGE(
  SUBTYPE = inet,
  SUBTYPE_DIFF = inet_diff
)
```

Fortunately, the distance definition between two network addresses naturally has a very simple calculation method - just subtract them.

This newly defined type is also simple to use, with constructor functions automatically generated:

```bash
geo=# select misc.inetrange('64.60.116.156','64.60.116.161','[)');
inetrange | [64.60.116.156,64.60.116.161)

geo=# select '[64.60.116.156,64.60.116.161]'::inetrange;
inetrange | [64.60.116.156,64.60.116.161]
```

Square brackets and round brackets represent closed and open intervals respectively, consistent with mathematical notation.

Also, detecting whether an IP address falls within a given IP range is quite straightforward:

```bash
geo=# select '[64.60.116.156,64.60.116.161]'::inetrange @> '64.60.116.160'::inet as res;
res | t
```

With range types, we can start building our data table.




-------------

## 0x03 Range Indexes

Actually, finding IP geographic correspondence data took me over an hour, but completing this requirement only took a few minutes.

Assuming we already have such data:

```sql
create table geoips
(
  ips          inetrange,
  geo          geometry(Point),
  country_code text,
  region_code  text,
  city_name    text,
  ad_code      text,
  postal_code  text
);
```

The data inside looks roughly like this:

```bash
SELECT ips,ST_AsText(geo) as geo,country_code FROM geoips

 [64.60.116.156,64.60.116.161] | POINT(-117.853 33.7878) | US
 [64.60.116.139,64.60.116.154] | POINT(-117.853 33.7878) | US
 [64.60.116.138,64.60.116.138] | POINT(-117.76 33.7081)  | US
```

Then querying records containing a certain IP address can be written as:

```sql
SELECT * FROM ip WHERE ips @> inet '67.185.41.77';
```

For 6 million records, about a 600M table, brute force table scanning on the author's machine averaged 900ms, roughly single-core QPS is 1.1, and a 48-core production machine would be around thirty to forty. Definitely unusable.

```sql
CREATE INDEX ON geoips USING GiST(ips);
```

Query time changed from 1 second to 340 microseconds, roughly a 3000x improvement.

```bash
-- pgbench
\set ip random(0,4294967295)
SELECT * FROM geoips WHERE ips @> :ip::BIGINT::INET;

-- result
latency average = 0.342 ms
tps = 2925.100036 (including connections establishing)
tps = 2926.151762 (excluding connections establishing)
```

Converted to production QPS, it's roughly 100,000 QPS - absolutely delightful.

If you need to convert geographic coordinates to administrative divisions, you can refer to the previous article: Using PostGIS to efficiently solve administrative division geocoding problems.

One geocoding also takes about 100 microseconds. The overall QPS for converting from IP to province-city-district-county on a single machine can easily handle tens of thousands (full load all day is equivalent to seven to eight billion calls, you simply can't max it out).




-------------

## 0x04 EXCLUDE Constraints

The problem has been basically solved at this point, but there's still one issue. How to avoid the embarrassing situation of one IP returning two records?

Data integrity is extremely important, but data integrity guaranteed by applications isn't always reliable: people make mistakes, programs have bugs. If data integrity can be enforced through database constraints, that would be ideal.

However, some constraints are quite complex, such as ensuring IP ranges in a table don't overlap, similarly ensuring boundaries of various cities in a geographic division table don't overlap. Traditionally implementing such guarantees was quite difficult: for example, `UNIQUE` constraints cannot express this semantics, and `CHECK` with stored procedures or triggers, while capable of implementing such checks, are quite tricky. PostgreSQL's `EXCLUDE` constraints can elegantly solve this problem. Modify our `geoips` table:

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

Here `EXCLUDE USING gist (ips WITH &&)` means that overlapping ranges are not allowed on the `ips` field - newly inserted fields cannot overlap with any existing ranges (`&&` being true). And `DEFERRABLE INITIALLY IMMEDIATE` means to check constraints on all rows at the end of the statement. Creating this constraint will automatically create a GIST index on the `ips` field, so manual creation is unnecessary.




-------------

## 0x05 Summary

This article introduced how to use PostgreSQL features to efficiently and elegantly solve the IP geolocation lookup problem. Performance is excellent - 0.3ms to locate among 6 million records; complexity is ridiculously low - just one table DDL solves this problem without even explicitly creating indexes; data integrity is fully guaranteed - problems that would take hundreds of lines of code to solve now only require adding constraints, fundamentally ensuring data integrity.

PostgreSQL is so awesome, quickly learn and use it! What? You ask me where to find the data? Search for MaxMind for the truth - you can find free GeoIP data in hidden little corners.