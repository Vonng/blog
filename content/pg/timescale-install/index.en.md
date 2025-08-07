---
title: "TimescaleDB Quick Start"
date: 2018-09-07
author: "vonng"
summary: >
  TimescaleDB is a PostgreSQL extension plugin that provides time-series database functionality.
tags: [PostgreSQL, PG Management, Extensions]
---

* Official website: https://www.timescale.com
* Official documentation: https://docs.timescale.com/v0.9/main
* Github: https://github.com/timescale/timescaledb

---------------

## Why Use TimescaleDB

### What is Time-Series Data?

We keep talking about what "time-series data" is, how it differs from other data, and why?

Many applications or databases actually take too narrow a view and equate time-series data with specific forms of server metrics:

```
Name:    CPU

Tags:    Host=MyServer, Region=West

Data:
2017-01-01 01:02:00    70
2017-01-01 01:03:00    71
2017-01-01 01:04:00    72
2017-01-01 01:05:01    68
```

But in reality, in many monitoring applications, different metrics are typically collected (e.g., CPU, memory, network statistics, battery life). Therefore, considering each metric separately doesn't always make sense. Consider this alternative "broader" data model that maintains correlation between simultaneously collected metrics.

```
Metrics: CPU, free_mem, net_rssi, battery

Tags:    Host=MyServer, Region=West

Data:
2017-01-01 01:02:00    70    500    -40    80
2017-01-01 01:03:00    71    400    -42    80
2017-01-01 01:04:00    72    367    -41    80
2017-01-01 01:05:01    68    750    -54    79
```

This type of data belongs to a **broader** category, whether it's temperature readings from sensors, stock prices, machine state, or even login counts to applications.

**Time-series data is data that uniformly represents how systems, processes, or behaviors change over time.**

### Characteristics of Time-Series Data

If you examine how it's generated and ingested carefully, time-series databases like TimescaleDB typically have these important characteristics:

- **Time-centric**: Data records always have a timestamp.
- **Append-only**: Data is almost entirely append-only (inserts).
- **Recent**: New data is typically about recent time intervals; we less frequently update or backfill missing data from old time intervals.

The frequency or regularity of data doesn't matter - it can be collected every millisecond or every hour. It can also be collected regularly or irregularly (e.g., when certain *events* occur, rather than at predetermined times).

But doesn't every database have time fields? One major difference between time-series data (and databases supporting them) compared to other data like standard relational "business" data is that **changes to data are inserts rather than overwrites**.

### Time-Series Data is Everywhere

Time-series data is everywhere, but some environments particularly create torrents of it.

- **Monitoring computer systems**: Virtual machines, servers, container metrics (CPU, available memory, network/disk IOP), service and application metrics (request rate, request latency).
- **Financial trading systems**: Classic securities, newer cryptocurrencies, payments, trading events.
- **Internet of Things**: Data from sensors on industrial machines and equipment, wearable devices, vehicles, physical containers, pallets, smart home consumer devices, etc.
- **Event applications**: User/customer interaction data like clickstreams, page views, logins, signups, etc.
- **Business intelligence**: Tracking key metrics and overall business health.
- **Environmental monitoring**: Temperature, humidity, pressure, pH, pollen count, air flow, carbon monoxide (CO), nitrogen dioxide (NO2), particulate matter (PM10).
- (and more)

---------------

## Time-Series Data Model

TimescaleDB uses a "wide table" data model, which is very common in relational databases. This distinguishes Timescale from most other time-series databases, which typically use a "narrow table" model.

Here, we discuss why we chose the wide table model and how we recommend using it for time-series data, using an Internet of Things (IoT) example.

Envision a distributed group of 1,000 IoT devices designed to collect environmental data at different time intervals. This data might include:

- **Identifiers:** `device_id`, `timestamp`
- **Metadata:** `location_id`, `dev_type`, `firmware_version`, `customer_id`
- **Device metrics:** `cpu_1m_avg`, `free_mem`, `used_mem`, `net_rssi`, `net_loss`, `battery`
- **Sensor metrics:** `temperature`, `humidity`, `pressure`, `CO`, `NO2`, `PM10`

For example, your incoming data might look like this:

| Timestamp           | Device ID | cpu_1m_avg | free_mem | Temperature | location_id | dev_type |
|---------------------|-----------|------------|----------|-------------|-------------|----------|
| 2017-01-01 01:02:00 | ABC123    | 80         | 500MB    | 72          | 335         | field    |
| 2017-01-01 01:02:23 | def456    | 90         | 400MB    | 64          | 335         | roof     |
| 2017-01-01 01:02:30 | ghi789    | 120        | 0MB      | 56          | 77          | roof     |
| 2017-01-01 01:03:12 | ABC123    | 80         | 500MB    | 72          | 335         | field    |
| 2017-01-01 01:03:35 | def456    | 95         | 350MB    | 64          | 335         | roof     |
| 2017-01-01 01:03:42 | ghi789    | 100        | 100MB    | 56          | 77          | roof     |

Now, let's look at various ways to model this data.

### Narrow Table Model

Most time-series databases would represent this data in the following way:

- Represent each metric as a separate entity (e.g., treat `cpu_1m_avg` and `free_mem` as two different things)
- Store a series of "time", "value" pairs for that metric
- Represent metadata values as "tag sets" associated with that metric/tag set combination

In this model, each metric/tag set combination is considered a separate "time series" containing a series of time/value pairs.

Using our example above, this approach would result in 9 different "time series", each defined by a unique set of tags.

```
1. {name:  cpu_1m_avg,  device_id: abc123,  location_id: 335,  dev_type: field}
2. {name:  cpu_1m_avg,  device_id: def456,  location_id: 335,  dev_type: roof}
3. {name:  cpu_1m_avg,  device_id: ghi789,  location_id:  77,  dev_type: roof}
4. {name:    free_mem,  device_id: abc123,  location_id: 335,  dev_type: field}
5. {name:    free_mem,  device_id: def456,  location_id: 335,  dev_type: roof}
6. {name:    free_mem,  device_id: ghi789,  location_id:  77,  dev_type: roof}
7. {name: temperature,  device_id: abc123,  location_id: 335,  dev_type: field}
8. {name: temperature,  device_id: def456,  location_id: 335,  dev_type: roof}
9. {name: temperature,  device_id: ghi789,  location_id:  77,  dev_type: roof}
```

The number of such time series is the cross product of each tag's cardinality (i.e., (#names) × (#device IDs) × (#location IDs) × (#device types)).

And each of these "time series" has its own set of time/value sequences.

Now, if you collect each metric independently and have little metadata, this approach might be useful.

But overall, we think this approach is limited. It loses the inherent structure in the data, making it difficult to ask various useful questions. For example:

- What was the system state when `free_mem` went to 0?
- How do `cpu_1m_avg` and `free_mem` correlate?
- What's the average `temperature` by `location_id`?

We also find this approach cognitively confusing. Are we really collecting 9 different time series, or just one dataset containing various metadata and metric readings?

### Wide Table Model

In contrast, TimescaleDB uses a wide table model that reflects the inherent structure in the data.

Our wide table model looks exactly like the initial data stream:

| Timestamp           | Device ID | cpu_1m_avg | free_mem | Temperature | location_id | dev_type |
|---------------------|-----------|------------|----------|-------------|-------------|----------|
| 2017-01-01 01:02:00 | ABC123    | 80         | 500MB    | 72          | 42          | field    |
| 2017-01-01 01:02:23 | def456    | 90         | 400MB    | 64          | 42          | roof     |
| 2017-01-01 01:02:30 | ghi789    | 120        | 0MB      | 56          | 77          | roof     |
| 2017-01-01 01:03:12 | ABC123    | 80         | 500MB    | 72          | 42          | field    |
| 2017-01-01 01:03:35 | def456    | 95         | 350MB    | 64          | 42          | roof     |
| 2017-01-01 01:03:42 | ghi789    | 100        | 100MB    | 56          | 77          | roof     |

Here, each row is a new reading with a set of metrics and metadata at a given time. This allows us to preserve relationships in the data and ask more interesting or exploratory questions than before.

Of course, this isn't a new format: this is common in relational databases. This is also why we find this format more intuitive.

### JOINing with Relational Data

TimescaleDB's data model has another similarity to relational databases: it supports JOINs. Specifically, additional metadata can be stored in secondary tables and then used during queries.

In our example, we could have a separate locations table that maps `location_id` to other metadata about that location. For example:

| location_id | name          | latitude   | longitude  | zip_code | region |
|-------------|---------------|------------|------------|----------|--------|
| 42          | Grand Central | 40.7527°N  | 73.9772°W  | 10017    | NYC    |
| 77          | Hall 7        | 42.3593°N  | 71.0935°W  | 02139    | MA     |

Then during queries, by joining our two tables, we can ask questions like: What's the average `free_mem` of our devices in zip code 10017?

Without joins, we'd need to denormalize data and store all metadata in each measurement row. This creates data bloat and makes data management more difficult.

With joins, metadata can be stored independently and mappings updated more easily.

For example, if we wanted to update our "region" for `location_id` 77 (e.g., from "MA" to "Boston"), we can make this change without having to go back and overwrite historical data.

---------------

## Architecture & Concepts

TimescaleDB is implemented as a PostgreSQL extension, meaning Timescale databases run within entire PostgreSQL instances. This extension model allows databases to leverage many of PostgreSQL's attributes, like reliability, security, and connectivity with various third-party tools. At the same time, TimescaleDB fully leverages the high customization available to extensions by adding hooks within PostgreSQL's query planner, data model, and execution engine.

From the user's perspective, TimescaleDB exposes what appear to be singular tables called **hypertables**, which are actually an abstraction or virtual view of many individual tables called **chunks**.

![Hypertables and chunks](https://assets.iobeam.com/images/docs/illustration-hypertable-chunk.svg)

Chunks are created by partitioning hypertable data across one or more dimensions: all hypertables are partitioned by time interval, and can be partitioned by keys like device ID, location, user ID, etc. We sometimes call this partitioning across "time and space".

### Terminology

#### Hypertables

The primary point of interaction with data is a hypertable, an abstraction of a single continuous table across all time and space intervals, so it can be queried via standard SQL.

In fact, all user interactions with TimescaleDB are with hypertables. Creating tables and indexes, altering tables, inserting data, selecting data, etc. can (and should) all be executed on the hypertable.

A hypertable is defined by a standard schema with column names and types, where at least one column specifies a time value, and another column (optionally) specifies an additional partitioning key.

> Tip: See our [data model][] for further discussion of various ways to organize data depending on your use case; the simplest and most natural is in "wide tables" like many relational databases.

A single TimescaleDB deployment can store multiple hypertables, each with different schemas.

Creating a hypertable in TimescaleDB requires two simple SQL commands: `CREATE TABLE` (using standard SQL syntax), followed by `SELECT create_hypertable()`.

Time indexes and partition keys are automatically created on hypertables, although additional indexes can also be created (and TimescaleDB supports all PostgreSQL index types).

#### Chunks

Internally, TimescaleDB automatically splits each hypertable into **chunks**, each chunk corresponding to a specific time interval and a region of the partition key space (using hashing). These partitions are disjoint (non-overlapping), which helps the query planner minimize the set of chunks it has to touch to resolve queries.

Each chunk is implemented using a standard database table. (Internally in PostgreSQL, this chunk is actually a "child table" of the "parent" hypertable.)

Chunks are right-sized to ensure that all B-trees of a table's indexes can reside in memory during inserts. This avoids thrashing that can occur when modifying arbitrary locations in these trees.

Additionally, by avoiding overly large chunks, we can avoid expensive "vacuum" operations when deleting deleted data according to automated retention policies. These operations can be performed at runtime by simply dropping chunks (internal tables) rather than deleting individual rows.

---------------

## Single-Node vs. Cluster

TimescaleDB performs this extensive partitioning on both **single-node** deployments and **cluster** deployments (in development). While partitioning is traditionally only used for scaling across multiple machines, it also allows us to scale to high write rates (and improves parallel queries) even on single machines.

TimescaleDB's current open-source version only supports single-node deployments. Notably, TimescaleDB's single-node version has been benchmarked on commercial machines with high availability based on over 10 billion rows without loss of insert performance.

### Benefits of Single-Node Partitioning

A common problem in scaling database performance on single computers is the significant cost/performance tradeoff between memory and disk. Eventually, our entire dataset doesn't fit in memory, and we need to write our data and indexes to disk.

Once data is large enough that we can't fit all pages of indexes (e.g., B-trees) in memory, updating random parts of trees may involve swapping data from disk. Databases like PostgreSQL maintain one B-tree (or other data structure) for each table index to efficiently find values in that index. So when you index more columns, the problem compounds.

However, since each chunk created by TimescaleDB is itself stored as a separate database table, all its indexes are only built on these much smaller tables rather than a single table representing the entire dataset. So if we size these chunks correctly, we can put the latest tables (and their B-trees) entirely in memory and avoid the problem of swapping to disk, while maintaining support for multiple indexes.

For more information about the motivation and design of TimescaleDB's adaptive space/time chunking, see our [technical blog post][chunking].

---------------

## TimescaleDB vs. PostgreSQL

TimescaleDB provides three major advantages over vanilla PostgreSQL or other traditional RDBMS for storing time-series data:

1. Much higher data ingestion rates, especially as database scales.
2. Query performance that's equivalent to *orders of magnitude better*.
3. Time-oriented features.

And since TimescaleDB still allows you to use PostgreSQL's full functionality and tooling - for example, JOINs with relational tables, geospatial queries via PostGIS, and any connector that can speak PostgreSQL, `pg_dump`, `pg_restore` - there's **no** reason **not** to use TimescaleDB for storing time-series data in PostgreSQL nodes.

### Higher Write Rates

For time-series data, TimescaleDB achieves higher and more stable ingestion rates than PostgreSQL. As described in our [architecture discussion](https://docs.timescale.com/introduction/architecture#benefits-chunking), PostgreSQL's performance degrades significantly once indexed tables can no longer fit in memory.

Specifically, whenever a new row is inserted, the database needs to update the index (e.g., B-tree) for each indexed column in the table, which will involve swapping one or more pages from disk. Throwing more memory at this problem only delays the inevitable - once your time-series table reaches tens of millions of rows, throughput of 10K-100K+ rows per second collapses to hundreds of rows per second.

TimescaleDB solves this problem by extensively leveraging space-time partitioning, even when running on *single machines*. Therefore, all writes to recent time intervals only apply to tables kept in memory, so updating any secondary indexes is also fast.

Benchmarks show clear advantages of this approach. Database clients insert moderately sized batches of data containing time, device tag sets, and multiple numerical metrics (10 in this case). The following benchmark at 1 billion rows (on single machine) simulates common monitoring scenarios. Here, experiments were performed on a standard Azure VM (DS4 v2, 8 cores) with network-attached SSD storage.

![img](https://assets.timescale.com/benchmarks/timescale-vs-postgres-insert-1B.jpg)

We observed that PostgreSQL and TimescaleDB started at roughly the same speed for the first 20M requests (106K and 114K respectively), or over 1M metrics per second. However, around fifty million rows, PostgreSQL's performance began to decline sharply. In the last 100M rows, it averaged only 5K rows/sec, while TimescaleDB maintained 111K rows/sec throughput.

In short, Timescale loaded the billion-row database in **one-fifteenth** the total time of PostgreSQL, and had throughput **20x** higher than PostgreSQL at these larger scales.

Our TimescaleDB benchmarks show it maintains constant performance beyond 10B rows even with a single disk.

Furthermore, users utilizing multiple disks on one computer can provide stable performance for **billions of rows**, whether in RAID configurations or using TimescaleDB's support for spreading single hypertables across multiple disks (via multiple tablespaces, unlike traditional PostgreSQL tables).

### Superior or Similar Query Performance

On single-disk machines, many simple queries that only perform index lookups or table scans perform similarly between PostgreSQL and TimescaleDB.

For example, on a 100M row table with indexed time, hostname, and CPU usage information, the following query takes less than 5ms for each database:

```
SELECT date_trunc('minute', time) AS minute, max(user_usage)
  FROM cpu
  WHERE hostname = 'host_1234'
    AND time >= '2017-01-01 00:00' AND time < '2017-01-01 01:00'
  GROUP BY minute ORDER BY minute;
```

Similar queries involving basic scans of indexes are also equivalent between the two:

```
SELECT * FROM cpu
  WHERE usage_user > 90.0
    AND time >= '2017-01-01' AND time < '2017-01-02';
```

Larger queries involving time-based GROUP BY - common in time-oriented analysis - typically achieve superior performance in TimescaleDB.

For example, the following query touching 33M rows is **5x** faster in TimescaleDB when the entire (hyper)table is 100M rows, and about **2x** faster at 1B rows.

```
SELECT date_trunc('hour', time) as hour,
    hostname, avg(usage_user)
  FROM cpu
  WHERE time >= '2017-01-01' AND time < '2017-01-02'
  GROUP BY hour, hostname
  ORDER BY hour;
```

Additionally, queries that can leverage time ordering can perform *much* better in TimescaleDB.

For example, TimescaleDB introduces a time-based "merge append" optimization to minimize the number of groups that must be processed to perform the following operation (considering that time is already sorted). For our 100M row table, this results in query latency **396x** faster than PostgreSQL (82ms vs. 32566ms).

```
SELECT date_trunc('minute', time) AS minute, max(usage_user)
  FROM cpu
  WHERE time < '2017-01-01'
  GROUP BY minute
  ORDER BY minute DESC
  LIMIT 5;
```

We'll soon publish more complete benchmark comparisons between PostgreSQL and TimescaleDB, along with software to replicate our benchmarks.

The high-level result of our query benchmarks is that for almost **all queries** we've tried, TimescaleDB achieves **similar or superior (or extremely superior) performance** to PostgreSQL.

One additional cost of TimescaleDB compared to PostgreSQL is more complex planning (assuming single hypertables can be composed of many chunks). This can translate to a few milliseconds of planning time, which can have disproportionate impact on very low-latency queries (<10ms).

### Time-Oriented Features

TimescaleDB also contains many time-oriented features not found in traditional relational databases. These include special query optimizations (like the merge append above) that provide some huge performance improvements for time-oriented queries, as well as other time-oriented functions (some listed below).

#### Time-Oriented Analytics

TimescaleDB includes *new* functionality for time-oriented analytics, including some of these features:

- **Time bucketing**: A more powerful version of the standard `date_trunc` function that allows arbitrary time intervals (e.g., 5 minutes, 6 hours, etc.) and flexible grouping and offsets, not just second, minute, hour, etc.
- **Last** and **first** aggregates: These functions allow you to get values from one column ordered by another column. For example, `last(temperature, time)` would return the latest temperature value based on time within a group (e.g., an hour).

These types of functions enable very natural time-oriented queries. For example, the following financial query prints opening, closing, high, and low prices for each asset.

```
SELECT time_bucket('3 hours', time) AS period
    asset_code,
    first(price, time) AS opening, last(price, time) AS closing,
    max(price) AS high, min(price) AS low
  FROM prices
  WHERE time > NOW() - interval '7 days'
  GROUP BY period, asset_code
  ORDER BY period DESC, asset_code;
```

The ability to order by auxiliary columns (even different from the set) enables some powerful query types. For example, a technique common in financial reports is "bi-temporal modeling", which separates observation time from the time the record was observed. In such models, corrections are inserted as new rows (with updated *time_recorded* fields) and don't replace existing data.

The following query returns daily prices for each asset, ordered by the latest recorded price.

```
SELECT time_bucket('1 day', time) AS day,
    asset_code,
    last(price, time_recorded)
  FROM prices
  WHERE time > '2017-01-01'
  GROUP BY day, asset_code
  ORDER BY day DESC, asset_code;
```

For more information about TimescaleDB's current (and growing) list of time functions, [see our API](https://docs.timescale.com/api#time_bucket).

#### Time-Oriented Data Management

TimescaleDB also provides certain data management features that aren't easily available or performant in PostgreSQL. For example, when dealing with time-series data, data often builds up quickly. Therefore, you want to write *data retention* policies like "only store one week of raw data".

In practice, it's common to combine this with continuous aggregation, so you can maintain two hypertables: one containing raw data, another containing data already aggregated to minute or hourly aggregates. Then you might define different retention policies on the two (hyper)tables to store aggregated data for longer periods.

TimescaleDB allows efficient deletion of old data at the **chunk** level rather than row level through its `drop_chunks` functionality.

```
SELECT drop_chunks(interval '7 days', 'conditions');
```

This will drop all chunks in the 'conditions' hypertable containing only data older than this duration (files), rather than deleting any individual data rows within chunks. This avoids fragmentation in underlying database files, which in turn avoids the need for vacuum that can be too expensive in very large tables.

For more details, see our [data retention](https://docs.timescale.com/api/data-retention) discussion, including how to automate data retention policies.

---------------

## TimescaleDB vs. NoSQL

Compared to general NoSQL databases (e.g., MongoDB, Cassandra) or more specialized time-oriented databases (e.g., InfluxDB, KairosDB), TimescaleDB provides qualitative and quantitative differences:

- **Full SQL**: Even at scale, TimescaleDB provides standard SQL query capabilities for time-series data. Most (all?) NoSQL databases require learning new query languages or use at best "SQL-ish" (which still isn't compatible with existing tools).
- **Operational simplicity**: With TimescaleDB, you only need to manage one database for both relational data and time-series data. Otherwise, users typically need to store data in two databases: a "normal" relational database and a second time-series database.
- **JOINs** can be performed with both relational data and time-series data.
- Query **performance** is faster for different query sets. In NoSQL databases, more complex queries are typically slow or full table scans, while some databases can't even support many natural queries.
- **Managed like PostgreSQL**, and inherits support for different data types and indexes (B-tree, hash, range, BRIN, GiST, GIN).
- **Native geospatial data support**: Data stored in TimescaleDB can leverage PostGIS's geometry data types, indexes, and queries.
- **Third-party tools**: TimescaleDB supports anything that can speak SQL, including BI tools like Tableau.

### When *not* to use TimescaleDB?

Then, you might not want to use TimescaleDB if any of the following are true:

- **Simple read requirements**: If you only need fast key-value lookups or single-column rollups, in-memory or column-oriented databases might be more appropriate. The former obviously can't scale to the same data volumes, however, the latter performs significantly worse on more complex queries.
- **Very sparse or unstructured data**: Although TimescaleDB leverages PostgreSQL's support for JSON/JSONB formats and handles sparsity quite efficiently (bitmaps for null values), in some cases, schema-less architectures might be more appropriate.
- **Heavy compression is a priority**: Benchmarks show TimescaleDB running on ZFS achieves about 4x compression ratio, but compression-optimized column stores might be more suitable for higher compression ratios.
- **Infrequent or offline analytics**: If slower response times are acceptable (or response times are limited to a small number of pre-computed metrics), and you don't expect many applications/users to access the data simultaneously, you can avoid using databases and just store data in distributed file systems.

---------------

## Installation

**Mac** users can directly use brew to install - the most hassle-free method, can install PostgreSQL and PostGIS together.

```bash
# Add our tap
brew tap timescale/tap

# To install
brew install timescaledb

# Post-install to move files to appropriate place
/usr/local/bin/timescaledb_move.sh
```

On EL-based operating systems:

```bash
sudo yum install -y https://download.postgresql.org/pub/repos/yum/9.6/redhat/fedora-7.2-x86_64/pgdg-redhat10-10-1.noarch.rpm

wget https://timescalereleases.blob.core.windows.net/rpm/timescaledb-0.9.0-postgresql-9.6-0.x86_64.rpm
# For PostgreSQL 10:
wget https://timescalereleases.blob.core.windows.net/rpm/timescaledb-0.9.0-postgresql-10-0.x86_64.rpm

# To install
sudo yum install timescaledb
```

---------------

## Configuration

Add the following configuration to `postgresql.conf` to load this plugin when PostgreSQL starts.

```ini
shared_preload_libraries = 'timescaledb'
```

Execute the following command in the database to create the timescaledb extension.

```sql
CREATE EXTENSION timescaledb;
```

---------------

## Tuning

A parameter that's quite important for timescaledb is the number of locks.

TimescaleDB relies heavily on table partitioning to scale time-series workloads, which has implications for [lock management](https://www.postgresql.org/docs/current/static/runtime-config-locks.html). During queries, hypertables need to acquire locks on many chunks (sub-tables), which can exhaust the default limit of allowed locks. This can cause warnings like:

```
psql: FATAL:  out of shared memory
HINT:  You might need to increase max_locks_per_transaction.
```

To avoid this problem, it's necessary to modify the default value (usually 64) to increase the maximum number of locks. Since changing this parameter requires database restart, it's recommended to estimate future growth. For most cases, the recommended configuration is:

```ini
max_locks_per_transaction = 2 * num_chunks
```

`num_chunks` is the upper limit of **chunks** that might exist in **hypertables**.

This configuration considers that queries on hypertables might request locks roughly equal to the number of chunks in the hypertable, doubled if using indexes.

Note this parameter isn't a precise limit; it only controls the **average** number of object locks per transaction.

---------------

## Creating Hypertables

To create a hypertable, you start with a regular SQL table, then convert it to a hypertable through the `create_hypertable` function ([API reference](https://docs.timescale.com/api#create_hypertable)).

The following example creates a hypertable that can track temperature and humidity across a series of devices over time.

```
-- We start by creating a regular SQL table

CREATE TABLE conditions (
  time        TIMESTAMPTZ       NOT NULL,
  location    TEXT              NOT NULL,
  temperature DOUBLE PRECISION  NULL,
  humidity    DOUBLE PRECISION  NULL
);
```

Next, convert it to a hypertable using `create_hypertable`:

```
-- This creates a hypertable that is partitioned by time
--   using the values in the `time` column.

SELECT create_hypertable('conditions', 'time');

-- OR you can additionally partition the data on another
--   dimension (what we call 'space partitioning').
-- E.g., to partition `location` into 4 partitions:

SELECT create_hypertable('conditions', 'time', 'location', 4);
```

---------------

## Insert and Query

Insert data into the hypertable through normal SQL `INSERT` commands, for example using millisecond timestamps:

```
INSERT INTO conditions(time, location, temperature, humidity)
  VALUES (NOW(), 'office', 70.0, 50.0);
```

Similarly, querying data is done through normal SQL `SELECT` commands.

```
SELECT * FROM conditions ORDER BY time DESC LIMIT 100;
```

SQL `UPDATE` and `DELETE` commands also work as expected. For more examples using TimescaleDB's standard SQL interface, see our [usage page](https://docs.timescale.com/using-timescaledb).