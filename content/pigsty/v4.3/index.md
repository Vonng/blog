---
title: "Pigsty v4.3：510扩展与Ubuntu26"
linkTitle: "Pigsty v4.3 510扩展与Ubuntu26"
date: 2026-05-04
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.3.0)）
summary: >
  Pigsty v4.3 新增 50 个 PostgreSQL 扩展，可用扩展总数达到 510。新增 Ubuntu 26.04 x86_64/arm64 支持，更新 Supabase、pgEdge、PolarDB、Grafana、MinIO 与一批基础设施软件包。
series: [Pigsty]
tags: [Pigsty]
---

Pigsty v4.3 正式发布。如果说 v4.2 的主题是 “十二内核”，那么 v4.3 的主题就是 “扩展密度”。

在这个版本中，支持的 PG 扩展数量从 460 个暴涨至 510 个，达到新高度。
在操作系统支持上，Ubuntu 26.04 进入支持矩阵，Ubuntu 20.04 正式退场。
Supabase、pgEdge、PolarDB、Grafana、MinIO 这些核心组件也完成了一轮集中刷新。

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.3.0) | [**发布注记**](https://pigsty.cc/docs/about/release/#v430)


------

## Pigsty v4.3：成为主流

通常来说，在 GitHub 上，5000 star 是一个分水岭，代表一个开源项目进入 “主流” 的行列。
最直观的福利就是 —— 有资格申请免费的 ChatGPT / Claude 订阅了。

Pigsty 最近 [**刚迈过了这个门槛**](/pg/extension-504/)：当前的 Star 5066，GitHub 上 Star > 5066 的仓库有 11621 个，也就是排名 1 万左右，前 0.005% 的项目。
对于数据库发行版这样的赛道来说，Star 的含金量会更高 —— 从 Star 上来看，Pigsty 已经是 PG 发行版赛道的 No.3，Linux 原生 PG 发行版赛道的 No.1 了。

最让我惊讶的是 Pigsty.IO 网站的流量，在三月份的时候，Pigsty.io 的月 UV 还不到两千万，在四月底的时候，就已经突破一亿了。
其中 99%+ 的流量来自 AI/Agent。这意味着 Pigsty 网站已经成为主流 AI 的关键语料，以及 AI Agent 使用的基础设施。
对于一个 “个人项目” 来说，这确实是难能可贵的成就了。



------

## 扩展总数突破 510

PostgreSQL 最强的地方是扩展性，但扩展生态的工程现实并不轻松。v4.3 新增约 50 个 PostgreSQL 扩展，可用扩展总数达到 [**510 个**](https://pigsty.cc/ext/list)。新增扩展覆盖面很广：

- `block_copy_command`、`external_file`、`logical_ddl`、`pg_query_rewrite` 这类偏内核与 DDL/执行机制的工具。
- `datasketches`、`onesparse`、`rdkit`、`pghydro`、`provsql` 这类数据科学、稀疏计算、化学信息、地理水文、概率数据库方向的扩展。
- `pg_text_semver`、`pg_variables`、`pg_when`、`pgcalendar`、`pglock` 这类日常开发与管理工具。
- `postgresbson`、`pgproto`、`re2`、`pgmq`、`pgmqtt` 这类协议、队列、正则和消息相关组件。
- `storage_engine`、`pg_pathcheck`、`pg_savior`、`pg_textsearch` 这类需要更认真理解加载方式或风险边界的高级扩展。

其中不少扩展已经跨过了 pgrx 版本迁移，例如从 `0.16.1` 切到 `0.17.0`，甚至 `pg_search` 和 `pg_trickle` 已经进入 pgrx `0.18.0` 线。
Rust 扩展生态越来越活跃，这很好，但对发行版维护者来说，也意味着每轮构建都要额外处理 Rust toolchain、cargo 依赖、PG 版本适配和平台差异。

用户看到的是一行 `CREATE EXTENSION`，维护者看到的是一张矩阵，一两百个包。不过现在老冯的扩展维护流程已经接入了 Agent 工作流。
无论是新增扩展，还是版本更新，都有一套完整的自动化流程，所以尽管扩展数量越来越多，维护成本不增反降，依然在一个人的维护能力范围内。


------

## Ubuntu 26.04 进入支持矩阵

v4.3 新增 **Ubuntu 26.04 x86_64 / arm64** 支持，同时正式弃用 Ubuntu 20.04。

Pigsty 当前支持 8 个主要操作系统版本，覆盖 x86_64 与 arm64 两种架构，一共是 16 个平台组合：

| 系列     | 版本    | x86_64 | arm64 | 备注           |
|:-------|:------|:-------|:------|:-------------|
| EL     | 8     | 支持     | 支持    | 维护中，临近 EOL   |
| EL     | 9     | 支持     | 支持    | 维护中          |
| EL     | 10    | 支持     | 支持    | 维护中          |
| Debian | 12    | 支持     | 支持    | 维护中          |
| Debian | 13    | 支持     | 支持    | 维护中          |
| Ubuntu | 22.04 | 支持     | 支持    | 维护中，临近 EOL   |
| Ubuntu | 24.04 | 支持     | 支持    | noble，当下使用最多 |
| Ubuntu | 26.04 | 新增     | 新增    | v4.3 起进入支持矩阵 |

Ubuntu 24.04（noble）仍然是当下使用最多的系统版本。Ubuntu 26.04 也许会在后续几年中逐步替代 Ubuntu 24.04，成为很多用户的新基线。

其实我们在 Ubuntu 26.04 发布当天就已经添加了初步支持，不过很多 Pigsty 提供的三方扩展还需要花时间构建与核验。
这次 Ubuntu 26.04 的常规扩展和离线安装包已经就位；Rust 扩展目前还没有提供，后续会继续补齐。

此外，Ubuntu 24.04 的版本也从 24.04.3 升级为 24.04.4，Debian 13 的版本从 13.3 升级到 13.4

Pigsty 使用的 vagrant 和 terraform 模板也都相应更新到最新的版本。
不过阿里云目前还没有提供 Ubuntu 26.04 的镜像。


------

## 内核更新：Supabase、pgEdge、PolarDB

**Supabase** 自建模板更新到最新版本。Pigsty 是极少数几个提供企业级 Supabase 自建方案的开源 PG 发行版之一。这次我们把 Supabase 模板更新到了最新版本，另外，我们还提供了一个 “Supabase” 青春版 —— Insforge 的自建支持。

**pgEdge** 更新到 PG 18。pgEdge 的核心价值是基于 PostgreSQL 的多主复制，底层依赖 Spock 等三个扩展。这次 Spock 支持的最新 PG 大版本从 17 提升到了 18，我们也相应更新并重新构建。

**PolarDB** 更新到 PG 17，对应版本来到 `17.9.1.0`。PolarDB 是共享存储架构的 PostgreSQL 内核分支，之前基线停留在 PG 15，这次跨到 PG 17。

**OrioleDB** 继续更新到 OriolePG 17.18 与 OrioleDB beta15 / 1.7。OrioleDB 仍然处在快速演进阶段，不建议在生产库里激进采用，但作为 PostgreSQL 存储引擎方向的前沿项目，可以尝尝鲜。

**Cloudberry** 更新到 2.1.0，并新增 `cloudberry-backup` 与 `cloudberry-pxf` 包。上一版 Pigsty 把 Cloudberry 带回发行矩阵，这一版补齐了周边工具。


------

## Grafana 13 与 Victoria 组件刷新

可观测性是 Pigsty 的基本盘。这次的可观测性技术栈也进行了批量更新。
最显著的改动是 Grafana 大版本更新，从 12 到 13 引入了许多新功能，比如支持在 Dashboard 里使用 Tab，这带来了更多有趣的玩法。

v4.3 将 Grafana 更新到 **13.0.1**，并同步刷新插件包：

- `grafana`：12.4.1 -> 13.0.1
- `grafana-plugins`：12.3.0 -> 13.0.0
- `grafana-infinity-ds`：3.7.4 -> 3.8.0
- `grafana-victoriametrics-ds`：0.23.1 -> 0.24.0

Victoria 系列也进行了集中更新：

- `victoria-metrics`：1.138.0 -> 1.142.0
- `victoria-metrics-cluster`：1.138.0 -> 1.142.0
- `vmutils`：1.138.0 -> 1.142.0
- `victoria-logs`：1.48.0 -> 1.50.0
- `vlagent` / `vlogscli`：1.48.0 -> 1.50.0
- `victoria-traces`：0.8.0 -> 0.8.2

同时也修了个用户反馈的小问题，VictoriaTraces 的 Grafana 数据源路径修正为 `/select/jaeger`。



------

## etcd CVE 修复

之前，etcd 3.6.8 爆出来一个 CVE，3.6.9 修复了但引入了新的问题，给 member list API 加上了 Auth，导致 PG 高可用组件 Patroni 失效（4.1.0 以前版本），Patroni 4.1.1 修复了这个问题。

这里要提醒一下用户，Patroni <= 4.1.0 与 etcd <= 3.6.8 配合使用；而 Patroni >= 4.1.1 与 etcd >= 3.6.9 配合使用，也就是这两个软件的版本必须配套。老配老，新配新，否则就会有问题。

之前在 v4.2.2 中，EL 侧已经更新了 etcd 3.6.10 与 patroni 4.1.1，但是因为 APT 仓库更新慢，所以 DEB 侧还停留在 etcd 3.6.8 与 patroni 4.1.0 的老版本上。现在 v4.3 中，DEB 侧也完成了更新，用户可以放心升级了。



------

## MinIO CVE 修复

老冯之前 fork 了 MinIO，四月份修复了几个 CVE，写了一篇《[续命 MinIO，承诺兑现](/db/minio-promise-kept)》聊了聊这个事，完整背景和漏洞细节可以看那篇。
Pigsty v4.3 实装了修复后的新版本：`20260417000000`。

这批修复覆盖 OIDC/JWT、LDAP STS 登录、复制头元数据、S3 Select、unsigned-trailer 签名校验等路径。对 Pigsty 用户来说，重点不是每个漏洞的利用细节，而是对象存储组件已经切到带修复的版本，离线包也一并更新了。

现在老冯的这个 fork（Silo）已经被一些项目用在实际生产环境中了，比如 Grafana Loki。silo 文档站每个月有千万级别的请求量，Docker Hub 上的下载也达到了 10 万+。
应该是目前影响力最大的 MinIO fork 了。老冯虽然挺开心，但重申一下这并不是我的主业，我只是确保 Pigsty 用户有这么一个能用的开源对象存储选项就可以了。

然后最近发现 RustFS 竟然也成了奇绩校友，跟他们聊天得知后面准备把 RustFS 做成 MinIO 的 Drop-In 替代。老冯觉得如果这个目标真能实现，我会认真考虑直接用 RustFS 替换 MinIO。
这次欣慰地看到 RustFS 告别 Alpha 阶段，发布了第一个 Beta 版本，我也打好了包。大概计划在七月左右会有 GA 版本。


------

## Vagrant 模板统一切到 cloud-image

Vagrant 对很多人来说只是本地测试工具，但对 Pigsty 这种需要验证多操作系统、多架构、多拓扑的项目来说，它是很重要的开发与验收入口。

v4.3 将 [Vagrant 模板](https://pigsty.io/docs/deploy/vagrant) 统一切换到 cloud-image 系列镜像。
主要是因为，这是唯一一个完整覆盖 Virtualbox/Libvirt amd64/arm64 四种排列组合下所有 Pigsty 支持的操作系统的镜像族

这个改动主要是为了降低系统镜像差异带来的不确定性。传统 box 镜像质量参差不齐，网络、磁盘、cloud-init、guest tools 的行为都可能有细微差异。
cloud-image 是发行版官方更标准、更持续维护的路径，统一到这条线之后，后续适配和排障都会简单很多。

不过这个镜像的默认网卡名不再是 eth1 了，如果你需要测试 VIP 相关的功能，请记得调整配置中的网卡名称。



------

## 几个值得单独提的修复

v4.3 还有一些看似不起眼，但属于是用户真实撞上的问题的修复。

**PostgreSQL 用户名校验放宽**：现在允许少量特殊符号 `@.-` 出现在用户名定义中。现实里很多企业账号体系会使用邮箱式用户名或带域标识的用户名，数据库发行版不应该用过窄的正则把这些合法需求挡掉。

**IPv6 nameserver 解析修复**：旧逻辑只提取 IPv4 DNS Server，遇到 IPv6 nameserver 时会漏掉配置。现在修复后，可以正确处理 IPv6 DNS 场景。IPv6 支持常常不是主线需求，但一旦环境里有，它就是硬需求。

------

## 其他的一些特性

此外，在 Pigsty v4.3 中，我们还试点加入了 Hindsight 记忆框架（基于 PG 与 pgvector）和 Hermes Agent 自建模板支持。它们都还属于试点功能，这里就不展开了。

--------

## 小结

Pigsty v4.3 说大不大，没有框架，接口上的改动。但说小也不小，一口气上新了 50 个扩展。

它没有一个单点爆炸的新功能，但它把很多用户真正关心的东西一起往前推进了：更多扩展，更新的操作系统，更新的内核分支，更新的监控栈，更稳的 Vagrant 模板，修复 CVE 的对象存储包，修正了一批实际会踩到的小问题。

数据库发行版的价值，很多时候就体现在这些不性感的地方。你不需要自己去追 50 个扩展的构建状态，不需要自己检查 Ubuntu 26.04 的包矩阵，不需要自己处理 MinIO CVE 分支，不需要自己整理 Grafana 13 插件和 Victoria 组件版本，不需要自己猜 Vagrant 镜像该用哪个。

Pigsty 把这些东西收敛成一个版本。你拿来用就行。下面附完整的 v4.3.0 提交注记与包变更摘要，方便按需查阅。



--------

## v4.3.0 提交注记

**亮点**

- 新增约 50 个 PostgreSQL 扩展，总可用数量达到 510 个
- 支持 Ubuntu 26.04 x86_64/arm64，弃用 Ubuntu 20.04 支持；小版本更新至 Debian 13.4 / Ubuntu 24.04.4
- 内核更新：Supabase 更新至最新版本，pgEdge 更新至 PG 18，PolarDB 更新至 PG 17
- Grafana 更新至 13.0.1，MinIO 使用修复 CVE 后的 pgsty/Silo 分支。
- Vagrant 模板统一切换至 cloud-image 系列镜像。

**问题修复**

- PostgreSQL 用户名校验放宽，允许 `@.-` 几个字符出现在用户名中。
- 修复 IPv6 nameserver 解析，避免 DNS 配置只匹配提取 IPv4 的旧 DNS Server。
- VictoriaTraces Grafana 数据源路径改为 `/select/jaeger`。
- Vagrant 磁盘探测更稳健，新增 EL vagrant 镜像 guest 网络修复脚本 bin/el-fix。

**PostgreSQL 与扩展包变更汇总**

| 包名                   | 旧版本                  | 新版本                  | 备注                                      |
|:---------------------|:---------------------|:---------------------|:----------------------------------------|
| `block_copy_command` | -                    | 0.1.5                | 新增；PG 14-18；Rust/pgrx 0.17.0            |
| `cloudberry`         | 2.0.0                | 2.1.0                | 内核包组；RPM release 2 修复 initdb errno 问题   |
| `cloudberry-backup`  | -                    | 2.1.0                | 新增 Cloudberry 备份工具包                     |
| `cloudberry-pxf`     | -                    | 2.1.0                | 新增 Cloudberry PXF 包                     |
| `credcheck`          | 4.6                  | 4.7                  | 升级；PG 14-18；PGDG                        |
| `datasketches`       | -                    | 1.7.0                | 新增；PG 14-18                             |
| `ddl_historization`  | 0.0.7                | 0.2                  | 升级                                      |
| `documentdb`         | 0.109                | 0.110                | 升级到上游版本；PG 15-18                        |
| `external_file`      | -                    | 1.2                  | 新增；PG 14-18                             |
| `logical_ddl`        | -                    | 0.1.0                | 新增；PG 14-18                             |
| `nominatim_fdw`      | 1.1.0                | 1.2                  | 升级                                      |
| `onesparse`          | -                    | 1.0.0                | 新增；仅 PG 18                              |
| `orioledb`           | RPM beta14 / DEB 1.6 | RPM beta15 / DEB 1.7 | 配套 OriolePG 17.18                       |
| `oriolepg`           | 17.16                | 17.18                | 内核补丁集更新                                 |
| `parray_gin`         | -                    | 1.5.0                | 新增后升级；PG 14-18                          |
| `pg_accumulator`     | -                    | 1.1.3                | 新增；PG 14-18                             |
| `pg_anon`            | 3.0.1                | 3.0.13               | 升级；Rust/pgrx 0.16.1 -> 0.17.0           |
| `pg_background`      | 1.8                  | 1.9.2                | 仅 DEB                                   |
| `pg_bikram_sambat`   | -                    | 0.1.0                | 新增；Bikram Sambat 日期类型与 AD/BS 转换函数       |
| `pg_byteamagic`      | -                    | 0.2.4                | 新增；PG 14-18                             |
| `pg_cardano`         | 1.1.1                | 1.2.0                | 升级；Rust/pgrx 0.17.0                     |
| `pg_clickhouse`      | 0.1.5                | 0.2.0                | 升级                                      |
| `pg_datasentinel`    | -                    | 1.0                  | 新增；PG 15-18                             |
| `pg_dbms_job`        | 1.5                  | 2.0                  | 升级；PG 14-18；PGDG                        |
| `pg_dispatch`        | -                    | 0.1.5                | 新增；PG 14-18                             |
| `pg_failover_slots`  | 1.2.0                | 1.2.1                | 升级                                      |
| `pg_fsql`            | -                    | 1.1.0                | 新增；PG 14-18                             |
| `pg_incremental`     | 1.4.1                | 1.5.0                | 升级                                      |
| `pg_isok`            | -                    | 1.4.1                | 新增；PG 14-18                             |
| `pg_ivm`             | 1.13                 | 1.14                 | 升级；PG 14-18                             |
| `pg_kazsearch`       | -                    | 2.0.0                | 新增；PG 16-18；Rust/pgrx 0.17.0            |
| `pg_liquid`          | -                    | 0.1.7                | 新增；PG 14-18                             |
| `pg_pathcheck`       | -                    | 0.9.1                | 新增；PG 17-18；需 shared_preload_libraries  |
| `pg_query_rewrite`   | -                    | 0.0.5                | 新增；PG 14-18                             |
| `pg_regresql`        | -                    | 2.0.0                | 新增；PG 14-18                             |
| `pg_rrf`             | -                    | 0.0.3                | 新增；PG 14-17；Rust/pgrx 0.16.1 -> 0.17.0  |
| `pg_savior`          | 0.0.1                | 0.1.0                | 升级；高风险 DDL/DML 防护 hook；需 preload 或 LOAD |
| `pg_search`          | 0.22.2               | 0.23.1               | 升级；PG 15-18；pgrx 0.18.0                 |
| `pg_slug_gen`        | -                    | 1.0.0                | 新增；PG 15-18                             |
| `pg_stat_ch`         | -                    | 0.3.6                | 新增后升级；PG 16-18；EL8 break                |
| `pg_store_plans`     | 1.9                  | 1.10                 | 升级                                      |
| `pg_strict`          | 1.0.3                | 1.0.5                | 升级；Rust/pgrx 0.16.1 -> 0.17.0           |
| `pg_text_semver`     | -                    | 1.2.1                | 新增；PG 14-18                             |
| `pg_textsearch`      | 0.5.0                | 1.1.0                | 升级；PG 17-18；需 shared_preload_libraries  |
| `pg_trickle`         | 0.16.0               | 0.40.0               | 升级；仅 PG 18；pgrx 0.18.0                  |
| `pg_tzf`             | 0.2.3                | 0.2.4                | 升级；Rust/pgrx 0.17.0                     |
| `pg_vectorize`       | 0.26.0               | 0.26.1               | 升级；Rust/pgrx 0.16.1 -> 0.17.0           |
| `pg_variables`       | -                    | 1.2.5                | 新增；PG 14-18                             |
| `pg_when`            | -                    | 0.1.9                | 新增；PG 14-18；Rust/pgrx 0.17.0            |
| `pgxicor`            | 0.1.0                | 0.1.1                | 升级                                      |
| `pgcalendar`         | -                    | 1.1.0                | 新增；PG 14-18                             |
| `pgclone`            | -                    | 4.0.0                | 新增后升级；PG 14-18                          |
| `pgelog`             | -                    | 1.0.2                | 新增；PG 14-18                             |
| `pglinter`           | 1.1.1                | 1.1.2                | 升级；Rust/pgrx 0.16.1 -> 0.17.0           |
| `pglock`             | -                    | 1.0.0                | 新增；PG 14-18                             |
| `pgmq`               | 1.11.0               | 1.11.1               | 升级；PG 14-18                             |
| `pgmqtt`             | -                    | 0.1.0                | 新增；PG 14-18；Rust/pgrx 0.16.1 -> 0.17.0  |
| `pgproto`            | -                    | 0.5.0                | 新增后升级；原生 Protobuf 支持                    |
| `pghydro`            | -                    | 6.6                  | 新增；PG 14-18                             |
| `pgx_ulid`           | 0.2.2                | 0.2.3                | 升级；Rust/pgrx 0.17.0                     |
| `plv8`               | 3.2.4                | 3.2.4-2              | 仅 RPM；EL10 构建修复                         |
| `PolarDB`            | 15.15                | 17.9.1.0             | PG 15 -> 17                             |
| `postgresbson`       | -                    | 2.0.2                | 新增；PG 14-18                             |
| `postgis`            | 3.6.2                | 3.6.3                | 仅 DEB                                   |
| `prefix`             | 1.2.10               | 1.2.11               | 升级；PG 14-18；PGDG                        |
| `provsql`            | -                    | 1.2.3                | 新增；PG 14-18                             |
| `rdf_fdw`            | -                    | 2.5.0                | 新增后升级；PG 14-18                          |
| `rdkit`              | -                    | 202503.6             | 新增；PG 14-18                             |
| `re2`                | -                    | 0.1.1                | 新增；PG 16-18                             |
| `storage_engine`     | -                    | 1.3.4                | 新增后升级；PG 14-18；列式与行压缩表访问方法              |
| `supautils`          | 3.1.0                | 3.2.1                | 升级                                      |
| `system_stats`       | 3.2                  | 4.0                  | 升级                                      |
| `timescaledb`        | 2.25.2               | 2.26.4               | 升级；TSL 小版本更新                            |
| `ulak`               | -                    | 0.0.2                | 新增；PG 14-18                             |
| `wrappers`           | 0.5.7                | 0.6.0                | 升级；Rust/pgrx 0.16.1 -> 0.17.0           |
{.stretch-last}


**基础设施软件包更新**

| 包名                           | 旧版本            | 新版本            | 备注                    |
|:-----------------------------|:---------------|:---------------|:----------------------|
| `alertmanager`               | 0.31.1         | 0.32.1         |                       |
| `agentsview`                 | 0.15.0         | 0.26.0         |                       |
| `claude`                     | 2.1.81         | 2.1.123        | 通过 8118 代理下载并核验       |
| `code`                       | 1.112.0        | 1.118.1        | 直链元数据更新               |
| `code-server`                | 4.112.0        | 4.117.0        | 直链元数据更新               |
| `codex`                      | 0.116.0        | 0.125.0        | 从预发布链收敛到稳定版后继续升级      |
| `crush`                      | 0.51.2         | 0.64.0         | 直链元数据更新               |
| `dblab`                      | 0.34.3         | 0.38.0         |                       |
| `duckdb`                     | 1.5.0          | 1.5.2          |                       |
| `etcd`                       | 3.6.9          | 3.6.10         | 统一软件包版本               |
| `garage`                     | 2.2.0          | 2.3.0          |                       |
| `genai-toolbox`              | 0.27.0         | 1.1.0          | 上游已更名为 mcp-toolbox    |
| `golang`                     | 1.26.1         | 1.26.2         |                       |
| `grafana`                    | 12.4.1         | 13.0.1         | 主版本升级后继续刷新元数据         |
| `grafana-infinity-ds`        | 3.7.4          | 3.8.0          |                       |
| `grafana-plugins`            | 12.3.0         | 13.0.0         | Noarch 插件包，手工归集       |
| `grafana-victoriametrics-ds` | 0.23.1         | 0.24.0         |                       |
| `hugo`                       | 0.158.0        | 0.161.1        |                       |
| `maddy`                      | 0.8.2          | 0.9.3          |                       |
| `mcli`                       | 20260321000000 | 20260417000000 | pgsty 分支，修复 cve       |
| `minio`                      | 20260325000000 | 20260417000000 | pgsty 分支，修复 cve       |
| `mongodb_exporter`           | 0.49.0         | 0.50.0         |                       |
| `node_exporter`              | 1.10.2         | 1.11.1         |                       |
| `nodejs`                     | 24.14.0        | 24.15.0        | 维持在 24.x 策略线          |
| `npgsqlrest`                 | 3.11.1         | 3.12.0         |                       |
| `opencode`                   | 1.2.27         | 1.14.30        | 改为版本化缓存并重新构建          |
| `pg_exporter`                | 1.2.1          | 1.2.2          | 直链元数据更新               |
| `pgflo`                      | 0.0.15         | -              | 已移除                   |
| `pgschema`                   | 1.7.4          | 1.9.0          |                       |
| `pig`                        | 1.3.2          | 1.4.1          | 仅更新元信息                |
| `postgrest`                  | 14.7           | 14.10          |                       |
| `prometheus`                 | 3.10.0         | 3.11.3         |                       |
| `rainfrog`                   | 0.3.17         | 0.3.18         |                       |
| `rclone`                     | 1.73.2         | 1.73.5         | 直链元数据更新               |
| `rustfs`                     | 1.0.0-alpha.89 | 1.0.0-b1       | 预发布版本线                |
| `sabiql`                     | 1.8.2          | 1.11.1         |                       |
| `seaweedfs`                  | 4.17           | 4.22           |                       |
| `sqlcmd`                     | 1.9.0          | 1.10.0         |                       |
| `stalwart`                   | 0.15.5         | 0.16.2         |                       |
| `tigerbeetle`                | 0.16.77        | 0.17.2         |                       |
| `tigerfs`                    | 0.5.0          | 0.6.0          |                       |
| `timescaledb-tools`          | 0.18.2         | 0.19.0         | 重新构建 timescaledb-tune |
| `uv`                         | 0.10.12        | 0.11.8         |                       |
| `victoria-logs`              | 1.48.0         | 1.50.0         | 主包                    |
| `victoria-metrics`           | 1.138.0        | 1.142.0        |                       |
| `victoria-metrics-cluster`   | 1.138.0        | 1.142.0        | VictoriaMetrics 配套组件  |
| `victoria-traces`            | 0.8.0          | 0.8.2          |                       |
| `vip-manager`                | 4.0.0          | 4.2.0          | 直链元数据更新               |
| `vlagent`                    | 1.48.0         | 1.50.0         | VictoriaLogs 配套组件     |
| `vlogscli`                   | 1.48.0         | 1.50.0         | VictoriaLogs 配套组件     |
| `vmutils`                    | 1.138.0        | 1.142.0        | VictoriaMetrics 配套组件  |
| `vector`                     | 0.54.0         | 0.55.0         | 直链元数据更新               |
| `v2ray`                      | 5.47.0         | 5.48.0         |                       |
| `xray`                       | 26.2.6         | 26.3.27        |                       |

**校验和**

```bash
58a914fce7bc521b65e167f66e7961a3  pigsty-v4.3.0.tgz
9ce070efb0420057a83c632b2856d1b3  pigsty-pkg-v4.3.0.d12.aarch64.tgz
bf21c36d3aff94a1a6353130597ffa85  pigsty-pkg-v4.3.0.d12.x86_64.tgz
81b4790c4e5567cee9d1beadd06e48e6  pigsty-pkg-v4.3.0.d13.aarch64.tgz
06baab9341ab683eaeea2e066b28a0f4  pigsty-pkg-v4.3.0.d13.x86_64.tgz
fb4bf751df5e09f547c49b8ab7cac9a0  pigsty-pkg-v4.3.0.el10.aarch64.tgz
a3e752c8148122d1eaea74a6d8d8df0d  pigsty-pkg-v4.3.0.el10.x86_64.tgz
cb2a9af36615513e66fd5ac3e9f4d797  pigsty-pkg-v4.3.0.el9.aarch64.tgz
e24641a879dec7a8eea74dab42f85920  pigsty-pkg-v4.3.0.el9.x86_64.tgz
6b675fd8d9e039193481f0838aa4b92c  pigsty-pkg-v4.3.0.u22.aarch64.tgz
c0e344ccb9d190a619591e5d46116424  pigsty-pkg-v4.3.0.u22.x86_64.tgz
3e0ec9534cf595201ec79eb1fc6549d8  pigsty-pkg-v4.3.0.u24.aarch64.tgz
0a3d19513eca9615bdd66a4b2bf66f1d  pigsty-pkg-v4.3.0.u24.x86_64.tgz
683a10ff8fd993358d6befa9f4e02913  pigsty-pkg-v4.3.0.u26.aarch64.tgz
fd1ea5cd5554bfe91fadd51ad80860e3  pigsty-pkg-v4.3.0.u26.x86_64.tgz
```
