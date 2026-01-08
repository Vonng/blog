---
title: "Pigsty v4.0: Victoria Stack + Security Hardening"
linkTitle: "Pigsty v4.0 Release"
date: 2025-12-19
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v4.0.0))
summary: >
  VictoriaMetrics/Logs replace Prometheus/Loki for 10x observability performance, Vector handles logs, unified UI, firewall/SELinux/credential hardening.
series: [Pigsty]
tags: [Pigsty]
---


**Release Date: 2026-01-07** | [GitHub](https://github.com/pgsty/pigsty/releases/tag/v4.0.0-c1) | [Docs EN](https://pigsty.io) | [Docs CN](https://pigsty.cc)

```bash
curl https://pigsty.cc/get | bash
```

**244 commits**, 554 files changed, +94,508 / -41,374 lines

---

## Highlights

- **Observability Revolution**: Prometheus → VictoriaMetrics (10x perf), Loki+Promtail → VictoriaLogs+Vector
- **Security Hardening**: Auto-generated passwords, etcd RBAC, firewall/SELinux modes, permission tightening
- **Database Management**: `pg_databases` state (create/absent/recreate), instant clone with `strategy`
- **PITR & Fork**: `/pg/bin/pg-fork` for instant CoW cloning, enhanced `pg-pitr` with pre-backup
- **Multi-Cloud Terraform**: AWS, Azure, GCP, Hetzner, DigitalOcean, Linode, Vultr, TencentCloud templates
- **AI Agent**: Add support for claude code, opencode and uv
- **License**: AGPL-3.0 → Apache-2.0

---

## Software Versions

### Infrastructure

| Package | Version | Package | Version |
|---------|---------|---------|---------|
| grafana | 12.3.1 | victoria-metrics | 1.132.0 |
| victoria-logs | 1.43.1 | vector | 0.52.0 |
| alertmanager | 0.30.0 | blackbox_exporter | 0.28.0 |
| etcd | 3.6.7 | duckdb | 1.4.3 |
| pg_exporter | 1.1.1 | pgbackrest_exporter | 0.22.0 |
| minio | 20251203 | pig | 0.9.0 |
| uv | 0.9.18 (**new**) | opencode | 1.0.223 (**new**) |

### PostgreSQL Extensions

**New**: [pg_textsearch](https://github.com/timescale/pg_textsearch) 0.1.0, [pg_clickhouse](https://github.com/clickhouse/pg_clickhouse/) 0.1.0, [pg_ai_query](https://github.com/benodiwal/pg_ai_query) 0.1.1

**Updated**: IvorySQL 5.1, timescaledb 2.24.0, pg_search 0.20.4, pg_duckdb 1.1.1, pg_biscuit 2.0.1, pg_anon 2.5.1, pg_enigma 0.5.0, pg_session_jwt 0.4.0, pg_vectorize 0.26.0, vchord_bm25 0.3.0, wrappers 0.5.7

**PG18 Deb Fixes**: pg_vectorize, pg_tiktoken, pg_tzf, pglite_fusion, pgsmcrypto, pgx_ulid, plprql, pg_summarize, supautils

---

## Breaking Changes

### Observability Stack

| Before | After |
|--------|-------|
| Prometheus | VictoriaMetrics |
| Loki | VictoriaLogs |
| Promtail | Vector |

### Parameters

| Removed | Replacement |
|---------|-------------|
| `node_disable_firewall` | `node_firewall_mode` (off/none/zone) |
| `node_disable_selinux` | `node_selinux_mode` (disabled/permissive/enforcing) |
| `pg_pwd_enc` | removed |
| `infra_pip` | `infra_uv` |

### Defaults Changed

| Parameter | Before → After |
|-----------|----------------|
| `grafana_clean` | true → false |
| `effective_io_concurrency` | 1000 → 200 |
| `install.yml` | renamed to `deploy.yml` (symlink kept) |

---

## Observability

- Using the new VictoriaMetrics to replace Prometheus — achieving several times the performance with a fraction of the resources.
- Using the new log collection solution: VictoriaLogs + Vector, replacing Promtail + Loki.
- Unified log format adjustments for all components, PG logs use UTC timestamp (log_timezone)
- Adjusted PostgreSQL log rotation method, using weekly truncated log rotation mode
- Recording temporary file allocations over 1MB in PG logs, enabling PG 17/18 log new parameters in specific templates
- Added Nginx Access & Error / Syslog / PG CSV / Pgbackrest vector log parsing configurations
- Datasource registration now runs on all Infra nodes, Victoria datasources automatically registered in Grafana
- Added `grafana_pgurl` parameter allowing Grafana to use PG as backend metadata storage
- Added `grafana_view_pgpass` parameter to specify password used by Grafana Meta datasource
- `pgbackrest_exporter` default options now set a 120s internal cache interval (originally 600s)
- `grafana_clean` parameter default now changed from `true` to `false`, i.e., not cleaned by default.
- Added new metric collector `pg_timeline`, collecting more real-time timeline metrics `pg_timeline_id`
- `pg_exporter` updated to 1.1.1, fixing numerous historical issues.

---

## Interface Improvements

- `install.yml` playbook now renamed to `deploy.yml` for better semantics.
- `pg_databases` database provisioning improvements:
    - Added database removal capability: use `state` field to specify `create`, `absent`, `recreate` states.
    - Added clone capability: use `strategy` parameter in database definition to specify clone method
    - Support newer version locale config parameters: `locale_provider`, `icu_locale`, `icu_rules`, `builtin_locale`
    - Support `is_template` parameter to mark database as template database
    - Added more type checks, avoiding character parameter injection
    - Allow specifying `state: absent` in extension to remove extensions
- `pg_users` user provisioning improvements: added `admin` parameter, similar to `roles`, but with `ADMIN OPTION` permission for re-granting.

---

## Parameter Optimization

- `pg_io_method` parameter, auto, sync, worker, io_uring four options available, default worker
- `idle_replication_slot_timeout`, default 7d, crit template 3d
- `log_lock_failures`, oltp, crit templates enabled
- `track_cost_delay_timing`, olap, crit templates enabled
- `log_connections`, oltp/olap enables authentication logs, crit enables all logs.
- `maintenance_io_concurrency` set to 100 if using SSD
- `effective_io_concurrency` reduced from 1000 to 200
- `file_copy_method` parameter set to `clone` for PG18, providing instant database cloning capability
- For PG17+, if `pg_checksums` switch is off, explicitly disable checksums during patroni cluster initialization
- Fixed issue where `duckdb.allow_community_extensions` always took effect
- Allow specifying HBA trusted "intranet segments" via `node_firewall_intranet`
- pg_hba and pgbouncer_hba now support IPv6 localhost access

---

## Architecture Improvements

- On Infra nodes, set fixed `/infra` symlink pointing to Infra data directory `/data/infra`.
- Infra data now defaults to `/data/infra` directory, making container usage more convenient.
- Local software repo now placed at /data/nginx/pigsty, /www now a symlink to /data/nginx for compatibility.
- DNS resolution records now placed under `/infra/hosts` directory, solving Ansible SELinux race condition issues
- pg_remove/pg_pitr etcd metadata removal tasks now run on etcd cluster instead of depending on admin_ip management node
- Simplify the 36-node simu template into the 20-node version.
- Adapted to upstream changes, removed PGDG sysupdate repo, removed all llvmjit related packages on EL systems
- Using full OS version numbers (`major.minor`) for EPEL 10 / PGDG 9/10 repos
- Allow specifying `meta` parameter in repo definitions to override yum repo definition metadata
- Added `/pg/bin/pg-fork` script for quickly creating CoW replica database instances
- Adjusted `/pg/bin/pg-pitr` script, now usable for instance-level PITR recovery
- Ensure vagrant libvirt templates default to 128GB disk, mounted at `/data` with xfs.
- Ensure pgbouncer no longer modifies `0.0.0.0` listen address to `*`.
- Multi-cloud Terraform templates: AWS, Azure, GCP, Hetzner, DigitalOcean, Linode, Vultr, TencentCloud

---

## Security Improvements

- `configure` now auto-generates random strong passwords, avoiding security risks from default passwords.
- Removed `node_disable_firewall`, added `node_firewall_mode` supporting off, none, zone three modes.
- Removed `node_disable_selinux`, added `node_selinux_mode` supporting disabled, permissive, enforcing three modes.
- Added nginx basic auth support, allowing optional HTTP Basic Auth for Nginx Servers.
- Fixed ownca certificate validity issues, ensuring Chrome can recognize self-signed certificates.
- Changed MinIO module default password to avoid conflict with well-known default passwords
- Enabled etcd RBAC, each cluster can now only manage its own PostgreSQL database cluster.
- etcd root password now placed in `/etc/etcd/etcd.pass` file, readable only by administrators
- Configured correct SELinux contexts for HAProxy, Nginx, DNSMasq, Redis and other components
- Revoked executable script ownership permissions from all non-root users
- Added admin_ip to Patroni API allowed access IP whitelist
- Always create admin system user group, patronictl config restricted to admin group users only
- Added `node_admin_sudo` parameter allowing specification/adjustment of database administrator sudo permission mode (all/nopass)
- Fixed several `ansible copy content` field empty error issues.
- Fixed some legacy issues in `pg_pitr`, ensuring no race conditions during patroni cluster recovery.

---

## Bug Fixes

- Fixed ownca certificate validity for Chrome compatibility
- Fixed Vector 0.52 syslog_raw parsing issue
- Fixed pg_pitr multiple replica clonefrom timing issues
- Fixed Ansible SELinux race condition in dnsmasq
- Fixed EL9 aarch64 patroni & llvmjit issues
- Fixed Debian groupadd path issue
- Fixed empty sudoers file generation
- Fixed pgbouncer pid path (`/run/postgresql`)
- Fixed `duckdb.allow_community_extensions` always active
- Hidden pg_partman for EL8 due to upstream break

---

## Compatibility

| OS                 | x86_64 | aarch64 |
|--------------------|:------:|:-------:|
| EL 8/9/10          |   ✅    |    ✅    |
| Debian 11/12/13    |   ✅    |    ✅    |
| Ubuntu 22.04/24.04 |   ✅    |    ✅    |

**PostgreSQL**: 13, 14, 15, 16, 17, 18
