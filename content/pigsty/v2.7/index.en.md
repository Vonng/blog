---
title: "Pigsty v2.7: Extension Superpack"
linkTitle: "Pigsty v2.7 Release Notes"
date: 2024-05-21
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.7.0)）
summary: >
  255 PostgreSQL extensions ship out of the box, plus Docker templates for Odoo/Supabase/PolarDB and new PITR dashboards.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.7.0

Pigsty 2.7 celebrates PostgreSQL’s extensibility: 255 extensions are bundled, including ParadeDB’s `pg_search`/`pg_lakehouse`, Supabase’s `wrappers`/`pg_graphql`/`pg_jsonschema`, Tembo’s `pgmq`/`pg_tier`/`pg_vectorize`/`pg_later`, duckdb_fdw, pgsmcrypto, pg_tiktoken, parquet_s3_fdw, plv8, pg_tde, pg_dirtyread, md5hash, pg_idkit, plprql, pg_roaringbitmap, and more. pgvector 0.7 brings sparse vectors, half-precision, 4k dims, binary quantization, new distances, and SIMD.

Docker templates now cover Odoo, Jupyter, Supabase GA, PolarDB (for “Xinchuang” compliance), and more; arm64 packages exist for infra + pgsql modules. A PITR dashboard tracks restoration in real time, and guardrails prevent users from running playbooks on unmanaged hosts.

--------

## v2.7.0 Release Notes

- Feature roundup: massive extension drop (see list above), Docker templates (Odoo, Jupyter, PolarDB, Supabase, Bytebase latest, pg_exporter), arm64 builds, new installer fetching from Cloudflare, PITR observability, per-distro config files, Docker-ready groundwork.
- Software: PostgreSQL 16.3, Patroni 3.3, pgBackRest 2.51, VIP Manager 2.5, HAProxy 2.9.7, Grafana 10.4.2, Prometheus 2.51, Loki/Promtail 3.0 (breaking), Alertmanager 0.27, Blackbox 0.25, Node Exporter 1.8, pgBackRest exporter 0.17, DuckDB 0.10.2, etcd 3.5.13, MinIO May 2024, pev2 1.11, pgvector 0.7, pg_tle 1.4, hydra 1.1.2, pg_graphql 1.5.4, pg_net 0.9.1.
- Fixes & API: `node_write_etc_hosts` toggle, `prometheus_sd_dir`, `configure --proxy`, avoid Promtail label explosions, Alertmanager v2 API, PGSQL cert path `/pg/cert/ca.crt`, plus assorted bug fixes.
