---
title: "Pigsty v1.0: GA With a Monitoring Overhaul"
linkTitle: "Pigsty v1.0 Release Notes"
date: 2021-07-26
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v1.0.0)）
summary: >
  Pigsty 1.0 graduates to GA: a batteries-included PostgreSQL distro with a rebuilt monitoring stack and opinionated HA automation.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v1.0.0

After a year of iterations Pigsty finally ships 1.0 GA. Pigsty (**P**ostgre**S**QL **I**n **G**raphic **STY**le) is a full PostgreSQL distribution that glues together provisioning, HA, service discovery, routing, monitoring, alerting, and logging. Think of it as the Debian of Postgres.

## What Pigsty Solves

Pigsty targets teams that want a production-grade PG fleet without reinventing deployment, monitoring, HA, access control, or tooling. Out of the box you get:

| Role | Description |
|------|-------------|
| Distribution | Batteries-included PostgreSQL runtime |
| Monitoring | Deep visibility into PG internals |
| Deployment | Declarative HA provisioning |
| Sandbox | Local lab + visualization toolkit |
| License | Apache 2.0, no strings attached |

## Distribution Mindset

Similar to how Debian or RHEL sits on top of the Linux kernel, Pigsty sits on top of PostgreSQL and bundles everything needed to run it well: tuned config, HA wiring, dashboards, logging, and tooling. The focus is professional-grade monitoring, easy deployments, reliable architecture, sandbox convenience, and a permissive license.

## Batteries Included

Spin up a fresh VM, run a single command, and within ~10 minutes you have infra, databases, monitoring, and control planes online. Experts get deep knobs; everyone else gets sane defaults. Tools like JupyterLab and ECharts are pre-wired for analysts who want to go from ingestion to visualization quickly.

## Observability That Actually Helps

Pigsty’s monitoring stack spans ~1200 metrics, 20+ dashboards, and more than a thousand panels. It drills from fleet-level heat maps all the way down to per-table, per-query, per-function stats. The three main apps are:

- **PGSQL** – the metric workhorse built on Prometheus + Grafana.
- **PGCAT** – an interactive catalog browser.
- **PGLOG** – a real-time CSV log explorer backed by Loki.

Everything is open, customizable, and portable. Drop the monitoring stack onto any existing PG fleet or even other data services like Redis.

## Deployment Story

Ansible-backed IaC gives you declarative control: describe the cluster in YAML or via the GUI/CLI and Pigsty creates/destroys/scales it. A CMDB mode plus CLI/GUI wrappers keep day‑2 ops approachable, while 160+ tunables let experts shape every part of the runtime.

## High Availability

Clusters are multi-instance, self-healing, and fronted by integrated load balancers. Any surviving node can serve read-write traffic; failover usually completes within seconds and read-only traffic keeps flowing. The default topology combines DNS, L2 VIP, and HAProxy but you can swap pieces out as needed.

## Sandboxes and Data Apps

Need a local lab? Vagrant + VirtualBox spins up a single-node (2c/4g) sandbox or a four-node topology for HA experiments. Beyond the database, Pigsty bundles PG + JupyterLab + Grafana/ECharts so you can ship proof-of-concept data apps quickly. The repo even ships demo projects like COVID dashboards and ISD weather explorers.

## Roadmap & Community

The roadmaps highlight work on deeper observability, richer tooling, and more kernels. Everything lives under Apache 2.0 so commercial users can take it straight to production. The motto stays simple: help people **use Postgres well** and **use the best database**.

--------

## v1.0.0 Release Notes

- Monitoring stack rebuilt on Grafana 8 with fresh dashboards, derived metrics, PG14 support, simplified labels (job/cls/ins), richer alerts, and real-time log search.
- Added Citus and TimescaleDB to the default install alongside PG 14 beta2 support.
- New roles: `register` (decouples infra & pgsql), `loki`/`promtail` (logging), `environ` (shell setup), and `remove` (clean teardown). Prometheus now defaults to static SD.
- Every database registers as a Grafana data source automatically. Consul registration moved under `register`; tags updated.
- App framework shipped with core apps (`pgsql`, `pgcat`, `pglog`) plus demo apps `covid` and `isd`. JupyterLab + ECharts panel included.
- Helper scripts (`createpg`, `createdb`, `createuser`, CMDB inventory loaders) and removal of old playbooks.
- New variables: `node_meta_pip_install`, `grafana_admin_username`, `grafana_database`, `grafana_pgurl`, `pg_shared_libraries`, `pg_exporter_auto_discovery`, `pg_exporter_exclude_database`, `pg_exporter_include_database`. `grafana_url` renamed to `grafana_endpoint`.
- Bug fixes for tz defaults, `nofile` limits, and pgbouncer inventory generation.

## v1.0.1 Release Notes (2021-09-14)

- Docs now include Chinese plus machine-translated English.
- `pgsql-remove` leaves primaries alone; Start-At-Task no longer breaks when `pg_instance` is unset.
- Dropped Citus from `shared_preload_libraries` to avoid forced `max_prepared_transactions`.
- `configure` checks sudo via `ssh -t sudo -n ls`; `pg-backup` typo fixed.
- NTP sanity alert removed (redundant with ClockSkew); skipped `collector.systemd` to trim exporter overhead.
