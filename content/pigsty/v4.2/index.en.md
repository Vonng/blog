---
title: "Pigsty v4.2: Release Notes Placeholder"
linkTitle: "Pigsty v4.2 Placeholder"
date: 2026-02-28
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v4.2.0))
summary: >
  This is the English placeholder post for Pigsty v4.2. The content is temporarily filled with the v4.2.0 release notes and will be replaced later.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.2.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v420)

> This is a placeholder draft. The current content is copied from the v4.2.0 release notes and will be replaced with the final English blog post.

--------

## v4.2.0 Commit Note

**Highlights**

- Aligned with PostgreSQL out-of-band minor updates: 18.3, 17.9, 16.13, 15.17, 14.22.
- Total PostgreSQL extension coverage reaches 461 packages.
- Kernel updates across Babelfish, AgensGraph, pgEdge, OriolePG, OpenHalo, and Cloudberry.
- Babelfish template now uses a Pigsty-maintained PG17-compatible build, with no WiltonDB repo dependency.
- Supabase images and self-hosted templates are refreshed to the latest stack, using Pigsty-maintained [pgsty/minio](https://github.com/pgsty/minio).

**Major Changes**

- `mssql` now defaults to Babelfish PG17 (`pg_version: 17`, `pg_packages: [babelfish, pgsql-common, sqlcmd]`) and no longer requires an extra `mssql` repo.
- Kernel install paths are normalized in `pg_home_map`: `mssql -> /usr/babelfish-$v/`, `gpsql -> /usr/local/cloudberry`.
- `package_map` adds a dedicated `cloudberry` mapping and fixes `babelfish*` aliases to versioned RPM/DEB package names.
- Redis data root default changes from `/data` to `/data/redis`; deployment blocks legacy defaults, while `redis_remove` keeps backward-compatible cleanup.
- `configure` now supports absolute `-o` output paths with auto-created parent directories, tri-state region detection (CN/global/offline fallback), and a fix for `behind_gfw()` hangs.
- Debian/Ubuntu default repo URL mappings (`updates/backports/security`) and China mirror components are corrected to prevent bootstrap package failures.
- Supabase stack is updated (including PostgREST `14.5` and Vector `0.53.0`) and now includes missing S3 protocol credential variables.
- Rich/Sample templates explicitly define `dbuser_meta` defaults; `node.sh` systemd completion is simplified.
- `pgbackrest` stanza initialization now retries (2 attempts, 5-second interval) to reduce lock contention with `archive-push`.
- Vibe template now ships `@anthropic-ai/claude-code`, `@openai/codex`, and `happy-coder`, and includes `age` in the default example.

**PG Software Updates**

- PostgreSQL 18.3, 17.9, 16.13, 15.17, 14.22
- [RPM Changelog 2026-02-27](https://pigsty.io/docs/repo/pgsql/rpm/#2026-02-27)
- [DEB Changelog 2026-02-27](https://pigsty.io/docs/repo/pgsql/deb/#2026-02-27)
- Core upgrades: `timescaledb 2.25.0 -> 2.25.1`, `citus 14.0.0-3 -> 14.0.0-4`, `pg_search -> 0.21.9`
- New/rebuilt: `pgedge 17.9`, `spock 5.0.5`, `lolor 1.2.2`, `snowflake 2.4`, `babelfish 5.5.0`, `cloudberry 2.0.0`
- Kernel-side updates: `oriolepg 17.11 -> 17.16`, `orioledb beta12 -> beta14`, `openhalo 14.10 -> 1.0(14.18)`

| Package             | Old Version     | New Version | Notes                                    |
|:--------------------|:----------------|:------------|:-----------------------------------------|
| `timescaledb`       | 2.25.0          | 2.25.1      |                                          |
| `citus`             | 14.0.0-3        | 14.0.0-4    | Rebuilt from the latest official release |
| `age`               | 1.7.0           | 1.7.0       | Added PG 17 support for version 1.7.0    |
| `pgmq`              | 1.10.0          | 1.10.1      | Package currently unavailable            |
| `pg_search`         | 0.21.7 / 0.21.6 | 0.21.9      | Previous RPM/DEB versions differ         |
| `oriolepg`          | 17.11           | 17.16       | OriolePG kernel update                   |
| `orioledb`          | beta12          | beta14      | Matches OriolePG 17.16                   |
| `openhalo`          | 14.10           | 1.0         | Updated and renamed, based on 14.18      |
| `pgedge`            | -               | 17.9        | New multi-master edge-distributed kernel |
| `spock`             | -               | 5.0.5       | New core pgEdge extension                |
| `lolor`             | -               | 1.2.2       | New core pgEdge extension                |
| `snowflake`         | -               | 2.4         | New core pgEdge extension                |
| `babelfishpg`       | -               | 5.5.0       | New BabelfishPG package group            |
| `babelfish`         | -               | 5.5.0       | New Babelfish compatibility package      |
| `antlr4-runtime413` | -               | 4.13        | New runtime dependency for Babelfish     |
| `cloudberry`        | -               | 2.0.0       | RPM build only                           |
| `pg_background`     | -               | 1.8         | DEB build only                           |

**Infrastructure Software Updates**

| Name                          | Old Version      | New Version      |
|:------------------------------|:-----------------|:-----------------|
| `grafana`                     | 12.3.2           | 12.4.0           |
| `prometheus`                  | 3.9.1            | 3.10.0           |
| `mongodb_exporter`            | 0.47.2           | 0.49.0           |
| `victoria-metrics`            | 1.135.0          | 1.136.0          |
| `victoria-metrics-cluster`    | 1.135.0          | 1.136.0          |
| `vmutils`                     | 1.135.0          | 1.136.0          |
| `victoria-logs`               | 1.45.0           | 1.47.0           |
| `vlagent`                     | 1.45.0           | 1.47.0           |
| `vlogscli`                    | 1.45.0           | 1.47.0           |
| `loki`                        | 3.6.5            | 3.6.7            |
| `promtail`                    | 3.6.5            | 3.6.7            |
| `logcli`                      | 3.6.5            | 3.6.7            |
| `grafana-victorialogs-ds`     | 0.24.1           | 0.26.2           |
| `grafana-victoriametrics-ds`  | 0.21.0           | 0.23.1           |
| `grafana-infinity-ds`         | 3.7.0            | 3.7.2            |
| `redis_exporter`              | 1.80.2           | 1.81.0           |
| `etcd`                        | 3.6.7            | 3.6.8            |
| `dblab`                       | 0.34.2           | 0.34.3           |
| `tigerbeetle`                 | 0.16.72          | 0.16.74          |
| `seaweedfs`                   | 4.09             | 4.13             |
| `rustfs`                      | 1.0.0-alpha.82   | 1.0.0-alpha.83   |
| `uv`                          | 0.10.0           | 0.10.4           |
| `kafka`                       | 4.1.1            | 4.2.0            |
| `npgsqlrest`                  | 3.7.0            | 3.10.0           |
| `postgrest`                   | 14.4             | 14.5             |
| `caddy`                       | 2.10.2           | 2.11.1           |
| `rclone`                      | 1.73.0           | 1.73.1           |
| `pev2`                        | 1.20.1           | 1.20.2           |
| `genai-toolbox`               | 0.25.0           | 0.27.0           |
| `opencode`                    | 1.1.59           | 1.2.15           |
| `claude`                      | 2.1.37           | 2.1.59           |
| `codex`                       | 0.104.0          | 0.105.0          |
| `code`                        | 1.109.2          | 1.109.4          |
| `code-server`                 | 4.108.2          | 4.109.2          |
| `nodejs`                      | 24.13.1          | 24.14.0          |
| `pig`                         | 1.1.2            | 1.3.0            |
| `stalwart`                    | -                | 0.15.5           |
| `maddy`                       | -                | 0.8.2            |

**API Changes**

- `pg_mode` now includes `agens` and `pgedge`.
- `mssql` defaults are updated to `pg_version: 17` and `pg_packages: [babelfish, pgsql-common, sqlcmd]`.
- Kernel/package alias mappings are updated in `pg_home_map` and `package_map` (Babelfish, OpenHalo, IvorySQL, Cloudberry, pgEdge family).
- `redis_fs_main` now defaults to `/data/redis`, with deployment guardrails and backward-compatible cleanup behavior.
- `configure` output path handling and region detection logic are updated, with offline fallback warnings and unified SSH probe timeouts.
- `grafana.ini.j2` is updated for Grafana 12.4 config changes and deprecations.

**Compatibility Notes**

- If existing Redis configs still use `redis_fs_main: /data`, migrate to `/data/redis` before deployment.
- Grafana 12.4 changes data link merge behavior. This release moves key links into field overrides; review custom dashboards accordingly.

**26 commits**, 122 files changed, +2,116 / -2,215 lines (`v4.1.0..v4.2.0`, 2026-02-15 ~ 2026-02-28)

**Checksums**

```bash
24a90427a7e7351ca1a43a7d53289970  pigsty-v4.2.0.tgz
d980edf5eeb0419d4f1aa7feb0100e14  pigsty-pkg-v4.2.0.d12.aarch64.tgz
24bc237d841457fbdcc899e1d0a3f87e  pigsty-pkg-v4.2.0.d12.x86_64.tgz
e395b38685e2ecbe9c3a2850876d9b7b  pigsty-pkg-v4.2.0.d13.aarch64.tgz
c5c8776f9bead9f29528b26058801f83  pigsty-pkg-v4.2.0.d13.x86_64.tgz
28ea40434bd06135fc8adc0df1c8407d  pigsty-pkg-v4.2.0.el10.aarch64.tgz
58ad715ac20dc1717d1687daecfcf625  pigsty-pkg-v4.2.0.el10.x86_64.tgz
008f955439ea311581dd0ebcf5b8bd34  pigsty-pkg-v4.2.0.el8.aarch64.tgz
2acfd127a517b09f07540f808fe9547a  pigsty-pkg-v4.2.0.el8.x86_64.tgz
58e62a92f35291a40e3f05839a1b6bc4  pigsty-pkg-v4.2.0.el9.aarch64.tgz
d311bfdf5d5f60df5fe6cb3d4ced4f9c  pigsty-pkg-v4.2.0.el9.x86_64.tgz
c98972fe9226657ac1faa7b72a22498b  pigsty-pkg-v4.2.0.u22.aarch64.tgz
44a174ee9ba030ac1ea386cf0b85f6e7  pigsty-pkg-v4.2.0.u22.x86_64.tgz
143e404f4681c7d0bbd78ef7982cd652  pigsty-pkg-v4.2.0.u24.aarch64.tgz
00dfa86f477f3adff984906211ab3190  pigsty-pkg-v4.2.0.u24.x86_64.tgz
```
