---
title: "Pigsty v1.3: Redis Joins the Party"
linkTitle: "Pigsty v1.3 Release Notes"
date: 2021-11-30
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v1.3.0)）
summary: >
  Redis support, a rebuilt PGCAT, and sharper PGSQL dashboards headline Pigsty 1.3.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v1.3.0

Pigsty 1.3 adds Redis as a first-class citizen, rebuilds the catalog explorer (PGCAT), and tightens the PGSQL monitoring experience.

## Redis Support

Redis is now provisioned the same declarative way as PG. The demo ships with three clusters covering Standalone, Sentinel, and Cluster topologies. Define a cluster in YAML—just like Postgres—and run `redis.yml -l <cluster>` to stand it up. Grafana dashboards cover fleet/cluster/instance views automatically once the cluster exists.

## PGCAT 2.0

PGCAT now exposes instance-level, database-level, and table-level views with better navigation and richer stats (e.g., per-column details). It only needs a connection string; no agents required. Even monitor-only deployments get the full catalog browsing experience.

## PGSQL Enhancements

PGSQL dashboards gained quick-glance panels for the top ten metrics per cluster/instance, and PGSQL Service was redesigned for clarity. Cross-links between PGSQL and PGCAT make it easy to bounce from metrics to catalog context. Migration scripts and profiling helpers were refined as well.

--------

## v1.3.0 Release Notes

- **Redis**: deploy Standalone/Sentinel/Cluster modes; dashboards for overview/cluster/instance.
- **PGCAT**: new Instance and Database dashboards plus a redesigned Table view.
- **PGSQL**: quick metrics panels, simplified Service dashboard, cross-links with PGCAT.
- Grafana data sources auto-register during monitor-only deployments.
- Package updates: default PostgreSQL 14.1 (PG13 stays in the bundle), Greenplum RPMs, Redis RPM/source, `perf` tool.

## v1.3.1 Release Notes

- Dashboard polish for PGSQL + PGCAT (layout fixes, key-metric panels, new bloat/index sections, Grafana 8.3 support, Redis links on homepage).
- Deployment tooling: `infra-demo.yml`, optional `infra-jupyter.yml` and `infra-pgweb.yml`, `pg` alias for admin, Timescale tuning for Patroni, SSL-friendly Citus configs, PGDG14 extension coverage, node_exporter 1.3.1, PostgREST 9.0.0 packages.
- Security and bug fixes: Grafana 8.3.1 CVE patch, register-role start-at-task bugs, homepage rendering without `pg_cluster`, style tweaks.
