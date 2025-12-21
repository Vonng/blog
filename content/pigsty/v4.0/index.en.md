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

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.0.0-b1) | [**Release Note**](https://pigsty.io/docs/releasenote/#v400)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v4.0.0)


--------

## v4.0.0-b1


### Highlights

- Infra module completely revamped — Victoria observability stack delivers **10x performance boost**!
- Log solution upgraded to VictoriaLogs + Vector — epic performance and usability improvements!
- Pigsty UI integrated for a cohesive user experience.
- Global security enhancements — firewall, SELinux, permission hardening
- Docker container version available for quick evaluation

### Software Versions

**Infrastructure Packages**

MinIO now uses RPM/DEB packages maintained by pgsty itself.

- victoria-metrics  : 1.132.0
- victoria-logs     : 1.41.0
- blackbox_exporter : 0.28.0
- duckdb            : 1.4.3
- rclone            : 1.72.1
- pev2              : 1.19.0
- pg_exporter       : 1.1.0
- pig               : 0.8.0
- rclone            : 1.72.1
- genai-toolbox     : 0.23.0
- minio             : 20251203120000

**PG Extension Packages**

- [pg_textsearch](https://github.com/timescale/pg_textsearch): 0.1.0 new extension
- [pg_clickhouse](https://github.com/clickhouse/pg_clickhouse/): 0.1.0 new extension
- [pg_ai_query](https://github.com/benodiwal/pg_ai_query): 0.1.1 new extension
- timescaledb    : 2.23.1  -> 2.24.0
- pg_search      : 0.20.0  -> 0.20.4
- pg_duckdb      : 1.1.0-1 -> 1.1.0-2, official release version
- pg_biscuit     : 1.0     -> 2.0.1, repository renamed
- pg_convert     : 0.0.4   -> 0.0.5, removed PG 13 support
- pgdd           : 0.6.0   -> 0.6.1, removed PG 13 support
- pglinter       : 1.0.0   -> 1.0.1
- pg_session_jwt : 0.3.3   -> 0.4.0
- pg_anon        : 2.4.1   -> 2.5.1
- pg_enigma      : 0.4.0   -> 0.5.0
- wrappers       : 0.5.6   -> 0.5.7
- pg_vectorize   : 0.25.0  -> 0.26.0

Fixed PG 18 Deb packages: pg_vectorize, pg_tiktoken, pg_tzf, pglite_fusion, pgsmcrypto, pgx_ulid, plprql


### Observability

- Using the new VictoriaMetrics to replace Prometheus — achieving several times the performance with a fraction of the resources.
- Using the new log collection solution: VictoriaLogs + Vector, replacing Promtail + Loki.
- Unified log format adjustments for all components, PG logs use UTC timestamp (log_timezone)
- Adjusted PostgreSQL log rotation method, using weekly truncated log rotation mode
- Recording temporary file allocations over 1MB in PG logs, enabling PG 17/18 log new parameters in specific templates
- Added Nginx Access & Error / Syslog / PG CSV / Pgbackrest vector log parsing configurations
- Datasource registration now runs on all Infra nodes, Victoria datasources automatically registered in Grafana
- Added `grafana_pgurl` parameter allowing Grafana to use PG as backend metadata storage
- Added `grafana_view_pgpass` parameter to specify password used by Grafana Meta datasource

### Parameter Optimization

- `pg_io_method` parameter, auto, sync, worker, io_uring four options available, default worker
- `idle_replication_slot_timeout`, default 7d, crit template 3d
- `log_lock_failures`, oltp, crit templates enabled
- `track_cost_delay_timing`, olap, crit templates enabled
- `log_connections`, oltp/olap enables authentication logs, crit enables all logs.
- `maintenance_io_concurrency` set to 100 if using SSD
- `effective_io_concurrency` reduced from 1000 to 200
- For PG17+, if `pg_checksums` switch is off, explicitly disable checksums during patroni cluster initialization
- Fixed issue where `duckdb.allow_community_extensions` always took effect
- Allow specifying HBA trusted "intranet segments" via `node_firewall_intranet`
- pg_hba and pgbouncer_hba now support IPv6 localhost access


### Architecture Improvements

- On Infra nodes, set fixed `/infra` symlink pointing to Infra data directory `/data/infra`.
- Infra data now defaults to `/data/infra` directory, making container usage more convenient.
- Local software repo now placed at /data/nginx/pigsty, /www now a symlink to /data/nginx for compatibility.
- DNS resolution records now placed under `/infra/hosts` directory, solving Ansible SELinux race condition issues
- pg_remove/pg_pitr etcd metadata removal tasks now run on etcd cluster instead of depending on admin_ip management node


### Security Improvements

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
