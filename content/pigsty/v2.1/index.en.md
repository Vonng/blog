---
title: "Pigsty v2.1: Vector + PG12–16"
linkTitle: "Pigsty v2.1 Release Notes"
date: 2023-06-09
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.1.0)）
summary: >
  PGVector ships by default, PG12–16 (including 16 beta) are supported, and Grafana gets a modern UI refresh.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.1.0

Pigsty 2.1 tracks the PG summer releases: PG16 beta clusters spin up just like any other version, PG12–15 binaries plus their extension suites land in the offline bundles, and pgvector 0.4+ is baked in so you can build AI retrieval flows without touching a compiler.

PG16’s new observability surfaces (`pg_stat_io`, last scan timestamps, `n_tup_newpage_upd`, etc.) are wired into the dashboards so you can reason about IO-heavy workloads with the same ease you debug queries. Grafana 9.5.x brings a new shell, and we bundle Volkov Labs plugins (ECharts, SVG/text, forms, dynamic calendars) plus `echarts-gl` assets so 3D charts work offline.

Three new helper scripts ship in `bin/`: `validate` sanity-checks your YAML before running Ansible, `repo-add` pushes repo definitions to hosts, and `profile` captures perf flame graphs remotely. It’s a nice quality-of-life bump for operators.

--------

## v2.1.0 Release Notes

- PG16 beta1 + PG12–15 support, with pgvector, PostGIS, TimescaleDB, Citus, pg_repack, wal2json, pglogical, pg_cron, passwordcheck_cracklib built for each version.
- Grafana 9.5.3 plus six additional plugins (Volkov Labs ECharts/Data Manipulation) and offline `echarts-gl` assets.
- New scripts: `bin/profile` (remote perf flame graphs), `bin/validate` (config linter), `bin/repo-add` (push repo definitions).
- Observability: dashboards updated for `pg_stat_io` and PG16 scan timestamp metrics.
- Package refresh: PostgreSQL 15.3/14.8/13.11/12.15/16b1, pgBackRest 2.46, pgbouncer 1.19, Redis 7.0.11, Loki/Promtail 2.8.2, Prometheus 2.44, TimescaleDB 2.11.0, MinIO 20230518, Bytebase 2.2.0.
