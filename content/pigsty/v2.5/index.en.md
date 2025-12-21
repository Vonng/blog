---
title: "Pigsty v2.5: Ubuntu & PG16"
linkTitle: "Pigsty v2.5 Release Notes"
date: 2023-10-24
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.5.0)）
summary: >
  Ubuntu/Debian joins the supported OS matrix, PG16 becomes the primary kernel, and new extensions plus monitoring updates keep rolling in.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.5.0

On 10/24 Pigsty 2.5 landed with full Ubuntu (20.04/22.04) and Debian (bullseye/bookworm) support. That means offline bundles, repo mirrors, and matching features for every major distro. PG16 replaces PG14 as the default major, and we now publish our own CDN (`repo.pigsty.cc`) for RPM/DEB packages.

New extensions include Hydra (columnar storage), PostgresML/Supabase/Postgres GraphQL updates, `pointcloud`, `imgsmlr`, `pg_similarity`, `pg_bigm`, and more. Monitoring picked up dedicated PGSQL Exporter/Patroni dashboards plus a redesigned PGSQL Query view built around the “DM/M/%M” methodology.

--------

## v2.5.0 Release Notes

- Ubuntu/Debian support with per-distro configs and offline bundles; Anolis OS compatibility added.
- CDN-backed package repos (`repo.pigsty.cc`), modular repo definitions, virtualenv + python3-pip defaults.
- Monitoring: new PGSQL Exporter & Patroni dashboards, PGSQL Query redesign.
- Extensions: PostGIS 3.4 (EL8/9), `pointcloud`, `imgsmlr`, `pg_similarity`, `pg_bigm`, Hydra column store, pg_embedding removed (use pgvector).
- Software: Grafana 10.1.5, Prometheus 2.47, Loki/Promtail 2.9.1, Node Exporter 1.6.1, Bytebase 2.10, Patroni 3.1.2, pgbouncer 1.21, pg_exporter 0.6, pgBackRest 2.48, pgbadger 12.2, pg_graphql 1.4, pg_net 0.7.3, FerretDB 0.12.1, SealOS 4.3.5, Supabase 20231013.
- Defaults updated for repo modules, package lists, `pg_libs` (timescaledb removed), `pg_extensions` (PG16-ready set), Patroni `wal_keep_size` removed.

## v2.5.1 Release Notes

- PostgreSQL 16.1 / 15.5 / 14.10 / 13.13 / 12.17 / 11.22, Patroni 3.2, pgBackRest 2.49, Citus 12.1, TimescaleDB 2.13, Grafana 10.2, FerretDB 1.15, SealOS 4.3.7, Bytebase 2.11.1.
- pgs up: PG16 extensions (pg_repack, timescaledb) now available, PGCAT filter cleaned up, new `wool.yml` template for tiny Alibaba ECS, EL9 adds `python3-jmespath` to satisfy Ansible.
