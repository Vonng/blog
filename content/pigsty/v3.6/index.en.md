---
title: "Pigsty v3.6: The Ultimate PostgreSQL Distribution"
linkTitle: "Pigsty v3.6 Release"
date: 2025-07-25
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v3.6.0))
summary: >
  New doc site, PITR playbook, Percona PG TDE kernel support, and Supabase self-hosting optimization make v3.6 the last major release before 4.0.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.6.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v360)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.6.0)

Pigsty v3.6 is officially released. After two months of careful refinement, this will be the last major version before v4.0, featuring extensive refactoring and improvements that lay a solid foundation for building the ultimate all-in-one PostgreSQL distribution.

This version deeply optimizes and refactors deployment tasks for PostgreSQL, MinIO, and Etcd, adds **Percona PG TDE** kernel support with out-of-the-box transparent encryption functionality. Additionally, the Supabase self-hosting experience has been comprehensively optimized, destructive database operations have been completely removed from idempotent playbooks, and a new fully automated `pgsql-pitr` playbook enables one-click point-in-time recovery.

The installation process has been further simplified: from four steps to three steps (download, configure, install), now defaulting to online installation mode which skips local software repository construction.


--------

## New Kernel Support: Percona PG TDE

Percona's `pg_tde` extension has finally reached 1.0 GA after years of development. Many "enterprise-grade" PostgreSQL distributions tout "transparent encryption" as a core selling point — `pg_tde` may be the first mature enough open-source transparent encryption extension, providing truly enterprise-grade transparent encryption for open-source PostgreSQL.

![](percona-tde.jpg)

Currently, this extension requires running on a patched PostgreSQL kernel — Percona's Postgres distribution. Pigsty added support immediately after the announcement — just two commands to enable and install, while enjoying Pigsty's full RDS capabilities: monitoring, high availability, PITR, IaC, and more — identical to the vanilla PG kernel.

With this, the number of PostgreSQL kernels supported by Pigsty has reached **10**.

![](kernels.jpg)

Pigsty has become a distribution of PostgreSQL distributions — a "**meta-distribution**." Various PostgreSQL fork kernels can be transformed into "enterprise-grade database services" with high availability, monitoring, IaC, and PITR capabilities under Pigsty's umbrella.


--------

## Extension Ecosystem Continues to Strengthen

Besides the Percona transparent encryption kernel, OrioleDB also released 1.5 beta12 — Supabase's CEO revealed it's nearing official GA. Pigsty has immediately compiled the OrioleDB-patched version of PG and its extensions.

Another noteworthy extension is `pgactive` — an AWS-developed and open-sourced **PG multi-active extension** that claims to solve sub-second high availability failover. This extension depends on the missing `pgfeutils` and has compilation barriers — Pigsty provides out-of-the-box binary packages.

![](extensions.jpg)

Available extensions have reached **423**. PG18 beta2, OrioleDB, TimescaleDB, Citus, FerretDB & DocumentDB, DuckDB, Etcd, and more have completed routine version updates.

The extension catalog site has also been completely revamped using Next.js reconstruction, with significantly improved appearance. New address: [https://pgext.cloud](https://pgext.cloud)

![](ext-catalog.jpg)


--------

## Supabase Self-Hosting Experience Optimization

Pigsty v3.6 provides a smoother Supabase self-hosting experience and fixes several issues in Supabase's official templates:

- logflare replication slot not advancing
- Massive error log printing
- Studio unable to view two Analytics logs

Production-grade Supabase self-hosting requires just a few commands:

![](supabase.jpg)

Additionally, Pigsty now defaults to using Docker Registry mirror sites provided by 1Panel, significantly improving download speeds in mainland China.

Currently, Pigsty and StackGres are the only two open-source vendors providing Supabase self-hosting solutions: Pigsty delivers on bare Linux systems, StackGres delivers on Kubernetes.


--------

## PITR Recovery Enhancement

In previous versions, Pigsty provided the `pg-pitr` script for "semi-automatic" PITR recovery assistance. This version adds a fully automated `pgsql-pitr` playbook for one-click point-in-time recovery.

![](pitr.jpg)

This playbook automatically performs the following operations:

- Pause high availability failover
- Shut down PostgreSQL
- Generate and execute pgbackrest PITR recovery command to specified target point
- Verify and restart PostgreSQL
- Re-enable high availability failover

Supports fast retry (in-place incremental) for precise recovery point targeting. Also adds a new use case: performing PITR recovery on newly started instances (or detached replicas) to avoid affecting existing business, then extracting data from the new instance for manual import.


--------

## ETCD Management Simplified

This version refactors the Etcd module, adding independent `etcd-rm.yml` playbook and scaling SOP scripts.

Previously, scaling etcd involved a series of complex command operations — now just a few simple commands:

```bash
bin/etcd-add              # Create etcd cluster, or refresh existing cluster state
bin/etcd-add 10.10.10.11  # Scale out etcd cluster, add a new member
bin/etcd-rm               # Remove entire etcd cluster
bin/etcd-rm 10.10.10.11   # Remove specified member from cluster
```

The `etcd.yml` playbook **no longer cleans existing ETCD clusters** — cleanup is now handled by dedicated roles and playbooks, making maintenance simpler and clearer.


--------

## MinIO Module Improvements

The MinIO module has been refactored with a new Plain HTTP mode and adjusted default bucket and user configuration.

Previous versions enabled HTTPS for MinIO by default (via locally CA-signed self-signed certificates), avoiding intranet traffic snooping but causing some hassles: clients outside the Pigsty management node (like containers) need to trust that CA to access MinIO.

This version adds a switch allowing MinIO to run in pure HTTP mode. Note: pgbackrest doesn't accept HTTP-mode MinIO, so local MinIO storage for PG backups still requires HTTPS mode. HTTP mode is only suitable for pure external service scenarios.

![](minio.jpg)

Default bucket configuration has also been adjusted:

| Original Config | New Config |
|-------|-------|
| pgsql, infra, redis | pgsql, meta, data |

Dedicated users `s3user_meta` and `s3user_data` have been created for `meta` and `data` buckets, with same-named policies for each bucket. With this design, applications like Supabase and Dify can directly use these two buckets without manual creation.


--------

## Installation Process Simplified

Installation steps reduced from four to three:

| Original Flow | New Flow |
|-------|-------|
| Download → Bootstrap → Configure → Install | Download → Configure → Install |

The "bootstrap" step (extracting offline packages or configuring upstream repos to install Ansible) has been merged into the download script — running the install script automatically executes `./bootstrap`.

```bash
curl -fsSL https://repo.pigsty.io/get | bash; cd ~/pigsty; ./configure; ./install.yml
```

![](install-1.jpg)


--------

## Online Installation by Default

The default installation strategy has changed: instead of downloading locally first then installing, it now installs directly from upstream internet sources.

![](install-2.jpg)

This change brings significant benefits:

- **Fewer failure points**: Many user-reported installation errors occurred during local repo download and Nginx service startup phases (like el9.aarch64 patroni-etcd installation failure due to PGDG configuration errors)
- **Faster speed**: Only downloads packages that actually need to be installed, rather than downloading everything at once
- **Simpler configuration**: No need to handle Nginx security policies and firewall configuration issues

A large proportion of users install Pigsty on single-node Linux and "don't need" the multi-node consistency provided by local software repositories. Users who need local repos can re-enable via simple configuration (`repo_enabled`, `node_repo_modules`) or directly use the `rich` / `full` templates that enable local repos by default.


--------

## New Documentation Site

The new documentation site is now live: [https://doc.pgsty.com](https://doc.pgsty.com)

![](doc-site.jpg)

This site is built with Next.js and Fumadocs modern frontend stack — thanks to Lantian You and Claude Code for the strong assist. The English version is mostly complete; Chinese version is under translation. Contributions via GitHub PR or Issues are welcome.


--------

## Other Improvements

- **tuned module optimization**: Optimized for modern hardware and NVMe disks, removed outdated configuration parameters, added NVMe/virtualized SSD scheduling/readahead parameter optimizations
- **MCP Toolbox integration**: Integrated Google's newly released MCP Toolbox (database MCP toolbox), with preset template SQL solving some database security issues
- **Configuration template adjustments**: All configuration templates adjusted to **single-node** mode for quicker onboarding


--------

## Next Steps: v4.0 and DBA Agent

PostgreSQL 18 will be released in September — Pigsty plans to officially release v4.0 after PG 18's release. Main improvement directions:

| Area | Plan |
|-----|------|
| CLI Tool | pig fully wraps Ansible playbook functionality, interface preliminarily finalized |
| Monitoring System | VictoriaMetrics / VictoriaLogs replace Prometheus / Loki |
| Log Collection | vector replaces outdated promtail |
| Portal Component | Considering Caddy to replace Nginx (TBD) |

The main theme of v4.x will be **DBA Agent**. Pigsty already has the complete context needed for a DBA Agent — the core being this industry-leading PG monitoring system. Once the domain knowledge accumulated in documentation is rich enough, wrapping MCP around the Pig CLI tool will birth a capable fully self-driving database DBA Agent.

![](dba-agent.jpg)



--------
--------

## v3.6.0

Pigsty v3.6.0 released with new documentation site and PITR enhancement!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.6.0
```

### Highlights

- New documentation site: https://doc.pgsty.com
- Added `pgsql-pitr` playbook and backup/recovery tutorials, improved PITR experience
- New kernel support: Percona PG TDE (PG17)
- Optimized Supabase self-hosting experience, updated to latest version, resolved series of official template issues
- Simplified installation steps, defaults to online installation, more efficient and simple, bootstrap process (installing ansible) embedded in install script

### Design Improvements

- Improved Etcd module implementation, added independent `etcd-rm.yml` playbook and scaling SOP scripts
- Improved MinIO module implementation, supports HTTP mode, creates three buckets with different properties out-of-the-box
- Re-adjusted and organized all configuration templates for easier use
- Uses faster Docker Registry mirror sites for mainland China
- Optimized tuned OS parameter templates for modern hardware and NVMe disks
- Added `pgactive` extension for multi-master replication and sub-second failover
- Adjusted `pg_fs_main` / `pg_fs_backup` default values, simplified file directory structure design

### Bug Fixes

- Fixed pgbouncer config file error by @housei-zzy
- Fixed OrioleDB issues on Debian platform
- Fixed tuned shm config parameter issues
- Offline packages directly use PGDG source, avoiding out-of-sync mirror sites
- Fixed IvorySQL libxcrypt dependency issues
- Replaced broken and slow EPEL repository sites
- Fixed `haproxy_enabled` flag functionality

### Infrastructure Package Updates

New Victoria Metrics / Victoria Logs related packages:

- genai-toolbox 0.9.0 (new)
- victoriametrics 1.120.0 -> 1.121.0 (refactored)
- vmutils 1.121.0 (renamed victoria-metrics-utils)
- grafana-victoriametrics-ds 0.15.1 -> 0.17.0
- victorialogs 1.24.0 -> 1.25.1 (refactored)
- vslogcli 1.24.0 -> 1.25.1
- vlagent 1.25.1 (new)
- grafana-victorialogs-ds 0.16.3 -> 0.18.1
- prometheus 3.4.1 -> 3.5.0
- grafana 12.0.0 -> 12.0.2
- vector 0.47.0 -> 0.48.0
- grafana-infinity-ds 3.2.1 -> 3.3.0
- keepalived_exporter 1.7.0
- blackbox_exporter 0.26.0 -> 0.27.0
- redis_exporter 1.72.1 -> 1.77.0
- rclone 1.69.3 -> 1.70.3

### Database Package Updates

- PostgreSQL 18 Beta2 update
- pg_exporter 1.0.1, updated to latest dependencies with Docker image
- pig 0.6.0, updated latest extensions and repo list, with `pig install` subcommand
- vip-manager 3.0.0 -> 4.0.0
- ferretdb 2.2.0 -> 2.3.1
- dblab 0.32.0 -> 0.33.0
- duckdb 1.3.1 -> 1.3.2
- etcd 3.6.1 -> 3.6.3
- ferretdb 2.2.0 -> 2.4.0
- juicefs 1.2.3 -> 1.3.0
- tigerbeetle 0.16.41 -> 0.16.50
- pev2 1.15.0 -> 1.16.0

### PG Extension Package Updates

- OrioleDB 1.5 beta12
- OriolePG 17.11
- plv8 3.2.3 -> 3.2.4
- postgresql_anonymizer 2.1.1 -> 2.3.0
- pgvectorscale 0.7.1 -> 0.8.0
- wrappers 0.5.0 -> 0.5.3
- supautils 2.9.1 -> 2.10.0
- citus 13.0.3 -> 13.1.0
- timescaledb 2.20.0 -> 2.21.1
- vchord 0.3.0 -> [0.4.3](https://github.com/tensorchord/VectorChord/releases/tag/0.4.3)
- pgactive 2.1.5 (new)
- documentdb 0.103.0 -> 0.105.0
- pg_search 0.17.0


### API Changes

* `pg_fs_backup`: Renamed to `pg_fs_backup`, default value `/data/backups`.
* `pg_rm_bkup`: Renamed to `pg_rm_backup`, default value `true`.
* `pg_fs_main`: Default value now adjusted to `/data/postgres`.
* `nginx_cert_validity`: New parameter to control Nginx self-signed certificate validity period, default `397d`.
* `minio_buckets`: Default value adjusted to create three buckets named `pgsql`, `meta`, `data`.
* `minio_users`: Removed `dba` user, added `s3user_meta` and `s3user_data` users corresponding to `meta` and `data` buckets.
* `minio_https`: New parameter allowing MinIO to use HTTP mode.
* `minio_provision`: New parameter allowing skipping MinIO provisioning phase (skip bucket and user creation).
* `minio_safeguard`: New parameter that aborts operation when executing `minio-rm.yml` if enabled.
* `minio_rm_data`: New parameter controlling whether to delete minio data directory when executing `minio-rm.yml`.
* `minio_rm_pkg`: New parameter controlling whether to uninstall minio package when executing `minio-rm.yml`.
* `etcd_learner`: New parameter allowing etcd to initialize as learner.
* `etcd_rm_data`: New parameter controlling whether to delete etcd data directory when executing `etcd-rm.yml`.
* `etcd_rm_pkg`: New parameter controlling whether to uninstall etcd package when executing `etcd-rm.yml`.

### Checksums

```bash
df64ac0c2b5aab39dd29698a640daf2e  pigsty-v3.6.0.tgz
cea861e2b4ec7ff5318e1b3c30b470cb  pigsty-pkg-v3.6.0.d12.aarch64.tgz
2f253af87e19550057c0e7fca876d37c  pigsty-pkg-v3.6.0.d12.x86_64.tgz
0158145b9bbf0e4a120b8bfa8b44f857  pigsty-pkg-v3.6.0.el8.aarch64.tgz
07330d687d04d26e7d569c8755426c5a  pigsty-pkg-v3.6.0.el8.x86_64.tgz
311df5a342b39e3288ebb8d14d81e0d1  pigsty-pkg-v3.6.0.el9.aarch64.tgz
92aad54cc1822b06d3e04a870ae14e29  pigsty-pkg-v3.6.0.el9.x86_64.tgz
c4fadf1645c8bbe3e83d5a01497fa9ca  pigsty-pkg-v3.6.0.u22.aarch64.tgz
5477ed6be96f156a43acd740df8a9b9b  pigsty-pkg-v3.6.0.u22.x86_64.tgz
196169afc1be02f93fcc599d42d005ca  pigsty-pkg-v3.6.0.u24.aarch64.tgz
dbe5c1e8a242a62fe6f6e1f6e6b6c281  pigsty-pkg-v3.6.0.u24.x86_64.tgz
```


See [GitHub Release](https://github.com/pgsty/pigsty/releases/tag/v3.6.0) for more details.



--------

## v3.6.1

Pigsty v3.6.1 released with PostgreSQL minor version updates!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.6.1
```


### Highlights

- PostgreSQL 17.6, 16.10, 15.14, 14.19, 13.22, and 18 Beta 3 support
- Using Pigsty-provided PGDG APT/YUM mirrors in mainland China to resolve update supply issues
- New website homepage: https://pgsty.com
- Added el10, debian 13 implementation stubs, and el10 Terraform images


### Infrastructure Package Updates

- Grafana 12.1.0
- pg_exporter 1.0.2
- pig 0.6.1
- vector 0.49.0
- redis_exporter 1.75.0
- mongo_exporter 0.47.0
- victoriametrics 1.123.0
- victorialogs: 1.28.0
- grafana-victoriametrics-ds 0.18.3
- grafana-victorialogs-ds 0.19.3
- grafana-infinity-ds 3.4.1
- etcd 3.6.4
- ferretdb 2.5.0
- tigerbeetle 0.16.54
- genai-toolbox 0.12.0


### Database Package Updates

- pg_search 0.17.3

### API Changes

- Removed `br_filter` kernel module from `node_kernel_modules` default value.
- Uses OS major version number when adding PGDG YUM source, no longer uses minor version number.


### Checksums

```bash
045977aff647acbfa77f0df32d863739  pigsty-pkg-v3.6.1.d12.aarch64.tgz
636b15c2d87830f2353680732e1af9d2  pigsty-pkg-v3.6.1.d12.x86_64.tgz
700a9f6d0db9c686d371bf1c05b54221  pigsty-pkg-v3.6.1.el8.aarch64.tgz
2aff03f911dd7be363ba38a392b71a16  pigsty-pkg-v3.6.1.el8.x86_64.tgz
ce07261b02b02b36a307dab83e460437  pigsty-pkg-v3.6.1.el9.aarch64.tgz
d598d62a47bbba2e811059a53fe3b2b5  pigsty-pkg-v3.6.1.el9.x86_64.tgz
13fd68752e59f5fd2a9217e5bcad0acd  pigsty-pkg-v3.6.1.u22.aarch64.tgz
c25ccfb98840c01eb7a6e18803de55bb  pigsty-pkg-v3.6.1.u22.x86_64.tgz
0d71e58feebe5299df75610607bf448c  pigsty-pkg-v3.6.1.u24.aarch64.tgz
4fbbab1f8465166f494110c5ec448937  pigsty-pkg-v3.6.1.u24.x86_64.tgz
083d8680fa48e9fec3c3fcf481d25d2f  pigsty-v3.6.1.tgz
```


See [GitHub Release](https://github.com/pgsty/pigsty/releases/tag/v3.6.1) for more details.

--------
