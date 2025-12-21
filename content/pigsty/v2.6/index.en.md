---
title: "Pigsty v2.6: PostgreSQL Crashes the OLAP Party"
linkTitle: "Pigsty v2.6 Release"
date: 2024-02-27
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v2.6.0))
summary: >
  Pigsty v2.6 makes PostgreSQL 16.2 the default, introduces ParadeDB and DuckDB support, and brings epic-level OLAP improvements.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v2.6.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v260)

[![](featured.webp)](https://github.com/pgsty/pigsty/releases/tag/v2.6.0)

On the last day of February, Pigsty v2.6 is officially released! This version makes PostgreSQL 16 the default major version and introduces a series of new extensions, including [**ParadeDB**](https://www.paradedb.com/) and DuckDB, elevating PostgreSQL's OLAP analytical capabilities to an entirely new level. Calling it the HTAP benchmark and database all-rounder is well-deserved.

Additionally, we've completely refreshed the Pigsty official website, documentation, and blog, presenting six more refined core value propositions. Globally, we're now using the Cloudflare-powered domain **pigsty.io** as the default official site and repository address. The original pigsty.cc domain, website, and repos continue to serve as mirrors within China.

Finally, we're officially launching transparently-priced Pigsty Pro and service subscriptions, providing advanced features and support options for users who need them.


------

## Epic-Level Analytics Enhancement

TPC-H and ClickBench are authoritative analytics benchmarks. ClickBench provides horizontal comparisons of many OLAP databases, serving as quantifiable references. In this representative example, we can see relative performance of many well-known database components (lower time is better):

![olap.jpg](olap.jpg)

c6a.4xlarge, 500gb gp2 / 1 billion records

This chart shows PostgreSQL and its ecosystem extensions' performance. Native untuned PostgreSQL takes (**x1000**), while tuned it reaches (**x47**). The PG ecosystem also has three analytics-related extensions: columnar **Hydra** (**x42**), time-series **TimescaleDB** (**x103**), and distributed **Citus** (**x262**). But compared to top-tier OLAP-focused systems — Umbra, ClickHouse, Databend, SelectDB (**x3~x4**) — there's still a 10x+ performance gap. However, the recent arrival of [**ParadeDB**](https://www.paradedb.com/) and **DuckDB** has changed this!

**ParadeDB's** native PG extension **pg_analytics** achieves second-tier (**x10**) performance, only 3-4x behind top-tier OLAP databases. Considering the extra benefits — ACID, data freshness, no ETL, no extra learning curve, no separate service to maintain (not to mention it also provides ElasticSearch-quality full-text search) — this performance gap is usually acceptable.

And **DuckDB** (**x3.2**) elevates OLAP to an entirely new level — setting aside academic databases like Umbra, DuckDB may be the fastest practical analytics database. While not a PG extension itself, it's an embeddable component, and projects like **DuckDB FDW** and **pg_quack** let PostgreSQL fully leverage DuckDB's complete analytical performance!

![duck.jpg](duck.jpg)

Appreciation from ParadeDB's founder and DuckDB FDW's author


------

## New Value Propositions

Value propositions are the soul of a database distribution. In this version, we present **six core values** as shown:

![value1.jpg](value1.jpg)

This diagram lists six core problems PostgreSQL solves: Postgres extensibility, Infrastructure reliability, Graphics observability, Service availability, Toolbox maintainability, and component composabilitY.

![value2.jpg](value2.jpg)

Pigsty's six abbreviations form the PIGSTY acronym — besides **P**ostgreSQL **i**n **G**reat **STY**le, these six value propositions offer another interpretation:

> **P**ostgres, **I**nfras, **G**raphics, **S**ervice, **T**oolbox, **Y**ours.
>
> Your graphical Postgres infrastructure service toolbox.

We've also redesigned the logo, from the sunglasses-wearing pig head to a hexagonal composition with colors matching key components (PG Blue, ETCD Teal, Grafana Orange, Ansible Black, Redis/MinIO Red, Nginx Green) — a condensed version of the large hexagon above. The original sunglasses pig will continue as Pigsty's mascot.

![mascot.jpg](mascot.jpg)


------

## New Website

In this version, we've renovated the old website using the latest Docsy documentation framework, updating substantial content. We abandoned flashy impractical designs, putting Pigsty's value propositions and core features directly on the landing page.

![web1.jpg](web1.jpg)

The real content lives in the documentation. We restructured the doc directory:

![web2.jpg](web2.jpg)

After letting go of pure Markdown purism, we can use attractive styles and features in documentation:

![web3.jpg](web3.jpg)

Beyond docs, we've organized recent articles into the Pigsty blog, divided into six columns: Cloud Computing Mudslide, Database Veteran Driver, and PostgreSQL's Ecosystem, Development, Administration, and Kernel sections.

![web4.jpg](web4.jpg)

Meanwhile, Pigsty's software repositories now have global mirrors powered by Cloudflare R2, hosted on Cloudflare for smooth access worldwide (China users can continue using pigsty.cc).


------

## PostgreSQL 16 Becomes Default

The last notable feature: in Pigsty v2.6, PostgreSQL 16 (16.2) officially replaces PostgreSQL 15 as the default major version.

Three months ago, we noted that PostgreSQL's main extensions were in place, plus with the second minor release, it was production-ready.

Pigsty v2.6 coincides with PostgreSQL 16.2's third minor release, and important extensions like Hydra, PGML, and AGE have followed to PG 16. So we've decided to officially upgrade the default PG major version to 16, making it the only supported major version in the open-source edition (except EL7).

Therefore, another important technical decision in this version: we've removed the default PG 12-15 packages and extensions from the open-source edition. This doesn't mean Pigsty doesn't support PG 12-15 — with minor config adjustments, you can easily use older PostgreSQL versions and extensions — but we won't run integration tests against these versions (though they've been thoroughly tested in older Pigsty releases).

![pg16.jpg](pg16.jpg)

Similarly, we've narrowed the open-source support scope to EL 8 / EL 9 and Ubuntu 22.04 — the three most widely-used OS distributions. In Pigsty 2.5, we supported PG 12-16 (five major versions) times seven OS distributions, totaling 34 combinations, plus upcoming ARM support, creating significant testing pressure.

Focusing the open-source edition on one core PG major version and three mainstream OS distributions better utilizes R&D bandwidth to meet the majority of open-source users' needs. Again, this doesn't mean Pigsty can't run on older systems — you can still run smoothly on EL7, Ubuntu 20.04, Debian 11/12, but we won't provide offline packages, smoke tests, or support for these OSes.

Supporting niche/legacy OSes and outdated major versions isn't needed by the vast majority of users but requires substantial extra effort and cost, so it's included in our paid commercial support.


------

## Open Source vs Pro Edition

Some open-source users have feedback: "I don't need stuff unrelated to PostgreSQL slowing down downloads/installation and adding management complexity — Redis, MinIO, Docker, K8S, Supabase — you think they help PG, but flashy extras only slow my attack speed."

The specific feature division isn't finalized yet, so 2.6 may be the last fully-featured open-source Pigsty version. But the basic principle: the open-source edition will retain all core modules and PG extensions (PGSQL, INFRA, NODE, ETCD), while modules less related to PostgreSQL may become Pro edition content later.

![pro.jpg](pro.jpg)

Going forward, the Pigsty open-source edition will focus on doing one thing well — providing reliable, highly-available, extensible local PostgreSQL RDS services. Practical features like Docker templates may still stay in the open-source edition.

This doesn't mean these features disappear from open-source Pigsty — seasoned open-source veterans can still easily recreate them by modifying config files — but they won't be default components of the open-source version.


------

## Commercial Subscriptions

Open source is a passion project powered by love, but sustainable development requires commercial interests. In this version, we officially launch commercial Pigsty editions, providing richer support options for those who need them.

Besides additional feature modules, Pigsty Professional Subscriptions provide consulting Q&A and backstop services, supporting a broader range of operating systems and database versions:

![svc.jpg](svc.jpg)

While Pigsty's mission is providing out-of-the-box database services — even with self-healing HA for hardware failures and PITR for software/human errors — you might spin it up and go a year, two, three without issues. Statistically, that's normal.

But database problems are usually big problems. Misusing databases also tends to become big problems. So we provide expert consulting and services for paying customers as ultimate backstop for difficult issues. (Example: we've rescued a burned Gitlab database with no backups). We also offer professional PostgreSQL DBA consulting services: backup, security, compliance recommendations, management and development best practices, performance evaluation and optimization, design guidance and Q&A.

![sub.jpg](sub.jpg)

Often, turning the ordinary into extraordinary and achieving orders-of-magnitude improvements comes down to one sentence from an expert. This is especially true for PostgreSQL, whose soul is extensibility and whose extension ecosystem is incredibly rich. Our services ensure every dollar you spend is worthwhile and spent on what truly matters.


------

## Looking Forward

Pigsty's next major version is planned as v3, officially implementing the open-source/pro feature division. We'll complete missing extension DEBs for Ubuntu/Debian systems and provide a CLI tool to wrap management operations. We may package Pigsty itself as RPM/DEB, and plan beta MYSQL monitoring/deployment support.

For monitoring, we'll redesign PostgreSQL monitoring dashboards based on PG 16's IO metrics, provide MySQL monitoring capability, and try using Vector as an alternative to Promtail for log collection. We already have monitoring for Alibaba Cloud RDS PG and PolarDB; we also plan AWS RDS and Aurora monitoring support in v3.0.

For infrastructure, we're choosing to abandon "cheap" Tencent Cloud CDN, fully embracing more reliable, faster, and cheaper Cloudflare to serve global users. Tencent Cloud CDN may serve as a domestic mirror for Pro edition acceleration.

Pigsty's product and interfaces will stabilize in v2.6 and v3.0 — it's already doing great on product and technology fronts! Even exceeding RDS in some areas (like extension support and monitoring!). So upcoming work will shift focus to marketing and sales. Sustainable open-source operations require user and customer support. If Pigsty has helped you, please consider sponsoring us or purchasing our service subscriptions.


----------------

## v2.6.0 Release Notes

**Highlights**

* PostgreSQL 16 is now the default major version (16.2)
* New [ParadeDB](https://www.paradedb.com/) extensions: `pg_analytics`, `pg_bm25`, and `pg_sparse`
* New [DuckDB](https://duckdb.org/) and `duckdb_fdw` support
* Global Cloudflare CDN https://repo.pigsty.io and China CDN https://repo.pigsty.cc

**Configuration Changes**

- Replaced `node_repo_method` with `node_repo_modules`, removed `node_repo_local_urls`
- Temporarily disabled Grafana unified alerting to avoid "Database Locked" errors
- New `node_repo_modules` parameter to specify upstream repos added to nodes
- Removed `node_local_repo_urls`, functionality replaced by `node_repo_modules` & `repo_upstream`
- Removed `node_repo_method` parameter, functionality replaced by `node_repo_modules`
- Added new `local` source in `repo_upstream`, used via `node_repo_modules` to replace `node_local_repo_urls`
- Reorganized `node_default_packages`, `infra_packages`, `pg_packages`, `pg_extensions` defaults
- When replacing `repo_upstream.baseurl`, if EL8/9 PGDG minor-version-specific repos are available, use `major.minor` instead of `major` for $releasever for better minor version compatibility

**Software Upgrades**

- Grafana 10.3
- Prometheus 2.47
- node_exporter 1.7.0
- HAProxy 2.9.5
- Loki / Promtail 2.9.4
- minio-20240216110548 / mcli-20240217011557
- etcd 3.5.11
- Redis 7.2.4
- Bytebase 2.13.2
- DuckDB 0.10.0
- FerretDB 1.19
- Metabase: new Docker app template

**PostgreSQL Extensions**

- PostgreSQL minor version upgrades: 16.2, 15.6, 14.11, 13.14, 12.18
- PostgreSQL 16: now promoted to default major version
- pg_exporter 0.6.1: security fix
- Patroni 3.2.2
- pgBadger 12.4
- pgBackRest 2.50
- vip-manager 2.3.0
- PostGIS 3.4.2
- TimescaleDB 2.14.1
- Vector extension PGVector 0.6.0: added parallel HNSW index creation
- New extension [duckdb_fdw](https://github.com/alitrack/duckdb_fdw) v1.1 for reading/writing DuckDB data
- New extension [pgsql-gzip](https://github.com/pramsey/pgsql-gzip) for Gzip compression/decompression v1.0.0
- New extension [pg_sparse](https://github.com/paradedb/paradedb/tree/dev/pg_sparse) for efficient sparse vectors (ParadeDB) v0.5.6
- New extension [pg_bm25](https://github.com/paradedb/paradedb/tree/dev/pg_bm25) for high-quality BM25 full-text search (ParadeDB) v0.5.6
- New extension [pg_analytics](https://github.com/paradedb/paradedb/tree/dev/pg_analytics) with SIMD + columnar storage for analytics (ParadeDB) v0.5.6
- Upgraded AIML extension [pgml](https://github.com/postgresml/postgresml) to v2.8.1 with PG 16 support
- Upgraded columnar extension [hydra](https://github.com/hydradatabase/) to v1.1.1 with PG 16 support
- Upgraded graph extension [age](https://github.com/apache/age) to v1.5.0 with PG 16 support
- Upgraded GraphQL extension [pg_graphql](https://github.com/supabase/pg_graphql) to v1.5.0 for Supabase support

```bash
MD5 (pigsty-v2.6.0.tgz) = 330e9bc16a2f65d57264965bf98174ff
MD5 (pigsty-pkg-v2.6.0.debian11.x86_64.tgz) = 81abcd0ced798e1198740ab13317c29a
MD5 (pigsty-pkg-v2.6.0.debian12.x86_64.tgz) = 7304f4458c9abd3a14245eaf72f4eeb4
MD5 (pigsty-pkg-v2.6.0.el7.x86_64.tgz) = f914fbb12f90dffc4e29f183753736bb
MD5 (pigsty-pkg-v2.6.0.el8.x86_64.tgz) = fc23d122d0743d1c1cb871ca686449c0
MD5 (pigsty-pkg-v2.6.0.el9.x86_64.tgz) = 9d258dbcecefd232f3a18bcce512b75e
MD5 (pigsty-pkg-v2.6.0.ubuntu20.x86_64.tgz) = 901ee668621682f99799de8932fb716c
MD5 (pigsty-pkg-v2.6.0.ubuntu22.x86_64.tgz) = 39872cf774c1fe22697c428be2fc2c22
```
