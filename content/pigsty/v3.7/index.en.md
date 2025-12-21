---
title: "Pigsty v3.7: PG18 Default + OS Explosion"
linkTitle: "Pigsty v3.7 Release Notes"
date: 2025-12-03
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.7.0)）
summary: >
  PG18 becomes the default, four new OS targets land, Supabase/Percona/IvorySQL refresh, and Pigsty wins the “PostgreSQL Magneto” award.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.7.0

Pigsty 3.7 ships PG18 as the default kernel with 437 packaged extensions. Debian 13 and EL10 join the matrix across x86/ARM, bringing the supported OS count to 14. Supabase, IvorySQL, PolarDB, and Percona TDE kernels were updated, as were Prometheus/Grafana/DuckDB/Etcd. Pigsty picked up the “PostgreSQL Magneto” award for its extension work.

Highlights include the PG18-ready extension catalog, new OS templates, massive build automation (84 combos, 60k+ packages), fresh dashboards, parameter template improvements, and a roadmap aimed at making Pigsty the Ubuntu of Postgres.

--------

## v3.7.0 Release Notes

- PG18 default, PG13 enters EOL; PG18 features (Temporal PK, UUIDv7, Skip Scan, AIO, generated columns, OAuth) fully supported.
- OS support: EL10 + Debian 13 (x86/ARM); EL8/Debian11/Ubuntu20 enter maintenance-only mode.
- Kernels: Supabase docker images updated, IvorySQL 5.0, Percona TDE on PG18.1, PolarDB 15.15.5, FerretDB 2.7, OpenHalo/OrioleDB get Debian13/EL10 packages.
- Extensions: pg_duckdb 1.1, pg_mooncake 0.2, VectorChord 1.0, pg_search 0.20; automation rebuilds 84 combos; repo counts exceed 60k packages.
- Parameters: better CPU/thread/parallels defaults, new background worker resource tuning, new SOP docs.
- CLI: `pig` handles extension builds, `pg_pkg pg_pre` pre-script removes conflicting EL9 packages; numerous Ansible 2.19 compatibility fixes.
