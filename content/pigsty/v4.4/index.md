---
title: "Pigsty v4.4：从集成到发行"
linkTitle: "Pigsty v4.4 从集成到发行"
date: 2026-07-11
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.4.0)）
summary: >
  Pigsty v4.4 新增 Immich 与 JumpServer 应用模板，更新 Supabase 与 VIP 使用体验，并开始统一发行 PolarDB、IvorySQL 等 PostgreSQL 分支内核的软件包与文件系统布局。
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) | [**发布注记**](https://pigsty.cc/docs/about/release/#v440)

Pigsty v4.4 正式发布。表面上看，这是一个例行维护版本：PostgreSQL 18.4、531 个扩展、PG19 beta，以及十四组通过验收的离线安装制品。真正值得讲的变化，则集中在软件仓库与命令行工具上。

Pig 1.5 完成了 PostgreSQL 日常运维命令行的重构。克隆数据库、分叉实例、执行时间点恢复——这些原来散落在 Ansible、Shell、Patroni 与 pgBackRest 里的动作，现在有了一套统一的命令行接口。

与此同时，我们重新梳理了仓库中的 PG 内核分支：新增 Babelfish PG18，补齐 pgEdge PG15～18、AgensGraph PG17 与 OrioleDB PG16～18，并为 PolarDB、IvorySQL 提供自行构建的软件包。

这一版还将 Supabase 自建模板跟进到上游最新版本，并解决了一批兼容问题；同时新增自托管云相册 Immich、堡垒机 JumpServer 与个人财务管理工具 Maybe 的一键部署模板。


------

## Pig 1.5：统一运维入口

`pig` 最早只是 PostgreSQL 扩展包管理器，后来逐步承担 Pigsty 安装、软件仓库与 PostgreSQL 管理工作。到了 1.5，它已经不只是“能执行很多命令”，而是开始形成一套清晰的 PostgreSQL 操作界面。

| 命令         | 边界               | 典型用途                                       |
|:-----------|:-----------------|:-------------------------------------------|
| `pig pg`   | 本地 PostgreSQL 原语 | 启停、状态、连接、维护、数据库克隆与本地 PGDATA 分叉             |
| `pig pt`   | Patroni 集群操作     | 重启、重建副本、切主、故障转移、配置与日志                      |
| `pig pb`   | pgBackRest 低层原语  | 备份、仓库、备份集、清理与底层 restore                    |
| `pig pitr` | 恢复编排             | 协调 Patroni、PostgreSQL 与 pgBackRest 完成 PITR |

这一轮最重要的变化不是命令数量，而是**职责边界**。过去，这些操作主要靠 DBA 记住 SOP 与命令别名：什么时候调用什么工具，下一步做什么，会有什么副作用。现在，这些经验被直接写进命令，高风险操作统一沿着同一条链路推进：

> `state → plan → precheck → execute → verify → result → next_actions`

各阶段的结果与帮助信息既可以输出为人类可读的文本，也可以输出成便于机器和 Agent 处理的 JSON／YAML。通过这套 Agent-Native 接口，DBA、脚本与 Agent 可以共用同一个入口，获得所需上下文、风险判断与下一步提示。

抽象的话说多了没意思，下面来看几个具体例子。


------

### 克隆：给单个数据库开一个分支

新增命令 `pig pg clone` 可以快速克隆单个数据库。

```bash
pig pg clone meta meta_dev --plan   # 先查看计划
pig pg clone meta meta_dev -y       # 创建数据库副本
```

这里有一个经常被忽略的边界：`CREATE DATABASE ... TEMPLATE` 会终止源库现有会话。换句话说，数据库克隆虽然快，却不是毫无影响。`--plan` 的意义，就是在真正动手前把这些副作用摊开给你看。

对于开发测试、数据分析、模型实验和 Agent 反事实推演来说，这种廉价分支非常实用。生产库保持不动，实验在副本里进行；做坏了直接删除，再开一个新的分支即可。详细用法可以参考《[瞬间克隆 PostgreSQL 数据库，无需黑魔法](/pg/pg-pig-clone/)》。


------

### 分叉：给整个实例做一个沙箱

数据库克隆解决的是单库副本，而 `pig pg fork` 处理的是整个 PostgreSQL 实例，也就是 PGDATA 级别的物理分叉。

```bash
pig pg fork init dev --start        # 分叉为 /pg/data-dev 并启动
pig pg fork list                    # 查看本地分叉实例
pig pg fork stop dev                # 停止分叉实例
```

Pig 会为受管分叉写入元数据，并提供 `list`、`start`、`stop`、`rm` 等生命周期命令。在支持 CoW 的 XFS 上，分叉初始几乎不额外占用空间，后续只有新增或改写的数据块才会消耗容量。Pig 还会自动分配可用端口，让分叉实例与原实例并存。

它特别适合两类场景：一是在大规模、难回滚的操作前，留下一份低成本的本地分支；二是在事故恢复时拉起旁路实例，快速验证 PITR 目标与数据状态。


------

### 回到过去：恢复首先是一份计划

数据库恢复最危险的地方，从来不是缺一条命令，而是步骤太多、边界太模糊，而且人在事故压力下最容易犯错。

Pig 1.5 把低层恢复与高层编排明确拆开：

- `pig pb restore` 是 pgBackRest 的底层恢复原语，只负责文件与恢复目标。
- `pig pitr` 是面向 Pigsty／Patroni 环境的恢复编排入口，负责协调 Patroni、PostgreSQL 与 pgBackRest。

```bash
pig pitr -t "2026-07-10 12:00:00+08" --plan
pig pitr -t "2026-07-10 12:00:00+08" -y
```

恢复命令现在必须显式指定一个目标：最新状态、备份一致点、时间、LSN、事务 ID 或命名恢复点，不能把“没写目标”解释成某个危险默认值。结构化输出也不再充当确认；自动化执行破坏性操作时，必须明确传入 `-y/--yes`。

对于托管数据目录，`pig pitr` 会检查环境、停止 Patroni 与 PostgreSQL、执行 pgBackRest 恢复、按策略启动 PostgreSQL 并验证恢复状态，最后给出后续动作。恢复完成后，再由人或上层自动化确认数据状态，重新接入 Patroni 并切换流量。

核心不是“一键恢复”，而是把事故现场最容易出错的 SOP 固化下来：先看计划，再执行，最后验证。


------

## PostgreSQL 18.4、19 beta 与 531 个扩展

运维接口是这一版的主线，但发行版的基本盘也没有停下。

Pigsty v4.4 将 **PostgreSQL 18.4** 设为生产默认版本，同时增加一个精简的 **PostgreSQL 19 beta** 评估模板。PG19 beta1 尚未达到生产状态，v4.4 发布时使用的 pgBackRest 2.58 也无法识别它的控制文件格式，因此这套模板只用于尝鲜评估。

Pigsty 的 PG 扩展目录则从 v4.3 的 **510** 增加到 **531**。按方向来看，`pg_ducklake` 把 DuckDB、Parquet 与湖仓能力带进 PostgreSQL；`pg_stat_plans` 与 `pg_stat_backtrace` 补强查询计划和进程调用栈观测；升级后的 `pgmnemo` 与新加入的 `psql_bm25s`，则分别面向 Agent 记忆和 BM25 全文检索。

与此同时，OrioleDB 扩展到 PG16～18 并将 PG18 作为默认，pgEdge 覆盖 PG15～18，Babelfish 覆盖 PG17～18，IvorySQL 进入 5.x，AgensGraph 更新到 PG17，Cloudberry 与 PolarDB 也完成了路径和软件包重整。

这些细节看起来杂，但这就是发行版的工作：让 PostgreSQL 主线、扩展生态与内核分支同时保持可用、可安装、可升级。


------

## 应用更新：Immich、JumpServer、Maybe 与 Supabase

这一版新增了 [Immich](https://pigsty.cc/docs/app/immich/)、[JumpServer](https://pigsty.cc/docs/app/jumpserver/) 与 Maybe 三个应用模板，并更新了 Supabase。

### Immich：把照片库交给真正的 PostgreSQL

Immich 是一套开源的自托管照片与视频管理服务，可以把它理解成自己家里的 Google Photos 或 iCloud Photos。它有移动端自动备份、相册、地图、人脸识别和语义搜索，后端同时用到 PostgreSQL、向量检索、缓存和机器学习服务。其中，智能搜索与人脸识别需要 VectorChord 扩展 `vchord`，Pigsty 可以直接提供。

Immich 目前仍将照片原件存放在文件目录中，不直接支持对象存储。如果需要把存储池独立出来，可以用 JuiceFS 将 MinIO 或 S3 挂载为本地文件系统。

### JumpServer：把堡垒机也接进来

堡垒机是许多企业的刚需，JumpServer 则是常见的开源选择之一。JumpServer 4.x 使用 PostgreSQL 保存核心元数据，因此 Pigsty 顺手补上了相应的部署模板。

Maybe 也在这一版加入应用目录，它是一套个人财务与资产管理工具。三个模板方向不同，但思路一致：应用可以跑在容器里，数据不必跟着容器一起漂。

### Supabase：更新不只是换镜像

Supabase 更新很快，也是 Pigsty 应用模板里组件最多、兼容性最容易出问题的一套。v4.4 把 Studio、Auth、PostgREST、Realtime、Storage、Analytics、Edge Runtime 等组件跟进到 2026 年 7 月的上游版本，并做了一轮配套调整。

这次我们把 Analytics 放进独立的 `_supabase` 数据库与 `_analytics` 模式，避免日志分析表和业务对象混在一起；为 Studio 补齐 `pg_stat_statements` 兼容视图，让查询性能页面能够正常工作；同时适配新的 Publishable Key 与 Secret Key，调整 Kong 路由、Realtime 敏感接口、S3 兼容接口和服务健康检查。

Supabase 这种应用，单个容器能启动没有意义，十几个组件能一起升级、一起工作才算完成。v4.4 修的就是这些不起眼、但会直接决定模板能不能用的问题。


------

## VIP 网卡终于不用手填

另一个我很喜欢的改动，是 VIP 网卡自动识别。

过去 `vip_interface` 与 `pg_vip_interface` 默认写成 `eth0`。如果要启用 NODE／PG VIP，需要用户手工配置网卡名称，比较繁琐。

v4.4 添加了自动检测，把默认值改成了 `auto`：Pigsty 会根据清单里的节点 IP，反查它实际所在的网卡，再把结果交给 Keepalived 或 VIP Manager。手工指定仍然保留，但大多数用户再也不用先登录机器跑一遍 `ip addr`，然后回来填写参数。这个功能只有几行配置，却能直接避免一类部署失败。发行版的体验，往往就是由这种小事决定的。


------

## 备份默认改用 Zstandard

此前，pgBackRest 默认使用 LZ4 压缩。LZ4 速度快、吞吐高，依然适合 `wal_compression`；但备份仓库更看重压缩比，因此 v4.4 将 pgBackRest 的默认算法改为 Zstandard。实际测试中，只增加少量解压开销，就能让压缩比从 2.x 提升到 3.x，额外节省约三分之一的备份空间，这笔买卖很划算。

这次切换也暴露出一个问题：IvorySQL 官方内核没有添加 `--with-lz4`、`--with-zstd` 等构建参数，无法使用 LZ4 与 Zstandard。这也直接推动了下一项改造：统一构建 PG 内核分支。


------

## 统一构建 PG 内核分支

Pigsty 支持了许多不同风味的 PG 内核，其中 PolarDB 与 IvorySQL 此前直接使用上游构建的软件包。IvorySQL 的官方构建缺少几个关键编译参数，PolarDB 则缺少 Ubuntu 26.04 软件包。这两个问题我都提交给了上游。目前，[PolarDB #650](https://github.com/polardb/PolarDB-for-PostgreSQL/issues/650) 的 Ubuntu 26.04 构建支持已经合入，[IvorySQL #1377](https://github.com/IvorySQL/IvorySQL/issues/1377) 也确认会在下一个版本补齐相关选项；上游成品包则还要再等一次发布。

老冯可等不了那么久。既然已经自行构建了这么多内核分支，也不差这两个，正好借此一劳永逸地统一 FHS 布局。以 PolarDB 为例，上游包名是 `polardb-for-postgresql`，默认安装在 `/u01/polardb_pg_17`；Pigsty 的包叫 `polardb-17`，安装在 `/usr/polar-17`。默认端口、运行时搜索路径、开发头文件与扩展构建工具，也一并整理到位。

为了让 PolarDB 的构建可以稳定复现，我们还把它依赖的 PFSD 开发库单独打成 `polarstore` 软件包。开源版同时移除了 PolarDB Oracle 兼容内核及其专用监控配置，不再将这条闭源兼容路径列为内置支持。

做这件事也是在为下一步提前准备。目前，Pigsty 的 500 多个扩展主要面向原生 PostgreSQL 内核。接下来，我希望把“5 个原生 PG 大版本 × 16 组 Linux 平台（含仅在线支持的 EL8 双架构）”的构建矩阵，进一步拓展到十余种 PG 内核分支，让它们也能接入完整的 PG 扩展生态，而不是各自在 RPM 或 Docker 镜像里零散捆绑几个扩展。这才是 Meta Distribution 该有的样子。


------

## 写在最后与未来展望

做发行版，大部分工作都不适合拿来做漂亮的演示：改包名、理目录、补依赖、修构建脚本，再把十四组部署测试全部跑一遍。可一旦这些事情没人做，“开箱即用”就只是一句广告。

**把上游的多样性收进同一套工程约定，把最后一公里的麻烦留给发行版。** 这就是 Pigsty v4.4。

Pigsty 4.4 完工之后，我们已经开始筹备 5.0 版本。在 5.0 版本之前，可能会有一个 4.5 过渡版本。

5.0 版本将随着对今年九月份 PG19 的完整支持一同发布。Pigsty 19 引入了非常多强大的新功能特性。为了充分利用好这些功能特性，Pigsty 5.0 将进行针对性的调整。一些准备工作我们已经完成了。比如这次的 pg_exporter 更新到了 1.3.0，提供了对 PG-19 新监控指标的支持；一些 Patroni 参数模板也都已经为 PG-19 的修改预留好了位置和占位值。

Pigsty 5.0 将会有一个专门的企业级软件制品仓库，采用和开源版有所不同的策略：采用更为保守的更新策略，会保留所有的历史版本软件包、Debug 包、修复包，并定期提供快照。为了实现这个目标，我们还专门做了一个仓库管理工具，用来统一 APT 和 DNF 两侧的仓库管理。我们给它起名为 sow（母猪的意思），正好和包管理器 Pig（小猪）相互对应。

此外，我们还在进行一些有趣的尝试。比如说用 Go 重写 Patroni，至少第一阶段我们先把 Patroni 的客户端工具给重写了，从而提供更好的管理体验。这个项目我们给它起名叫 Boar（公猪的意思），与 sow（母猪）和小猪正好凑成一家子，在 Pigsty 里面相映成趣。

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) | [**发布注记**](https://pigsty.cc/docs/about/release/#v440)





------

## v4.4.0 发布注记

Pigsty v4.4.0 是一个维护版本，重点涵盖 PostgreSQL 18.4、PostgreSQL 19 beta 试用支持、531 个扩展、内核变体更新与更广泛的平台覆盖。

发布于 **2026-07-10**。参见 [GitHub 发布页面](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) 与 [v4.3.0 以来的完整变更](https://github.com/pgsty/pigsty/compare/v4.3.0...v4.4.0)。

**亮点特性**

- **PostgreSQL 18.4 / 19 beta**：PostgreSQL 18.4 现已成为生产默认版本，并提供精简的 PostgreSQL 19 beta 模板用于评估。
- **531 个扩展与内核更新**：扩展目录新增 21 个扩展，并在支持的平台矩阵上更新主要 PostgreSQL 内核变体。
- **Pig 1.5.1 与更安全的运维**：新增克隆、分叉与 PITR 工作流，并引入 VIP 网卡自动发现、pgBackRest Zstandard 压缩和独立的 Patroni 日志采集。
- **安全、应用与工具**：加固敏感配置处理与仓库安全自动化，增加应用模板，重新设计基础设施门户，并提供可选的 Codex 支持。
- **平台验证**：七个操作系统基线在 `x86_64` 与 `aarch64` 上的 14 组离线部署测试全部通过。
- **离线制品**：社区版在 GitHub 公开发布 Debian 13、EL 10、Ubuntu 24.04 的双架构离线包，共 6 个；其余已验证基线的预制离线包通过商业版提供。

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

**验证与校验和**

覆盖 EL9/10、Debian 12/13 与 Ubuntu 22/24/26，横跨 `x86_64` 和 `aarch64` 的 14 组离线部署测试全部完成，结果均为 `failed=0`、`unreachable=0`；EL8 仅继续支持在线安装。

以下 MD5 覆盖全部 14 个已验证制品，其中 6 个社区版制品上传至 GitHub，其余 8 个通过商业版交付；GitHub 会为已上传的社区版制品记录 SHA-256 摘要。

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
