---
title: "Pigsty v4.0: Victoria Stack + Security Hardening"
linkTitle: "Pigsty v4.0 Release Notes"
date: 2025-12-19
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v4.0.0)）
summary: >
  VictoriaMetrics/Logs replace Prometheus/Loki, Vector handles logs, the UI converges, and firewalls/SELinux/credentials get locked down.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v4.0.0

Pigsty 4.0 is a monitoring and security overhaul: VictoriaMetrics + VictoriaLogs deliver 10x observability performance, Vector replaces Promtail, the Pigsty UI merges into a single portal, default log formats go UTC, log rotation was redesigned, and new Grafana datasource controls (`grafana_pgurl`, `grafana_view_pgpass`) land. Docker images are available for quick evals.

Parameters now include `pg_io_method` (auto/sync/worker/io_uring), tightened defaults for idle replication slots, logging, IO concurrency, checksum handling, firewall/SELinux modes, and IPv6-ready HBA. Infra sees `/infra` symlinks, data under `/data/infra`, repo paths under `/data/nginx/pigsty`, host records under `/infra/hosts`, and Patroni etcd cleanup runs on the etcd cluster.

Security upgrades include random password generation during configure, optional HTTP Basic Auth per Nginx server, own CA fixes, new MinIO creds, etcd RBAC with secrets in `/etc/etcd/etcd.pass`, SELinux contexts for HAProxy/Nginx/Redis, admin API whitelists, admin group enforcement, and sudo controls via `node_admin_sudo`.

--------

## v4.0.0-b1 Release Notes

- VictoriaMetrics stack replaces Prometheus; Vector + VictoriaLogs replace Promtail + Loki; global logging standardized; log rotation switched to weekly; large temp-file logging, CSV/pgBackRest vector pipelines, automatic datasource registration across infra.
- Parameter + security knobs: `pg_io_method`, `idle_replication_slot_timeout`, `log_lock_failures`, `track_cost_delay_timing`, `log_connections`, IO concurrency tweaks, checksum handling, IPv6 HBAs, firewall/SELinux modes, `grafana_pgurl`/`grafana_view_pgpass`.
- Infra: `/infra` link, data under `/data/infra`, repo paths under `/data/nginx/pigsty`, hosts under `/infra/hosts`, etcd cleanup runs on etcd cluster.
- Security: random passwords, firewall/SELinux mode toggles, nginx basic auth, own CA validity fix, MinIO creds, etcd RBAC, service SELinux contexts, script ownership tightened, admin IPs whitelisted, admin group enforced.
