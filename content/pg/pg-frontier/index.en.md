---
title: PostgreSQL Ecosystem Frontier Developments
linkTitle: "PostgreSQL Ecosystem Frontier Developments"
date: 2025-01-24
author: vonng 
summary: Sharing some interesting recent developments in the PG ecosystem.
tags: [PostgreSQL,PG-Ecosystem]
---

Dear readers, I'm starting my vacation today. I might stop posting for two weeks, so Happy New Year in advance.

Of course, before starting vacation, this article shares some interesting recent developments in the PG ecosystem. Yesterday I also hurried to release Pigsty 3.2.2 and Pig v0.1.3 while I still had time: this version brought available PG extensions from 350 all the way to 400, including most of the exciting stuff above. Here's a brief introduction:

**Omnigres**: Full-stack web development frontend and backend in PG

**PG Mooncake**: Achieving ClickHouse analytical performance in PG

**Citus**: Distributed extension Citus 13 supporting PG17 finally arrived

**FerretDB**: Emulating PG as MongoDB, 2.0 has 20x performance improvement

**ParadeDB**: Providing ES full-text search capabilities in PG, PG block storage implementation

Pigsty 3.2.2: Putting all the above into one box, ready to use out of the box

------

## Omnigres

In the day before yesterday's "[Database as Architecture](https://mp.weixin.qq.com/s/8NS15_fkuR_gSLG50MNtMQ)", I already introduced this interesting project — Omnigres. Simply put, it can stuff all business logic, even web servers and entire backends into the PostgreSQL database.

For example, the following SQL will start a web server, serving `/www` as a web server root directory. This means you can completely stuff a classic frontend-backend-database three-tier application into a single database!

If you're familiar with Oracle, you might find this somewhat similar to Oracle Apex. But in PostgreSQL, you can develop stored procedures in over twenty programming languages, not just limited to PL/SQL! And Omnigres provides far more than just an HTTPD server — it has 33 extension plugins, basically providing a "Web development standard library" in PG.

As the saying goes: "What goes around comes around." In ancient times, many C/S, B/S architecture applications were just a few clients directly reading and writing databases. But later, as business logic became more complex and hardware performance (relative to business needs) was stretched, many things were stripped from databases, forming traditional three-tier architectures.

Hardware development has given database servers abundant performance again, and database software development has made stored procedure writing much easier. So the trend of splitting and stripping might very well reverse — business logic originally separated from databases might return to databases. I think Omnigres, as well as Supabase, are attempts at such "reunification."

If you have hundreds of thousands of TPS, dozens of TB of data, or run some critical, life-and-death, massive core systems, this approach might not be suitable. But if you're running personal projects, small websites, or startup companies and edge innovation systems, this architecture will make your iteration more agile and development/operations simpler.

Pigsty v3.2.2 provides Omnigres extensions, which indeed took me considerable effort. With hands-on help from original author Yurii, I completed building and packaging on 10 Linux distribution major versions. Note that these plugins are in an extension repository that can be used independently — you don't necessarily need Pigsty to have these extensions. Omnigres and AutoBase PostgreSQL are also using this repository for extension delivery, which is indeed a great example of open-source ecosystem mutual benefit and win-win.

## pg_mooncake

Since the "DuckDB Stitching Competition" began, pg_mooncake was the last contestant to enter. They were so quiet I almost thought they had given up maintenance. But last week they delivered big, releasing 0.1.0 and directly killing into the top ten on the ClickBench leaderboard, on the same level as ClickHouse.

This is the first time PG + extension plugin analytical performance could directly kill into the Tier 0 of analytical rankings, worth remembering. It seems pg_duckdb has indeed welcomed a formidable rival — I think this is great news. While providing users more choices, it avoids monopoly dominance. Internal racing and competition within the ecosystem while pulling far ahead of other DBMS in analytical capabilities.

Most people's impression of PostgreSQL still stops at being a robust OLTP (Online Transaction Processing) database, rarely associating it with "real-time analytics." However, PostgreSQL's extensibility allows it to "break through" inherent impressions and carve out territory in real-time analytics. The mooncake team leveraged PostgreSQL's extensibility to write a native extension pg_mooncake. They embedded DuckDB's execution engine into columnar queries, allowing data processing in batch mode (rather than row-by-row) during execution, utilizing SIMD instruction sets for higher efficiency in scanning, grouping, and aggregation scenarios.

Mooncake adopted a more efficient metadata mechanism: rather than pulling metadata and statistics externally from storage formats like Parquet, they store them directly in PostgreSQL. This not only improves query optimization and execution speed but also supports more advanced features like file-level skipping and accelerated scanning.

Through these optimizations and designs, mooncake achieved amazing performance results (claimed 1000x). This allows PostgreSQL to no longer be just the traditional OLTP "heavy horse." Through sufficient optimization and engineering practice, it can completely compete with professional analytical databases in analytical performance while retaining PostgreSQL's advantages of strong flexibility and mature ecosystem. This means future data stacks might be much simpler than now — you no longer need big data full stacks and ETL — top-tier analytical performance can be achieved inside Postgres.

Pigsty officially provides mooncake 0.1 version binaries in v3.2.2. Please note this extension is mutually exclusive with pg_duckdb because they both bring their own libduckdb, so you can only choose one in a system. This is quite regrettable, but I raised an issue hoping they can share a libduckdb. Compiling these two rival extensions really takes a toll since you have to compile DuckDB from scratch each time.

Finally, from this extension's name (mooncake), it's not hard to see this is a Chinese-led team. More and more Chinese people appearing and being active in the PostgreSQL ecosystem is truly delightful.

> Blog: ClickBench says Postgres is a great analytical database https://www.mooncake.dev/blog/clickbench-v0.1

------

## ParadeDB

ParadeDB is an old friend of Pigsty. We've supported ParadeDB from very early on and witnessed its growth, becoming a leader in providing ElasticSearch capability alternatives in the PostgreSQL ecosystem.

`pg_search` is ParadeDB's Postgres-based extension that implements custom indexes to support full-text search and analytical functionality. This extension is powered by the Rust-written, Lucene-inspired search library [Tantivy](https://github.com/quickwit-oss/tantivy).

pg_search released new version 0.14 in the past two weeks. In this version, they switched to PG native block storage instead of relying on Tantivy's own file format. This architectural improvement brought tremendous reliability improvements and several times performance enhancement, truly amazing, and marks it no longer being a "Frankenstein" but deeply natively integrated into PG.

Before `v0.14.0`, `pg_search` didn't use Postgres's block storage and buffer cache. This meant the extension would create some files not managed by Postgres and directly read their contents from disk. While it's not uncommon for extensions to directly access the filesystem (see note 1), after migrating to block storage, `pg_search` simultaneously achieved the following goals:

1. Deep integration with Postgres Write-Ahead Log (WAL), enabling physical replication of indexes.
2. Support for crash recovery and point-in-time recovery.
3. Full support for Postgres MVCC (Multi-Version Concurrency Control).
4. Integration with Postgres buffer cache, dramatically improving index creation speed and write throughput.

![img](https://www.paradedb.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fblock_storage_create_index.de1454d3.png&w=3840&q=75) ![img](https://www.paradedb.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fblock_storage_tps.598e54c0.png&w=3840&q=75)

pg_search's latest version has been included in Pigsty. Of course, we also provide other extensions offering similar full-text search/tokenization capabilities, such as pgroonga, pg_bestmatch, hunspell, and Chinese tokenization zhparser, for users to choose as needed.

> Blog: Full-Text-Search Using Postgres Block Storage Layout https://www.paradedb.com/blog/block_storage_part_one

------

## citus

pg_duckdb and pg_mooncake are new OLAP stars in the PG ecosystem, while Citus and Hydra are veteran OLAP (or HTAP) extensions. The day before yesterday, Citus released version 13.0.0, officially providing support for PostgreSQL's latest major version 17. This means all **major** extensions have completed adaptation to PG 17. PG 17, let's go!

Citus is the distributed extension in the PG ecosystem, capable of smoothly converting single-machine PostgreSQL master-slave deployments into horizontal distributed clusters. After Microsoft's acquisition, Citus became fully open source, with the cloud service version called Hyperscale PG or CosmosDB PG.

Generally speaking, under contemporary hardware conditions, the vast majority of users won't encounter scenarios requiring distributed databases — but such scenarios do exist. For example, the friend in "[Big Fool Paying for Pain: Escaping Cloud Computing Scam Mills](https://mp.weixin.qq.com/s/zwJ2T2Vh_R7xD8IKPso31Q)" considered using Citus because cloud disks were too expensive and went off track. So Pigsty also recently updated to support Citus.

Usually, distributed database operations and management are much more troublesome than master-slave setups, but we designed an elegant abstraction making Citus deployment and management very simple — you just need to treat them as multiple horizontal PostgreSQL clusters. The following configuration can spin up a 10-node Citus cluster with one command.

I recently also wrote a tutorial on deploying Citus high-availability clusters for interested users: https://pigsty.cc/docs/tasks/citus/

> Blog: Citus v13.0.0 Release Notes: https://github.com/citusdata/citus/blob/v13.0.0/CHANGELOG.md

------

## FerretDB

Finally, we welcome FerretDB 2.0. FerretDB is an old friend of Pigsty. Marcin shared the joy of the new version release with me first. Unfortunately, FerretDB 2.0 is still RC, so I can only wait for the official version release before updating to the Pigsty repository, missing this Pigsty v3.2.2 release window. But no worries, it'll be in the next version!

FerretDB is an adapter middleware that converts PostgreSQL into MongoDB "wire protocol compatible" — providing Apache 2.0 licensed, "truly open source" MongoDB. FerretDB 2.0 relies on Microsoft's newly open-sourced DocumentDB PostgreSQL extension, achieving significant leaps in performance, compatibility, support, and flexibility, capable of handling more complex use scenarios. Main highlights include:

- Over 20x performance improvement
- Higher functional compatibility
- Support for vector search
- Support for replication
- Extensive support and services

FerretDB provides MongoDB users the path of least resistance for smooth migration to PostgreSQL — you don't need to modify application code to achieve seamless substitution, maintaining MongoDB API compatibility while enjoying the superpowers provided by hundreds of extensions in the PG ecosystem.

> Blog: https://blog.ferretdb.io/ferretdb-releases-v2-faster-more-compatible-mongodb-alternative/

------

## Pigsty 3.2.2

Finally, there's Pigsty v3.2.2. This release brings 40 brand new extension plugins (though 33 come from Omnigres), plus updated versions of existing extensions (like Citus, ParadeDB, PGML). Meanwhile, we also promoted and followed up on PolarDB PG supporting ARM64 and Debian systems, and followed up on IvorySQL's latest PostgreSQL 17.2 compatible version 4.2.

Well, sounds like just version following work, but if it weren't for that, I couldn't release and launch the day before vacation! Anyway, welcome everyone to try these new extension plugins. If you encounter any problems, please give feedback, but I can't guarantee anything during vacation, haha.

By the way, some users gave feedback that Pigsty's old website was too "ugly," with a strong technical straight-man vibe, cramming all information densely on the homepage. I think they have a point, so I recently found a frontend template and redid the website homepage, which seems to have more "international flair."

Honestly, I haven't touched frontend for seven or eight years. Last time I fiddled was during the jQuery era. This time, Next.js/Vercel and these new tricks made me dizzy. But fortunately, after figuring it out, it wasn't too complex, especially with help from GPT o1 pro and Cursor. I finished everything in a day. The amazing productivity boost brought by AI is indeed impressive.

Well, that's the recent PostgreSQL ecosystem news. I'm also ready to pack my bags — afternoon flight to Thailand, hoping not to encounter telecom fraud. Here's wishing everyone Happy New Year in advance!

-