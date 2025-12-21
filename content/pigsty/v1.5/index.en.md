---
title: "Pigsty v1.5: Docker Apps + Self-Monitoring"
linkTitle: "Pigsty v1.5 Release Notes"
date: 2022-05-17
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v1.5.0)）
summary: >
  Docker-backed apps, infra self-monitoring, ETCD support, and better cold backups make Pigsty 1.5 the most complete PG distro yet.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v1.5.0

Pigsty 1.5 doubles down on developer convenience: Docker is enabled on the meta node with curated app templates, infra components monitor themselves, ETCD becomes an alternative DCS, cold backups improve, and the CMDB learns about Redis/MatrixDB clusters.

## Docker-Powered App Ecosystem

Pigsty now treats Docker as a first-class dependency on the management node. Stateful engines (Postgres, Redis) stay bare-metal; stateless apps spin up via Docker Compose with single `make up` commands. Templates cover Gitea, PgAdmin, Bytebase, PGWEB, MinIO, JupyterLab, SchemaSpy, PgBadger, GitLab, Harbor, Jira, Confluence, Odoo, Mastodon, Discourse, Keycloak, and more. Need MongoDB compatibility? Launch FerretDB. Need a wiki? `wiki.js` is included. JupyterLab still runs natively by default for tighter database access, but a helper playbook can deploy it via Docker too.

## Better Backups & Delayed Replicas

Cold backups now run nightly via declarative cron entries. WAL archiving already covered the last 24 hours; with daily fulls plus WAL shipping, you can restore to any point in the last day. Delayed replicas become a checkbox: declare `pg_delay` and Pigsty bootstraps a lagged standby cluster. `pg_probackup` is bundled for power users, and MinIO images lay the groundwork for cross-region backup buckets.

## CMDB 2.0 + API

The CMDB schema was rewritten so Redis and MatrixDB metadata live alongside Postgres. Load configs into CMDB with `bin/inventory_load` and switch with `bin/inventory_cmdb`. Grafana’s CMDB Overview dashboard visualizes every cluster/member. PostgREST (bundled) exposes REST endpoints for CRUD; Swagger specs + SDKs fall out automatically. Want more? Fire up Kong from the Docker bundle to get full API gateway features.

## Infra Self-Monitoring

INFRA components register themselves via `infra_register`, so Prometheus/Grafana/Loki/etc. show up as neon-green peers next to PGSQL/REDIS. Dedicated dashboards (Prometheus Overview, Grafana Overview, Loki Overview, Infra Overview) let you observe the observers.

## ETCD as DCS + Better Logging

Setting `pg_dcs_type: etcd` swaps Consul for ETCD as the Patroni DCS. You can even run both (ETCD for HA, Consul for discovery). DCS dashboards track health for both clusters. Every upstream service now writes structured access logs that Loki parses, so NGINX traffic analysis and other log insights are point-and-click.

--------

## v1.5.0 Release Notes

- **Docker**: `docker.tgz` bundle ships PgAdmin, PgWeb, PostgREST, Bytebase, Kong, MinIO, etc.; Docker enabled on the meta node.
- **Infra Monitoring**: Nginx, ETCD, Consul, Prometheus, Grafana, Loki all register themselves; new dashboards for CMDB, DCS, Nginx, Grafana, Prometheus, and revamped INFRA overview.
- **CMDB**: now stores Redis and MatrixDB clusters; visual dashboards.
- **Service Discovery**: Consul can now auto-discover all monitoring targets when combined with service registration.
- **Backups**: cron templates for daily full backups, `pg_probackup` packages, delayed standby automation, MinIO images for offsite storage.
- **DCS**: ETCD playbook/role; `pg_dcs_type` selects Consul or ETCD; DCS Overview dashboard.
- **Redis**: init/remove at per-instance granularity; systemd services enabled by default.
- **Logging**: Loki/Promtail installed via RPM; upstream services log structured events for analysis.
- **Upgrades**: PostgreSQL 14.3, Redis 6.2.7, pg_exporter 0.5.0, Consul 1.12.0, vip-manager 1.0.2, Grafana 8.5.2, Loki/Promtail 2.5.0.
- **API**: new knobs (`node_data_dir`, `node_crontab_overwrite`, `node_crontab`, `nameserver_enabled`, `prometheus_enabled`, `grafana_enabled`, `loki_enabled`, `docker_enable`, `consul_enable`, `etcd_enable`, `pg_checksum`, `pg_delay`); cleanup/safeguard flags standardized; numerous renames listed in the Chinese notes are applied here as well.

## v1.5.1 Release Notes

- Urgent PG14 fix: default kernel now 14.4 to avoid `CREATE/REINDEX INDEX CONCURRENTLY` corruption bugs. Upgrade ASAP.
- Component bumps: HAProxy 2.6.0, Grafana 9.0.0, Prometheus 2.36.0, Patroni 2.1.4.
- Fixes: `pgsql-migration.yml` typo, HAProxy PID removal, dropped i686 packages, systemd services enabled by default.
- `grafana_database` and `grafana_pgurl` are deprecated.
- New sample apps: wiki.js and FerretDB (MongoDB API on Postgres).
