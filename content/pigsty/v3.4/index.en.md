---
title: "Pigsty v3.4: PITR Enhancement, Locale Best Practices, Auto Certificates"
linkTitle: "Pigsty v3.4 Release"
date: 2025-03-15
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v3.4.0))
summary: >
  Pigsty v3.4 adds pgBackRest backup monitoring, cross-cluster PITR restore, automated HTTPS certificates, locale best practices, and full-platform IvorySQL and Apache AGE support.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.4.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v340)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.4.0)

After a month of intensive development, Pigsty v3.4 is officially released. This version features significant architectural optimizations, addressing several core concerns highly valued by users and customers:

- Restore physical backup PITR from one cluster to another
- Monitoring metrics and dashboards for pgBackRest backup component
- Auto-apply HTTPS certificates when deploying applications
- Best practices for locale collation and character sets
- Oracle-compatible IvorySQL now available on all platforms
- Graph database extension Apache AGE now available on all platforms

Additionally, a new value proposition/feature introduction page was built using Cursor Vibe Coding: https://pigsty.cc/about/values/

![](values.jpg)


--------

## Auto Certificate Issuance

Many users use Pigsty for self-hosting Dify, Odoo, Supabase. User feedback indicated certificate issuance was cumbersome, requiring manual `certbot` calls, with requests to automate it.

![](certbot.jpg)

This version enhances Nginx configuration: when users define a `certbot` field on an Nginx Server, the `make cert` command completes certificate issuance and application in one step — no additional configuration or commands needed.

The Dify, Odoo, Supabase self-hosting templates all use this feature. After installation, `make cert` automatically updates or issues needed certificates. If `certbot_sign` = `true`, certificates are automatically issued during installation.

![](nginx-config.jpg)

v3.4 offers richer Nginx configuration options: use `config` to inject nginx config, use `enforce` to force HTTPS redirect. Self-hosted websites can now completely avoid touching traditional Nginx config files in most scenarios.


--------

## Locale Collation Best Practices

Many programmers aren't familiar with Locale/Collation rules, but this is actually an important configuration. Using improper Collation can not only cause several times performance loss but also lead to data inconsistency or even data loss — indexes are closely tied to collation rules. Collation is far from trivial.

Recommended reading:
- [Locale Collation in PG](https://pigsty.cc/blog/pg/collation/)
- PGCon.Dev 2024: [Collations from A to Z](https://www.pgcon.org/events/pgcondev2024/schedule/session/630/)

![](collation.jpg)

**Best Practice**: Always use `C` or `C.UTF-8` as Locale collation.

- **`C`**: Best compatibility, supported on all systems, but lacks Unicode character set knowledge — case functions fail for non-ASCII characters
- **`C.UTF-8`**: Adds Unicode semantics on top of `C`, more intuitive for users, but not supported by default on all systems
- **PostgreSQL 17 new feature**: Built-in support for both collations, no longer dependent on OS libc

Pigsty v3.4 reflects this best practice:

- All Locale-related parameters default to `C` (mainly `pg_lc_ctypes` changed from `en_US.UTF-8` to `C`), ensuring it runs on any system
- During auto-configuration, if PG >= 17 or system clearly supports `C.utf8`, Locale is configured as `C.UTF-8` for better Unicode semantics

Unless your database works intensively with specific language sorting scenarios, this default is best practice. You can specify other collation rules on queries/indexes/columns using PostgreSQL COLLATION syntax — PG + ICU supports 841 collation rules.


--------

## Point-in-Time Recovery Enhancement

Point-in-time recovery is a core feature of relational databases. Previously, Pigsty helped users perform semi-automatic PITR through `pg-pitr`. v3.4 significantly improves PITR support, now allowing easy selection of any backup from a centralized backup repository for restoration.

When defining `pg_pitr` parameter on a PG cluster, Pigsty auto-generates the `/pg/bin/pg-restore` command and `/pg/conf/pitr.conf` config file.

![](pitr-1.jpg)

When executing `pg-restore`, Pigsty automatically pauses the Patroni cluster, shuts down PG, begins in-place incremental PITR, and restarts PG after recovering to the specified point. Important improvement: when using a centralized backup repository, you can use another cluster's backup to overwrite the current cluster.

![](pitr-2.jpg)

For backup monitoring, v3.4 introduces `pgbackrest_exporter` to collect backup monitoring metrics, and the PGSQL PITR dashboard now displays current backup status. Previously, users could only query current status through PGCAT Instance with no history — this improvement greatly helps analyze backup status.


--------

## Extension Updates

After a year of continuous extension ecosystem expansion, Pigsty has now collected nearly all mainstream PG ecosystem extensions, reaching **405**. The explosive extension growth phase is essentially complete; recent versions shift focus back to architecture and infrastructure, with extensions mainly consolidating.

![](extensions.jpg)

v3.4 adds extension `pgspider_ext` for multi-data-source queries using various FDWs. Additionally, 28 extensions updated to latest versions with several version and bug fixes.

**Apache AGE Graph Database Extension**: The project's developers seem to have been laid off, and it's essentially in maintenance limbo. As a distribution, Pigsty does its best to provide support — we recompiled AGE 1.5.0 for PG 13-17 based on Debian patches, filling the gap of missing EL RPMs.

![](age.jpg)


--------

## Multi-Kernel Support Updates

Pigsty v3.4 updates support for the latest versions of PolarDB, IvorySQL, and Babelfish.

Following PolarDB, **IvorySQL** becomes the second PostgreSQL kernel available on all platforms across Pigsty's supported ten Linux distributions. Except for extension plugins, IvorySQL 4.4 experience is basically identical to PostgreSQL 17.4.

To use IvorySQL (Oracle compatibility mode), just modify four parameters:

```yaml
pg_mode: ivory                                                 # Use IvorySQL compatibility mode
pg_packages: [ ivorysql, pgsql-common ]                        # Install IvorySQL packages
pg_libs: 'liboracle_parser, pg_stat_statements, auto_explain'  # Load Oracle compatibility extensions
repo_extra_packages: [ ivorysql ]                              # Download IvorySQL packages
```

![](polardb.jpg)

![](kernels.jpg)

Also updated Supabase template to latest version, updated Citus to 13.0.2. Next steps will focus on OrioleDB (OLTP performance-focused) and OpenHalo (MySQL protocol compatibility) kernels.


--------

## Infrastructure Enhancements

v3.4 updates many Infra package versions, adding new components:

| Component | Description |
|-----|------|
| JuiceFS | Mount S3/MinIO as local filesystem |
| Restic | Similar to pgBackRest but for file backup |
| TimescaleDB EventStreamer | Extract data change streams from TimescaleDB hypertables |

![](infra.jpg)

These components are now downloaded by default and ready to install.

Another change: the following packages added to default download list:

```
docker-ce docker-compose-plugin ferretdb2 duckdb restic juicefs vray grafana-infinity-ds
```

Docker usage is indeed high, mainly for running pgAdmin and similar software, so it's now in the default download.


--------

## v3.5 Feature Preview

v3.5 planned features:

| Area | Plan |
|-----|------|
| CLI | `pig` CLI fully wrapping Pigsty Playbooks |
| Config | Vibe Config Wizard and MCP Server |
| Docker | Debian 12 x86/ARM Pigsty Docker image |
| Kernel | OrioleDB and OpenHalo support |



--------

## v3.4.0 Release Notes

Pigsty v3.4.0 released — MySQL compatibility and comprehensive enhancements!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.4.0
```

### New Features

- Added new pgBackRest backup monitoring metrics and dashboards
- Enhanced Nginx server config options with auto Certbot signing support
- Now prioritizes PostgreSQL built-in `C`/`C.UTF-8` locale
- IvorySQL 4.4 now fully supported on all platforms (RPM/DEB on x86/ARM)
- Added new packages: Juicefs, Restic, TimescaleDB EventStreamer
- Apache AGE graph database extension now fully supported on EL for PostgreSQL 13–17
- Improved `app.yml` playbook: launch standard Docker apps without extra config
- Upgraded Supabase, Dify, and Odoo app templates to latest versions
- Added electric app template, local-first PostgreSQL sync engine

### Infrastructure Packages

- **+restic** 0.17.3
- **+juicefs** 1.2.3
- **+timescaledb-event-streamer** 0.12.0
- **Prometheus** 3.2.1
- **AlertManager** 0.28.1
- **blackbox_exporter** 0.26.0
- **node_exporter** 1.9.0
- **mysqld_exporter** 0.17.2
- **kafka_exporter** 1.9.0
- **redis_exporter** 1.69.0
- **pgbackrest_exporter** 0.19.0-2
- **DuckDB** 1.2.1
- **etcd** 3.5.20
- **FerretDB** 2.0.0
- **tigerbeetle** 0.16.31
- **vector** 0.45.0
- **VictoriaMetrics** 1.113.0
- **VictoriaLogs** 1.17.0
- **rclone** 1.69.1
- **pev2** 1.14.0
- **grafana-victorialogs-ds** 0.16.0
- **grafana-victoriametrics-ds** 0.14.0
- **grafana-infinity-ds** 3.0.0

### PostgreSQL Related

- **Patroni** 4.0.5
- **PolarDB** 15.12.3.0-e1e6d85b
- **IvorySQL** 4.4
- **pgbackrest** 2.54.2
- **pev2** 1.14
- **WiltonDB** 13.17

### PostgreSQL Extensions

- **pgspider_ext** 1.3.0 (new extension)
- **apache age** 13–17 el rpm (1.5.0)
- **timescaledb** 2.18.2 → 2.19.0
- **citus** 13.0.1 → 13.0.2
- **documentdb** 1.101-0 → 1.102-0
- **pg_analytics** 0.3.4 → 0.3.7
- **pg_search** 0.15.2 → 0.15.8
- **pg_ivm** 1.9 → 1.10
- **emaj** 4.4.0 → 4.6.0
- **pgsql_tweaks** 0.10.0 → 0.11.0
- **pgvectorscale** 0.4.0 → 0.6.0 (pgrx 0.12.5)
- **pg_session_jwt** 0.1.2 → 0.2.0 (pgrx 0.12.6)
- **wrappers** 0.4.4 → 0.4.5 (pgrx 0.12.9)
- **pg_parquet** 0.2.0 → 0.3.1 (pgrx 0.13.1)
- **vchord** 0.2.1 → 0.2.2 (pgrx 0.13.1)
- **pg_tle** 1.2.0 → 1.5.0
- **supautils** 2.5.0 → 2.6.0
- **sslutils** 1.3 → 1.4
- **pg_profile** 4.7 → 4.8
- **pg_snakeoil** 1.3 → 1.4
- **pg_jsonschema** 0.3.2 → 0.3.3
- **pg_incremental** 1.1.1 → 1.2.0
- **pg_stat_monitor** 2.1.0 → 2.1.1

### API Changes

- Added new Docker parameters: `docker_data` and `docker_storage_driver` ([#521](https://github.com/pgsty/pigsty/pull/521) by [@waitingsong](https://github.com/waitingsong))
- Added new infra parameter: `alertmanager_port` to specify AlertManager port
- Added new infra parameter: `certbot_sign` for certificate issuance during nginx init (default false)
- Added new infra parameter: `certbot_email` for email used when requesting certificates via Certbot
- Added new infra parameter: `certbot_options` for additional Certbot parameters
- Updated IvorySQL: starting from IvorySQL 4.4, default binaries placed under `/usr/ivory-4`
- Changed `pg_lc_ctype` and other locale-related parameter defaults from `en_US.UTF-8` to `C`
- For PostgreSQL 17 with `UTF8` encoding and `C` or `C.UTF-8` locale, PostgreSQL's built-in locale rules now take priority
- `configure` auto-detects if PG version and environment both support `C.utf8` and adjusts locale options accordingly
- Set default IvorySQL binary path to `/usr/ivory-4`
- Updated `pg_packages` default to `pgsql-main patroni pgbouncer pgbackrest pg_exporter pgbadger vip-manager`
- Updated `repo_packages` default to `[node-bootstrap, infra-package, infra-addons, node-package1, node-package2, pgsql-utility, extra-modules]`
- Removed `LANG` and `LC_ALL` environment variable settings from `/etc/profile.d/node.sh`
- Now using `bento/rockylinux-8` and `bento/rockylinux-9` as EL Vagrant box images
- Added new alias `extra_modules` containing additional optional modules
- Updated PostgreSQL aliases: `postgresql`, `pgsql-main`, `pgsql-core`, `pgsql-full`
- GitLab repo now included in available modules
- Docker module merged into infrastructure module
- `node.yml` playbook now includes `node_pip` task for configuring pip mirrors on each node
- `pgsql.yml` playbook now includes `pgbackrest_exporter` task for collecting backup metrics
- `Makefile` now allows using `META`/`PKG` environment variables
- Added `/pg/spool` directory as pgBackRest temporary storage
- Disabled pgBackRest `link-all` option by default
- Enabled block-level incremental backup for MinIO repos by default

### Bug Fixes

- Fixed exit status code in `pg-backup` ([#532](https://github.com/pgsty/pigsty/pull/532) by [@waitingsong](https://github.com/waitingsong))
- In `pg-tune-hugepage`, limit PostgreSQL to use only huge pages ([#527](https://github.com/pgsty/pigsty/pull/527) by [@waitingsong](https://github.com/waitingsong))
- Fixed logic error in `pg-role` task
- Corrected type conversion for huge page config parameters
- Fixed default value issue for `node_repo_modules` in `slim` template

### Checksums

```bash
768bea3bfc5d492f4c033cb019a81d3a  pigsty-v3.4.0.tgz
7c3d47ef488a9c7961ca6579dc9543d6  pigsty-pkg-v3.4.0.d12.aarch64.tgz
b5d76aefb1e1caa7890b3a37f6a14ea5  pigsty-pkg-v3.4.0.d12.x86_64.tgz
42dacf2f544ca9a02148aeea91f3153a  pigsty-pkg-v3.4.0.el8.aarch64.tgz
d0a694f6cd6a7f2111b0971a60c49ad0  pigsty-pkg-v3.4.0.el8.x86_64.tgz
7caa82254c1b0750e89f78a54bf065f8  pigsty-pkg-v3.4.0.el9.aarch64.tgz
8f817e5fad708b20ee217eb2e12b99cb  pigsty-pkg-v3.4.0.el9.x86_64.tgz
8b2fcaa6ef6fd8d2726f6eafbb488aaf  pigsty-pkg-v3.4.0.u22.aarch64.tgz
83291db7871557566ab6524beb792636  pigsty-pkg-v3.4.0.u22.x86_64.tgz
c927238f0343cde82a4a9ab230ecd2ac  pigsty-pkg-v3.4.0.u24.aarch64.tgz
14cbcb90693ed5de8116648a1f2c3e34  pigsty-pkg-v3.4.0.u24.x86_64.tgz
```


--------

## v3.4.1 Release Notes

Pigsty v3.4.1 released — OpenHalo and OrioleDB kernel support!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.4.1
```

### Highlights

- Added support for MySQL protocol-compatible PostgreSQL kernel on EL: [openHalo](https://pigsty.cc/docs/pgsql/kernel/openhalo)
- Added support for OLTP-enhanced PostgreSQL kernel on EL: [orioledb](https://pigsty.cc/docs/pgsql/kernel/orioledb)
- Optimized pgAdmin 9.2 app template with auto server list update and pgpass password filling
- Increased PG default max connections to 250, 500, 1000
- Removed `mysql_fdw` extension with dependency errors from EL8

### Infrastructure Updates

- pig 0.3.4
- etcd 3.5.21
- restic 0.18.0
- ferretdb 2.1.0
- tigerbeetle 0.16.34
- pg_exporter 0.8.1
- node_exporter 1.9.1
- grafana 11.6.0
- zfs_exporter 3.8.1
- mongodb_exporter 0.44.0
- victoriametrics 1.114.0
- minio 20250403145628
- mcli 20250403170756

### Extension Updates

- pg_search upgraded to 0.15.13
- citus upgraded to 13.0.3
- timescaledb upgraded to 2.19.1
- pgcollection RPM upgraded to 1.0.0
- pg_vectorize RPM upgraded to 0.22.1
- pglite_fusion RPM upgraded to 0.0.4
- aggs_for_vecs RPM upgraded to 1.4.0
- pg_tracing RPM upgraded to 0.1.3
- pgmq RPM upgraded to 1.5.1

### Checksums

```bash
471c82e5f050510bd3cc04d61f098560  pigsty-v3.4.1.tgz
4ce17cc1b549cf8bd22686646b1c33d2  pigsty-pkg-v3.4.1.d12.aarch64.tgz
c80391c6f93c9f4cad8079698e910972  pigsty-pkg-v3.4.1.d12.x86_64.tgz
811bf89d1087512a4f8801242ca8bed5  pigsty-pkg-v3.4.1.el9.x86_64.tgz
9fe2e6482b14a3e60863eeae64a78945  pigsty-pkg-v3.4.1.u22.x86_64.tgz
```

See [GitHub Release](https://github.com/pgsty/pigsty/releases/tag/v3.4.1) for more details.
