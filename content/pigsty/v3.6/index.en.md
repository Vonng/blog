---
title: "Pigsty v3.6: Docs + PITR Boost"
linkTitle: "Pigsty v3.6 Release Notes"
date: 2025-07-25
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.6.0)）
summary: >
  New docs, Percona TDE, Supabase polish, and a one-command PG PITR playbook headline Pigsty 3.6.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.6.0

Pigsty 3.6 is the last major release before 4.0, focusing on refactors and UX: PG/MinIO/Etcd roles were rewritten, Percona PG TDE joins the kernel list, Supabase self-hosting gets log fixes, and a `pgsql-pitr` playbook automates point-in-time recovery. Install flow shrinks to download→configure→install, with online installers favored by default.

Supabase setups now default to faster Docker registries, templates remove destructive database tasks, and the new doc site (Next.js + Fumadocs) is live at https://doc.pgsty.com. PITR automation pauses HA, restores from pgBackRest, and re-enables Patroni. Etcd/MinIO roles were rebuilt, `infra` data moves under `/data/infra`, and pig CLI integration continues.

--------

## v3.6.0 Release Notes

- Highlights: new doc site, `pgsql-pitr` playbook, Percona PG TDE kernel, Supabase WTS improvements, simplified install (online-first, three steps), Docker default on meta node.
- Design tweaks: Etcd/MinIO rewrites, bootstrap merges, online repos default, new doc site, `infra` data relocation, pig-based workflows for etcd/pitr scripts.
- Monitoring: HTTP-mode MinIO pipes, vector-based logs, admin templates reorganized, tuned profiles for NVMe, new `pgactive` extension, default storage layout adjustments.
- Fixes: pgbouncer config, Docker group, Grafana plugin caching, Promtail/Loki state issues, numerous Ansible compatibility fixes.
