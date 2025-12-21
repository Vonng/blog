---
title: "Pigsty v1.4: Modular Architecture + MatrixDB"
linkTitle: "Pigsty v1.4 Release Notes"
date: 2022-03-31
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v1.4.0)）
summary: >
  Pigsty 1.4 tears the stack into INFRA, NODES, PGSQL, and REDIS modules, adds MatrixDB warehouses, and ships a global CDN.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v1.4.0

Pigsty 1.4 is the biggest refactor yet: the platform is now modular, Redis and MatrixDB join the supported engines, the monitoring system levels up again, and downloads move behind a fast CDN.

## Modular Architecture

Everything is rebuilt as four mix-and-match modules:

| Module | Purpose |
|--------|---------|
| INFRA | shared services: monitoring, alerting, logging, DNS, NTP |
| NODES | host lifecycle + repo/bootstrap/log agents |
| PGSQL | PostgreSQL provisioning/HA |
| REDIS | Redis provisioning/HA |

Run INFRA+NODES+PGSQL on one host for a self-contained RDS, or fan any combo across your fleet. Future engines (Kafka, MinIO, MySQL…) will just be additional modules.

## Beyond Postgres

Pigsty already handled PG + Redis. Now it adds MatrixDB, a Greenplum 7 derivative built on PG12 with native time-series extensions. MatrixDB clusters are defined with the same PGSQL configs (master/standby + segment primary/mirrors) and monitored with a dedicated Matrix dashboard plus the existing PGSQL set. Redis dashboards also got overhauled.

## Observability Evolution

- **Hosts**: node monitoring is standalone, meaning Pigsty can act purely as a host monitoring stack. New dashboards cover overview/cluster/instance/alerts with `node_cluster` and `nodename` identities.
- **Logs**: Loki + Promtail are now on by default, packaged as RPMs. Logs are visible under the INFRA overview and the PGLOG app (now treated as an APP dashboard).
- **PGSQL**: Cluster dashboards were redesigned to highlight what matters, and PGSQL Databases adds cluster-level views of tables/queries with treemaps that highlight size vs frequency/latency. PGSQL Alerts focus strictly on database alerts; PGSQL Shard debuts for sharded workloads.
- **APP area**: dashboards tagged `APP` + `Overview` show up as first-class apps (e.g., PGLOG). The `pigsty-app` repo now hosts sample apps: ISD, COVID, DBENG, AppLog, WorkTime, etc.

## CDN + Install Experience

Releases and bundles now live at `http://download.pigsty.cc`. Packages were trimmed from 1.3 GB to 940 MB; Matrix add-ons live in `matrix.tgz`. Use the helper script:

```bash
bash -c "$(curl -fsSL http://download.pigsty.cc/get)"
./download pkg matrix app
cd ~/pigsty && ./configure
make install
```

The script auto-detects whether to pull from GitHub or Tencent Cloud CDN based on your network.

## Case Study: Tantan

Dating app Tantan migrated ~100 PostgreSQL clusters (13.4k vCPU) onto Pigsty 1.3.1 with the new 1.4 monitoring stack. Chaos drills randomly killed primaries/replicas with auto failover keeping write impact under a minute—Pigsty’s HA story has serious mileage.

--------

## v1.4.0 Release Notes

- Architecture split into INFRA/NODES/PGSQL/REDIS; combine modules to suit single-node, PG-only, Redis-only, or future database scenarios.
- CDN + `download` script, curl installer (`http://get.pigsty.cc/latest`).
- Monitoring grouped into INFRA/NODES/REDIS/PGSQL/APP with Loki enabled by default, hidden `ds` selector, consistent `ip` labels, new dashboards (INFRA Overview, Log Instance, PGLOG apps, Node Overview/Cluster/Instance/Alerts, PGSQL Cluster refresh, PGSQL Databases, PGSQL Alerts, PGSQL Shard, Redis dashboards with node metrics).
- MatrixDB playbook (`pigsty-matrix.yml`), PGSQL Matrix dashboard, sample config `pigsty-mxdb.yml`.
- Upgrades: PostgreSQL 14.2, PostGIS 3.2, Timescale 2.6, Patroni 2.1.3, HAProxy 2.5.5, pg_exporter 0.4.1, Grafana 8.4.4, Prometheus 2.33.4, Greenplum 6.19.4 / MatrixDB 4.4.0, Loki RPMs.
- Fixes: Patroni no longer depends on Consul, Prometheus path fixes, vip-manager tweaks, typo cleanups.
- New vars: `node_cluster`, `nodename_overwrite`, `nodename_exchange`, `node_dns_hosts_extra`, `patroni_enabled`, `pgbouncer_enabled`, `pg_exporter_params`, `pg_provision`, `no_cmdb`.

## v1.4.1 Release Notes

- Docker enabled by default on the meta node; lots of ready-made Dockerized apps can now ride shotgun.
- Fixes for Promtail/Loki config, Grafana legacy alerts, Loki data path, patroni aliases, exemplars disabled by default, `autovacuum_freeze_max_age` bumped to 1e9, and nameserver tweaks.
