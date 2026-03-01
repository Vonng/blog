---
title: "Pigsty v4.2：12内核齐开花"
linkTitle: "Pigsty v4.2 12内核齐开花"
date: 2026-02-28
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.2.0)）
summary: >
  这是 Pigsty v4.2 中文博客占位稿，当前内容暂用 v4.2.0 发布注记填充，后续将替换为正式文章。
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.2.0) | [**发布注记**](https://pigsty.cc/docs/about/release/#v420)









--------

## v4.2.0 提交注记

**亮点特性**

- 离线小版本跟进 PostgreSQL 紧急小版本：18.3、17.9、16.13、15.17、14.22。
- PostgreSQL 扩展总数达到 461 个。
- PG 内核更新：Babelfish、AgensGraph、pgEdge、OriolePG、OpenHalo、Cloudberry。
- Babelfish 模板切换到 Pigsty 自建维护的 PG17 兼容版本，移除对 WiltonDB 仓库的依赖。
- 更新 Supabase 镜像与自建模板至最新版本，使用自行维护的 [MinIO 分支 pgsty/minio](https://github.com/pgsty/minio)

**主要变更**

- `mssql` 模板切换到 Babelfish PG17 默认：`pg_version: 17`，`pg_packages: [babelfish, pgsql-common, sqlcmd]`，并移除额外 `mssql` repo 依赖。
- `pg_home_map` 调整：`mssql` 指向 `/usr/babelfish-$v/`，`gpsql` 指向 `/usr/local/cloudberry`，统一内核路径语义。
- `package_map` 新增 `cloudberry` 独立映射，并修复 `babelfish*` 组件别名到版本化包名（RPM/DEB）。
- Redis 默认主目录从 `/data` 调整为 `/data/redis`；部署阶段阻止旧默认值继续使用，`redis_remove` 增加旧路径兼容清理。
- `configure` 支持 `-o` 绝对路径输出并自动建目录；区域探测改为三态（境内/境外/离线回退），修复 `behind_gfw()` 卡住问题。
- 修复 Debian/Ubuntu 默认仓库 URL（`updates/backports/security` 对应关系）与中国区镜像组件字段，避免节点初始化拉包失败。
- Supabase 应用栈例行升级（含 PostgREST `14.5`、Vector `0.53.0` 等）并补齐 S3 协议访问密钥变量。
- Rich/Sample 模板显式补全 `dbuser_meta` 默认值；`node.sh` 中 systemd 自动补全逻辑简化。
- `pgbackrest` 初始化增加重试（2 次、间隔 5 秒），缓解 `stanza-create` 与 `archive-push` 锁竞争失败。
- Vibe 模板更新：内置 `@anthropic-ai/claude-code`、`@openai/codex`、`happy-coder` 等 npm 工具，默认示例补入 `age` 扩展。


**PG 软件更新**

- PostgreSQL 18.3, 17.9, 16.13, 15.17, 14.22
- [RPM Changelog 2026-02-27](https://pigsty.cc/docs/repo/pgsql/rpm/#2026-02-27)
- [DEB Changelog 2026-02-27](https://pigsty.cc/docs/repo/pgsql/deb/#2026-02-27)
- 核心升级：`timescaledb 2.25.0 -> 2.25.1`，`citus 14.0.0-3 -> 14.0.0-4`，`pg_search -> 0.21.9`
- 新增/重建：`pgedge 17.9`，`spock 5.0.5`，`lolor 1.2.2`，`snowflake 2.4`，`babelfish 5.5.0`，`cloudberry 2.0.0`
- 内核配套：`oriolepg 17.11 -> 17.16`，`orioledb beta12 -> beta14`，`openhalo 14.10 -> 1.0(14.18)`

| 包名                  | 旧版本             | 新版本      | 备注                    |
|:--------------------|:----------------|:---------|:----------------------|
| `timescaledb`       | 2.25.0          | 2.25.1   |                       |
| `citus`             | 14.0.0-3        | 14.0.0-4 | 使用最新官方版本重新构建          |
| `age`               | 1.7.0           | 1.7.0    | 新增 PG 17 的 1.7.0 版本支持 |
| `pgmq`              | 1.10.0          | 1.10.1   | 当前没有该扩展包              |
| `pg_search`         | 0.21.7 / 0.21.6 | 0.21.9   | RPM/DEB 旧版本不同         |
| `oriolepg`          | 17.11           | 17.16    | OriolePG 内核更新         |
| `orioledb`          | beta12          | beta14   | 配套 OriolePG 17.16     |
| `openhalo`          | 14.10           | 1.0      | 更新并重命名，14.18          |
| `pgedge`            | -               | 17.9     | 新增多主边缘分布式内核           |
| `spock`             | -               | 5.0.5    | 新增，pgEdge 核心扩展        |
| `lolor`             | -               | 1.2.2    | 新增，pgEdge 核心扩展        |
| `snowflake`         | -               | 2.4      | 新增，pgEdge 核心扩展        |
| `babelfishpg`       | -               | 5.5.0    | 新增 BabelfishPG 包组     |
| `babelfish`         | -               | 5.5.0    | 新增 Babelfish 兼容包      |
| `antlr4-runtime413` | -               | 4.13     | 新增 Babelfish 依赖运行时    |
| `cloudberry`        | -               | 2.0.0    | 仅 RPM 构建              |
| `pg_background`     | -               | 1.8      | 仅 DEB 构建              |

**基础设施软件更新**

| 名称                           | 旧版本            | 新版本            |
|:-----------------------------|:---------------|:---------------|
| `grafana`                    | 12.3.2         | 12.4.0         |
| `prometheus`                 | 3.9.1          | 3.10.0         |
| `mongodb_exporter`           | 0.47.2         | 0.49.0         |
| `victoria-metrics`           | 1.135.0        | 1.136.0        |
| `victoria-metrics-cluster`   | 1.135.0        | 1.136.0        |
| `vmutils`                    | 1.135.0        | 1.136.0        |
| `victoria-logs`              | 1.45.0         | 1.47.0         |
| `vlagent`                    | 1.45.0         | 1.47.0         |
| `vlogscli`                   | 1.45.0         | 1.47.0         |
| `loki`                       | 3.6.5          | 3.6.7          |
| `promtail`                   | 3.6.5          | 3.6.7          |
| `logcli`                     | 3.6.5          | 3.6.7          |
| `grafana-victorialogs-ds`    | 0.24.1         | 0.26.2         |
| `grafana-victoriametrics-ds` | 0.21.0         | 0.23.1         |
| `grafana-infinity-ds`        | 3.7.0          | 3.7.2          |
| `redis_exporter`             | 1.80.2         | 1.81.0         |
| `etcd`                       | 3.6.7          | 3.6.8          |
| `dblab`                      | 0.34.2         | 0.34.3         |
| `tigerbeetle`                | 0.16.72        | 0.16.74        |
| `seaweedfs`                  | 4.09           | 4.13           |
| `rustfs`                     | 1.0.0-alpha.82 | 1.0.0-alpha.83 |
| `uv`                         | 0.10.0         | 0.10.4         |
| `kafka`                      | 4.1.1          | 4.2.0          |
| `npgsqlrest`                 | 3.7.0          | 3.10.0         |
| `postgrest`                  | 14.4           | 14.5           |
| `caddy`                      | 2.10.2         | 2.11.1         |
| `rclone`                     | 1.73.0         | 1.73.1         |
| `pev2`                       | 1.20.1         | 1.20.2         |
| `genai-toolbox`              | 0.25.0         | 0.27.0         |
| `opencode`                   | 1.1.59         | 1.2.15         |
| `claude`                     | 2.1.37         | 2.1.59         |
| `codex`                      | 0.104.0        | 0.105.0        |
| `code`                       | 1.109.2        | 1.109.4        |
| `code-server`                | 4.108.2        | 4.109.2        |
| `nodejs`                     | 24.13.1        | 24.14.0        |
| `pig`                        | 1.1.2          | 1.3.0          |
| `stalwart`                   | -              | 0.15.5         |
| `maddy`                      | -              | 0.8.2          |


**API变化**

- `pg_mode` 增加 `agens` 与 `pgedge`。
- `mssql` 默认配置改为 `pg_version: 17` + `pg_packages: [babelfish, pgsql-common, sqlcmd]`。
- `pg_home_map` 与 `package_map` 的内核/包别名映射更新（Babelfish / OpenHalo / IvorySQL / Cloudberry / pgEdge 家族）。
- `redis_fs_main` 默认值改为 `/data/redis`，并新增部署保护与移除兼容策略。
- `configure` 输出路径与区域探测逻辑更新，增加离线回退告警；SSH 探测统一超时参数。
- `grafana.ini.j2` 跟进 Grafana 12.4 新配置项与废弃项调整。

**兼容性说明**

- 存量 Redis 配置如果仍使用 `redis_fs_main: /data`，请先改为 `/data/redis` 再执行部署。
- Grafana 12.4 后 data link 合并行为变化，本版本已将关键链接下沉到字段 override 规避冲突；如有自定义看板，建议同步检查。

**26 个提交**，122 文件变更，+2,116 / -2,215 行（`v4.1.0..v4.2.0`，2026-02-15 ~ 2026-02-28）

**校验和**

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
