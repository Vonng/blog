---
title: "Pigsty v0.6: Provisioning Upgrades"
linkTitle: "Pigsty v0.6 Release Notes"
date: 2021-02-19
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.6.0)）
summary: >
  v0.6 reworks the provisioning flow, adds exporter toggles, and makes the monitoring stack portable across environments.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.6.0

Pigsty v0.6 responds to user feedback with a redesigned provisioning path plus a monitoring stack that can sit beside any managed PG fleet—even a MyBase cluster built elsewhere.

## Bug Fixes

- Patroni no longer resets PG HBA on restart.
- Fixed copy typos and the default primary for the `pg-test` sandbox cluster.
- Patched the dashboard title typo on PG Overview.

## Feature Work

- Monitoring supply chain overhaul: Prometheus can now run fully static, exporters accept `service_registry` toggles, and `exporter_binary_install` lets you drop binaries without hitting repos. Each exporter has its own `*_enabled` flag.
- Prometheus static discovery is rendered straight from inventory, so you can graft Pigsty dashboards onto any PG-as-a-service footprint.
- HAProxy provisioning adds a global console at `h.pigsty`, optional auth, fallback routing to the primary when all replicas die, and per-service weight tuning.
- ACL defaults now include `dbrole_offline` for slow-query/ETL workloads plus HBA rules that fence those workloads to marked nodes.
- Component refresh: PostgreSQL 13.2, Prometheus 2.25, pg_exporter 0.3.2, node_exporter 1.1, Consul 1.9.3, and a faster ZJU PG mirror.

## API Changes

New knobs:

```yaml
service_registry: consul
prometheus_options: '--storage.tsdb.retention=30d'
prometheus_sd_method: consul
prometheus_sd_interval: 2s
pg_offline_query: false
node_exporter_enabled: true
pg_exporter_enabled: true
pgbouncer_exporter_enabled: true
dcs_disable_purge: false
pg_disable_purge: false
haproxy_weight: 100
haproxy_weight_fallback: 1
```

Removed knobs:

```yaml
prometheus_metrics_path
prometheus_retention
```
