---
title: "Pigsty v0.9: CLI + Logs"
linkTitle: "Pigsty v0.9 Release Notes"
date: 2021-05-01
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.9.0)）
summary: >
  One-click installs, a beta CLI, and Loki-based logging make Pigsty easier to land.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.9.0

## New Stuff

- **One-liner install**: `curl -fsSL https://pigsty.cc/install | bash` bootstraps everything.
- **`pigsty-cli`**: wraps the common Ansible playbooks so you stop copy-pasting command lines. Still beta but already handy.
- **Loki + Promtail**: Postgres, pgbouncer, and Patroni logs stream into Grafana with metrics extracted from log volume. `infra-loki.yml` and `pgsql-promtail.yml` wire things up.
- **Binary exporters**: grab monitoring binaries with `files/get_bin.sh` if you don't want to rely on repos.
- **Flight mode**: once the meta node is initialized you can run `bin/upgrade` to switch into a dynamic inventory using data stored inside `pg-meta`.

## Fixes

- Cleaned up HAProxy health checks that were flooding PG and Patroni logs with `connection reset` noise.
- Patroni logs now carry readable timestamps (no more millisecond fragments) and explicit time zones.
- Monitoring queries run by `dbuser_monitor` log only when slower than 1s.
- Grafana role refactor keeps the API stable, but uses CDN-hosted plugin bundles for faster installs.
- Pgbouncer user creation now handles md5 passwords properly.
- Hardened SQL templates for DB/user creation, fixed DNS orchestration edge cases, and tidied Makefile typos.

## Knob Changes

- `node_disable_swap` defaults to `false`; Pigsty no longer nukes swap by default.
- `node_sysctl_params` stops writing kernel tunables unless you explicitly set them.
- `grafana_plugin: install` now means “download from CDN if cache is missing.”
- `repo_url_packages` pulls extra RPMs from the Pigsty CDN so installs inside China work out of the box.
- `proxy_env.no_proxy` includes the CDN endpoints.
- `grafana_customize` defaults to `false`; flip it on only if you have the Pigsty Pro UI bits.
- `node_admin_pk_current` adds your current `~/.ssh/id_rsa.pub` to the admin account.
- Loki/Promtail knobs: `loki_clean`, `loki_data_dir`, `promtail_enabled`, `promtail_clean`, `promtail_port`, `promtail_status_file`, `promtail_send_url`.
