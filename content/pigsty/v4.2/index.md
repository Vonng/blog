---
title: "Pigsty v4.2：12内核齐开花"
linkTitle: "Pigsty v4.2 12内核齐开花"
date: 2026-02-28
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.2.0)）
summary: >
  Pigsty v4.2 把一套配置变成 12 种企业级 PostgreSQL 风味：图数据库、多主复制、MPP 数仓与多种兼容内核统一纳入 Pigsty
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.2.0) | [**发布注记**](https://pigsty.cc/docs/about/release/#v420)

Pigsty v4.2 正式发布，紧随 PostgreSQL 紧急号外小版本更新。

本次更新同时交付了三款全新 PG 内核 —— 图数据库 AgensGraph、多写分布式 pgEdge、MPP 数仓 Cloudberry —— 并重建了 Babelfish、OrioleDB、OpenHalo 三款既有内核。至此，Pigsty 支持的内核总数达到了 **12 个**。

你可以用一份配置文件，把所有这些不同风味的 PostgreSQL 部署为自带监控、高可用、时间点恢复与 IaC 的企业级数据库服务。这大概就是 "Meta PG 发行版" 的含义。

------

## 内核大观园

PostgreSQL 以极致的可扩展性闻名。生态中有超过 1000 个扩展，Pigsty 则提供了其中 461 个开箱即用。

但有些能力是扩展做不到的 —— 比如**定制语法**。如果你想在 PostgreSQL 里原生使用 Oracle 的 PL/SQL、SQL Server 的 T-SQL、MongoDB 的 BSON 协议、或者 Cypher 图查询语法，而不是通过函数调用来模拟，那你就需要修改内核。这也是为什么 Pigsty 不仅提供生态中数量最多的扩展，还要支持不同的内核分支。

在 Pigsty 里使用这些内核，和使用原版 PostgreSQL 几乎没有区别 —— 同样的部署流程、同样的监控面板、同样的高可用机制、同样的备份恢复。区别只是配置文件里改一个 `pg_mode` 的值。一行配置的差异，工程上的大一统。

| 内核                      | pg_mode  | 定位                         | PG 基线   |
|:------------------------|:---------|:---------------------------|:--------|
| **PostgreSQL**          | `pgsql`  | 原版内核 + 461 扩展              | 14 ~ 18 |
| **Babelfish**           | `mssql`  | SQL Server 兼容（T-SQL / TDS） | 17      |
| **IvorySQL**            | `ivory`  | Oracle 兼容（PL/iSQL）         | 18      |
| **OrioleDB**            | `oriole` | 新存储引擎，解决 MVCC 膨胀           | 17      |
| **pgEdge**              | `pgedge` | 多主分布式复制                    | 17      |
| **Percona TDE**         | `tde`    | 透明数据加密                     | 17      |
| **AgensGraph**          | `agens`  | 图数据库（Cypher）               | 16      |
| **OpenHalo**            | `halo`   | MySQL 协议兼容                 | 14      |
| **Cloudberry**          | `gpsql`  | MPP 分析型数仓                  | 14      |
| **PolarDB**             | `polar`  | 共享存储架构                     | 15      |
| **Citus**               | `citus`  | 分布式 HTAP                   | 17      |
| **Ferret / DocumentDB** | `mongo`  | MongoDB 协议兼容               | 17      |

十二内核，一份配置。下面逐个展开。

------

## 原生 PostgreSQL

这次 PostgreSQL 的小版本更新值得单独提一下。

18.2 系列引入了 `substring` 与 WAL 回放相关的回归问题 —— 修漏洞的时候带进了新 bug。社区反应很快，两周后紧急发布了 18.3 / 17.9 / 16.13 / 15.17 / 14.22 补丁版本。Pigsty 的做法还是老规矩 —— 新版本发布次日，离线安装包就绪、所有扩展重新编译验证、文档同步更新。你要做的就是一行命令的事。

扩展总数也顺势推到了 **461** 个。

如果你追求极致的可扩展性和最佳的稳定性，原生 PostgreSQL 始终是最佳默认选择。Pigsty 支持处于生命周期内的 PG 14 到 PG 18。值得一提的是，本版本是最后一个支持 PG 13 的版本，后续最低版本将升至 PG 14。

------

## pgEdge：原生多主复制

pgEdge 是本次新增的重量级选手。

传统 PostgreSQL 高可用是一主多从 —— 写操作只能发往主节点。pgEdge 的核心扩展 Spock 打破了这个限制：集群中的每个节点都可以读写，数据通过逻辑复制在节点间异步同步，冲突通过可配置策略自动解决。

严格来说，pgEdge 不是一个全新的内核，而是基于标准 PostgreSQL + Spock 扩展的多主方案。但由于多主复制的一些底层能力需要内核补丁（这些 Patch 尚未合并到 PostgreSQL 主干），它目前不得不以"Patch 内核 + 扩展"的方式发布。这一点和 OrioleDB、Percona TDE 类似 —— 如果 PostgreSQL 主干未来合并了这些 Patch，它们都可以转变为纯扩展形态工作，这是非常值得期待的趋势。

我很看好这个项目。pgEdge 团队有几位 PostgreSQL 社区的内核老将，技术功底很扎实。关于它的开源历程也值得一说：之前它使用的是类似 Confluent 风格的 Source Available 协议（pgEdge Community License），严格来说不算开源。但 2025 年 9 月，它全面转向了 PostgreSQL License。

不过有个细节需要注意：**源代码遵循 PostgreSQL 协议，但官方提供的二进制包依然受商业许可约束**。具体来说，开发环境可以免费使用，但生产环境必须付费订阅。

老冯直接基于 PostgreSQL 协议的源码自行打包 —— 制作了带 Patch 的 PostgreSQL 内核包，并在 Pigsty 支持的全部主流操作系统上完成适配。没有外部依赖，从 Pigsty 仓库直接装就行，不存在生产环境的许可问题。当然，如果你想用他们的云服务和商业支持，也欢迎去打钱支持一下。

pgEdge 由三个核心扩展组成：

- **Spock 5.0.5**：多主逻辑复制引擎，每个节点同时处理读写
- **Lolor 1.2.2**：大对象逻辑复制
- **Snowflake 2.4**：分布式序列号生成

冲突解决方面，pgEdge 提供了多种策略：最简单的"最后写入获胜"（LWW）、专门的 CRDT 方案、冲突日志表、以及用户自定义策略。如果你有全球地理分布的需求 —— 比如北京、法兰克福、弗吉尼亚各放一个节点，用户就近读写 —— 这种多主模式非常合适。它相当于在 PostgreSQL 生态里原生提供了类似 CockroachDB / TiDB 的多写能力，只不过底座还是那个你熟悉的 PostgreSQL。

在 Pigsty 中使用只需要：`configure -c pgedge`。

------

## AgensGraph：图数据库

AgensGraph 的定位是基于 PostgreSQL 的多模型图数据库 —— 在一个引擎内同时原生支持关系模型和属性图模型，而不是像 Neo4j 那样另起炉灶。这是由韩国 Bitnine 团队发起主导的项目。

有人会问：PostgreSQL 生态里不是有 Apache AGE 这个图扩展吗？为什么还要做 fork 内核？

这里有个有意思的渊源：**AGE 和 AgensGraph 其实是同一个团队做的**。最初他们做的是 AgensGraph 这个内核 fork，大概 1000 多个 Star。后来他们尝试以扩展形式实现类似功能，做了 AGE 并捐献给 Apache。结果扩展形式反而更受欢迎，拿到了 4000 多个 Star。AGE 虽然去年经历了一阵维护风波，但最近已恢复更新，发布了针对 PG 17/18 的 1.7.0 版本。

那 fork 版本还有什么存在价值？至少四个方面：

**一是原生语法**。在 AGE 里，你需要用函数调用来执行 Cypher 查询（把查询字符串传进去）；而在 AgensGraph 里，你可以直接写 `CREATE GRAPH`，Cypher 是一等公民语法。

**二是存储优化**。它的存储引擎针对图属性做了专门优化，理论上性能更好（虽然我还没实际 bench 过）。

**三是查询优化统一**。Cypher、JSON、SQL 三种查询语言在优化器层面是统一处理的，这种原生实现方式很有意思。

**四是向量兼容**。AgensGraph 最近宣称支持了 pgvector 兼容，意味着可以在同一个库里做 Graph RAG —— 图 + 向量的组合检索。这是当下非常火的前沿方向。这个专门的 vector 插件我还没打包进来，后面可能会补上。

当然，fork 路径的代价也很明显：版本跟进 PG 主线的难度很高。目前 PG 已经到 18 了，AgensGraph 还是基于 PG 16。这始终是 fork 方案的宿命，要落后一两个大版本。

在 Pigsty 中使用：`configure -c agens`。

------

## Cloudberry：MPP 数仓

Cloudberry 是本次新增的第三款内核。它是一个 Apache 项目，由 HashData 团队主导，本质上是 Greenplum 7 的 fork —— 但做了不少改进，比如内核从 Greenplum 的 PG 12 升级到了 PG 14，补上了不少好用的新特性。

Cloudberry 2.0 发布后就不再提供官方二进制包了 —— 之前 1.6 还有 RPM，现在也没了。我等了几个月没见到官方有计划解决这个问题，就决定在 Claude 的帮助下自己动手。打包过程整体顺利，只是在个别较新的操作系统上需要改些代码、打几个补丁。之前只有 RPM，现在 DEB 也有了，Pigsty 支持的 14 个 Linux 发行版上全部可用。

关于 Cloudberry/Greenplum 的部署脚本和监控方案，其实早在 Pigsty v1.4 就做过，后来因为用户太少就去掉了。毕竟上 MPP 数仓的体量不是一般公司能达到的。所以我们思忖再三，先将其作为 Beta 模块按需提供 —— 包已经打好放在仓库里了，你可以直接下载使用；完整的部署剧本会在后续版本中择机提供。

------

## Babelfish：SQL Server 兼容

说完三个新增内核，再来聊三个**重建**的内核。

Babelfish 是 AWS 开源的 SQL Server 兼容层 —— 让 PostgreSQL 理解 T-SQL 语法和 TDS 协议，你的 SQL Server 应用不改驱动、不改大部分查询，就能连上 PostgreSQL 跑起来。好项目，但打包构建实在是复杂，复杂到专门有一个开源项目 WiltonDB 就是干这件事的。

老冯之前偷懒，直接用了 WiltonDB 打的包。说实话，那个包的质量一直让我不太舒服：不支持 Debian 全系列和 EL10，依赖体系跟标准 PG 不一样，而且版本还停留在 PG15 —— 但 Babelfish 上游都已经支持 PG17 了。

这次一不做二不休，自己打。有了前面几个内核的打包经验，这个反而简单了 —— 把 Babelfish 的四个核心扩展打成一个包，配合一个 Patch 内核包，开箱即用。现在**不再依赖外部 WiltonDB 仓库**，直接从 Pigsty 仓库安装即可。版本升级到了 **Babelfish 5.5 + PG17**。

在 Pigsty 中使用：`configure -c mssql`。

------

## OrioleDB：新存储引擎

OrioleDB 是被 Supabase 收购的新一代 PostgreSQL 存储引擎项目，目标是从根本上解决 MVCC 膨胀问题 —— 用 Undo Log 替代传统的 Dead Tuple + VACUUM 机制。

本次重建升级到了 **OrioleDB Beta14**，基于 OriolePG 17.16 构建。新版本的一个重要进展是支持了 PITR 增量备份恢复能力。仍处于 Beta 阶段，不建议关键生产环境使用。但作为 PostgreSQL 存储引擎的未来演进方向之一，值得持续关注和实验。

在 Pigsty 中使用：`configure -c oriole`。

------

## OpenHalo：MySQL 协议兼容

OpenHalo 是重建的第三个内核。它提供了 MySQL 线缆协议兼容 —— 你可以同时用 MySQL 客户端和 PG 客户端读写同一个数据库，这个能力非常有意思。

由易景羲和团队开发，是少数几家踏踏实实做事、并且愿意把成果开源出来的国产数据库公司，很难得。

这次更新的变化：

- 版本从 PG 14.10 升级到 **PG 14.18**
- 版本号正式更新为 **1.0**，按照 Pigsty 打包规范重新调整了命名

虽然基线版本是 PG14，稍显陈旧，但在 MySQL 迁移场景下确实是一个值得考虑的选择。

在 Pigsty 中使用：`configure -c mysql`。

------

## 其余六位常驻选手

除了本次新增和重建的六款内核，Pigsty 还有六位一直在的"常驻选手"：

**IvorySQL**（`pg_mode: ivory`）—— 瀚高出品的 Oracle PL/SQL 兼容内核，目前基于 PG 18.1。

**Percona TDE**（`pg_mode: tde`）—— 透明数据加密，满足合规场景中"落盘加密"的刚需。更新节奏稍慢于 PG 主线，后续会跟进到最新版本。

**PolarDB**（`pg_mode: polar`）—— 阿里开源的共享存储架构 PG 内核，更新了小版本。值得一提的是，本版本中我们已经**去掉了带信创资质的 PolarDB-O 的支持**，开源版只保留社区 PG 版本。

**Citus**（`pg_mode: citus`）—— 微软出品的分布式扩展，正式发布 14.0.0 版本，支持 PG 18。

**Ferret / DocumentDB**（`pg_mode: mongo`）—— MongoDB 协议兼容方案，让你用 MongoDB 驱动直连 PostgreSQL。

**Supabase** 自建模板也例行升级到了最新版本。

------

## 一份配置，十核齐飞

说了这么多内核，最好玩的事情其实是这个：我们做了一个 `demo/kernels.yml` 配置文件 —— 如果你有 10 台虚拟机，可以用这个模板**一键拉起 10 个不同的 PG 内核**。

每个集群都有独立的监控面板、高可用、备份恢复，就像管理 10 个标准 PostgreSQL 一样。纯属炫技，但也是一个很好的参考模板：如果你想在一套 Pigsty 里混合部署多种内核，具体该怎么配置。

这不是 PPT 上的架构图，是跑得起来的代码。

------

## 正名：企业级

眼尖的朋友可能已经发现，网站首页的 Slogan 换了。

以前叫 "Battery-Included, Local-First FLOSS RDS"，现在改成了：**"开箱即用的企业级开源 PostgreSQL 发行版，自带高可用、PITR、IaC 监控与 461 个扩展"**。

先澄清一件事：这不是说 Pigsty 的质量刚刚才达到"企业级"。实际上，Pigsty 从很早就在生产环境中被各行各业的企业使用了 —— 金融、政务、制造、互联网，靠的是 Patroni + pgBackRest + 可观测性这套经过实战检验的组合。有些所谓的"企业级方案"，论高可用不比 Patroni 强，论备份恢复不比 pgBackRest 好，监控系统更是一塌糊涂。能力一直在，只是之前我不太愿意给自己贴这个标签。

为什么？因为老冯一直觉得"企业级"这个词听起来比"云"还古老，甚至带有一种"传统杀猪盘二次方"的气质。所以宁可叫"Battery-Included"、叫"FLOSS RDS"，也不愿意把这个词放上去。后来我想明白了：不应该因为这个词被别人用烂了，就回避一个本来属于自己的描述。Pigsty 的高可用、备份恢复、监控告警、安全加固、合规能力，每一项都经得起和商业方案正面对比。实力到了，该戴的帽子就戴上，不亏心。

另一个变化是**去掉了"RDS 替代"**的说法。以前叫自己"开源 RDS 替代"，是一种借力定位——用人们熟悉的品类锚点来解释"Pigsty 是什么"。但到了今天，我们有信心说：不需要用别人来定义自己。Pigsty 就是 Pigsty，一个企业级的 PostgreSQL 发行版。在 PostgreSQL 发行版的赛道上 —— Linux 原生这条路线里 —— Pigsty 就是最能打的。





------

## 其他改进

除了内核大戏，v4.2 还有一些值得注意的工程改进：

**Redis 目录规范化**：默认目录从 `/data` 调整为 `/data/redis`。存量配置如果还用 `/data`，需要先改过来再升级，部署阶段会阻止旧路径继续使用。

**Configure 脚本优化**：支持 `-o` 绝对路径输出并自动建目录；区域探测改为三态（境内/境外/离线回退），修复了 `behind_gfw()` 卡住的问题。

**pgBackRest 初始化容错**：`stanza-create` 增加重试（2 次、间隔 5 秒），缓解与 `archive-push` 的锁竞争。踩过这个坑的人知道它有多烦。

**Supabase 应用栈升级**：PostgREST 14.5、Vector 0.53.0，S3 访问密钥变量补齐。

**Vibe 模板更新**：内置 `@anthropic-ai/claude-code`、`@openai/codex`、`happy-coder` 等工具，AI 编码沙箱开箱即用。

**基础设施例行升级**：Grafana 12.4、Prometheus 3.10、VictoriaMetrics 1.136、etcd 3.6.8、Kafka 4.2 等。注意 Grafana 12.4 有 data link 合并行为变化，自定义面板需检查。

**首页改版**：之前用 Claude Code 糊了一版，有人反映太丑了，批评得很有道理。这次让 Codex 重新优化了一轮，好看不少。后面有空会继续打磨。

------

## 后续展望

Pigsty 作为开源项目，我觉得已经达到了相当完善的程度。后续的工作重心会逐渐转向子项目：

**Pig CLI** 最近更新了很多强大功能 —— 把 PostgreSQL、Patroni、PgBouncer、pgBackRest 的管理全部封装成了命令行工具，方便 Claude Code 这样的 DBA Agent 调用。这种同时为人类 DBA 和 AI Agent 设计的命令行工具，我称之为 Agent-Native CLI。

**DBA Agent** 方面，最近写了一些 Claude Skills 和提示词模板，让 Pigsty 环境可以被 AI 工具感知。这样你就可以把 Claude Code 放进 Pigsty 环境里，让它帮你干活。

Pigsty 本身会继续跟着 PG 小版本的节奏走。下个版本可能会正式补上 Cloudberry 的部署剧本，加上本地 SMTP 服务器支持（maddy / stalwart）。大的新功能暂时不急 —— 当前这个架构持续稳定地跑下去，就挺好。






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




------

## v4.2.1

这是一个维护版本，新增了 3 个扩展插件，

**主要变更**

- **新增扩展**：`pg_eviltransform` 加入 GIS 包组，`pg_pinyin` 加入 FTS 包组，`pg_qos` 加入 Admin 包组 —— 均支持 PG 14–18。
- **移除 PG13**：所有平台变体（EL7/8/9/10、Debian 12/13、Ubuntu 22/24，x86_64 与 aarch64）中的 `pgdg13`、`pgdg13-nonfree` 仓库条目和 PG13 包别名（`pg13-*`）全部移除。
- 配置模板（`fat.yml`、`pro.yml`、`dev.yml`、`el.yml`、`debian.yml`）不再引用 PG13 包或仓库。扩展版本注释更新为仅覆盖 PG 14–18。
- **Percona 仓库**：Origin URL 从 `ppg-18.1` 更新为 `ppg-18.3`，跟踪最新 Percona PostgreSQL 发行版。
- **Nginx 仓库**：Debian/Ubuntu 平台上 Nginx 上游 APT 仓库的模块标签从 `infra` 修正为 `nginx`。
- **UV Venv 修复**：`roles/node/tasks/pkg.yml` 现在会先检查虚拟环境是否已存在，避免重复执行 `uv venv` 导致的冗余创建或重新置备报错。
- **Docker 镜像**：Pigsty Docker 镜像基础包中新增 `less`。
- **Demo 配置**：`el.yml` 和 `debian.yml` 示例配置的默认防火墙规则新增 `5432` 端口，支持直接访问 PostgreSQL。

**兼容性说明**

PostgreSQL 13 已于 2025-11-13 [到达生命周期终点](https://www.postgresql.org/support/versioning/)。
PGDG YUM 仓库已经归档移除 [pg13](https://yum.postgresql.org/news/pg13-end-of-life/) / [pg12](https://yum.postgresql.org/news/pg12-end-of-life/) 目录。
如果您在 EL 系统上安装 Pigsty （即使没有使用 PG 13 版本），也有可能因为仓库访问失败而导致安装或更新失败。

您可以选择直接使用 Pigsty v4.2.1，或者手工修改 `roles/node_id/vars/` 您对应操作系统 `repo_upstream_default` 变量，移除仓库定义中的 pg13 一行即可。

此外，EL8 仍然在 Pigsty 的兼容操作系统中，但从此版本开始将不再发布 el8 的离线软件包。

本版本没有其他破坏性 API 或配置变更。

**7 个提交**，84 文件变更，+4,925 / -5,351 行（`v4.2.0..v4.2.1`，2026-03-04 ~ 2026-03-06）

**PostgreSQL 软件包更新**

| 包名               | 旧版本     | 新版本     | 备注                 |
|:-----------------|:--------|:--------|:-------------------|
| timescaledb      | 2.25.1  | 2.25.2  |                    |
| vchord           | 1.1.0   | 1.1.1   | 新增 clang 构建依赖，修复错误 |
| vchord_bm25      | 0.3.0-1 | 0.3.0-2 | 修复版本注入问题           |
| aggs_for_vecs    | 1.4.0   | 1.4.1   |                    |
| pg_search        | 0.21.9  | 0.21.12 |                    |
| pg_pinyin        | -       | 0.0.2   | 新增扩展               |
| pg_eviltransform | -       | 0.0.2   | 新增扩展               |
| pg_qos           | -       | 1.0.0   | 新增扩展，QoS 资源治理      |


**基础设施软件包更新**

| 名称                           | 旧版本            | 新版本            | 备注 |
|:-----------------------------|:---------------|:---------------|:---|
| `asciinema`                  | 3.1.0          | 3.2.0          |    |
| `grafana-infinity-ds`        | 3.7.2          | 3.7.3          |    |
| `victoria-metrics`           | 1.136.0        | 1.137.0        |    |
| `victoria-metrics-cluster`   | 1.136.0        | 1.137.0        |    |
| `vmutils`                    | 1.136.0        | 1.137.0        |    |
| `hugo`                       | 0.155.3        | 0.157.0        |    |
| `opencode`                   | 1.2.15         | 1.2.17         |    |
| `rustfs`                     | 1.0.0-alpha.83 | 1.0.0-alpha.85 |    |
| `seaweedfs`                  | 4.13           | 4.15           |    |
| `tigerbeetle`                | 0.16.74        | 0.16.75        |    |
| `uv`                         | 0.10.4         | 0.10.8         |    |
| `codex`                      | 0.105.0        | 0.110.0        |    |
| `claude`                     | 2.1.59         | 2.1.68         |    |
| `xray`                       | -              | 26.2.6         | 新增 |
| `gost`                       | -              | 2.12.0         | 新增 |
| `sabiql`                     | -              | 1.6.2          | 新增 |
| `agentsview`                 | -              | 0.10.0         | 新增 |


**校验和**

```bash
262b7671424a38b208872582fe835ef8  pigsty-v4.2.1.tgz
62edcca1d1e572a247be018e1c26eda8  pigsty-pkg-v4.2.1.d12.aarch64.tgz
1d55367e2fd9106e6f18b7ee112be736  pigsty-pkg-v4.2.1.d12.x86_64.tgz
f122b1e5ba8a7ae8e3dc6e6dd53eba65  pigsty-pkg-v4.2.1.d13.aarch64.tgz
617a76bfc8df8766e78abf24339152eb  pigsty-pkg-v4.2.1.d13.x86_64.tgz
908509b350403ad1a4a27a88795fee06  pigsty-pkg-v4.2.1.el10.aarch64.tgz
70cb4afd90ed7aea6ab43a264f8eb4a8  pigsty-pkg-v4.2.1.el10.x86_64.tgz
98fbd67334f5c674b12e6af81ef76923  pigsty-pkg-v4.2.1.el9.aarch64.tgz
687fa741ccd9dcf611a2aa964bcf1de8  pigsty-pkg-v4.2.1.el9.x86_64.tgz
a2a30f4b1146b3e79be91d5be57615b6  pigsty-pkg-v4.2.1.u22.aarch64.tgz
7a1f571bd8526106775c175ba728eee1  pigsty-pkg-v4.2.1.u22.x86_64.tgz
a5574071bac1955798265f71ad73c3d4  pigsty-pkg-v4.2.1.u24.aarch64.tgz
59a7632c650a3c034f1fe6cd589d7ab5  pigsty-pkg-v4.2.1.u24.x86_64.tgz
```
