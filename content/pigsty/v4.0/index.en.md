---
title: "Pigsty v4.0.0: Observability Revolution & Security Hardening"
linkTitle: "Pigsty v4.0.0 Release"
date: 2026-01-25
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v4.0.0))
summary: >
  VictoriaMetrics/Logs replace Prometheus/Loki, new JUICE/VIBE modules, comprehensive security improvements, multi-cloud support, license change to Apache-2.0.
series: [Pigsty]
tags: [Pigsty]
---

## Quick Start

```bash
curl https://pigsty.io/get | bash -s v4.0.0
```

**299 commits**, 595 files changed, +117,624 / -327,455 lines

**Release Date: 2025-12-25** | [GitHub](https://github.com/pgsty/pigsty/releases/tag/v4.0.0) | [Docs EN](https://pigsty.io) | [Docs CN](https://pigsty.cc)

---

## Highlights

- **Observability Revolution**: Prometheus → VictoriaMetrics (10x perf), Loki+Promtail → VictoriaLogs+Vector
- **Security Hardening**: Auto-generated passwords, etcd RBAC, firewall/SELinux modes, permission tightening, Nginx Basic Auth
- **New Module**: JUICE - Mount PostgreSQL as filesystem with PITR recovery capability
- **New Module**: VIBE - AI coding sandbox with Claude Code, JupyterLab, VS Code Server
- **Database Management**: `pg_databases` state (create/absent/recreate), instant clone with `strategy`
- **PITR & Fork**: `/pg/bin/pg-fork` for instant CoW cloning, enhanced `pg-pitr` with pre-backup
- **HA Enhancement**: `pg_rto_plan` with 4 RTO presets (fast/norm/safe/wide), `pg_crontab` scheduled tasks
- **Multi-Cloud Terraform**: AWS, Azure, GCP, Hetzner, DigitalOcean, Linode, Vultr, TencentCloud templates
- **License Change**: AGPL-3.0 → Apache-2.0


[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v4.0.0)


---

## Infrastructure Package Updates

MinIO now uses [**pgsty/minio**](https://github.com/pgsty/minio) fork RPM/DEB.

| Package           | Version  | Package             | Version |
|-------------------|----------|---------------------|---------|
| victoria-metrics  | 1.133.0  | victoria-logs       | 1.43.1  |
| vector            | 0.52.0   |                     |         |
| grafana           | 12.3.1   | alertmanager        | 0.30.0  |
| etcd              | 3.6.7    | duckdb              | 1.4.3   |
| pg_exporter       | 1.1.2    | pgbackrest_exporter | 0.22.0  |
| blackbox_exporter | 0.28.0   | node_exporter       | 1.10.2  |
| minio             | 20251203 | pig                 | 0.9.1   |
| claude            | 2.1.9    | opencode            | 1.1.23  |
| uv                | 0.9.26   | asciinema           | 3.1.0   |
| prometheus        | 3.9.1    | pushgateway         | 1.11.2  |
| juicefs           | 1.4.0    | code-server         | 4.100.2 |

---

## New Modules

v4.0.0 adds two **optional modules** that don't affect core Pigsty functionality:

**JUICE Module**: JuiceFS Distributed Filesystem

- Uses PostgreSQL as metadata engine, supports PITR recovery for filesystem
- Multiple storage backends: PostgreSQL large objects, MinIO, S3
- Multi-instance deployment with Prometheus metrics per instance
- New `node-juice` dashboard for JuiceFS monitoring
- New `juice.yml` playbook for deployment
- Parameters: `juice_cache`, `juice_instances`

**VIBE Module**: AI Coding Sandbox (Code-Server + JupyterLab + Claude Code)

- **Code-Server**: VS Code in browser
  - Deploy Code-Server with Nginx reverse proxy for HTTPS
  - Supports Open VSX and Microsoft extension galleries
  - Set `code_enabled: false` to disable
  - Parameters: `code_enabled`, `code_port`, `code_data`, `code_password`, `code_gallery`

- **JupyterLab**: Interactive computing environment
  - Deploy JupyterLab with Nginx reverse proxy for HTTPS
  - Python venv configuration for data science libraries
  - Set `jupyter_enabled: false` to disable
  - Parameters: `jupyter_enabled`, `jupyter_port`, `jupyter_data`, `jupyter_password`, `jupyter_venv`

- **Claude Code**: AI coding assistant CLI configuration
  - Configure Claude Code CLI, skip onboarding
  - Built-in OpenTelemetry config sending metrics/logs to Victoria stack
  - New `claude-code` dashboard for usage monitoring
  - Set `claude_enabled: false` to disable
  - Parameters: `claude_enabled`, `claude_env`

- New `vibe.yml` playbook for full VIBE deployment
- Use `conf/vibe.yml` template for quick AI coding sandbox setup
- Common parameter: `vibe_data` (default `/fs`) for workspace directory

---

## PostgreSQL Extension Updates

Major extensions add PG 18 support: age, citus, documentdb, pg_search, timescaledb, pg_bulkload, rum, etc.

**New Extensions**:
- [pg_textsearch](https://github.com/timescale/pg_textsearch) 0.4.0 - TimescaleDB full-text search
- [pg_clickhouse](https://github.com/clickhouse/pg_clickhouse/) 0.1.2 - ClickHouse FDW
- [pg_ai_query](https://github.com/benodiwal/pg_ai_query) 0.1.1 - AI query extension
- [etcd_fdw](https://github.com/pgsty/etcd_fdw) 0.0.0 - etcd FDW
- [pg_ttl_index](https://github.com/pg-ttl-index) 0.1.0 - TTL index
- [pljs](https://github.com/plv8/pljs) 1.0.4 - JavaScript procedural language
- [pg_retry](https://github.com/pg-retry/pg_retry) 1.0.0 - Retry extension
- [pg_weighted_statistics](https://github.com/pgsty/pg_weighted_statistics) 1.0.0 - Weighted statistics
- [pg_enigma](https://github.com/pgsty/pg_enigma) 0.5.0 - Encryption extension
- [pglinter](https://github.com/pgsty/pglinter) 1.0.1 - SQL Linter
- [documentdb_extended_rum](https://github.com/microsoft/documentdb) 0.109 - DocumentDB RUM
- [mobilitydb_datagen](https://github.com/MobilityDB) 1.3.0 - MobilityDB data generator

**Major Updates**:

| Extension       | Old     | New    | Notes                  |
|-----------------|---------|--------|------------------------|
| timescaledb     | 2.23.x  | 2.24.0 | +PG18                  |
| pg_search       | 0.19.x  | 0.21.2 | ParadeDB, +PG18        |
| citus           | 13.2.0  | 14.0.0 | Distributed PG, +PG18  |
| documentdb      | 0.106   | 0.109  | MongoDB compat, +PG18  |
| age             | 1.5.0   | 1.6.0  | Graph DB, +PG18        |
| pg_duckdb       | 1.1.0   | 1.1.1  | DuckDB integration     |
| vchord          | 0.5.3   | 1.0.0  | VectorChord            |
| vchord_bm25     | 0.2.2   | 0.3.0  | BM25 full-text search  |
| pg_biscuit      | 1.0     | 2.2.2  | Biscuit auth           |
| pg_anon         | 2.4.1   | 2.5.1  | Data anonymization     |
| wrappers        | 0.5.6   | 0.5.7  | Supabase FDW           |
| pg_vectorize    | 0.25.0  | 0.26.0 | Vectorization          |
| pg_session_jwt  | 0.3.3   | 0.4.0  | JWT session            |
| pg_partman      | 5.3.x   | 5.4.0  | Partition mgmt, PGDG   |
| pgmq            | 1.8.0   | 1.8.1  | Message queue          |
| pg_bulkload     | 3.1.22  | 3.1.23 | Bulk load, +PG18       |
| pg_timeseries   | 0.1.7   | 0.2.0  | Time series            |
| pg_convert      | 0.0.4   | 0.1.0  | Type conversion        |

pgBackRest updated to 2.58 with HTTP support.

---

## Observability

- VictoriaMetrics replaces Prometheus — achieving several times the performance with a fraction of the resources
- VictoriaLogs + Vector replaces Promtail + Loki for log collection
- Unified log format for all components, PG logs use UTC timestamp (log_timezone)
- PostgreSQL log rotation changed to weekly truncated rotation mode
- Recording temp file allocations over 1MB in PG logs, enabling PG 17/18 log parameters in specific templates
- Added Vector parsing configs for Nginx/Syslog/PG CSV/Pgbackrest/Grafana/Redis/etcd/MinIO logs
- Datasource registration now runs on all Infra nodes, Victoria datasources auto-registered in Grafana
- New `grafana_pgurl` parameter for using PG as Grafana backend storage
- New `grafana_view_password` parameter for Grafana Meta datasource password
- `pgbackrest_exporter` default cache interval reduced from 600s to 120s
- `grafana_clean` default changed from `true` to `false`
- New `pg_timeline` collector for real-time timeline metrics `pg_timeline_id`
- `pg_exporter` updated to 1.1.2 with `pg_timeline` collector and numerous fixes
- New `node-vector` dashboard for Vector monitoring
- New `node-juice` dashboard for JuiceFS monitoring
- New `claude-code` dashboard for Claude Code usage monitoring
- PGSQL Cluster/Instance dashboards add version banner
- All dashboards use compact JSON format, significantly reducing file size

---

## Interface Improvements

**Playbook Rename**
- `install.yml` renamed to `deploy.yml` for better semantics
- New `vibe.yml` playbook for VIBE AI coding sandbox

**pg_databases Improvements**
- Database removal: use `state` field (`create`, `absent`, `recreate`)
- Database cloning: use `strategy` parameter for clone method
- Support newer locale params: `locale_provider`, `icu_locale`, `icu_rules`, `builtin_locale`
- Support `is_template` to mark template databases
- Added type checks to prevent character parameter injection
- Allow `state: absent` in extension to remove extensions

**pg_users Improvements**
- New `admin` parameter similar to `roles` but with `ADMIN OPTION` for re-granting
- New `set` and `inherit` options for user role attributes

**pg_hba Improvements**
- Support `order` field for HBA rule priority
- Support IPv6 localhost access
- Allow specifying trusted intranet via `node_firewall_intranet`

**Other Improvements**
- Default privileges for Supabase roles
- `node_crontab` auto-restores original crontab on `node-rm`
- New `infra_extra_services` for homepage service entries

---

## Parameter Optimization

**I/O Parameters**
- `pg_io_method`: auto, sync, worker, io_uring options, default worker
- `maintenance_io_concurrency` set to 100 for SSD
- `effective_io_concurrency` reduced from 1000 to 200
- `file_copy_method` set to `clone` for PG18 instant database cloning

**Replication & Logging**
- `idle_replication_slot_timeout`: default 7d, crit template 3d
- `log_lock_failures`: enabled for oltp, crit templates
- `track_cost_delay_timing`: enabled for olap, crit templates
- `log_connections`: auth logs for oltp/olap, full logs for crit

**HA Parameters**
- New `pg_rto_plan` integrating Patroni & HAProxy RTO config
  - `fast`: Fastest failover (~15s), for high availability requirements
  - `norm`: Standard mode (~30s), balanced (default)
  - `safe`: Safe mode (~60s), reduced false positives
  - `wide`: Relaxed mode (~120s), for geo-distributed deployments
- `pg_crontab`: scheduled tasks for postgres dbsu
- For PG17+, explicitly disable checksums if `pg_checksums` is off
- Crit template enables Patroni strict sync mode

**Backup & Recovery**
- PITR default `archive_mode` changed to `preserve`
- `pg-pitr` supports pre-recovery backup

**Other**
- Fixed `duckdb.allow_community_extensions` always active issue
- pg_hba and pgbouncer_hba now support IPv6 localhost

---

## Architecture Improvements

**Directories & Portal**
- Fixed `/infra` symlink pointing to `/data/infra` on Infra nodes
- Infra data defaults to `/data/infra` for container convenience
- Local repo at `/data/nginx/pigsty`, `/www` symlinks to `/data/nginx`
- DNS records moved to `/infra/hosts`, solving Ansible SELinux race condition
- Default homepage domain renamed from `h.pigsty` to `i.pigsty`, added Chinese homepage

**Scripts**
- New `/pg/bin/pg-fork` for instant CoW replica creation
- Enhanced `/pg/bin/pg-pitr` for instance-level PITR with pre-backup
- New `/pg/bin/pg-drop-role` for safe user deletion
- New `bin/pgsql-ext` for extension installation
- Restored `pg-vacuum` and `pg-repack` scripts

**New Playbooks**
- `juice.yml`: Deploy JuiceFS instances
- `vibe.yml`: Deploy VIBE AI sandbox (Code-Server, JupyterLab, Claude Code)

**Module Improvements**
- Explicit cron/cronie package installation for minimal system compatibility
- UV Python manager moved from `infra` to `node` module, new `node_uv_env` parameter
- `pg_remove`/`pg_pitr` etcd metadata removal now runs on etcd cluster
- Simu template simplified from 36 to 20 nodes
- Removed PGDG sysupdate repo and llvmjit packages on EL systems
- Using full OS version (`major.minor`) for EPEL 10 / PGDG 9/10 repos
- Allow `meta` parameter in repo definitions
- Vagrant libvirt templates default to 128GB disk with xfs at `/data`
- Ensure pgbouncer doesn't modify `0.0.0.0` to `*`
- New 10-node and Citus Vagrant templates
- Restored EL7 compatibility

**Multi-Cloud**
- Terraform templates: AWS, Azure, GCP, Hetzner, DigitalOcean, Linode, Vultr, TencentCloud

---

## Security Improvements

**Password Management**
- `configure` supports `-g` flag for auto-generating strong random passwords
- Changed MinIO default password to avoid well-known defaults

**Firewall & SELinux**
- Replaced `node_disable_firewall` with `node_firewall_mode` (off/none/zone)
- Replaced `node_disable_selinux` with `node_selinux_mode` (disabled/permissive/enforcing)
- Configured correct SELinux contexts for HAProxy, Nginx, DNSMasq, Redis

**Access Control**
- Enabled etcd RBAC, each cluster can only manage its own PG cluster
- etcd root password stored in `/etc/etcd/etcd.pass`, admin-readable only
- Added `admin_ip` to Patroni API whitelist
- Always create admin system group, patronictl restricted to admin group
- New `node_admin_sudo` parameter for admin sudo mode (all/nopass)
- Revoked script ownership from non-root users

**Certificates & Auth**
- Nginx Basic Auth support for optional HTTP authentication
- Fixed ownca certificate validity for Chrome recognition
- New `vip_auth_pass` parameter for VRRP authentication

**Other**
- Fixed `ansible copy content` empty field errors
- Fixed `pg_pitr` race conditions during Patroni cluster recovery
- Protected `files/pki/ca` directory with mode 0700

---

## Bug Fixes

| Issue                                    | Resolution                              |
|------------------------------------------|-----------------------------------------|
| ownca certificate Chrome compatibility   | Set ownca_not_after correctly           |
| Vector 0.52 syslog_raw parsing           | Adapted to new Vector format            |
| pg_pitr multi-replica clonefrom timing   | Fixed Patroni recovery race condition   |
| Ansible SELinux dnsmasq race condition   | Moved DNS records to /infra/hosts       |
| EL9 aarch64 patroni & llvmjit            | Hotfix for ARM64 compatibility          |
| Debian groupadd path                     | Fixed user group add path               |
| Empty sudoers file generation            | Prevented empty sudoers config          |
| pgbouncer pid path                       | Use `/run/postgresql`                   |
| duckdb.allow_community_extensions active | Fixed DuckDB extension config           |
| pg_partman EL8 upstream break            | Hidden pg_partman on EL8                |
| HAProxy service template variable path   | Fixed variable reference                |
| Redis remove task variable name          | Fixed redis_seq to redis_node           |
| MinIO reload handler ineffective         | Removed ineffective handler             |
| vmetrics_port default value              | Corrected to 8428                       |
| pg-failover-callback script              | Handle all Patroni callback events      |
| pg-vacuum transaction block              | Fixed transaction handling              |
| pg_sub_16 parallel logical worker        | Added PG16+ parallel replication        |
| FerretDB cert SAN and restart policy     | Fixed cert config and restart           |
| Polar Exporter metric types              | Corrected metric type definitions       |
| proxy_env package install missing        | Fixed proxy env propagation             |
| patroni_method=remove service issue      | Fixed postgres service in remove mode   |
| Docker default data directory            | Updated to correct path                 |
| EL10 cache compatibility                 | Fixed EL10 cache issues                 |
| etcd/MinIO removal cleanup incomplete    | Fixed systemd service and DNS cleanup   |

---

## Parameter Changes

**New Parameters**

| Parameter                | Type   | Default       | Description                           |
|--------------------------|--------|---------------|---------------------------------------|
| `node_firewall_mode`     | enum   | none          | Firewall mode: off/none/zone          |
| `node_selinux_mode`      | enum   | permissive    | SELinux mode                          |
| `node_firewall_intranet` | string | -             | HBA trusted intranet                  |
| `node_admin_sudo`        | enum   | nopass        | Admin sudo privilege level            |
| `pg_io_method`           | enum   | worker        | I/O method: auto/sync/worker/io_uring |
| `pg_rto_plan`            | dict   | -             | RTO presets: fast/norm/safe/wide      |
| `pg_crontab`             | list   | []            | postgres dbsu scheduled tasks         |
| `vip_auth_pass`          | string | -             | VRRP auth password                    |
| `grafana_pgurl`          | string | -             | Grafana PG backend URL                |
| `grafana_view_password`  | string | DBUser.Viewer | Grafana Meta datasource password      |
| `infra_extra_services`   | list   | []            | Homepage extra service entries        |
| `juice_cache`            | path   | /data/juice   | JuiceFS cache directory               |
| `juice_instances`        | dict   | {}            | JuiceFS instance definitions          |
| `vibe_data`              | path   | /fs           | VIBE workspace directory              |
| `code_enabled`           | bool   | true          | Enable Code-Server                    |
| `code_port`              | port   | 8443          | Code-Server listen port               |
| `code_data`              | path   | /data/code    | Code-Server data directory            |
| `code_password`          | string | Code.Server   | Code-Server password                  |
| `code_gallery`           | enum   | openvsx       | Extension gallery: openvsx/microsoft  |
| `jupyter_enabled`        | bool   | true          | Enable JupyterLab                     |
| `jupyter_port`           | port   | 8888          | JupyterLab listen port                |
| `jupyter_data`           | path   | /data/jupyter | JupyterLab data directory             |
| `jupyter_password`       | string | Jupyter.Lab   | JupyterLab access token               |
| `jupyter_venv`           | path   | /data/venv    | Python venv path                      |
| `claude_enabled`         | bool   | true          | Enable Claude Code configuration      |
| `claude_env`             | dict   | {}            | Claude Code extra env vars            |
| `node_uv_env`            | path   | /data/venv    | Node UV venv path, empty to skip      |
| `node_pip_packages`      | string | ''            | pip packages for UV venv              |

**Removed Parameters**

| Parameter               | Replacement                       |
|-------------------------|-----------------------------------|
| `node_disable_firewall` | `node_firewall_mode`              |
| `node_disable_selinux`  | `node_selinux_mode`               |
| `infra_pip_packages`    | `node_pip_packages`               |
| `pgbackrest_clean`      | Unused, removed                   |
| `pg_pwd_enc`            | Removed, always scram-sha-256     |
| `code_home`             | `vibe_data`                       |
| `jupyter_home`          | `vibe_data`                       |

**Default Value Changes**

| Parameter                  | Change                    | Notes                    |
|----------------------------|---------------------------|--------------------------|
| `grafana_clean`            | true → false              | Don't clean by default   |
| `effective_io_concurrency` | 1000 → 200                | More reasonable default  |
| `node_firewall_mode`       | zone → none               | Disable firewall rules   |
| `install.yml`              | Renamed to `deploy.yml`   | Better semantics         |

---

## Compatibility

| OS                 | x86_64 | aarch64 |
|--------------------|:------:|:-------:|
| EL 8/9/10          |   ✅    |    ✅    |
| Debian 11/12/13    |   ✅    |    ✅    |
| Ubuntu 22.04/24.04 |   ✅    |    ✅    |

**PostgreSQL**: 13, 14, 15, 16, 17, 18

---

## Checksums

```bash
# v4.0.0 offline package checksums (TBD)
```
