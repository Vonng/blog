---
title: "Pigsty v3.4: PITR Boost + Auto Certs"
linkTitle: "Pigsty v3.4 Release Notes"
date: 2025-03-15
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.4.0)）
summary: >
  pgBackRest backups get first-class monitoring + cross-cluster restores, certbot automation makes HTTPS trivial, IvorySQL/AGE go full-platform.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.4.0

Pigsty 3.4 focuses on ops pain points: PITR now works seamlessly across clusters (auto-generated `/pg/bin/pg-restore` picks backups from a central repo), pgBackRest exporter + dashboards ship by default, and certbot integration means `make cert` handles TLS for Odoo/Dify/Supabase templates. Locale best practices are enforced (default `C`/`C.UTF-8`), IvorySQL and Apache AGE get full support across EL/Deb/Ubuntu, and pgspider_ext joins the 405-extension catalog.

--------

## v3.4.0 Release Notes

- Highlights: cross-target PITR restore, pgBackRest monitoring/dashboard, optional certbot automation per Nginx server, locale defaults updated, IvorySQL & AGE RPM/DEB coverage, 28 extensions updated + `pgspider_ext` added.
- Infra: JuiceFS, Restic, Timescale EventStreamer added to repo; Docker/FerretDB2/DuckDB/restic/juicefs/grafana-infinity-ds now in default download set.
- Kernel updates: PolarDB, IvorySQL 4.4, Babelfish, Supabase templates, Citus 13.0.2.

## v3.4.1 Release Notes

- Maintenance refresh (per bottom section of Chinese note) continuing the backup/cert improvements, plus minor bug fixes.
