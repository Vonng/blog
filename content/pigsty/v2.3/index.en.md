---
title: "Pigsty v2.3: Richer App Ecosystem"
linkTitle: "Pigsty v2.3 Release Notes"
date: 2023-08-20
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.3.0)）
summary: >
  Postgres minor updates, Redis 7.2, NocoDB/FerretDB integrations, and keepalived-based node VIPs land in Pigsty 2.3.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.3.0

Pigsty 2.3 shipped alongside the August PG point releases (15.4/14.9/13.12/12.16/16 beta3) to patch CVE-2023-39417. Patroni 3.1.0 keeps HA in sync. The release doubles down on the app ecosystem: FerretDB turns Postgres into a MongoDB-compatible endpoint, NocoDB offers an Airtable-style UI, and Bytebase updates to 2.6.0. Operators get cluster-wide L2 VIPs via keepalived plus full monitoring coverage, so even HAProxy or MinIO frontends can be fully redundant.

Monitoring tweaks build on the v2.2 redesign: VIP pings surface prominently, PG dashboards include lock-wait graphs, Redis panels got a facelift, MinIO metrics match the latest releases, and MySQL/Mongo stubs pave the way for future modules.

--------

## v2.3.0 Release Notes

- VIP monitoring for nodes/PGSQL, L2 VIP option for node clusters.
- Security updates: PostgreSQL 15.4/14.9/13.12/12.16 + 16 beta3, Patroni 3.1.0.
- Pigsty RPM repos moved to HTTPS (`get.pigsty.cc`, `demo.pigsty.cc`).
- Apps: Bytebase 2.6.0, FerretDB 1.8, new NocoDB template.
- Redis upgraded to 7.2 with refreshed dashboards; FerretDB support; MySQL monitoring stubs.
- Node VIP API group adds eight parameters for keepalived config.

## v2.3.1 Release Notes

- pgvector 0.5 (HNSW), PostgreSQL 16 RC1 (EL8/EL9), SealOS bundle for one-command Kubernetes, TimescaleDB 2.11.2, Grafana 10.1, Loki/Promtail 2.8.4, Redis Stack 7.2, FerretDB 1.9, pgbadger 1.12.2.
- Fixes: repo download globbing, VIP DNS defaults, watchdog sudo permissions, bootstrap/wildcard repo issues, doc updates.
