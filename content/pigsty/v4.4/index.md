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

Pigsty v4.4 正式发布。

表面上看，这是一个常规维护版本：PostgreSQL 18.4、531 个扩展、PG19 beta，以及十四组通过验收的离线安装制品。
但在我看来，这一版真正重要的变化，是 Pigsty 开始从“集成上游软件包” 走向 “自己做发行”。

以前我们把十二种 PostgreSQL 内核装进同一套部署、监控、高可用与备份体系，称之为“Meta PG 发行版”。
做深以后就会发现，最后一公里的问题往往不在 Ansible，而在软件包本身：目录各不相同，构建选项参差不齐，依赖没有包，新的操作系统没人管。

所以 v4.4 往下多走了一层。我们开始自己构建这些分支内核，统一包名、依赖和文件系统布局，再把它们放进 Pigsty 软件仓库。
应用层也新增了两个很有代表性的模板：Immich 与 JumpServer。


------

## 应用更新：Immich，JumpServer，Maybe，与 Supabase

这一版新增了 [Immich](https://pigsty.cc/docs/app/immich/)、Maybe 与 [JumpServer](https://pigsty.cc/docs/app/jumpserver/) 三个应用模板

### Immich：把照片库交给真正的 PostgreSQL

Immich 是一套开源的自托管照片与视频管理服务，可以把它理解成自己家里的 Google Photos 或 iCloud Photos。它有移动端自动备份、相册、地图、人脸识别和语义搜索，背后正好需要 PostgreSQL、向量检索、缓存和机器学习服务。

上游的 Docker Compose 自带一套 PostgreSQL；Pigsty 的模板没有沿用这套一次性数据库，而是直接接入 Pigsty 管理的 PostgreSQL，并启用 VectorChord 与 `earthdistance`。照片原件留在 `/data/immich/library`，元数据与向量索引进入数据库，机器学习与应用服务继续由容器承载。

我不太愿意把一个 `docker-compose.yml` 扔给用户就叫“应用模板”。数据库既然已经是 Pigsty 最擅长的部分，就应该顺手接上监控、备份、时间点恢复和高可用，而不是再藏一套无人维护的 PostgreSQL 容器。
当然，pgBackRest 只保护数据库，照片原件仍然要单独做文件备份。Pigsty 提供的 MinIO 和 JuiceFS 模块则可以解决这个部分的问题。

### JumpServer：把堡垒机也接进来

JumpServer 是另一类典型应用：组件多，启动顺序复杂，而且数据库一旦丢失，账号、资产与审计记录也会一起消失。

Pigsty v4.4 的模板会准备 PostgreSQL 用户、数据库与访问规则，再部署 JumpServer 服务和门户入口。
我们还把数据库迁移、会话连接池、固定容器网段、域名校验这些容易踩坑的地方实际跑了一遍。最后用户看到的仍然是一份配置和一次部署，但模板背后已经替你处理掉了应用与数据库之间的接缝。

Maybe 也在这一版加入应用目录，它是一套个人财务与资产管理工具。三个模板方向不同，但思路一致：应用可以跑在容器里，数据不必跟着容器一起漂。


------

## Supabase：更新不只是换镜像

Supabase 更新很快，也是 Pigsty 应用模板里组件最多、兼容性最容易出问题的一套。v4.4 把 Studio、Auth、PostgREST、Realtime、Storage、Analytics、Edge Runtime 等组件跟进到 2026 年 7 月的上游版本，并做了一轮配套调整。

这次我们把 Analytics 放进独立的 `_supabase` 数据库与 `_analytics` 模式，避免日志分析表和业务对象混在一起；为 Studio 补齐 `pg_stat_statements` 兼容视图，让查询性能页面能够正常工作；同时适配新的 Publishable Key 与 Secret Key，调整 Kong 路由、Realtime 敏感接口、S3 兼容接口和服务健康检查。

Supabase 这种应用，单个容器能启动没有意义，十几个组件能一起升级、一起工作才算完成。v4.4 修的就是这些不起眼、但会直接决定模板能不能用的问题。


------

## VIP 网卡终于不用猜了

另一个我很喜欢的改动，是 VIP 网卡自动识别。

过去 `vip_interface` 与 `pg_vip_interface` 默认写成 `eth0`。
这个名字在老机器上很常见，在云主机、KVM、Vagrant 和新版 Linux 上却可能是 `ens18`、`enp0s8`，或者别的可预测网卡名。
用户照着样例部署高可用，最容易在这个地方莫名其妙地失败。

v4.4 把默认值改成了 `auto`：Pigsty 会根据清单里的节点 IP，反查它实际所在的网卡，再把结果交给 Keepalived 或 VIP Manager。
当然，仍然可以手工指定，但大多数用户再也不用先登录机器跑一遍 `ip addr` 然后再来填参数。

这个功能只有几行配置，却能直接避免一类部署失败。发行版的体验，往往就是由这种小事决定的。


------

## 我们开始自己发行 PG 内核

如果说应用模板和 VIP 是看得见的改进，那么这一版真正重的工作，都藏在软件仓库里。

v4.4 为 PolarDB、IvorySQL、Babelfish、AgensGraph、OrioleDB、pgEdge 与 Cloudberry 等 PostgreSQL 分支内核建立或刷新了自己的 RPM、DEB 构建链
，OpenHalo 的成品包也完成了更新。PolarDB 升到 17.10，AgensGraph 升到 PG17，IvorySQL 升到 PG18；
Babelfish 同时提供 PG17 与 PG18，OrioleDB 覆盖 PG16～18，pgEdge 覆盖 PG15～18。

版本号不是重点。重点是这些软件开始经过同一条发行链路：
从源码归档、构建配方、编译选项和运行依赖，到包名、安装目录、仓库元数据，
再到不同操作系统和 CPU 架构上的安装验证，都由 Pigsty 来 负责。

例如，PolarDB 上游的包名是 `polardb-for-postgresql`，默认装到 `/u01/polardb_pg_17`；
Pigsty 的包叫 `polardb-17`，安装在 `/usr/polar-17`。我们还把默认端口、运行时搜索路径、开发头文件与扩展构建工具一并整理好，
让它表现得像一个正常的、可以被自动化管理的 PostgreSQL 内核。

IvorySQL 也做了同样的重打包，新包按 `/usr/ivory-18` 布局。v4.4 仍然兼容上游现有软件包，但后续会逐步统一到 Pigsty 自己发行的内核包上。
只有这样，一份配置才能在不同内核、不同系统上得到可预测的结果。

这就是我理解的 Distribution：不只是把别人的仓库地址抄进来，而是愿意为软件包最终呈现给用户的样子负责。

当然，这么做的契机是因为上游包确实没有达到我们想要的状态。


------

## 给上游提 Issue，也为自己兜底

自己打包，不等于关起门来另起炉灶。构建过程中发现的问题，我们照样会提交给上游。

PolarDB 当时没有 Ubuntu 26.04 的 DEB 包，我们提交了 [Issue #650](https://github.com/polardb/PolarDB-for-PostgreSQL/issues/650)。
上游随后合入了 Ubuntu 26.04 的构建支持并关闭问题。

IvorySQL 的官方包没有打开 LZ4、Zstd 等常用构建选项，我们也提交了 [Issue #1377](https://github.com/IvorySQL/IvorySQL/issues/1377)，维护者已经确认会在下一版补齐。

上游愿意跟进当然是好事，但我的判断没有变：Pigsty 最终仍然会统一使用自己发行的内核包。
原因并不复杂。每个上游只需要照顾自己的产品习惯，而 Pigsty 要让十几种内核共享同一套安装、监控、备份与高可用体系。
目录放在哪里、包叫什么、依赖如何声明、能不能装开发扩展，这些看似琐碎的目录规范（FHS）与打包约定，恰恰是自动化能否成立的基础。

而且，如果我们下一步要为这些内核分支也提供完整的扩展支持，那么自己打包内核也是必由之路。


------

## PolarFS 也得有一个包

PolarDB 是这轮重打包里最典型的例子。它的完整构建需要 PFSD 开发库，也就是 PolarStore／PolarFS 这一层依赖，但常见 Linux 仓库里并没有一个可以直接安装的开发包。

于是我们把它单独做成了 `polarstore` 软件包，提供 PFSD 的头文件与静态库，并补齐 `zlog` 等构建依赖。
现在 PolarDB 的 RPM 与 DEB 都可以显式声明这项依赖，构建机不需要再手工复制一套开发库，也不用依赖某台机器里提前塞好的文件。

这件事听上去一点也不酷，但它很能说明发行版的价值：把源码树里的偶然条件，变成仓库里可追踪、可复现的依赖关系。

这一版也做了一次减法：正式从开源支持清单中移除 PolarDB Oracle 兼容版，以及随附的专用监控采集配置。
社区版本今后聚焦开放的 PolarDB-PG 内核；需要 Oracle 语法兼容时，Pigsty 里仍然有 IvorySQL 这条更清晰的路线。


------

## PostgreSQL 18.4、531 个扩展，以及其他修复

v4.4 将 PostgreSQL 18.4 作为新的生产默认版本，并提供精简的 PostgreSQL 19 beta 配置用于评估。
扩展总数从 510 增加到 531，新加入 `pg_ducklake`、`psql_bm25s`、`pg_orca`、`pg_sorted_heap`、`pg_stat_plans`、`pg_mockable` 等二十一个扩展。

Pig 1.5.1 新增了数据库克隆、实例分叉与时间点恢复接口；pgBackRest 默认改用 Zstandard 压缩；
Patroni 日志落盘并单独采集。Redis Sentinel 鉴权、EL10 仓库、VirtualBox 路由、既有 `/www` 目录复用，以及敏感配置文件权限等问题也在这一版完成修复。

七个操作系统基线在 `x86_64` 与 `aarch64` 上的十四组离线部署测试全部通过。
EL8 仍然支持在线安装，但不再提供 v4.4 离线包。完整的软件包与兼容性变化，我放在文末的提交注记中。


------

## 写在最后

做发行版，大部分工作都不适合拿来做漂亮的演示：改包名、理目录、补依赖、修构建脚本，再把十四组安装矩阵全部跑一遍。可一旦这些事情没人做，“开箱即用”就只是一句广告。

从 v3.6 开始，我们把 Pigsty 称为 Meta PG 发行版；到了 v4.4，这个说法又多了一层实际含义。
上面可以一键部署 Immich、JumpServer 和 Supabase，下面有 PostgreSQL 18.4、531 个扩展与十几种分支内核，而最底下的软件包、FHS、依赖和验证链路，也开始由我们自己掌握。

**把上游的多样性收进同一套工程约定，把最后一公里的麻烦留给发行版。** 这就是 Pigsty v4.4。

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
