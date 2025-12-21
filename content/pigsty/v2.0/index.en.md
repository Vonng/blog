---
title: "Pigsty v2.0: Open RDS Alternative"
linkTitle: "Pigsty v2.0 Release Notes"
date: 2023-02-26
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.0.0)）
summary: >
  Pigsty 2.0 goes all-in on being a better, local-first, open-source replacement for managed PostgreSQL RDS.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.0.0

Pigsty 2.0 is a line in the sand: we want a self-hosted RDS experience that can dethrone cloud lock-in. “Pigsty” now stands for **PostgreSQL In Great STYle**—the database at its best, with everything you need to run it like a cloud vendor but on your own terms.

## RDS-Class Distribution

Pigsty packages PG15 with TimescaleDB, PostGIS, and Citus—fully interoperable out of the box—plus the tooling and automation to run them as a service. Modules (`INFRA`, `NODE`, `PGSQL`, `ETCD`, `MINIO`, `REDIS`, and friends) snap together so you can cover everything from a single-node sandbox to a fleet of HA clusters, caches, and object storage. Offline bundles let you deploy in dark sites with one command.

## Observability That Scales

Grafana + Prometheus + Loki + Alertmanager + PushGateway + Blackbox = a modern, open observability stack. Every Pigsty-managed component auto-registers and exports metrics/logs. Thousands of curated metrics and dashboards help you reason about fleets, nodes, queries, tables, indexes, and even the monitoring stack itself. Drop it onto your existing databases or RDS instances if you just want the observability goodness.

## Reliability + PITR

HA is table stakes. Pigsty builds Patroni clusters with ETCD-backed consensus and VIP-managed traffic. FailSafe defaults keep primaries online even if the DCS hiccups. For human error, pgBackRest-based PITR is built in: local backups keep two days of history; optional MinIO/S3 targets extend that to weeks with AES-encrypted archives. Disaster recovery is now part of the base experience, not an add-on.

## Security Hardening

Pigsty 2.0 adds a self-signed CA, SSL everywhere (Nginx, PostgreSQL, Pgbouncer, Patroni, ETCD), SCRAM-SHA-256 auth, encrypted backups, and explicit HBA definitions. Password changes no longer leak into logs. High-security templates enforce client cert auth if you need it.

## Compatibility + Maintainability

EL7/8/9 supported (RHEL, CentOS, Rocky, Alma, Oracle Linux) with per-OS offline bundles. VIP manager, Node roles (HAProxy, Docker, node_exporter, promtail), and INFRA components (dnsmasq, blackbox, pushgateway) were revamped. Config templates auto-tune to hardware, region-aware mirrors speed up installs, Terraform/Vagrant templates help you spin up labs, and there’s a growing library of shell helpers plus playbooks for monitoring/migrating existing databases.

--------

## v2.0.0 Release Notes

- Fully integrated PG15.2 + PostGIS 3.3 + TimescaleDB 2.10 + Citus 11.2 stack; Patroni 3.0 with HA Citus support, FailSafe, ETCD DCS, and pgBackRest 2.44 PITR (local + MinIO/S3 targets).
- New standalone modules: ETCD (with scaling + monitoring) and MINIO (multi-disk/node S3 replacement). NODE module now owns HAProxy, Docker, node_exporter, promtail, chronyd; INFRA module covers dnsmasq, nginx, Prometheus, Grafana, Loki, blackbox_exporter, pushgateway.
- Security: Pigsty CA, SSL everywhere, SCRAM auth, AES-encrypted backups, HBA rules in config, high-security templates.
- Maintainers’ joy: auto hardware tuning, configurable log roots, `${admin_ip}` placeholder, region-aware mirrors, Terraform/Vagrant templates, monitor/migration playbooks, new shell helpers, cleaned-up Ansible roles, per-db/role pgbouncer options.
- API churn: dozens of new variables (admin IP, CA metadata, repo controls, SSL ports, etc.), explicit remaps/renames documented above, legacy DCS/PG install knobs removed. License shifts to AGPL v3 due to Grafana/MinIO dependencies.

## v2.0.1 Release Notes

- Branding/security polish: new logo compliant with PG trademark, Grafana 9.4, Patroni 3.0.1, default Grafana service file, safer dashboard sync via `copy`, bootstrap restores repo files, asciinema demos.
- Security-hardening template tweaks: safer monitoring roles, `dual.yml` for 2-node builds, `crit.yml` enables connection logging and passwordcheck.
- Patroni now binds to `{{ inventory_hostname }}`; `pg_listen` supports `${ip}/${lo}/${vip}` placeholders.
- Misc: monitoring users lose default `dbrole_readonly`, log permissions set explicitly, numerous doc improvements.
