---
title: "Pigsty v4.4：克隆、分叉、回到过去"
linkTitle: "克隆、分叉、回到过去"
date: 2026-07-11
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.4.0)）
summary: >
  Pigsty v4.4 随 Pig 1.5.1 把数据库克隆、实例分叉与时间点恢复收进一套可预览、可确认、可验证的命令行接口；同时交付 PostgreSQL 18.4、531 个扩展和 14 组离线平台。
series: [Pigsty]
tags: [Pigsty]
---

Pigsty v4.4 正式发布。

如果说 v4.2 的主题是“十二内核”，v4.3 的主题是“扩展密度”，那么 v4.4 要讲的是另一件事：**一把 PIG，怎样管住数据库运维。**

PostgreSQL 18.4、531 个扩展、PG19 beta 模板与十四组离线制品构成了这一版的发行底座；真正的新东西来自 Pig 1.5。
1.5.0 完成了 PostgreSQL 日常运维命令面的重构，1.5.1 又补齐 PG19 beta 的显式构建开关、内核分支与仓库支持。
克隆数据库、分叉实例、执行时间点恢复，这些原来散落在 Ansible、Shell、Patroni 与 pgBackRest 里的动作，现在有了一套统一的命令行接口。

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) | [**发布注记**](https://pigsty.cc/docs/about/release/#v440)


------

## Pig 1.5：先把职责分清楚

`pig` 最早只是 PostgreSQL 扩展包管理器，后来逐步承担 Pigsty 安装、软件仓库与 PostgreSQL 管理工作。到了 1.5，它已经不只是“能执行很多命令”，而是开始形成一套清晰的 PostgreSQL 操作界面。

这一轮最重要的变化不是命令数量，而是**职责边界**：

| 命令         | 边界               | 典型用途                                       |
|:-----------|:-----------------|:-------------------------------------------|
| `pig pg`   | 本地 PostgreSQL 原语 | 启停、状态、连接、维护、数据库克隆与本地 PGDATA 分叉             |
| `pig pt`   | Patroni 集群操作     | 重启、重建副本、切主、故障转移、配置与日志                      |
| `pig pb`   | pgBackRest 低层原语  | 备份、仓库、备份集、清理与底层 restore                    |
| `pig pitr` | 恢复编排             | 协调 Patroni、PostgreSQL 与 pgBackRest 完成 PITR |

这张表的意义很实在：以前靠 DBA 背下来的 SOP——什么时候停 Patroni、什么时候调用 pgBackRest、恢复后能不能启动——现在写进命令本身。高风险操作都沿着同一条链路推进：

> `state → plan → precheck → execute → verify → result → next_actions`

人、脚本和 Agent 因此共用一套入口。Agent-Native 的关键不在 JSON，而在危险动作先有计划，执行后有验证，失败时知道下一步。


------

## 克隆：给单个数据库开一个分支

PostgreSQL 18 带来的 `file_copy_method=clone`，配合 XFS 等支持 CoW 的文件系统，可以在极低成本下克隆一个大数据库。Pigsty v4.0 已经通过 IaC 提供数据库克隆，并以 `/pg/bin/pg-fork` 提供实例分叉；v4.4 的变化，是把数据库克隆做成真正适合日常使用的命令：`pig pg clone`。

```bash
pig pg clone meta meta_dev --plan   # 先查看计划
pig pg clone meta meta_dev -y       # 创建数据库副本
```

当 PostgreSQL 版本、`file_copy_method` 与底层文件系统满足条件时，数据库文件可以通过 CoW 快速克隆；否则仍然可以退化为普通模板复制。Pig 会在计划里告诉你源库、目标库、连接方式、文件系统条件和风险。

这里有一个经常被忽略的边界：`CREATE DATABASE ... TEMPLATE` 会终止源库现有会话。换句话说，数据库克隆虽然快，却不是毫无影响。`--plan` 的意义，就是在真正动手前把这些副作用摊开给你看。

对于开发测试、数据分析、模型实验和 Agent 反事实推演来说，这种廉价分支非常实用。生产库保持不动，实验在副本里进行；做坏了直接删除，再开一个新的分支即可。详细用法可以参考《[瞬间克隆 PostgreSQL 数据库，无需黑魔法](/pg/pg-pig-clone/)》。


------

## 分叉：给整个实例做一个沙箱

数据库 Clone 解决的是单库副本，而 `pig pg fork` 处理的是整个 PostgreSQL 实例，也就是 PGDATA 级别的物理分叉。

```bash
pig pg fork init dev --start        # 分叉为 /pg/data-dev 并启动
pig pg fork list                    # 查看本地分叉实例
pig pg fork stop dev                # 停止分叉实例
```

Pig 会为受管分叉写入元数据，并提供 list、start、stop、rm 等生命周期命令。它特别适合两类场景：一类是从当前实例快速创建隔离沙箱；另一类是事故恢复前先分叉一份数据，在旁路实例上验证恢复目标和数据状态。

Fork 只管理本地 PGDATA，不自动接入 Patroni、systemd、VIP 与业务流量，也不处理外部表空间、远程 WAL 和备份保留。需要跨节点、归档与完整 HA 语义时，仍然回到 pgBackRest、Patroni 和 Pigsty 的集群工作流。


------

## 回到过去：恢复首先是一份计划

数据库恢复最危险的地方，从来不是缺一条命令，而是步骤太多、边界太模糊，而且人在事故压力下最容易犯错。

Pig 1.5 把低层恢复与高层编排明确拆开：

- `pig pb restore` 是 pgBackRest 的低层 restore 原语，只负责文件与恢复目标。
- `pig pitr` 是面向 Pigsty / Patroni 环境的恢复编排入口，负责协调 Patroni、PostgreSQL 与 pgBackRest。

```bash
pig pitr -t "2026-07-10 12:00:00+08" --plan
pig pitr -t "2026-07-10 12:00:00+08" -y
```

恢复命令现在必须显式指定一个目标：最新状态、备份一致点、时间、LSN、事务 ID 或命名恢复点，不能把“没写目标”解释成某个危险默认值。结构化输出也不再充当确认；自动化执行破坏性操作时，必须明确传入 `-y/--yes`。

对于托管数据目录，`pig pitr` 会检查环境、停止 Patroni 与 PostgreSQL、执行 pgBackRest restore、按策略启动 PostgreSQL 并验证恢复状态，最后给出后续动作。它不会擅自把节点重新接回 Patroni，也不会替你完成 failover、VIP 或流量切换——恢复后的数据必须先由人或上层自动化确认。

它并不承诺“无脑一键恢复”，只是把事故现场最容易出错的 SOP 固化下来：DBA 可以先看计划，Agent 也不至于越权。


------

## PostgreSQL 18.4、19 beta 与 531 个扩展

运维接口是这一版的主线，但发行版的基本盘也没有停下。

Pigsty v4.4 将 **PostgreSQL 18.4** 设为生产默认版本，同时增加一个精简的 **PostgreSQL 19 beta** 评估模板。两者的定位刻意分开：PG18.4 是完整生产路径；PG19 模板接入 PGDG 测试仓库，只安装最小运行时，不安装扩展，也暂时禁用尚未理解 PG19 beta1 控制文件格式的内置 pgBackRest 2.58。

这意味着你可以提前观察 PG19，但不会误把 beta 试用能力当成生产支持。发行版既要追得快，也要清楚地告诉用户哪里可以放心用，哪里只是尝鲜。

扩展目录则从 v4.3 的 **510** 增加到 **531**。21 个新增扩展里，挑三个方向来说：`pg_ducklake` 把 DuckDB、Parquet 与湖仓能力带进 PostgreSQL；`pg_stat_plans` 与 `pg_stat_backtrace` 补强查询计划和进程调用栈观测；`pgmnemo` 与 `psql_bm25s` 分别面向 Agent 记忆和 BM25 全文检索。其他扩展和完整版本表放在文末提交注记里。

与此同时，OrioleDB 扩展到 PG16/17/18 并将 PG18 作为默认，pgEdge 覆盖 PG15-18，Babelfish 覆盖 PG17/18，IvorySQL 进入 5.x，AgensGraph 更新到 PG17，Cloudberry 与 PolarDB 也完成了路径和软件包重整。

这些细节看起来杂，但这就是发行版的工作：把 PostgreSQL 主线、扩展生态与内核分支同时拉到一个可用、可安装、可升级的状态。


------

## 发行版的价值：把十四组矩阵跑通

一个包能编译出来，不等于一个发行版可以交付。真正困难的是把操作系统、架构、仓库、依赖、安装流程和运行状态一起跑通。

v4.4 的离线矩阵覆盖七个操作系统基线：EL 9.7 / 10.1、Debian 12.14 / 13.5，以及 Ubuntu 22.04.5 / 24.04.4 / 26.04.0；每个版本同时覆盖 `x86_64` 与 `aarch64`，总计 14 组组合。所有 14 次离线部署测试最终都以 `failed=0`、`unreachable=0` 完成。

这轮测试顺手抓出了 EL10 provider 冲突、Debian / Ubuntu 装包意外启动服务、VirtualBox 新镜像网卡等一批“只会在真机上出现”的问题。VIP 网卡现在可以根据节点主 IP 自动发现，应用敏感配置不再出现在 Ansible 输出里，`.env` 文件权限也收紧到 `0600`。

pgBackRest、Patroni、dnsmasq、HAProxy、etcd 与 Supabase 的升级注意事项，统一放在文末兼容性清单中。EL8 仍然支持在线安装，但不再提供 v4.4 离线包。这里必须区分“在线兼容”与“离线制品已经验收”——后者在 v4.4 中就是明确的十四组。


------

## 其他值得一提的改动

**应用模板**：新增 Immich、Maybe、JumpServer，并集中更新 Supabase、Dify、InsForge、Registry、Jupyter、Kong、Odoo、Teable、Mattermost 等应用栈和启动脚本。

**Supabase**：Analytics 迁移到独立的 `_supabase` 数据库与 `_analytics` 模式；旧版独立 FerretDB Compose 模板被移除，但 Pigsty 的 FERRET 模块仍然保留。

**基础设施门户**：重新设计响应式导航、暗色模式、服务入口与部署拓扑信息。它仍然只负责观测与访问，管理继续通过 IaC 与 CLI 完成。

**VIBE**：实验性模块支持按需安装 Codex CLI，并将 `AGENTS.md` 作为规范化的 Agent 指南。Codex 是可选支持，Claude Code 仍然是默认管理的编码 Agent。


------

## 写在最后

从 v4.0 的“为 Agent 而生”到 v4.4，Pigsty 一直在做同一件事：让 Agent 能动手，但不能乱来。克隆、分叉与 PITR 把这件事落到了数据库最危险的操作上——先给计划，条件不对就拒绝，做完还要验证。

**把复杂留给发行版，把确定性交给用户。** 这就是 v4.4。

下面附完整的 v4.4.0 提交注记与软件包变更，方便按需查阅。


--------

## v4.4.0 提交注记

```bash
curl -fsSL https://repo.pigsty.cc/get | bash -s v4.4.0
```

**68 个提交**，307 个文件变更，+9,337 / -11,719 行（`v4.3.0..v4.4.0`）。

**亮点特性**

- **PostgreSQL 18.4 / 19 beta**：PostgreSQL 18.4 现已成为生产默认版本，并提供精简的 PostgreSQL 19 beta 模板用于评估。
- **531 个扩展与内核更新**：扩展目录新增 21 个扩展，并在支持的平台矩阵上更新主要 PostgreSQL 内核变体。
- **Pig 1.5.1 与更安全的运维**：新增克隆、分叉与 PITR 工作流，并引入 VIP 网卡自动发现、pgBackRest Zstandard 压缩和独立的 Patroni 日志采集。
- **安全、应用与工具**：加固敏感配置处理与仓库安全自动化，增加应用模板，重新设计基础设施门户，并提供可选的 Codex 支持。
- **平台验证**：七个操作系统基线在 `x86_64` 与 `aarch64` 上的 14 组离线部署测试全部通过。

**兼容性变化**

- 新生成的 pgBackRest 配置改用 `compress-type=zst`；重新渲染前请保留有意设置的本地自定义项。[#744](https://github.com/pgsty/pigsty/issues/744)
- Patroni 日志改用 `/pg/log/patroni` 与 `job=patroni`；使用旧 syslog 选择器的自定义日志查询和告警规则需要同步更新。
- VIP 接口默认值改为 `auto`，dnsmasq 记录迁移到 `/etc/dnsmasq.d/pigsty`，同时 Pigsty 开始管理 `/etc/default/haproxy`；非标准网络环境应保留显式覆盖配置。
- etcd 默认后端配额从 16 GiB 降至 8 GiB；应用新配置前请先检查现有后端用量。
- `pig` 自动化脚本执行破坏性命令时必须传入 `-y/--yes`；`pig pb restore` 与 `pig pitr` 均要求指定且仅指定一个恢复目标。参见 [`pig` v1.5](https://pigsty.cc/docs/pig/release/#v150) 发布说明。
- Supabase Analytics 改用 `_supabase` 数据库与 `_analytics` 模式；现有部署切换新版栈前应先创建这些对象。

**安全与运维**

- `pg-pitr` 包装脚本加入更安全的恢复目标选择、时间线与 dry-run 支持，并加强对不安全恢复目标的检查。
- Ansible 输出不再显示应用敏感配置，生成的 `.env` 文件权限设为 `0600`，Grafana 也不再打印管理员密码。
- `dbsu` sudo 策略增加受控的日志查看权限；仓库同时加入安全策略、CodeQL、Dependabot、锁定 GitHub Actions 依赖版本与发布签名自动化。

**应用与工具**

- 新增 Immich、Maybe 与 JumpServer 模板，并更新 Supabase、Dify、InsForge、Registry、Jupyter、Kong、Odoo、Teable、Mattermost 及相关启动脚本。
- 重新设计中英双语基础设施门户；实验性 VIBE 模块支持按需安装 Codex CLI，Claude Code 仍是其默认托管编码代理。
- 移除旧版 FerretDB Compose 模板；FERRET 模块仍然可用。

**问题修复**

- 修复 EL10 PostgreSQL/libpq 软件包提供者冲突、EPEL 路径处理和 PGDG 小版本仓库规则。[#752](https://github.com/pgsty/pigsty/issues/752)
- `bootstrap` 过程会复用已有 `/www` 目录，并修复 Redis Sentinel HA 密码渲染问题。[#753](https://github.com/pgsty/pigsty/issues/753) [#748](https://github.com/pgsty/pigsty/issues/748)
- 修正 `pg_http`、`pg_gzip`、`apache-age` 与 `odbc_fdw` 的 RPM 包名和软件包分组。[#750](https://github.com/pgsty/pigsty/issues/750)
- 避免 Debian 与 Ubuntu 安装软件包时意外启动服务，并改进 EL9 aarch64 Patroni 包处理。
- 修复 VirtualBox 私有网络路由与默认网卡选择。
- 修复 shell 兼容性与 Vector 日志生命周期问题，以及 PG19 `io_workers`、Teable HBA 和若干应用运行时默认值。

**PostgreSQL 与扩展软件包变更**

本版本新增 21 个扩展，更新 PostgreSQL 18.4 软件包图谱，引入 PostgreSQL 19 beta 模板，并刷新主要内核变体。以下版本以最终仓库元数据为准；纳入离线包的版本同时与 v4.4.0 制品核对。PG 大版本范围表示扩展目录与软件仓库的覆盖范围。

[PostgreSQL RPM 变更](https://pigsty.cc/docs/repo/pgsql/rpm/) · [PostgreSQL DEB 变更](https://pigsty.cc/docs/repo/pgsql/deb/) · [基础设施软件包变更](https://pigsty.cc/docs/repo/infra/log/)

| 包名                    | 旧版本           | 新版本                            | 备注                                      |
|-----------------------|---------------|--------------------------------|-----------------------------------------|
| `polardb-17`          | `17.9.1.0`    | `17.10.1.0`                    | PG 17；新增 RPM 包                          |
| `agensgraph-17`       | `2.16.0`      | `2.17.0`                       | PG 17.10                                |
| `openhalodb-14`       | `1.0-beta`    | `1.0-2`                        | OpenHaloDB                              |
| `babelfish-17`        | `5.4.0`       | `5.4.0`                        | PG 17.7；重新构建                            |
| `babelfish-18`        | -             | `6.0.0`                        | PG 18.3                                 |
| `pgedge`              | `17.9 / 18.3` | `15.18 / 16.14 / 17.10 / 18.4` | 新增 PG 15/16；更新 PG 17/18；Spock 5.0.10    |
| `ivorysql-18`         | `5.0`         | `5.4`                          | PG 18；新增 RPM 包                          |
| `cloudberry`          | `2.1.0-1`     | `2.1.0-2 / 2.1.0-3`            | DEB/RPM 重新构建；RPM 路径为 `/usr/cloudberry`  |
| `cloudberry-backup`   | `2.1.0-1`     | `2.1.0-2 / 2.1.0-3`            | 备份子包                                    |
| `cloudberry-pxf`      | `2.1.0-1`     | `2.1.0-2 / 2.1.0-3`            | PXF 子包                                  |
| `pg_ducklake`         | -             | `1.0.0`                        | PG 14-18                                |
| `psql_bm25s`          | -             | `0.4.13`                       | BM25 检索；PG 17-18                        |
| `mongo_fdw`           | `5.5.3`       | `5.5.3`                        | 新增 DEB 打包；已有 PGDG RPM；PG 14-18          |
| `multicorn`           | `3.2`         | `3.2`                          | 新增 DEB 打包；已有 PGDG RPM；PG 14-18          |
| `pg_orca`             | -             | `1.0.0`                        | 仅 PG 18                                 |
| `pg_sorted_heap`      | -             | `0.14.0`                       | PG 16-18                                |
| `pg_stl`              | -             | `1.0.0`                        | PG 16-18                                |
| `fsm_core`            | -             | `1.1.0`                        | PG 15-18                                |
| `pg_projection`       | -             | `1.0.0`                        | PG 14-18                                |
| `graph`               | -             | `0.1.7`                        | PG 14-18                                |
| `jsonschema`          | -             | `0.1.9`                        | PG 14-18                                |
| `pg_durable`          | -             | `0.2.2`                        | PG 14-18                                |
| `pg_stat_log`         | -             | `0.1`                          | 仅 PG 18                                 |
| `pg_stat_plans`       | -             | `2.1.0`                        | PG 16-18                                |
| `pg_task`             | `1.0.0`       | `2.1.29`                       | PG 14-18；修复 pcre2grep 依赖                |
| `pg_stat_backtrace`   | -             | `1.0.0`                        | PG 14-18；依赖 libunwind                   |
| `pg_mockable`         | -             | `1.1.0`                        | PG 14-18                                |
| `db2fce`              | -             | `0.0.17`                       | PG 14-18                                |
| `pg_uuid_v8`          | -             | `1.0.0`                        | PG 14-18                                |
| `pg_extra_time`       | `2.0.0`       | `2.1.0`                        | PG 14-18                                |
| `pg_pinyin`           | `0.0.2`       | `0.0.4`                        | PG 14-18                                |
| `passwordpolicy`      | -             | `2.0.5`                        | PG 14-18                                |
| `pgdisablelogerror`   | -             | `1.0`                          | PG 14-18                                |
| `plpgsql_wrap`        | -             | `1.0`                          | PG 14-18                                |
| `timescaledb`         | `2.26.4`      | `2.28.2`                       | PG 15-18                                |
| `documentdb`          | `0.110`       | `0.113`                        | PG 15-18                                |
| `citus`               | `14.0.0-4`    | `14.1.0`                       | PG 16-18                                |
| `pgvector`            | `0.8.2`       | `0.8.4`                        | PG 14-18                                |
| `orioledb`            | `1.7-beta15`  | `1.8-beta16`                   | 面向 PG 16/17/18 构建                       |
| `pg_search`           | `0.23.1`      | `0.24.0`                       | PG 15-18                                |
| `pg_textsearch`       | `1.1.0`       | `1.2.0`                        | BM25 全文检索；PG 17-18                      |
| `storage_engine`      | `1.3.4`       | `2.4.0`                        | 升级到 PGXN 2.x；PG 15-18                   |
| `pg_clickhouse`       | `0.2.0`       | `0.3.2`                        | PGXN 版本更新；ClickHouse 集成                 |
| `provsql`             | `1.2.3`       | `1.10.0`                       | PGXN 版本更新；PG 14-18                      |
| `pgclone`             | `4.0.0`       | `4.3.2`                        | PGXN 版本更新；PG 14-18                      |
| `biscuit`             | `2.2.2`       | `2.4.0` DEB / `2.4.1` RPM      | PG 16-18                                |
| `pgmnemo`             | `0.7.2`       | `0.12.1`                       | PG 14-18                                |
| `rdf_fdw`             | `2.5.0`       | `2.6.0`                        | PG 14-18；libcurl 兼容性补丁                  |
| `roaringbitmap`       | `1.1.0`       | `1.2.0-2`                      | PG 14-18；修复 llvm-lto 打包                 |
| `plpgsql_check`       | `2.9.0`       | `2.9.2`                        | PG 14-18                                |
| `timescaledb_toolkit` | `1.22.0`      | `1.23.0`                       | PG 15-18；pgrx 0.18.1                    |
| `wrappers`            | `0.6.0`       | `0.6.1`                        | PG 14-18；pgrx 0.18.1                    |
| `pgrdf`               | `0.5.0`       | `0.6.4`                        | PG 14-17；pgrx 0.18.1                    |
| `pg_graphql`          | `1.5.12`      | `1.6.1`                        | PG 14-18；pgrx 0.18.1                    |
| `pg_anon`             | `3.0.13`      | `3.1.1`                        | PG 14-18；pgrx 0.18.1                    |
| `pg_kazsearch`        | `2.0.0`       | `2.2.0`                        | PG 16-18；pgrx 0.18.1                    |
| `pg_session_jwt`      | `0.4.0`       | `0.5.0`                        | PG 14-18；pgrx 0.18.1                    |
| `pg_tzf`              | `0.2.4`       | `0.3.0`                        | PG 14-18；pgrx 0.18.1                    |
| `pg_vectorize`        | `0.26.1`      | `0.26.2`                       | PG 14-18；pgrx 0.18.1                    |
| `pglinter`            | `1.1.2`       | `2.0.0`                        | PG 14-18；pgrx 0.18.1                    |
| `pgmqtt`              | `0.1.0`       | `0.3.0`                        | PG 14-18；pgrx 0.18.1                    |
| `etcd_fdw`            | `0.0.0`       | `0.0.1`                        | PG 14-18；pgrx 0.18.1                    |
| `pg_http`             | `1.7.0`       | `1.7.1`                        | PG 14-18；RPM 包重命名为 `pgsql_http_$v`      |
| `pg_gzip`             | `1.0.0`       | `1.1.0`                        | PG 14-18；RPM 包重命名为 `pgsql_gzip_$v`      |
| `age`                 | `1.7.0`       | `1.7.0`                        | PG 17-18；RPM 包重命名为 `age_$v`             |
| `pg_trickle`          | `0.40.0`      | `0.81.0`                       | 仅 PG 18                                 |
| `re2`                 | `0.1.1`       | `0.4.0`                        | PG 16-18                                |
| `pg_background`       | `1.9.2`       | `2.0.2` DEB / `2.0` RPM        | PG 14-18                                |
| `firebird_fdw`        | `1.4.1`       | `1.4.2`                        | PG 14-18                                |
| `pg_net`              | `0.20.2`      | `0.20.3`                       | DEB 与 EL10 RPM 更新；EL8/9 RPM 保持为 `0.9.2` |
| `pg_dirtyread`        | `2.7`         | `2.8`                          | PG 14-18                                |
| `pg_stat_ch`          | `0.3.6`       | `0.3.6`                        | PG 16-18；重新构建                           |
| `pggraph`             | `0.1.5`       | `0.1.7`                        | PG 14-18                                |
| `pgsql_tweaks`        | `1.0.2`       | `1.0.5`                        | PG 14-18；PGDG RPM 同时包含 `1.0.3`          |
| `pgfincore`           | `1.3.1`       | `1.4.0`                        | PG 14-18                                |
| `toastinfo`           | `1.5`         | `1.7`                          | PG 14-18                                |
| `pg_ivm`              | `1.14`        | `1.15` DEB / `1.14` RPM        | PG 14-18                                |
| `timeseries`          | `0.2.0`       | `0.2.1`                        | PG 14-18                                |
{.stretch-last}

**基础设施软件包变更**

| 软件包                          | 旧版本              | 新版本              | 备注                    |
|------------------------------|------------------|------------------|-----------------------|
| `pig`                        | `1.4.1`          | `1.5.1`          |                       |
| `pg_exporter`                | `1.2.2`          | `1.3.0`          |                       |
| `pgschema`                   | `1.9.0`          | `1.12.0`         |                       |
| `pgstream`                   | `1.0.1`          | `1.1.1`          |                       |
| `pg-hardstorage`             | -                | `1.0.8`          |                       |
| `codex`                      | `0.125.0`        | `0.144.1`        |                       |
| `claude`                     | `2.1.123`        | `2.1.206`        |                       |
| `opencode`                   | `1.14.30`        | `1.17.18`        |                       |
| `agentsview`                 | `0.26.0`         | `0.37.5`         |                       |
| `genai-toolbox`              | `1.1.0`          | `1.6.0`          | 软件包名为 `mcp-toolbox`   |
| `crush`                      | `0.64.0`         | `0.84.0`         |                       |
| `code`                       | `1.118.1`        | `1.128.0`        |                       |
| `code-server`                | `4.117.0`        | `4.127.0`        |                       |
| `victoria-metrics`           | `1.142.0`        | `1.147.0`        |                       |
| `victoria-metrics-cluster`   | `1.142.0`        | `1.147.0`        |                       |
| `vmutils`                    | `1.142.0`        | `1.147.0`        |                       |
| `victoria-logs`              | `1.50.0`         | `1.51.0`         |                       |
| `vlagent`                    | `1.50.0`         | `1.51.0`         |                       |
| `vlogscli`                   | `1.50.0`         | `1.51.0`         |                       |
| `victoria-traces`            | `0.8.2`          | `0.9.4`          |                       |
| `prometheus`                 | `3.11.3`         | `3.13.1`         |                       |
| `alertmanager`               | `0.32.1`         | `0.33.1`         |                       |
| `pushgateway`                | `1.11.2`         | `1.11.3`         |                       |
| `node_exporter`              | `1.11.1`         | `1.11.1`         | 补齐 tarball 缓存；修正版本元数据 |
| `redis_exporter`             | `1.82.0`         | `1.86.0`         |                       |
| `mongodb_exporter`           | `0.50.0`         | `0.51.0`         |                       |
| `grafana`                    | `13.0.1`         | `13.1.0`         |                       |
| `grafana-victorialogs-ds`    | `0.26.3`         | `0.29.0`         |                       |
| `grafana-victoriametrics-ds` | `0.24.0`         | `0.25.2`         |                       |
| `vector`                     | `0.55.0`         | `0.56.0`         |                       |
| `minio`                      | `20260417000000` | `20260618000000` |                       |
| `seaweedfs`                  | `4.22`           | `4.39`           |                       |
| `rustfs`                     | `1.0.0-b1`       | `1.0.0-b8`       | 预发布版本线                |
| `duckdb`                     | `1.5.2`          | `1.5.4`          |                       |
| `kafka`                      | `4.2.0`          | `4.3.1`          |                       |
| `etcd`                       | `3.6.10`         | `3.6.13`         |                       |
| `restic`                     | `0.18.1`         | `0.19.1`         |                       |
| `juicefs`                    | `1.3.1`          | `1.4.0`          |                       |
| `tigerbeetle`                | `0.17.2`         | `0.17.9`         |                       |
| `tigerfs`                    | `0.6.0`          | `0.7.0`          |                       |
| `caddy`                      | `2.11.2`         | `2.11.4`         |                       |
| `cloudflared`                | `2026.2.0`       | `2026.7.1`       |                       |
| `headscale`                  | `0.28.0`         | `0.29.2`         |                       |
| `v2ray`                      | `5.48.0`         | `5.51.2`         |                       |
| `nodejs`                     | `24.15.0`        | `24.18.0`        |                       |
| `golang`                     | `1.26.2`         | `1.26.5`         |                       |
| `hugo`                       | `0.161.1`        | `0.164.0`        |                       |
| `uv`                         | `0.11.8`         | `0.11.28`        |                       |
| `rclone`                     | `1.73.5`         | `1.74.4`         |                       |
| `asciinema`                  | `3.2.0`          | `3.2.1`          |                       |
| `stalwart`                   | `0.16.2`         | `0.16.12`        |                       |
| `maddy`                      | `0.9.3`          | `0.9.5`          |                       |
| `dblab`                      | `0.38.0`         | `0.43.0`         |                       |
| `npgsqlrest`                 | `3.12.0`         | `3.20.0`         |                       |
| `postgrest`                  | `14.10`          | `14.14`          |                       |
| `sabiql`                     | `1.11.1`         | `1.14.0`         |                       |
| `pev2`                       | `1.21.0`         | `1.22.0`         |                       |
| `rainfrog`                   | `0.3.18`         | `0.3.19`         |                       |
{.stretch-last}

**验证与校验和**

覆盖 EL9/10、Debian 12/13 与 Ubuntu 22/24/26，横跨 `x86_64` 和 `aarch64` 的 14 组离线部署测试全部完成，结果均为 `failed=0`、`unreachable=0`；EL8 仅继续支持在线安装。

以下 MD5 与最终发布清单一致；GitHub 也会为每个已上传制品记录 SHA-256 摘要。

```bash
7de8b932412f1863fd9c033a7be355d7  pigsty-pkg-v4.4.0.d12.aarch64.tgz
2e5006a8d35eb1c087dc0ed11cf14d14  pigsty-pkg-v4.4.0.d12.x86_64.tgz
955308c00d3890f6e82a6a83bc624760  pigsty-pkg-v4.4.0.d13.aarch64.tgz
350f31c66de0aafff3bd91c2c9d740a0  pigsty-pkg-v4.4.0.d13.x86_64.tgz
0b4817a8edbab0bdf37ecee730fb0412  pigsty-pkg-v4.4.0.el10.aarch64.tgz
4584a61e4456749e68d86e4817cfe526  pigsty-pkg-v4.4.0.el10.x86_64.tgz
21621daf510a532829c36464d48f9198  pigsty-pkg-v4.4.0.el9.aarch64.tgz
504afd5030e2738a25e1b4c570d0e654  pigsty-pkg-v4.4.0.el9.x86_64.tgz
461c999424dee587ca33fe1a63df40d7  pigsty-pkg-v4.4.0.u22.aarch64.tgz
20ccc5ab8f9f4648b05bcd304f9fb5fc  pigsty-pkg-v4.4.0.u22.x86_64.tgz
d092c48ee55116ed5e2c99a3d909ccdd  pigsty-pkg-v4.4.0.u24.aarch64.tgz
24fa5399d8421305961fcaf91325b382  pigsty-pkg-v4.4.0.u24.x86_64.tgz
36f69b699d8b3041d35384970e157631  pigsty-pkg-v4.4.0.u26.aarch64.tgz
330047d117b20f04317dce506edd5d9a  pigsty-pkg-v4.4.0.u26.x86_64.tgz
3077203c0c656ec99abc32b227f6566b  pigsty-v4.4.0.tgz
```
