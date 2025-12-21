---
title: "Pigsty v3.1: Supabase Auto-Deploy + PG17"
linkTitle: "Pigsty v3.1 Release Notes"
date: 2024-11-24
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.1.0)）
summary: >
  PG17 becomes the default, Supabase can be spun up with one playbook, MinIO guidance improves, and ARM/Ubuntu 24 joins the supported list.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.1.0

Pigsty 3.1 catches the PG17 wave: 17.2 is now the default kernel across ~340 extensions. Supabase self-hosting is turnkey (`supabase.yml`), MinIO playbooks get best-practice defaults, ARM64 builds (EL9/Debian12/Ubuntu22) and Ubuntu 24.04 land, and configuration management is simplified via package aliases + per-distro var files.

--------

## v3.1.0 Release Notes

- Highlights: PG17 default, Ubuntu 24.04 support, initial ARM64 support (EL9/Debian12/Ubuntu22), Supabase one-click deploy, MinIO improvements, scenario templates, `configure --version` flag, default extensions = `pg_repack`, `wal2json`, `pgvector`, auto checksums, repo/package aliasing, WiltonDB/IvorySQL/PolarDB mirrors.
- Software: PostgreSQL 17.2/16.6/15.10/14.15/13.18/12.22, Patroni 4.0.4, MinIO Nov 2024, Rclone 1.68.2, Prometheus 3.0, VictoriaMetrics 1.106, VictoriaLogs 1.0, exporters (MySQL/Redis/Mongo/Keepalived) bumped, DuckDB 1.1.3, etcd 3.5.17, TigerBeetle 0.16.13.
- API: `repo_upstream` per distro, `repo_packages`/`repo_extra_packages` accept alias map, `pg_checksum` defaults true, `pg_packages` trimmed, `pg_extensions` default `[]`, `infra_portal` path override for offline repos.
