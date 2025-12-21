---
title: "Pigsty v3.0: Pluggable Kernels & 340 Extensions"
linkTitle: "Pigsty v3.0 Release Notes"
date: 2024-08-25
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.0.0)）
summary: >
  340 extensions, EL/Deb parity, pluggable kernels (Babelfish/IvorySQL/PolarDB), Supabase on Debian, and a local-first RDS experience define Pigsty 3.0.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.0.0

Pigsty 3.0 is a major rev: 340 extensions ship across RPM + DEB, including cross-porting packages previously exclusive to EL or Debian. With Babelfish, IvorySQL, WiltonDB, PolarDB, Supabase, and FerretDB, you can swap the PG kernel to mimic SQL Server, Oracle, RAC, Firebase, or MongoDB while keeping Pigsty’s HA/IaC/PITR/observability stack.

A commercial Pigsty Pro tier debuts with MSSQL/Oracle/K8S/Victoria/Kafka/TigerBeetle modules, long-term support for older OSes, ported kernels, and tailor-made offline bundles. The default installer flow simplifies to `curl -> bootstrap -> configure -> install`.

--------

## Release Highlights

- 340 extensions covering analytics, FTS, GIS, vectors, OLAP, FDWs, audit/security, tooling, and convenience stacks (see list in the Chinese note); EL and Debian repos are now aligned.
- Supported kernels: PostgreSQL, Babelfish (SQL Server wire protocol), IvorySQL (Oracle compatibility), PolarDB (Oracle RAC flavor), Supabase GA (Debian), FerretDB (Mongo dialect).
- OS focus shifts to EL8/EL9/Debian12/Ubuntu22; EL7/Debian11/Ubuntu20 move into deprecated support. Offline bundles provided per OS/arch; Supabase now works on Debian.
- Bootstrap/configure scripts redesigned (`--conf`, `--proxy`, `--keep`), pgbouncer defaults set (`max_prepared_statements=128`, `server_lifetime=600`), Patroni templates get more workers/slots.
- Component upgrades: PostgreSQL 16.4/15.8/14.13/13.16/12.20, pg_exporter 0.7, Patroni 3.3.2, pgbouncer 1.23, pgBackRest 2.53, DuckDB 1.0, etcd 3.5.15, pg_timetable 5.9, FerretDB 1.23, VIP Manager 2.6, MinIO Aug 2024, Grafana 11.1, Loki 3.1, Prometheus 2.54, Pushgateway 1.9, Alertmanager 0.27, Blackbox 0.25, nginx_exporter 1.3.
