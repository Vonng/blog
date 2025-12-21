---
title: "Pigsty v3.5: 4K Stars, PG18 Beta, 421 Extensions"
linkTitle: "Pigsty v3.5 Release"
date: 2025-06-22
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v3.5.0))
summary: >
  Pigsty crosses 4K GitHub stars, adds PG18 beta support, pushes extensions to 421, ships new doc site, and completes OrioleDB/OpenHalo full-platform support.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.5.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v350)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.5.0)

Pigsty v3.5 is officially released. The project has crossed the **4,000+ Star** milestone on GitHub — a remarkable achievement for a database infrastructure project.

![](4k-star.jpg)

This version brings a brand-new documentation website, full-platform support for OrioleDB and OpenHalo kernels, Supabase self-hosting optimizations, monitoring system and architecture improvements, PostgreSQL 18 Beta support, routine PG minor version updates, and Apple ARM Vagrant support.


--------

## What is Pigsty?

Pigsty is a batteries-included PostgreSQL distribution that works like "self-driving software" for databases. It enables users to spin up enterprise-grade PostgreSQL database services at less than one-tenth the cost of cloud RDS — without needing professional DBAs. Features include high availability, PITR, monitoring, IaC capabilities, and 421 PG ecosystem extensions, running directly on 10 major Linux distributions without containers or Kubernetes.

![](arch-1.jpg)

![](arch-2.jpg)


--------

## PostgreSQL 18 Support

PostgreSQL 18 Beta1 has been released, with the stable version coming in September. PG 18 brings powerful new features like AIO, OAuth, and more — now available for preview in Pigsty (not for production use). Routine minor version updates are also available for 17.5, 16.9, 15.13, 14.18, and 13.21.

![](pg18.jpg)

Pigsty provides a new `pg18` configuration template for spinning up highly available RDS based on the PostgreSQL 18 Beta1 kernel. [pg_exporter](https://github.com/pgsty/pg_exporter) has just released version 1.0, with complete coverage of PG 18's new monitoring metrics. Users can also use the `pig` package manager to install PG 18 and corresponding PGDG extensions with a single command.


--------

## Supabase Self-Hosting Improvements

Pigsty's "enterprise-grade" Supabase self-hosting capability has been well-received — the Supabase self-hosting tutorial page traffic even exceeds the landing page. This version further optimizes the Supabase self-hosting workflow.

![](supabase.jpg)

**pgsodium Key Management Integration**: You can now specify a root key or provide a key retrieval script for the pgsodium extension that Supabase depends on. This provides data encryption capabilities and can derive a series of subkeys from the root key.

**logflare Replication Slot Fix**: The Supabase Analytics logflare component has a defect — when system tables have no update writes, it doesn't update WAL consumption progress, causing replication slots to retain data indefinitely. Pigsty uses a pre-configured cron job `supa-kick` that executes a "fake update" every minute to trigger progress advancement, preventing disk exhaustion.

Supabase-related extension versions and Docker image versions have also been updated.


--------

## OpenHalo and OrioleDB Full-Platform Support

The [OpenHalo](https://github.com/HaloTech-Co-Ltd/openHalo) kernel provides MySQL compatibility on top of PG 14, while the [OrioleDB](https://github.com/orioledb/orioledb) kernel provides a cloud-native, bloat-free PostgreSQL version. In v3.4, only RPM packages were provided — now they're fully available across all ten supported Linux systems.

OrioleDB has been acquired by Supabase and recently released its 11th Beta version. Although it hasn't yet become Supabase's default PG kernel fork, Pigsty is prepared in advance — ensuring seamless follow-up once Supabase decides to switch from vanilla PG to OrioleDB.


--------

## 421 Extensions

Available extensions have reached **421**, with numerous extensions receiving version updates. Notable new extensions:

**pgsentinel**: An observability extension providing Oracle Active Session History-like functionality, recording statistics and wait events for each session. Details: https://pgsty.com/ext/pgsentinel

**spat**: An experimental extension providing a Redis-like interface in PG, achieving Redis-like performance using shared memory. Currently in Alpha stage — not for production use.

The new extension encyclopedia website is now live, more beautiful and comprehensive than the previous version:

![](ext-site.jpg)


--------

## New Documentation Site

The Pigsty documentation site has been rebuilt with Next.js, stepping from static page rendering into the modern frontend era. New site address: [https://pgsty.com](https://pgsty.com)

![](doc-site.jpg)

Not only has the form been completely renovated, but the content has been thoroughly rewritten and reorganized for version 3.5, with extensive outdated information cleaned up. Currently only available in English — Simplified Chinese support coming soon.


--------

## Architecture Optimization

Pigsty v3.5 deeply optimized the PGSQL implementation:

- Merged and reduced task count
- Fine-tuned available task tags
- Unified template file naming
- Optimized system and database parameter defaults for modern NVMe environments
- Adjusted role divisions

**Important Change**: The `pgsql.yml` playbook's database deletion functionality has been completely removed. Starting with v3.5, database deletion can only be performed through the dedicated `pgsql-rm.yml` playbook, eliminating the need for various "safety valves" and "safeguards."

Refactored PGSQL playbook tasks:

![](pgsql-tasks.jpg)

Refactored pgsql-rm.yml playbook tasks:

![](pgsql-rm-tasks.jpg)


--------

## CLI Improvements

The `pig` command-line tool adds a new `do` subcommand, which can replace the wrapper scripts in the original `pigsty/bin` directory, executing various tasks in a unified, standardized manner.

![](pig-cli.jpg)

Currently in pilot phase with API not yet finalized — documentation planned after a period of refinement.


--------

## Monitoring Improvements

Grafana 12.0 is released with numerous breaking changes, and the monitoring system has been improved accordingly.

Analysis was performed on AWR requirements from Oracle DBA users: most metrics are already provided by PG and Pigsty — the only exception being **wait events**.

![](wait-events.jpg)

The PG kernel itself only provides current active wait states, with no historical wait event records. This can only be achieved through extensions — both `pg_wait_sampling` and `pgsentinel` provide this functionality, and monitoring dashboards now support wait event analysis.


--------

## Apple Vagrant Support

Pigsty provides Vagrant/Terraform sandbox templates, allowing users to easily spin up required virtual machine resources locally or in the cloud. Previously, Vagrant/VirtualBox had various issues with Apple ARM architecture support — after retesting, the Vagrant + VirtualBox combination now runs smoothly on Apple Silicon.

![](vagrant.jpg)

While not all Vagrant Boxes provide ARM64 on VirtualBox support, the main EL9 and Ubuntu 24.04 are supported. This means users can smoothly spin up virtual machines and run Pigsty on Apple MacBook (whether Intel or M-series ARM architecture).


--------

## Future Plans

The next version may be v3.6 or v4.0. Pigsty v4.0 is expected to release alongside PostgreSQL 18's stable version (September).

**Planned improvements**:

| Area | Plan |
|-----|------|
| OS | Add EL 10 support, compile and package all extensions |
| Log Collection | Replace promtail with vector |
| Installation | Simplify to three steps (Install / Configure / Deploy) |
| License | Consider releasing an Apache-licensed lightweight version |

![](featured.jpg)



--------
--------

## v3.5.0

Pigsty v3.5.0 released with PostgreSQL 18 Beta support!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.5.0
```

--------

### Highlights

- PG 18 (Beta) support, extensions updated, total reaches 421
- OrioleDB and OpenHalo kernels available on all platforms
- Can use `pig do` subcommand instead of `bin` scripts
- Enhanced Supabase self-hosting, resolving legacy issues like replication lag and key distribution
- Code refactoring and architecture optimization, improved Postgres and Pgbouncer default parameters
- Updated Grafana 12, pg_exporter 1.0 and related plugins, renovated dashboards

--------

### PostgreSQL 18 Support

- PostgreSQL 18 support
- PG18 monitoring metrics via pg_exporter 1.0.0
- PG18 installation aliases via pig 0.4.1
- `pg18` configuration template provided

--------

### Code Refactoring

- PGSQL refactored, PG monitoring extracted as separate `pg_monitor` role, `clean` logic removed
- Redundant duplicate tasks removed, similar items merged, configuration streamlined. `dir/utils` task blocks removed
- All extensions now install to `extensions` schema by default (consistent with Supabase security practices)
- Template files renamed, all `.j2` suffixes removed
- `SET` commands added to clear `search_path` for all `monitor` functions in templates, following Supabase security best practices
- Adjusted pgbouncer default parameters, increased default connection pool size, set connection pool cleanup query
- Added `pgbouncer_ignore_param` parameter to configure list of parameters for pgbouncer to ignore
- Added `pg_key` task for generating server-side keys required by `pgsodium`
- `sync_replication_slots` enabled by default for PG 17
- Sub-task tags re-adjusted to better match configuration section divisions

--------

### Module Refactoring

- `pg_remove` module refactored
  - Parameters renamed: `pg_rm_data`, `pg_rm_bkup`, `pg_rm_pkg` to control what gets deleted
  - Role code structure re-adjusted with clearer tag divisions
- New `pg_monitor` module added
  - `pgbouncer_exporter` no longer shares config file with `pg_exporter`
  - Added monitoring metrics for TimescaleDB, Citus, pg_wait_event
  - Uses `pg_exporter` 1.0.0, updated PG16/17/18 related monitoring metrics
  - Uses more compact, newly designed metric collector configuration files

--------

### Supabase Enhancements

Thanks to contributions from [@lawso017](https://github.com/lawso017)!

- Updated Supabase container images and database schemas to latest versions
- Now supports `pgsodium` server-side key loading by default
- Resolved logflare replication progress update issues via supa-kick cron job
- Added `set search_path` clause to functions in monitor schema for security best practices

--------

### CLI and Monitoring Updates

- CLI adds `pig do` command, allowing command-line tool to replace shell scripts in `bin/`
- Updated Grafana major version to 12.0.0, updated related plugin/datasource packages
- Updated Postgres datasource uid naming convention (to adapt to new `uid` length and character restrictions)
- Added Static Datasource
- Updated existing dashboards, fixed various legacy issues

--------

### Infrastructure Package Updates

- pig 0.4.2
- duckdb 1.3.0
- etcd 3.6.0
- vector 0.47.0
- minio 20250422221226
- mcli 20250416181326
- pev 1.5.0
- rclone 1.69.3
- mtail 3.0.8 (new)

--------

### Observability Package Updates

- grafana 12.0.0
- grafana-victorialogs-ds 0.16.3
- grafana-victoriametrics-ds 0.15.1
- grafana-infinity-ds 3.2.1
- grafana_plugins 12.0.0
- prometheus 3.4.0
- pushgateway 1.11.1
- nginx_exporter 1.4.2
- pg_exporter [1.0.0](https://github.com/pgsty/pg_exporter/releases/tag/v1.0.0)
- pgbackrest_exporter 0.20.0
- redis_exporter 1.72.1
- keepalived_exporter 1.6.2
- victoriametrics 1.117.1
- victoria_logs 1.22.2

--------

### Database Package Updates

- PostgreSQL 17.5, 16.9, 15.13, 14.18, 13.21
- PostgreSQL 18beta1 support
- pgbouncer 1.24.1
- pgbackrest 2.55
- pgbadger 13.1

--------

### PG Extension Package Updates

- spat [0.1.0a4](https://github.com/Florents-Tselai/spat) new extension
- pgsentinel [1.1.0](https://github.com/pgsentinel/pgsentinel/releases/tag/v1.1.0) new extension
- pgdd [0.6.0](https://github.com/rustprooflabs/pgdd) (pgrx 0.14.1) new extension
- convert [0.0.4](https://github.com/rustprooflabs/convert) (pgrx 0.14.1) new extension
- pg_tokenizer.rs [0.1.0](https://github.com/tensorchord/pg_tokenizer.rs) (pgrx 0.13.1)
- pg_render [0.1.2](https://github.com/mkaski/pg_render) (pgrx 0.12.8)
- pgx_ulid [0.2.0](https://github.com/pksunkara/pgx_ulid) (pgrx 0.12.7)
- pg_idkit [0.3.0](https://github.com/VADOSWARE/pg_idkit) (pgrx 0.14.1)
- pg_ivm [1.11.0](https://github.com/sraoss/pg_ivm)
- orioledb [1.4.0 beta11](https://github.com/orioledb/orioledb) added debian/ubuntu support
- openhalo [14.10](https://github.com/HaloTech-Co-Ltd/openHalo) added debian/ubuntu support
- omnigres 20250507 (latest version build failed on d12/u22)
- citus [12.0.3](https://github.com/citusdata/citus/releases/tag/v13.0.3)
- timescaledb [2.20.0](https://github.com/timescale/timescaledb/releases/tag/2.20.0) (removed PG14 support)
- supautils [2.9.2](https://github.com/supabase/supautils/releases/tag/v2.9.2)
- pg_envvar [1.0.1](https://github.com/theory/pg-envvar/releases/tag/v1.0.1)
- pgcollection [1.0.0](https://github.com/aws/pgcollection/releases/tag/v1.0.0)
- aggs_for_vecs [1.4.0](https://github.com/pjungwir/aggs_for_vecs/releases/tag/1.4.0)
- pg_tracing [0.1.3](https://github.com/DataDog/pg_tracing/releases/tag/v0.1.3)
- pgmq [1.5.1](https://github.com/pgmq/pgmq/releases/tag/v1.5.1)
- tzf-pg [0.2.0](https://github.com/ringsaturn/tzf-pg/releases/tag/v0.2.0) (pgrx 0.14.1)
- pg_search [0.15.18](https://github.com/paradedb/paradedb/releases/tag/v0.15.18) (pgrx 0.14.1)
- anon [2.1.1](https://gitlab.com/dalibo/postgresql_anonymizer/-/tree/latest/debian?ref_type=heads) (pgrx 0.14.1)
- pg_parquet [0.4.0](https://github.com/CrunchyData/pg_parquet/releases/tag/v0.3.2) (0.14.1)
- pg_cardano [1.0.5](https://github.com/Fell-x27/pg_cardano/commits/master/) (pgrx 0.12) -> 0.14.1
- pglite_fusion [0.0.5](https://github.com/frectonz/pglite-fusion/releases/tag/v0.0.5) (pgrx 0.12.8) -> 14.1
- vchord_bm25 [0.2.1](https://github.com/tensorchord/VectorChord-bm25/releases/tag/0.2.1) (pgrx 0.13.1)
- vchord [0.3.0](https://github.com/tensorchord/VectorChord/releases/tag/0.3.0) (pgrx 0.13.1)
- pg_vectorize [0.22.1](https://github.com/ChuckHend/pg_vectorize/releases/tag/v0.22.1) (pgrx 0.13.1)
- wrappers [0.4.6](https://github.com/supabase/wrappers/releases/tag/v0.4.6) (pgrx 0.12.9)
- timescaledb-toolkit [1.21.0](https://github.com/timescale/timescaledb-toolkit/releases/tag/1.21.0) (pgrx 0.12.9)
- pgvectorscale [0.7.1](https://github.com/timescale/pgvectorscale/releases/tag/0.7.1) (pgrx 0.12.9)
- pg_session_jwt [0.3.1](https://github.com/neondatabase/pg_session_jwt/releases/tag/v0.3.1) (pgrx 0.12.6) -> 0.12.9
- pg_timetable 5.13.0
- ferretdb 2.2.0
- documentdb [0.103.0](https://github.com/FerretDB/documentdb/releases/tag/v0.103.0-ferretdb-2.2.0) (added aarch64 support)
- pgml [2.10.0](https://github.com/postgresml/postgresml/releases/tag/v2.10.0) (pgrx 0.12.9)
- sqlite_fdw [2.5.0](https://github.com/pgspider/sqlite_fdw/releases/tag/v2.5.0) (fix pg17 deb)
- tzf [0.2.2](https://github.com/ringsaturn/pg-tzf/releases/tag/v0.2.2) 0.14.1 (rename src)
- pg_vectorize [0.22.2](https://github.com/ChuckHend/pg_vectorize/releases/tag/v0.22.2) (pgrx 0.13.1)
- wrappers [0.5.0](https://github.com/supabase/wrappers/releases/tag/v0.5.0) (pgrx 0.12.9)

--------

### Checksums

```bash
ab91bc05c54b88c455bf66533c1d8d43  pigsty-v3.5.0.tgz
4c9fabc2d1f0ed733145af2b6aff2f48  pigsty-pkg-v3.5.0.d12.x86_64.tgz
796d47de12673b2eb9882e527c3b6ba0  pigsty-pkg-v3.5.0.el8.x86_64.tgz
a53ef2cede1363f11e9faaaa43718fdc  pigsty-pkg-v3.5.0.el9.x86_64.tgz
36da28f97a845fdc0b7bbde2d3812a67  pigsty-pkg-v3.5.0.u22.x86_64.tgz
8551b3e04b38af382163e6857778437d  pigsty-pkg-v3.5.0.u24.x86_64.tgz
```

--------

See [GitHub Release](https://github.com/pgsty/pigsty/releases/tag/v3.5.0) for more details.
