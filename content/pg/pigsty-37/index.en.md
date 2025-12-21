---
title: Pigsty 3.7 – Magneto Award Edition
date: 2025-12-03
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Pigsty 3.7 ships PostgreSQL 18 as the default engine, adds Debian 13 + Enterprise Linux 10 (x86/ARM), expands to 437 extensions, and picks up the “PG Magneto” award.
tags: [PostgreSQL,Pigsty]
---

Pigsty v3.7.0 is out. Highlights:

- **PostgreSQL 18** as the default version (PG 13 enters sunset—v3.7 will be the last release supporting it).
- **New OS combos**: Debian 13 and EL10, both x86 and ARM, bringing the matrix to 14 supported distros.
- **437 extensions** packaged; Supabase/IvorySQL/PolarDB/Percona TDE kernels updated; Prometheus, Grafana, DuckDB, Etcd refreshed.
- Pigsty received the “PostgreSQL Magneto” award for extension ecosystem contributions.

## PG18 on top

PG 18 introduces temporal primary keys, UUID v7, index skip scans, async I/O, virtual generated columns, richer EXPLAIN, OAuth 2.0 auth. Pigsty 3.7 treats PG18 as production-ready. PG13.23 is its final minor release; Pigsty will drop PG13 after this version (all PG13 extensions were rebuilt one last time).

## Extension frenzy

Supporting PG18 wasn’t just swapping binaries. We needed the ecosystem: nearly every extension now builds for PG18 (Citus is the holdout). I patched dozens, updated 40 Rust extensions (pgrx bump), and coordinated major releases (pg_duckdb 1.1, pg_mooncake 0.2, vchord 1.0, pg_search 0.20). DuckDB integration is especially nice: pg_mooncake was rewritten in Rust and now coexists with pg_duckdb.

Expanding from 5 PG versions × 10 distros to 6 × 14 blows up the build matrix from 50 to 84 combos. Package count jumped from ~40k to ~60k. I spent two weeks automating the entire pipeline—now `pig build pkg <ext>` in a container handles dependency install, build, RPM/DEB output.

## New OS support

Debian 13 and EL10 each came with quirks (kernel params, SELinux policies, package naming). Pigsty 3.7 resolves them so you can deploy the same playbooks across the matrix. Supabase, IvorySQL, PolarDB, Percona TDE kernels were refreshed as well.

## Magneto award

At the 8th PostgreSQL Ecosystem Conference, Pigsty earned the “PostgreSQL Magneto” award for expanding the extension universe. Thanks to everyone using and contributing—you keep me grinding.
