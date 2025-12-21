---
title: MySQL vs. PostgreSQL @ 2025
summary: "A 2025 reality check on where PostgreSQL stands relative to MySQL across features, performance, quality, and ecosystem."
date: 2025-04-17
tags: [Database, MySQL, PostgreSQL]
series: [MySQL走好]
---

In 2025, PostgreSQL has opened a clear lead over MySQL on features, correctness, performance, and ecosystem—and the gap keeps widening. Here’s the panoramic view.

-------

## Features

### Release cadence

MySQL just dropped “Innovation” 9.3 ([release notes](https://dev.mysql.com/doc/refman/9.3/en/mysql-nutshell.html)), yet the changelog looks like more of the same patchwork. Search for “PostgreSQL 18” and you’ll find dozens of preview write-ups. Search “MySQL 9.3” and you get sighs. MySQL OG Ding Qi wrote “[MySQL’s innovation branch is losing its point](https://mp.weixin.qq.com/s/LLlOkGHIDhUCkJNLlmtXSQ).” Dege followed with “[MySQL Will Stay Mediocre](https://mp.weixin.qq.com/s/QnfCqVOsSxsnjfUZv9UPsg).” Percona CEO Peter Zaitsev penned “[Where Are You Going, MySQL?](/en/blog/db/sakila-where-are-you-going/),” “[Oracle Finally Killed MySQL](/en/blog/db/oracle-kill-mysql/),” and “[Can Oracle Save MySQL?](/en/blog/db/can-oracle-save-mysql/),” expressing open frustration.

### New capabilities

Take vectors—the hottest database feature in years. PostgreSQL sprouted half a dozen vector extensions (`pgvector`, `pgvector.rs`, `pg_embedding`, `latern`, `pase`, `pgvectorscale`, `vchord`). They competed fiercely; AWS poured resources into `pgvector`, delivering **150× speedups** in a year and turning bespoke vector DBs into a punchline.

Meanwhile PostgreSQL’s ecosystem is also [stitching DuckDB into PG](https://mp.weixin.qq.com/s/zoxaJBgNLreWc-TkqOJ8BQ). Extensions like [`pg_duckdb`](https://github.com/duckdb/pg_duckdb) and [`pg_mooncake`](https://pgmooncake.com/) now sit in the Tier‑0 bracket of ClickBench and even made the [Thoughtworks Technology Radar](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/04/tr_technology_radar_vol_32_cn.pdf). There’s an ElasticSearch replacement bake-off using Tantivy/BM25. PostgreSQL has effectively become a database development framework, not just an OLTP engine.

MySQL’s response? A [vector type](https://dev.mysql.com/doc/refman/9.0/en/vector-functions.html) that can’t compute distances or use indexes, plus enterprise-only JavaScript stored procedures—something Postgres shipped via `plv8` 15 years ago. MySQL clings to “relational OLTP.” PostgreSQL has gone multi-modal: relational, JSON, vectors, GIS, search, columnar analytics, and more.

### Extensibility

Abigale Kim (CMU) benchmarked [extensibility across major DBMSes](https://abigalekim.github.io/assets/pdf/Anarchy_in_the_Database_PGConfDev2024.pdf). PostgreSQL tops the chart with **375+ PGXN-listed extensions**—actual ecosystem numbers exceed 1,000. Pigsty alone ships 405 extension packages out of the box. The extension landscape spans GIS, time series, vectors, ML, OLAP, full-text, graph, etc., letting PG replace specialized components like MySQL, MongoDB, Kafka, Redis, ElasticSearch, Neo4j, and even warehouses/data lakes.

[PostgreSQL Is Eating the Database World](/en/blog/pg/pg-eat-db-world/) and “[Just Use Postgres](/en/blog/pg/just-use-pg/)” aren’t fringe slogans anymore; they’re mainstream practice.

MySQL’s “innovation releases” should usher in bold changes. Instead they ship timid tweaks, leaving glaring gaps.

-------

## Performance

Benchmarks are context-specific, but low-hanging comparisons are telling. Pigsty’s [TPC-H](https://pigsty.cc/blog/db/tpch/#pigsty) run on 8 vCPU x86 hardware shows PostgreSQL beating MySQL 9.x across all baseline queries. With `pg_duckdb`/`pg_mooncake` plugging into ClickHouse/DuckDB grade tooling, Postgres lands in the CH/StarRocks class for analytics.

Even MySQL’s traditional OLTP speed edge is gone. In December 2024, a straightforward sysbench/wrk test on identical hardware showed PostgreSQL 16 matching or exceeding MySQL 9.0 by simply turning on `prepared statements` and `cache prepared statements`. No black magic.

In short: PostgreSQL now outclasses MySQL in both OLTP and OLAP.

-------

## Quality & Correctness

This is where Postgres was always ahead—and the gap is now especially damaging for MySQL.

### JEPSEN verdict

JEPSEN’s [MySQL 8.0.34 analysis](https://jepsen.io/analyses/mysql-8.0.34) found that MySQL’s default **Repeatable Read (RR)** isn’t repeatable, atomic, or monotonic. It fails to meet **Monotonic Atomic View (MAV)**—the baseline most DBMSes provide at RC. MySQL’s RR is weaker than other vendors’ RC.

![mysql-bad-case.png](/en/blog/db/bad-mysql/)

To avoid anomalies you must go full Serializable. But MySQL’s serializable mode is slow and rarely used. You can sprinkle manual locks to paper over issues, but that kills performance and invites deadlocks.

PostgreSQL implemented Serializable Snapshot Isolation (SSI) in 9.1, delivering true serializable semantics with minimal overhead, and without Oracle’s quirks.

![consistency.png](consistency.png)

Prof. Li Haixiang’s “[Consistency Octagon](https://mp.weixin.qq.com/s/_BhAjcMkmthTf8Zw3RWKDw)” compares mainstream DBMS isolation levels. Blue/green = clean; yellow “A” = anomalies; red “D” = deadlock-heavy solutions. PostgreSQL SR (and CockroachDB’s PG-derived SR) sit in the clean corner. Oracle SR has mild issues. MySQL lights up yellow and red all over—poor correctness and performance.

Correctness shouldn’t be optional. MySQL chose performance over ACID fidelity decades ago. Now performance parity erases the one advantage they traded correctness for.

### Standards compliance

Both DBs have been inching toward SQL compliance, but details matter. Example: collations. With ICU, PostgreSQL offers 42 encodings and 815 collations. MySQL ships five core charsets and a few dozen collations—a stark reminder of where engineering effort goes.

-------

## Ecosystem

Usage drives ecosystem health. MySQL’s slogan “the world’s most popular open-source RDBMS” no longer matches data.

### Developers

StackOverflow surveys show PostgreSQL usage climbing steadily for eight years, overtaking MySQL in 2023 to become the most-used database overall. In front-end circles Postgres is dominant; Vercel’s seven managed storage services include four Postgres derivatives (Neon, Supabase, Nile, Gel), two Redis variants, one DuckDB—zero MySQL. DBDB.io counts far more PG-derived databases than MySQL derivatives.

### Vendors

On AWS RDS, PostgreSQL instances now outnumber MySQL by roughly 6:4 ([details](https://mp.weixin.qq.com/s/tuzmmkEIOsuq2-8rMbmVLw)). Even in mainland China, Aliyun’s RDS ratio dropped from 10:1 to 5:1 in favor of MySQL, with Postgres growing faster than MySQL in absolute instances.

Cloud vendors put their chips on PostgreSQL. AWS RDS’s combined MySQL/PG PM is PG core member Jonathan Katz, a key driver behind pgvector. Aurora’s new distributed DSQL is Postgres-only—MySQL support was skipped entirely. Google’s AlloyDB is 100% PostgreSQL-compatible, and Spanner now offers a PG interface. Alicloud’s PolarDB 2.0 (Oracle-compatible) is a PG fork.

### Capital

The biggest recent rounds ([example](https://mp.weixin.qq.com/s/fi_p3tTZTnwP5XDJrkVbQw)) are all PG-adjacent. MySQL-land has SingleStore and TiDB; MariaDB, once the torchbearer, is heading for delisting/privatization.

### Large deployments

Manufacturing, finance, non-internet orgs lean on PG’s correctness and feature set. During my stint at Apple we recorded factory IIoT data in PostgreSQL, with internal communities around it. Legacy internet giants still run piles of MySQL due to inertia, but upstarts—Cursor, Dify, Notion, Stripe components—default to PG. Cloudflare, Vercel, and major Node.js projects do too (Prisma’s PG support is markedly better).

-------

## What Happened to MySQL?

Did PostgreSQL “kill” MySQL? Peter Zaitsev argues in “[Oracle Finally Killed MySQL](/en/blog/db/sakila-where-are-you-going/)” that Oracle’s neglect and mismanagement did. “[Can Oracle Save MySQL?](https://pigsty.cc/blog/db/can-oracle-save-mysql)” lays out the root cause: MySQL’s IP belongs to Oracle. It isn’t community-owned like PostgreSQL. Neither MySQL nor MariaDB has broad independent contributors. They’re company-controlled codebases.

Cloud vendors (AWS et al.) built services atop MySQL without contributing back. Oracle saw no reason to invest in a product competitors monetized more than they did, so they focused on proprietary MySQL HeatWave. AWS cares about RDS/Aurora, not upstream. The community withered—and hyperscalers share the blame.

![dbms-market.png](dbms-market.png)

-------

## Summing Up

I love PostgreSQL, but I agree with Peter: a world where PG is the only open-source RDBMS isn’t healthy. Competition keeps us sharp. MySQL’s decline should be a cautionary tale for PG: avoid dominance by any single vendor. “[The cloud is eating open source](/en/blog/cloud/paradigm/)” is real—vendors write the control planes, hire experts, and capture most value while offloading R&D costs to the community. The control/monitoring code rarely returns to open source. MongoDB, Elastic, Redis, MySQL have all reacted with restrictive licenses. PostgreSQL must stay vigilant.

Thankfully PG still has stubborn contributors and companies fighting for balance. Pigsty is my attempt to offer an open, local-first alternative to managed RDS, and my “[Cloud Mudslide](/en/blog/cloud/)” series tries to expose cloud opacity.

MySQL had a great run; every show ends. It’s dying—stalled releases, lagging features, eroding performance, correctness wounds, shrinking ecosystem. That’s fate. PostgreSQL will carry the open-source database banner forward, walking the roads MySQL abandoned.

- [PostgreSQL Achieves an Overwhelming Advantage Over MySQL](https://mp.weixin.qq.com/s/tuzmmkEIOsuq2-8rMbmVLw)

- [← Previous](/en/blog/db/pg-kiss-duckdb/)
- [Next →](/en/blog/db/ai-agent-era/)
