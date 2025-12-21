---
title: "Pigsty v2.2: Monitoring Reborn"
linkTitle: "Pigsty v2.2 Release Notes"
date: 2023-08-04
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.2.0)）
summary: >
  Grafana 10 dashboards were rebuilt from scratch, the sandbox story scales to 42 nodes, and Pigsty now maintains its own RPM repos.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.2.0

Pigsty 2.2 is all about observability. Every dashboard was redesigned around Grafana 10’s UX, with color schemes keyed to each subsystem (PG blue, Redis red, Nginx green, etc.), stat tiles replacing the old grid jungle, state timelines for SLIs, and quick-drill navigation. Instances, nodes, ETCD, MinIO, HAProxy, services, databases, tables, and queries all share the same visual grammar: green/blue is boring, anything else demands attention. PGCAT still surfaces catalog context, but the UI is now consistent with the metrics side.

We also ship a playground meant for real-world rehearsal: a 42-node Vagrant sandbox driven by a <500-line config, plus libvirt/KVM templates. Citus 12, PG16 beta2, and UOS-v20 (a domestic Linux distro) join the compatibility matrix. To tame third-party RPM chaos, Pigsty now hosts its own EL repos (`pigsty-el` / `pigsty-misc`) so components like Redis, Prometheus, or Grafana are always available from a curated source.

--------

## v2.2.0 Release Notes

- **Highlights**: rebuilt dashboards (see http://demo.pigsty.cc), revamped Vagrant sandbox (VirtualBox + libvirt/KVM), Pigsty EL repos for stray RPMs, UOS-v20 support, new 42-node production-simulation template, standardized PGDG Citus packages on EL7.
- **Upgrades**: PG16 beta2, Citus 12, PostGIS 3.3.3, TimescaleDB 2.11.1, PGVector 0.44, Patroni 3.0.4, pgBackRest 2.47, pgbouncer 1.20, Grafana 10.0.3, Loki/Promtail 2.8.3, etcd 3.5.9, HAProxy 2.8.1, Redis 7.0.12, MinIO 20230711.
- **Fixes**: Docker group permissions, `infra` user supplementary groups, Redis Sentinel systemd state, bootstrap/configure edge cases, Grafana 10 CVE-2023-1410, CMDB pglog tags for PG14–16.
- **API**: optional `nginx_exporter_enabled`, repo defaults reorganized (new `pigsty-el`/`pigsty-misc`, dropped `citus`/`remi`), package lists consolidated, `.pigsty` switches to `PGDATABASE=postgres`, helper scripts relocated under `vagrant/`.
