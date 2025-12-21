---
title: "Pigsty v0.7: Monitor-Only Deployments"
linkTitle: "Pigsty v0.7 Release Notes"
date: 2021-03-01
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.7.0)）
summary: >
  Monitor-only deployments unlock hybrid fleets, while DB/user provisioning APIs get a serious cleanup.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.7.0

Pigsty v0.7 focuses on plugging existing fleets into Pigsty's observability stack. The new monitor-only flow lets you drop Pigsty dashboards onto databases that were provisioned elsewhere, and the declarative APIs for databases and users got a much needed redesign.

## Highlights

- Monitor-only deployment flow (`monly`) with its own playbook.
- Split static Prometheus target files by cluster for easier hand-editing.
- New helper playbooks: `pgsql-createuser.yml` and `pgsql-createdb.yml` for live clusters.
- Database and user schema definitions now cover owner/template/locale knobs plus per-role capabilities.
- Bug fixes for extension schema typos and pgbouncer reload.

## API Changes

New options:

```yaml
prometheus_sd_target: batch
exporter_install: none
exporter_repo_url: ''
node_exporter_options: '--no-collector.softnet --collector.systemd --collector.ntp --collector.tcpstat --collector.processes'
pg_exporter_url: ''
pgbouncer_exporter_url: ''
```

Removed option:

```yaml
exporter_binary_install
```

Structures affected: `pg_default_roles`, `pg_users`, `pg_databases`. Also fixed the `pg_default_privilegs` typo → `pg_default_privileges`.

## Monitor-Only Mode

When you just want Pigsty’s observability without touching the way databases were provisioned, run the `monly` flow. Infra still gets bootstrapped on the meta node via `./infra.yml`, but database nodes skip the provisioning playbooks and only run `./pgsql-monitor.yml`. Config gets much shorter—most of the time you only keep infra vars and a handful of monitoring knobs.

## Database Provisioning Interface

`pg_databases` now exposes owner/template/encoding/locale/connlimit/allowconn knobs plus `revokeconn` (strip `CONNECT` from `public`) and inline comments. Use `./pgsql-createdb.yml -e pg_database=<name>` to create or mutate live databases; the generated SQL lives inside `/pg/tmp/pg-db-<name>.sql` on the primary.

## User Provisioning Interface

`pg_users` swapped `username` → `name`, `groups` → `roles`, and exploded `options` into discrete flags (`login`, `superuser`, `createdb`, `createrole`, `inherit`, `replication`, `bypassrls`, `connlimit`). Users can also get `expire_at` / `expire_in` timers plus `pgbouncer` defaults to `false`. Apply changes through `./pgsql-createuser.yml -e pg_user=<name>` which renders `/pg/tmp/pg-user-<name>.sql` on the primary.
