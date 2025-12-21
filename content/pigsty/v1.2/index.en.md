---
title: "Pigsty v1.2: PG14 by Default"
linkTitle: "Pigsty v1.2 Release Notes"
date: 2021-11-03
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v1.2.0)）
summary: >
  PostgreSQL 14 becomes the default kernel, and monitor-only modes cover external fleets.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v1.2.0

Pigsty 1.2 switches the default engine to PostgreSQL 14, layers in TimescaleDB 2.5 + PostGIS 3.1 + Citus 10, and adds a true monitor-only deployment that can watch any reachable PG database.

## PG14 Is the New Default

PostgreSQL 14 shipped last month with major observability improvements. After production burn-in we now default to PG14 everywhere. TimescaleDB 2.5 and PostGIS 3.1 are enabled alongside Citus 10, so you get a "space-time distributed" stack out of the box.

## Monitor-Only Deployments

Two new monitoring profiles join the full install:

| Mode | Description |
|------|-------------|
| Full | standard Pigsty install (infra + control + monitoring) |
| Lean | monitor stack only |
| Minimal | no remote SSH needed—just feed connection URIs |

Minimal deployments run `pg_exporter` locally and hit remote databases over TLS. You still keep most Pigsty dashboards, which means you can monitor cloud RDS instances, MatrixDB, Greenplum, or any PG-compatible fork with only read access.

## Slimmer Templates

Only two base templates remain: production (default) and sandbox. Spec presets (`tiny` → `crit`) cover everything from 1c/1g sandboxes to 64c/400g beasts. `./configure && make install` is still the happy path.

## Utility Playbooks

- `pgsql-migration`: auto-generates scripts/commands for logical-replication migrations; already battle-tested in dozens of production moves.
- `pgsql-audit`: emits audit reports based on your policy requirements.

## Sample Apps

- **AppLog** visualizes iOS 15 privacy logs.
- **WorkTime** aggregates working-hour reports from major Chinese tech firms. Both were built in under an hour—Pigsty doubles as a rapid-prototyping environment.

## Looking Ahead

Plans include PGSQL v8 (role-oriented dashboards), PGCAT v2 (richer catalog explorer), and Redis v1 beta (Redis deployment and monitoring baked in).

--------

## v1.2.0 Release Notes

- Default PostgreSQL 14 + TimescaleDB 2.5 + PostGIS enabled in CMDB.
- Monitor-only mode with per-instance exporters running on the meta node; new PGSQL Cluster Monly dashboards.
- Component updates: Grafana 8.2.2, Pev2 0.11.9, Promscale 0.6.2, PGWeb 0.11.9; new extensions pglogical, pg_stat_monitor, orafce.
- Auto-detect hardware profiles and pick matching `node_tune` / `pg_conf` templates; reworked bloat views; removed Timescale/Citus internal monitoring.
- `pgsql-audit.yml` added; config templates reduced to `auto` and `demo`.
- Bug fixes for exporter ownership and REINDEX duplicates.

## Upgrade Notes

No API changes—existing `pigsty.yml` files still work (even PG13). Re-run `repo` for infra updates. For databases, logical replication migrations are recommended when PostGIS/TimescaleDB are involved. See `pgsql-migration.yml` for generated scripts.
