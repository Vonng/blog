---
title: "Pigsty v2.6: OLAP Punch"
linkTitle: "Pigsty v2.6 Release Notes"
date: 2024-02-27
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.6.0)）
summary: >
  PG16.2 becomes the default, ParadeDB and DuckDB integrations arrive, and the Pigsty site/docs/branding get a full refresh.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.6.0

Pigsty 2.6 leans into HTAP: PostgreSQL 16.2 is now the primary target, ParadeDB’s `pg_analytics`/`pg_bm25`/`pg_sparse` extensions bring columnar + search acceleration, and DuckDB + `duckdb_fdw` let you tap into one of the fastest OLAP engines from regular SQL. PGVector 0.6 adds parallel HNSW builds, Hydra, Age, and PGML are updated for PG16, and a new site/brand (pigsty.io via Cloudflare) accompanies the release along with commercial SKUs.

--------

## v2.6.0 Release Notes

- Highlights: PG16.2 default, ParadeDB extensions, DuckDB + FDW, new global CDN (`repo.pigsty.io`), refreshed docs + values, pro/enterprise support offerings.
- Config changes: `node_repo_modules` replaces `node_repo_method`/`node_repo_local_urls`; Grafana unified alerting disabled temporarily; package lists reshuffled; repo substitutions respect PGDG minor versions.
- Packages: Grafana 10.3, Prometheus 2.47, node_exporter 1.7, HAProxy 2.9.5, Loki/Promtail 2.9.4, etcd 3.5.11, Redis 7.2.4, Bytebase 2.13.2, DuckDB 0.10, FerretDB 1.19, MinIO Feb 2024 builds, Metabase template.
- PostgreSQL stack: 16.2/15.6/14.11/13.14/12.18, pg_exporter 0.6.1, Patroni 3.2.2, pgBadger 12.4, pgBackRest 2.50, vip-manager 2.3, PostGIS 3.4.2, TimescaleDB 2.14.1, PGVector 0.6.
- New extensions: `duckdb_fdw`, `pgsql-gzip`, ParadeDB’s `pg_sparse`/`pg_bm25`/`pg_analytics` (0.5.6), plus upgrades to PGML 2.8.1, Hydra 1.1.1, AGE 1.5, pg_graphql 1.5.
