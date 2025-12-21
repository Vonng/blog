---
title: "Pigsty v1.1: Home, Jupyter, and Plan Tools"
linkTitle: "Pigsty v1.1 Release Notes"
date: 2021-10-12
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v1.1.0)）
summary: >
  Fresh homepage UX plus JupyterLab, PGWeb, Pev2, and PgBadger integrations land in Pigsty 1.1.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v1.1.0

Pigsty 1.1 focuses on UX and tooling. The distro now ships a dedicated homepage that acts as the launchpad for every service, along with turnkey installs of JupyterLab, PGWeb, Pev2, PgBadger, and new sample apps.

## New Homepage

The old Grafana Home dashboard was a makeshift front page. We replaced it with a proper landing page served by the built-in Nginx—think offline docs + navigation for Consul, Grafana, Prometheus, Alertmanager, PGWeb, JupyterLab, and any custom apps you enable. Cluster/instance shortcuts and doc links (both Chinese and English) live there as well.

## JupyterLab

Jupyter is now a first-class citizen. Demo and personal templates enable it by default so data scientists can mix SQL + Python notebooks directly against Pigsty-managed databases. Production templates keep it disabled because arbitrary code execution on prod boxes is a bad idea, but you can opt in when needed.

## PGWeb

We also bundled PGWeb—a lightweight, browser-based PG client written in Go. Demo/personal templates have it enabled; production templates leave it off unless you explicitly allow it. PGWeb is perfect for light read-only access where users need a familiar GUI.

## Pev2 and PgBadger

Pev2 renders EXPLAIN plans as interactive trees, making auto_explain output much easier to reason about. PgBadger parses CSV logs into clean daily reports. A helper `bin/pglog-summary [ip] [date]` pulls logs and generates reports; cron it to keep rolling insights.

## Software Updates

PostgreSQL 14 is hot off the presses. Pigsty 1.1 supports it immediately (テンplate `pigsty-pg14`), though PG14 isn’t yet the default because TimescaleDB still needs an upstream release. Component versions:

| Component | Version |
|-----------|---------|
| PostgreSQL | 13.4 (PG14 optional) |
| pgbouncer | 1.16 |
| Grafana | 8.1.4 |
| Prometheus | 2.29 |
| node_exporter | 1.2.2 |
| HAProxy | 2.1.1 |
| Consul | 1.10.2 |
| vip-manager | 1.0.1 |

## Migration Playbook

`pgsql-migration.yml` automates logical-replication migrations. Feed it source/target cluster info and it generates the scripts to cut over with minimal downtime.

## Sample App: Privacy Log Explorer

A new demo app visualizes Apple’s iOS 15 privacy logs (AppLog). Export the log bundle from your iPhone and explore it via Pigsty.

## Handy Extras

- **Dummy file**: set `pg_dummy_filesize` to create `/pg/dummy` reserves (1–4 GB). Delete it during a disk-full event to reclaim emergency space.
- **Promscale**: packages are ready so you can pipe Prometheus metrics into TimescaleDB if that’s your thing.

--------

## v1.1.0 Release Notes

- New homepage, app/service/doc navigation, and offline docs.
- JupyterLab, PGWeb, PgBadger, Pev2, and `pglog` tooling integrated.
- Added `pg_dummy_filesize` reserve control.
- Component upgrades listed above.
- API updates: `nginx_upstream` structure change (breaking), new `app_list`, `docs_enabled`, and `pev2_enabled` options.
