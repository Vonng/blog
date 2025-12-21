---
title: "Pigsty v3.2：命令行工具pig，完备ARM支持，Supabase & Grafana 加强"
linkTitle: "Pigsty v3.2 发布注记"
date: 2024-12-29
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v3.2.0)）
summary: >
  PG包管理器与Pigsty命令行工具 pig 登场，ARM64 扩展仓库，Supabase & Grafana 加强。
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.2.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v320) | [微信公众号](https://mp.weixin.qq.com/s/FBAfu9mkL2GedZRgPq8h_w)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.2.0)

Pigsty 迎来了 2024 年的最后一次发布 v3.2。本次发布带来了命令行工具 `pig`，以及完善的 ARM 扩展支持，两者合体，为用户带来 10 大主流 Linux 系统上丝滑的 PostgreSQL 交付能力。

本次发布例行修复了一系列问题，同时跟进了 Supabase 发布周的密集变化，并为 Grafana 扩展插件与数据源提供了 RPM/DEB 包。


--------

## Pig 命令行工具

Pigsty v3.2 默认提供命令行工具 [**pig**](/blog/pg/pig)，可以用来进一步简化 Pigsty 的安装部署配置过程。但 `pig` 并非仅仅是 Pigsty 的命令行工具，它还是一个可以独立使用的全功能 PostgreSQL 包管理器。

在安装 PostgreSQL 扩展插件时，面对各种发行版、各种芯片架构，总是困难重重：大把时间耗费在过时的 README、晦涩的配置脚本和随机的 GitHub 分支中翻找；又或者受困于国内网络环境，仓库缺失、镜像被墙，下载速度堪忧。

![](pig-install.jpg)

**pig** 正式登场，为打包解决所有难题。这是一个全新的、基于 Go 的包管理器，能够统一处理 PostgreSQL 及其不断扩展的扩展库，而无需陷入调试泥潭。

![](pig-ride-elephant.jpg)

Pig 本身是用 Go 编写的轻量级二进制，无依赖、易安装：只需一行命令即可完成安装。它尊重操作系统的包管理传统，不重新发明轮子，基于 yum/dnf/apt 实现包管理。

Pig 专注于跨发行版的和谐 —— 无论是在 Debian、Ubuntu 还是 Red Hat 衍生版上，都可以获得单一、流畅的安装和更新 PostgreSQL 及任何扩展的方法，无需从源代码编译或处理半成品仓库。

![](pig-repo.jpg)

如果说 [**PostgreSQL 的未来是无法阻挡的可扩展性**](/blog/pg/pg-eat-db-world)，Pig 就是帮助解锁这种能力的工具。毕竟，没有人会抱怨 PostgreSQL 实例拥有太多扩展 —— 不用的时候没有任何影响，需要时就在手边，随取随用。

![](pig-ext.jpg)


--------

## ARM 扩展仓库

Pig 的幕后支撑是一个充满稀缺扩展与新发布扩展的[**补充扩展仓库**](/blog/pg/pg-ext-repo)，因此总可以轻松获取优质扩展 —— 经过测试、精心策划并准备就绪。

在最近一个月内，Pigsty 已经为 ARM64 系统架构完成了完整的支持。对五大主流 Linux 发行版（EL8、EL9、Debian12、Ubuntu 22/24）提供了**完整**的 ARM 支持。所谓完整，是指在 AMD64 上使用的配置文件可以一模一样用在 ARM64 架构的系统上。当然存在零星例外：极个别扩展目前缺少 ARM 支持，将在后续逐一解决。

![](arm-support.jpg)

Pigsty Extension Repo 集合了 340+ 精选 PostgreSQL 扩展，编译成方便使用的 `.rpm` 和 `.deb` 包，支持多版本、多架构：

| 扩展类别 | 支持情况 |
|---------|---------|
| TimescaleDB 时序套件 | 完整支持 |
| Supabase 相关扩展 | 全套到位 |
| DuckDB 分析扩展 | 已就绪 |
| 社区新扩展 | 持续收录 |

Pigsty 搭建了一个跨发行版的流水线，将社区自研的新扩展、历久弥新的老模块，以及官方 PGDG 包整合在一起，让它们能在 Debian、Ubuntu、Red Hat 系列等各大系统上一键无缝安装。

**关键设计原则**：不造轮子，而是直接基于每个发行版原生的包管理器（YUM、APT、DNF 等），保持与官方 PGDG 仓库的版本对齐。

从底层看，这个仓库是更大范围的 Pigsty PostgreSQL 发行版一部分，但也可以在自己的环境中独立使用，无需全部接纳 Pigsty。所有内容都是免费、开源的，整合起来非常轻松。已有多家 PostgreSQL 厂商将其作为额外的上游用于安装扩展。

针对 ARM64 平台的完整支持为更多芯片架构支持提供了信心。例如 IBM LinuxOne Cloud 提供的开源项目 s390x 大型机支持，Pigsty 也在评估这一方向的可能性。

![](ibm-linuxone.jpg)


--------

## Supabase 例行跟进

Pigsty 之前推出的 **Supabase 自建教程** 能让用户在一台机器上迅速拉起自建的 Supabase 服务。对于密集使用 Supabase 的创业群体引起了一定反响，因此持续在 Supabase 的最新版本上做跟进。

Supabase 在 2024 年的最后一个月里发布了一系列重要更新，Pigsty v3.2 也跟进了这些变化，为用户提供最新的 Supabase 版本。

Supabase 最近的一个重要动作是收购 OrioleDB —— 一个专注于提升 PostgreSQL OLTP 性能的内核分支。目前这项功能在 Supabase 中被标记为 Beta，作为用户的可选项存在。Pigsty 正在准备 OrioleDB 的 RPM/DEB 包，确保即使以后 Supabase 使用它作为主干，Pigsty 也能提供支持。

![](orioledb.jpg)

凭借这个契机，Pigsty 也准备进一步将扩展能力普及到更多的 PostgreSQL 分支上：

| 内核 | 兼容性 |
|-----|--------|
| IvorySQL 3/4 | Oracle 兼容 |
| WiltonDB | SQL Server 兼容 |
| PolarDB PG | 阿里云开源 |
| OrioleDB | OLTP 优化 |


--------

## Grafana 的可扩展性

Grafana 是非常流行的开源监控和可视化工具，拥有许多扩展插件：各类数据可视化面板与数据源。但这些扩展插件的安装和管理一直是个问题 —— Grafana 自己的 CLI 工具确实可以用于安装插件，不过国内用户必须科学上网才能使用，带来了很大的不便。

在 v3.2 中，常用的 Grafana 扩展面板与数据源插件都制作成了 RPM/DEB 包，方便开箱即用：

**架构无关扩展 (grafana-plugins)**：

| 类别 | 插件 |
|-----|------|
| 面板 | volkovlabs-echarts, image, form, table, variable |
| 面板 | knightss27-weathermap, marcusolsson-dynamictext |
| 面板 | marcusolsson-treemap, calendar, hourly-heatmap |
| 数据源 | marcusolsson-static, json, volkovlabs-rss, grapi |

**架构相关扩展**：

此外，针对那些架构相关（包含 x86、ARM 二进制）的数据源扩展制作了独立的 RPM/DEB 包。例如 Grafana 新推出的 **Infinity 数据源插件**：可以使用任意 REST/GraphQL API，使用 CSV/TSV/XML/HTML 作为数据源，这极大扩展了 Grafana 的数据接入能力。

![](grafana-infinity.jpg)

与此同时，还针对 VictoriaMetrics 和 VictoriaLogs 的 Grafana 数据源插件制作了 RPM/DEB 包，方便用户在 Grafana 中使用这两个开源的时序数据库和日志数据库。


--------

## 下一步的发展规划

目前 Pigsty 本身已经达到了相当成熟的状态。接下来一段时间的工作重心，将放在 `pig` 这个工具以及扩展仓库的维护上。

当前是一个难得的机会窗口：用户与开发者开始意识到 PostgreSQL 扩展的重要性，但 PostgreSQL 生态还没有扩展分发的事实标准。Pigsty 致力于让 `pig` 成为一个有影响力的 PostgreSQL 扩展插件分发标准。

当然，Pigsty 本身一直也缺少一个足够好用的 CLI 工具，接下来将把散落在各个 Ansible 剧本中的功能整合到 `pig` 中，让用户可以更方便地管理 Pigsty 与 PostgreSQL。


--------
--------

## v3.2.0 发行注记

### 亮点特性

- Pigsty 命令行工具：[`pig`](https://github.com/pgsty/pig) 0.2.0，可用于管理扩展插件。
- 提供五大发行版上 [340 个扩展](https://pgext.cloud/) 的 ARM64 扩展支持
- Supabase 发布周最新版本更新，全发行版均可自建。
- Grafana 更新至 11.4 ，新增 infinity 数据源。

### 软件包变化

- **新增扩展**
  - 新增 timescaledb, timescaledb-loader timescaledb-toolkit timescaledb-tool to PIGSTY repo
  - 新增 [pg_timescaledb](https://github.com/timescale/timescaledb)，针对 EL 进行的编译重制版本
  - 新增 [pgroonga](https://pgext.cloud/e/pgroonga)，针对 EL 全系进行编译重制
  - 新增 [vchord](https://github.com/tensorchord/VectorChord) 0.1.0
  - 新增 [pg_bestmatch.rs](https://github.com/tensorchord/pg_bestmatch.rs) 0.0.1
  - 新增 [pglite_fusion](https://github.com/frectonz/pglite-fusion) 0.0.3
  - 新增 [pgpdf](https://github.com/Florents-Tselai/pgpdf) 0.1.0

- **更新扩展**
  - pgvectorscale 0.4.0 -> 0.5.1
  - pg_parquet 0.1.0 -> 0.1.1
  - pg_polyline 0.0.1
  - pg_cardano 1.0.2 -> 1.0.3
  - pg_vectorize 0.20.0
  - pg_duckdb 0.1.0 -> 0.2.0
  - pg_search 0.13.0 -> 0.13.1
  - aggs_for_vecs 1.3.1 -> 1.3.2
  - `pgoutput` 被标记为新的 PostgreSQL Contrib 扩展

- **基础设施**
  - 新增 promscale 0.17.0
  - 新增 grafana-plugins 11.4
  - 新增 grafana-infinity-plugins
  - 新增 grafana-victoriametrics-ds
  - 新增 grafana-victorialogs-ds
  - vip-manager 2.8.0 -> 3.0.0
  - vector 0.42.0 -> 0.43.0
  - grafana 11.3 -> 11.4
  - prometheus 3.0.0 -> 3.0.1 (软件包名从 `prometheus2` 变更为 `prometheus`)
  - nginx_exporter 1.3.0 -> 1.4.0
  - mongodb_exporter 0.41.2 -> 0.43.0
  - VictoriaMetrics 1.106.1 -> 1.107.0
  - VictoriaLogs 1.0.0 -> 1.3.2
  - pg_timetable 5.9.0 -> 5.10.0
  - tigerbeetle 0.16.13 -> 0.16.17
  - pg_export 0.7.0 -> 0.7.1

- **缺陷修复**
  - el8.aarch64 添加 python3-cdiff 修复 patroni 依赖错漏问题
  - el9.aarch64 添加 timescaledb-tools ，修复官方仓库缺失问题
  - el9.aarch64 添加 pg_filedump ，修复官方仓库缺失问题

- **移除扩展**
  - **pg_mooncake** 因为与 `pg_duckdb` 冲突而被移除。
  - **pg_top** 因为出现太多版本出现缺失，因质量问题而淘汰。
  - **hunspell_pt_pt** 因为与 PG 官方字典文件冲突而被淘汰。
  - **pg_timeit** 因为无法在 AARCH64 架构上使用而被淘汰。
  - **pgdd** 因为缺乏维护，PG 17 与 pgrx 版本老旧而被标记为弃用。
  - **old_snapshot** 与 **adminpack** 被标记为 PG 17 不可用。
  - **pgml** 被设置为默认不下载不安装。


### API变化

- [`repo_url_packages`](https://pigsty.cc/zh/docs/ref/param/#repo_url_packages) 参数现在默认值为空数组，因为所有软件包现在都通过操作系统包管理器进行安装。
- `grafana_plugin_cache` 参数弃用，现在 Grafana 插件通过操作系统包管理器进行安装
- `grafana_plugin_list` 参数弃用，现在 Grafana 插件通过操作系统包管理器进行安装
- 原名为 `prod` 的 36 节点仿真模板现在重命名为 `simu`。
- 原本在 `node_id/vars` 针对每个发行版代码生成的配置，现在同样针对 `aarch64` 生成。
- `infra_packages` 中默认添加命令行管理工具 `pig`
- `configure` 命令同样会修改自动生成配置文件中 `pgsql-xxx` 别名的版本号。
- `adminpack` 在 PG 17 中被移除，因此从 Pigsty 默认扩展中被移除。

### 问题修复

- 修复了 `pgbouncer` 仪表盘选择器问题 [#474](https://github.com/Vonng/pigsty/issues/474)
- `pg-pitr` 新增 `--arg value` 参数解析支持 by [@waitingsong](https://github.com/Vonng/pigsty/pulls?q=is%3Apr+author%3Awaitingsong)
- 修复 Redis 日志信息 typo by [@waitingsong](https://github.com/Vonng/pigsty/pull/476)

### 软件包校验和

```
8fdc6a60820909b0a2464b0e2b90a3a6  pigsty-v3.2.0.tgz
d2b85676235c9b9f2f8a0ad96c5b15fd  pigsty-pkg-v3.2.0.el9.aarch64.tgz
649f79e1d94ec1845931c73f663ae545  pigsty-pkg-v3.2.0.el9.x86_64.tgz
c42da231067f25104b71a065b4a50e68  pigsty-pkg-v3.2.0.d12.aarch64.tgz
ebb818f98f058f932b57d093d310f5c2  pigsty-pkg-v3.2.0.d12.x86_64.tgz
24c0be1d8436f3c64627c12f82665a17  pigsty-pkg-v3.2.0.u22.aarch64.tgz
0b9be0e137661e440cd4f171226d321d  pigsty-pkg-v3.2.0.u22.x86_64.tgz
```
