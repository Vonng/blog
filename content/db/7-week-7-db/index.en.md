---
title: "7 Databases in 7 Weeks (2025)"
date: 2024-12-03
authors: ["matt-blewitt"]
origin: "https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/"
summary: >
  Is PostgreSQL the king of boring databases? Here are seven databases worth studying in 2025: PostgreSQL, SQLite, DuckDB, ClickHouse, FoundationDB, TigerBeetle, and CockroachDB—each deserving a week of deep exploration.
tags: [Database, PostgreSQL, SQLite, DuckDB, ClickHouse]
---

> Author: Matt Blewitt, Original: 7 Databases in 7 Weeks (2025)
>
> Translator: Feng Ruohang, database veteran, cloud computing mudslide

https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/


For a long time, I've been running Databases-as-a-Service, and there's always something new to keep up with in this field — new technologies, different approaches to solving problems, not to mention the constant stream of research coming out of universities. Looking ahead to 2025, consider spending a week diving deep into each of the following database technologies.

![A line drawing of a bookshelf, with the books labelled for each database covered - PostgreSQL, SQLite, DuckDB, ClickHouse, FoundationDB, TigerBeetle and CockroachDB](https://matt.blwt.io/7-databases-in-7-weeks-for-2025/header.webp)

--------

## Foreword

This isn't a "7 Best Databases" type of article, nor is it laying groundwork for a menu-style list of books — these are simply seven databases I think are worth spending about a week seriously studying. You might ask, "Why not Neo4j, MongoDB, MySQL/Vitess, or other databases?" The answer is mostly: I don't find them interesting. Also, I won't be covering Kafka or other similar streaming data services — they're definitely worth your time to learn, but they're outside the scope of this article.


--------

## Table of Contents

1. [PostgreSQL](#1-postgresql)
2. [SQLite](#2-sqlite)
3. [DuckDB](#3-duckdb)
4. [ClickHouse](#4-clickhouse)
5. [FoundationDB](#5-foundationdb)
6. [TigerBeetle](#6-tigerbeetle)
7. [CockroachDB](#7-cockroachdb)
8. [Wrap-up](https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/#wrap-up)


--------

## 1. PostgreSQL

### The Default Database

"Use Postgres for everything" has almost become a meme, and for good reason. [PostgreSQL](https://www.postgresql.org/) is the pinnacle of [boring technology](https://boringtechnology.club/), and should be your go-to choice when you need a client-server model database. PG follows ACID principles, has rich replication methods — including both physical and logical replication — and enjoys excellent support across all major vendors.

However, my favorite PostgreSQL feature is [extensions](https://wiki.postgresql.org/wiki/Extensions). In this regard, Postgres demonstrates a vitality that other databases struggle to match. Almost any functionality you want has a corresponding extension — [AGE](https://age.apache.org/) supports graph data structures and Cypher query language, [TimescaleDB](https://docs.timescale.com/self-hosted/latest/) supports time-series workloads, [Hydra Columnar](https://github.com/hydradatabase/hydra/tree/main/columnar) provides an alternative columnar storage engine, and so on. If you're interested in trying this yourself, I recently [wrote an article about building extensions](https://matt.blwt.io/post/building-a-postgresql-extension-line-by-line).

Because of this, Postgres shines as an excellent "default" database, and we're seeing more and more non-Postgres services using the [Postgres wire protocol](https://www.postgresql.org/docs/current/protocol.html) as a common layer-7 protocol to provide client compatibility. With a rich ecosystem, sensible defaults, and even the ability to run in browsers with [Wasm](https://pglite.dev/), this makes it a database worth understanding deeply.

Spend a week exploring the various possibilities of Postgres, while also understanding some of its limitations — [MVCC](https://www.geeksforgeeks.org/multiversion-concurrency-control-mvcc-in-postgresql/) can be somewhat temperamental. Implement a simple CRUD application in your favorite programming language, or even try building a Postgres extension.



--------

## 2. SQLite

### The Local-First Database

Moving away from the client-server model, we detour into "embedded" databases, starting with [SQLite](https://www.sqlite.org/index.html). I call it the "[local-first](https://www.inkandswitch.com/local-first/)" database because SQLite databases coexist directly with applications. A more famous example is [WhatsApp](https://www.whatsapp.com/), which stores chat records as local SQLite databases on devices. [Signal](https://signal.org/) does the same.

Beyond this, we're starting to see more innovative uses of SQLite, not just as a local ACID database. Tools like [Litestream](https://litestream.io/) provide streaming backup capabilities, [LiteFS](https://fly.io/docs/litefs/) provides distributed access capabilities, allowing us to design more interesting topological architectures. Extensions like [CR-SQLite](https://github.com/vlcn-io/cr-sqlite) allow the use of [CRDTs](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) to avoid conflict resolution when merging changesets, as exemplified by [Corrosion](https://github.com/superfly/corrosion).

Thanks to [Ruby on Rails 8.0](https://rubyonrails.org/2024/9/27/rails-8-beta1-no-paas-required), SQLite is also experiencing a small renaissance — 37signals fully invested in SQLite, building a series of Rails modules like [Solid Queue](https://github.com/rails/solid_queue), and configuring Rails through `database.yml` to operate multiple SQLite databases. [Bluesky](https://newsletter.pragmaticengineer.com/p/bluesky?open=false#§sqlite) uses SQLite as personal data servers — each user has their own SQLite database.

Spend a week using SQLite, exploring local-first architecture, and you might even research whether you can migrate from a Postgres client-server model to a SQLite-only pattern.


--------

## 3. DuckDB

### The Universal Query Database

Next is another embedded database, [DuckDB](https://duckdb.org/). Like SQLite, DuckDB aims to be an in-process database system, but focuses more on Online Analytical Processing (OLAP) rather than Online Transaction Processing (OLTP).

DuckDB's highlight is as a "universal query" database, using SQL as the preferred dialect. It can natively import data from CSV, TSV, JSON, and even formats like Parquet — check out [DuckDB's data sources list](https://duckdb.org/docs/data/data_sources.html)! This gives it tremendous flexibility — take a look at [this example of querying Bluesky's firehose](https://motherduck.com/blog/how-to-extract-analytics-from-bluesky/).

Like Postgres, DuckDB also has [extensions](https://duckdb.org/docs/extensions/overview), though the ecosystem isn't as rich — after all, DuckDB is relatively young. Many community-contributed extensions can be found in the [community extensions list](https://duckdb.org/community_extensions/list_of_extensions), and I particularly like [`gsheets`](https://duckdb.org/community_extensions/extensions/gsheets.html).

Spend a week using DuckDB for data analysis and processing — whether through Python Notebooks, tools like [Evidence](https://evidence.dev/), or even see how it combines with SQLite's "local-first" approach, offloading analytical queries from SQLite databases to DuckDB, since DuckDB can also [read SQLite data](https://duckdb.org/docs/guides/database_integration/sqlite.html).


--------

## 4. ClickHouse

### The Columnar Database

Leaving the embedded database realm but continuing in the analytical space, we encounter [ClickHouse](https://clickhouse.com/). If I could only choose two databases, I'd be very happy using just Postgres and ClickHouse — the former for OLTP, the latter for OLAP.

ClickHouse focuses on analytical workloads and supports very high ingestion rates through [horizontal scaling](https://clickhouse.com/docs/en/architecture/horizontal-scaling) and sharded storage. It also supports [tiered storage](https://clickhouse.com/docs/en/guides/separation-storage-compute), allowing you to separate "hot" and "cold" data — [GitLab](https://docs.gitlab.com/ee/development/database/clickhouse/tiered_storage.html) has quite detailed documentation on this.

ClickHouse has advantages when you need to run analytical queries on large datasets that DuckDB can't handle, or when you need "real-time" analytics. There's been a lot of "Benchmarketing" around these datasets, so I won't elaborate further.

Another reason I recommend learning ClickHouse is its excellent operational experience — deployment, scaling, backup, etc. all have [detailed documentation](https://clickhouse.com/docs/en/architecture/cluster-deployment) — even including setting up [appropriate CPU Governors](https://clickhouse.com/docs/en/operations/tips).

Spend a week exploring larger analytical datasets, or converting the DuckDB analysis above to ClickHouse deployment. ClickHouse also has an embedded version — [chDB](https://clickhouse.com/docs/en/chdb) — which can provide more direct comparisons.


--------

## 5. FoundationDB

### The Layered Database

Now we enter the "mind-bending" section of this list, with [FoundationDB](https://www.foundationdb.org/) taking the stage. You could say FoundationDB isn't a database, but rather the foundation component of databases. Used in production by companies like Apple, Snowflake, and [Tigris Data](https://www.tigrisdata.com/blog/building-a-database-using-foundationdb/), FoundationDB is worth your time because it's quite unique in the key-value storage world.

Yes, it's an ordered key-value store, but that's not what makes it interesting. At first glance, it has some peculiar [limitations](https://apple.github.io/foundationdb/known-limitations.html) — for example, transactions cannot affect more than 10MB of data, transactions must complete within five seconds of their first read. But as they say, constraints liberate us. By imposing these limitations, it can achieve complete ACID transactions at very large scales — I know of clusters running over 100 TiB.

FoundationDB is designed for specific workloads and has been [extensively tested](https://apple.github.io/foundationdb/testing.html) using simulation methods. This testing approach has been adopted by other technologies, including another database on this list and by [Antithesis](https://www.antithesis.com/), founded by some former FoundationDB members. For more on this, see related notes from [Tyler Neely](https://sled.rs/simulation.html) and [PhilEaton](https://notes.eatonphil.com/2024-08-20-deterministic-simulation-testing.html).

As mentioned, FoundationDB has some very specific semantics that take time to adapt to — their [features](https://apple.github.io/foundationdb/features.html) documentation and [anti-features](https://apple.github.io/foundationdb/anti-features.html) (functionality they don't intend to provide) are worth understanding to grasp the problems they're trying to solve.

But why is it a "layered" database? Because it proposes the [concept of layers](https://apple.github.io/foundationdb/layer-concept.html), rather than coupling storage engines with data models, they designed a storage engine flexible enough to remap its functionality to different layers. [Tigris Data](https://www.tigrisdata.com/blog/data-layer-foundationdb/) has an excellent article about building such layers, and the FoundationDB organization has some examples like the [Record Layer](https://github.com/FoundationDB/fdb-record-layer) and [Document Layer](https://github.com/FoundationDB/fdb-document-layer).

Spend a week going through the [tutorials](https://apple.github.io/foundationdb/tutorials.html), thinking about how to use FoundationDB as a replacement for databases like [RocksDB](https://rocksdb.org/). Maybe look at some [design patterns](https://apple.github.io/foundationdb/design-recipes.html) and read the [paper](https://www.foundationdb.org/files/fdb-paper.pdf).


--------

## 6. TigerBeetle

### The Extremely Correct Database

Following deterministic simulation testing, [TigerBeetle](https://tigerbeetle.com/) breaks from previous database patterns because it explicitly states it's **not** a general-purpose database — it's completely focused on financial transaction scenarios.

Why is it worth looking at? Single-purpose databases are rare, and databases as obsessed with correctness as TigerBeetle are even rarer, especially considering it's open source. They incorporate everything from [NASA's Power of 10](https://en.wikipedia.org/wiki/The_Power_of_10:_Rules_for_Developing_Safety-Critical_Code) and [protocol-aware recovery](https://www.usenix.org/conference/fast18/presentation/alagappan) to strict serializability and Direct I/O to avoid kernel page cache issues — it's all **very** impressive. Check out their [safety documentation](https://github.com/tigerbeetle/tigerbeetle/blob/a43f2205f5335cb8f56d6e8bfcc6b2d99a4fc4a4/docs/about/safety.md) and their [programming methodology](https://github.com/tigerbeetle/tigerbeetle/blob/a43f2205f5335cb8f56d6e8bfcc6b2d99a4fc4a4/docs/TIGER_STYLE.md) called Tiger Style!

Another interesting point is that TigerBeetle is written in [Zig](https://ziglang.org/) — a relatively new systems programming language, but apparently very aligned with the TigerBeetle team's goals.

Spend a week modeling your financial accounts in a locally deployed TigerBeetle — follow the [quick start](https://docs.tigerbeetle.com/quick-start) and look at the [system architecture](https://docs.tigerbeetle.com/coding/system-architecture) documentation to understand how to combine it with the more general-purpose databases mentioned above.


--------

## 7. CockroachDB

### The Globally Distributed Database

Finally, we return to where we started. In the last position, I was a bit torn. My initial thought was [Valkey](https://valkey.io/), but FoundationDB already covered the key-value storage need. I also considered graph databases, or databases like [ScyllaDB](https://www.scylladb.com/) or [Cassandra](https://cassandra.apache.org/_/index.html). I also considered [DynamoDB](https://aws.amazon.com/dynamodb/), but the inability to run it locally/freely discouraged me.

Ultimately, I decided to end with a globally distributed database — [CockroachDB](https://www.cockroachlabs.com/). It's compatible with the Postgres wire protocol and inherits some of the interesting features discussed earlier — large-scale horizontal scaling, strong consistency — while having some interesting features of its own.

CockroachDB achieves database scaling across multiple geographic regions, with a niche overlapping Google's [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) system. However, Spanner relies on atomic clocks and GPS clocks for extremely precise time synchronization, but ordinary hardware doesn't have such luxury configurations. Therefore, CockroachDB has some [clever solutions](https://www.cockroachlabs.com/blog/living-without-atomic-clocks/#How-does-CockroachDB-choose-transaction-timestamps?), dealing with NTP clock synchronization delays through retries or delayed reads. Nodes also compare clock drift and terminate membership if it exceeds maximum offset.

Another interesting feature of CockroachDB is how it uses [multi-region configuration](https://www.cockroachlabs.com/docs/stable/multiregion-overview), including [table localities](https://www.cockroachlabs.com/docs/stable/table-localities), providing different options based on your desired read-write trade-offs. Spend a week reimplementing the [`movr`](https://www.cockroachlabs.com/docs/v24.3/movr) example in your language and framework of choice.


--------

## Summary

We've explored many different databases, all used in production by some of the world's largest companies. Hopefully, this exposes you to some technologies you weren't familiar with before. Armed with this knowledge, go solve interesting problems!




--------

## Feng's Comments

In 2013, there was a book called "Seven Databases in Seven Weeks." That book introduced 7 "new (or reborn)" database technologies of the time, leaving an impression on me. Twelve years later, this series is getting updated again.



Looking back at the seven databases from that year, except for the original "hammer" PostgreSQL which is still around, all the other databases have changed completely. And PostgreSQL has evolved from a "hammer" to the "king of boring databases" — becoming the "default database" that won't flip over.

The databases on this list are basically all ones I've practiced with or am interested in/have good feelings about. Except for ClickHouse — CK is good, but I think DuckDB and its combination with PostgreSQL has the potential to overturn CK, plus it's MySQL protocol compatible ecosystem, so I really have no interest in it. If I were to design this list, I'd probably replace CK with either Supabase or Neon.



I think the author has very precisely grasped the trends in database technology development, and I highly agree with his choice of database technologies. Actually, among these seven databases, I've already deeply explored three of them. Pigsty itself is a high-availability PostgreSQL distribution that also integrates DuckDB, as well as DuckDB-grafted PG extensions. I've also made RPM/DEB packages for TigerBeetle as a dedicated financial transaction database for default download in the professional edition.

The other two databases are on my integration TODO list: for SQLite, besides FDW, the next step is to integrate ElectricSQL; providing sync capabilities between local PG and remote SQLite/PGLite; CockroachDB has always been on my TODO list, ready to add deployment support whenever I have spare time. FoundationDB is an object of my interest, and the next database I'm willing to spend time deeply researching will likely be this one.



Overall, I believe these technologies represent cutting-edge development trends in the field. If I were to envision the landscape ten years from now, it would probably look like this: FoundationDB, TigerBeetle, and CockroachDB will have their own niche ecosystem positions. DuckDB will likely shine in the analytical field, SQLite will continue to conquer territory on the local-first client side, and PostgreSQL will evolve from the "default database" to the ubiquitous "Linux kernel" of the database world. The main theme of the database field will become a battlefield of PostgreSQL distribution competition between Neon, Supabase, Vercel, RDS, and Pigsty.

After all, PostgreSQL devouring the database world isn't just talk — PostgreSQL ecosystem companies have taken almost all the money in the database field's capital market these past two years, with countless real money already voting with their feet by betting on it. Of course, how the future actually unfolds, let's wait and see.

